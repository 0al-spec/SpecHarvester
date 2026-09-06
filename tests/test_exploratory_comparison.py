import io
import json
import shutil
import tarfile
from pathlib import Path

import pytest

from spec_harvester.exploratory_comparison import (
    ExploratoryComparison,
    FrozenArchive,
    digest,
    main,
    page,
    safe_path,
    structured,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def comparison(tmp_path_factory):
    output = tmp_path_factory.mktemp("comparison") / "site"
    result = ExploratoryComparison(ROOT, output).write()
    return output, result


def test_all_surfaces_are_complete_and_byte_bound(comparison):
    output, result = comparison
    assert result["humanReview"] == "pending"
    assert result["publicationAuthorized"] is False
    assert [r["retainedPackageCount"] for r in result["repositories"]] == [4, 1, 1, 1, 77]
    evidence = ROOT / "SPECS/EVIDENCE/P56-T4"
    report = json.loads((evidence / "generation-report.json").read_text())
    lock = json.loads((evidence / "baseline-lock.json").read_text())
    for row in report["repositories"]:
        root = output / row["repositoryId"]
        for path, sha in row["files"].items():
            assert digest((root / "new/original" / path).read_bytes()) == sha
        for path, sha in lock["repositories"][row["repositoryId"]]["candidateFiles"].items():
            assert digest((root / "retained-files" / path).read_bytes()) == sha
        assert (root / "new/index.html").is_file()
        assert "Content-Security-Policy" in (root / "new/index.html").read_text()
        assert "fonts.googleapis.com" not in (root / "new/assets/spec-renderer.css").read_text()
        assert "Human review pending" in (root / "index.html").read_text()
        assert 'sandbox="allow-scripts allow-downloads"' in (root / "index.html").read_text()
        assert "Retained packages" in (root / "prior.html").read_text()
        assert (
            "Historical" in (root / "semantic.html").read_text()
            or row["repositoryId"] == "rtk-ai-rtk"
        )
    assert "Rejected historical proposal" in (output / "rtk-ai-rtk/semantic.html").read_text()
    worksheet = json.loads((output / "human-review-template.json").read_text())
    assert worksheet["reviewer"] is None
    for row in worksheet["repositories"]:
        assert len(row["surfaces"]) == 4
        for surface in row["surfaces"].values():
            assert len(surface["answers"]) == 5
            assert all(answer["verdict"] is None for answer in surface["answers"])
            assert surface["sourceLookups"] == []
    with pytest.raises(ValueError, match="output_must_not_exist"):
        ExploratoryComparison(ROOT, output).write()


@pytest.mark.parametrize("value", ["", "../x", "/x", "a/../b", "a//b", "a\\b", "https:x"])
def test_unsafe_paths_fail(value):
    with pytest.raises(ValueError, match="unsafe_path"):
        safe_path(value)


def test_untrusted_text_is_inert():
    text = '<script>alert(1)</script><img src="https://host/">'
    rendered = page(text, structured({text: [text, None]}))
    assert "<script>" not in rendered and "<img" not in rendered
    assert "&lt;script&gt;" in rendered
    assert "Not provided" in rendered
    assert "default-src 'none'" in rendered


def archive(tmp_path, entries):
    path = tmp_path / "archive.tar.gz"
    with tarfile.open(path, "w:gz") as tar:
        for name, kind in entries:
            member = tarfile.TarInfo(name)
            member.type = kind
            data = b"data"
            member.size = len(data) if kind == tarfile.REGTYPE else 0
            tar.addfile(member, io.BytesIO(data) if member.size else None)
    return path


@pytest.mark.parametrize(
    "entries,code",
    [
        ([("../escape", tarfile.REGTYPE)], "unsafe_path"),
        ([("link", tarfile.SYMTYPE)], "unsafe_archive_member"),
        ([("file", tarfile.REGTYPE), ("file", tarfile.REGTYPE)], "unsafe_archive_member"),
    ],
)
def test_bad_archives_are_not_extracted(tmp_path, entries, code):
    path = archive(tmp_path, entries)
    with pytest.raises(ValueError, match=code):
        FrozenArchive(path, digest(path.read_bytes())).read({})


def test_archive_hash_member_and_completeness_guards(tmp_path):
    path = archive(tmp_path, [("folder", tarfile.DIRTYPE), ("file", tarfile.REGTYPE)])
    frozen = FrozenArchive(path, digest(path.read_bytes()))
    assert frozen.read({"file": digest(b"data")}, exact=True) == {"file": b"data"}
    for selected, exact, code in [
        ({"file": "wrong"}, False, "member_digest_mismatch"),
        ({"missing": digest(b"data")}, False, "missing_archive_member"),
        ({}, True, "unexpected_archive_member"),
    ]:
        with pytest.raises(ValueError, match=code):
            frozen.read(selected, exact=exact)
    with pytest.raises(ValueError, match="archive_digest_mismatch"):
        FrozenArchive(path, "wrong").read({})
    link = tmp_path / "link"
    link.symlink_to(path)
    with pytest.raises(ValueError, match="unsafe_archive"):
        FrozenArchive(link, frozen.expected).read({})


def test_missing_baseline_is_unavailable_not_invented(tmp_path):
    assert ExploratoryComparison(ROOT, tmp_path).prior(tmp_path, None, {}) == 0
    assert "unavailable" in (tmp_path / "prior.html").read_text()
    assert "unavailable" in (tmp_path / "semantic.html").read_text()


@pytest.mark.parametrize(
    "change,error",
    [
        ("lock", "input_digest_mismatch"),
        ("targets", "invalid_five_target_set"),
        ("revision", "source_identity_mismatch"),
        ("candidate", "candidate_identity_mismatch"),
        ("readme", "readme_identity_mismatch"),
        ("errorCount", "invalid_diagnostic_count"),
        ("warningCount", "invalid_diagnostic_count"),
    ],
)
def test_tampered_inputs_fail_before_output(tmp_path, change, error):
    repo = tmp_path / "repo"
    evidence = repo / "SPECS/EVIDENCE/P56-T4"
    shutil.copytree(ROOT / "SPECS/EVIDENCE/P56-T4", evidence)
    shutil.copytree(ROOT / "SPECS/EVIDENCE/P56-T1", repo / "SPECS/EVIDENCE/P56-T1")
    report = json.loads((evidence / "generation-report.json").read_text())
    if change == "lock":
        (evidence / "baseline-lock.json").write_text("{}")
    elif change == "targets":
        report["repositories"] = []
    elif change == "revision":
        report["repositories"][0]["revision"] = "wrong"
    elif change == "candidate":
        report["repositories"][0]["candidateSha256"] = "wrong"
    elif change in ("errorCount", "warningCount"):
        report["repositories"][0][change] = (
            '<meta http-equiv="refresh" content="0;url=https://bad">'
        )
    else:
        preparation = json.loads((evidence / "preparation.json").read_text())
        preparation["repositories"][0]["readmeSha256"] = "wrong"
        data = json.dumps(preparation).encode()
        (evidence / "preparation.json").write_bytes(data)
        report["preparationSha256"] = digest(data)
    (evidence / "generation-report.json").write_text(json.dumps(report))
    output = tmp_path / "output"
    with pytest.raises(ValueError, match=error):
        ExploratoryComparison(repo, output).write()
    assert not output.exists()


def test_output_inside_repository_refused(tmp_path):
    with pytest.raises(ValueError, match="output_must_be_outside_repository"):
        ExploratoryComparison(ROOT, ROOT / "does-not-exist-p56").write()


@pytest.mark.parametrize("field", ["errorCount", "warningCount"])
@pytest.mark.parametrize("value", [True, -1, 1.5, None, "0"])
def test_counts_reject_non_integer_or_negative_values(tmp_path, field, value):
    repo = tmp_path / "repo"
    evidence = repo / "SPECS/EVIDENCE/P56-T4"
    shutil.copytree(ROOT / "SPECS/EVIDENCE/P56-T4", evidence)
    report = json.loads((evidence / "generation-report.json").read_text())
    report["repositories"][0][field] = value
    (evidence / "generation-report.json").write_text(json.dumps(report))
    output = tmp_path / "output"
    with pytest.raises(ValueError, match="invalid_diagnostic_count"):
        ExploratoryComparison(repo, output).write()
    assert not output.exists()


def test_renderer_failure_is_not_a_success(tmp_path):
    with pytest.raises(ValueError, match="retained_package_render_failed"):
        ExploratoryComparison(ROOT, tmp_path).package(
            tmp_path / "bad", {"specpm.yaml": b"{}"}, "bad"
        )


def test_cli_entrypoint(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["comparison", "--output", "/unused-test-output"])
    monkeypatch.setattr(ExploratoryComparison, "write", lambda self: {"test": True})
    main()
    assert json.loads(capsys.readouterr().out) == {"test": True}
