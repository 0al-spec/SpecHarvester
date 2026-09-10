"""Replay a bounded authoring artifact; not a semantic utility benchmark."""

import hashlib
import json
import re
import tarfile
from pathlib import Path, PurePosixPath

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "SPECS/EVIDENCE/P56-AXIOS-DISCOVERY"
AUTHOR = EVIDENCE / "author"
REVISION = "509719387e4993392ca40da03a49678269cdfb90"


def _read(path):
    return json.loads(path.read_text())


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _yaml_targets(value, prefix=""):
    targets = {prefix} if prefix else set()
    if isinstance(value, dict):
        for key, child in value.items():
            targets.update(_yaml_targets(child, f"{prefix}.{key}".strip(".")))
    elif isinstance(value, list):
        for child in value:
            if isinstance(child, dict) and "id" in child:
                targets.update(_yaml_targets(child, f"{prefix}.{child['id']}"))
    return targets


def _assert_reference(reference):
    name, _, selector = reference.partition(":")
    path = (AUTHOR / name).resolve()
    assert path.is_relative_to(AUTHOR.resolve()) and path.is_file()
    if not selector:
        return
    text = path.read_text()
    if name.endswith(".spec.yaml"):
        assert selector in _yaml_targets(yaml.safe_load(text))
    elif lines := re.fullmatch(r"lines? (\d+)(?:-(\d+))?", selector):
        start, end = int(lines[1]), int(lines[2] or lines[1])
        assert 1 <= start <= end <= len(text.splitlines())
    else:
        for token in re.split(r"[./]", selector):
            assert re.search(rf"\b{re.escape(token)}\b", text)


def test_discovery_follow_up_is_bound_and_does_not_replace_originals():
    receipt = _read(EVIDENCE / "verification.json")
    baseline = _read(ROOT / "SPECS/EVIDENCE/P56-T4/generation-report.json")
    original = next(row for row in baseline["repositories"] if row["repositoryId"] == "axios-axios")
    assert receipt["experiment"] == "p56-axios-discovery-depth/v1"
    assert receipt["author"]["model"] == "gpt-5.6-sol"
    assert receipt["author"]["reasoningEffort"] == "high"
    assert receipt["author"]["usage"] is None
    assert receipt["source"]["revision"] == original["revision"] == REVISION
    assert receipt["originalCandidateSha256"] == original["candidateSha256"]
    original_copy = AUTHOR / "original"
    assert {
        str(path.relative_to(original_copy)): _sha(path.read_bytes())
        for path in original_copy.rglob("*")
        if path.is_file()
    } == original["files"]
    assert receipt["authority"] == {
        "humanReview": "pending",
        "publicationAuthorized": False,
        "runtimeExecuted": False,
        "t6Completed": False,
    }
    assert receipt["runtimeIsolationProven"] is False
    actual = {
        str(path.relative_to(AUTHOR)): _sha(path.read_bytes())
        for path in AUTHOR.rglob("*")
        if path.is_file()
    }
    assert actual == receipt["authorArtifacts"]
    assert not any(path.is_symlink() for path in AUTHOR.rglob("*"))
    for path in AUTHOR.rglob("*"):
        if path.is_file():
            assert b"/Users/" not in path.read_bytes()


def test_capability_map_binds_ranges_to_retained_source_bytes():
    receipt = _read(EVIDENCE / "verification.json")
    archive = EVIDENCE / "sources.tar.gz"
    assert _sha(archive.read_bytes()) == receipt["source"]["archiveSha256"]
    sources = {}
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            path = PurePosixPath(member.name)
            assert member.isfile() and not path.is_absolute() and ".." not in path.parts
            assert member.name not in sources
            sources[member.name] = tar.extractfile(member).read()
    assert {path: _sha(data) for path, data in sources.items()} == receipt["source"]["files"]
    coverage = _read(AUTHOR / "capability-map.json")
    assert coverage["revision"] == REVISION
    assert coverage["experiment"] == receipt["experiment"]
    ids = [item["id"] for item in coverage["items"]]
    assert ids and len(ids) == len(set(ids))
    for item in coverage["items"]:
        assert item["userNeed"] and item["summary"] and item["sources"]
        for reference in item["sources"]:
            data = sources[reference["path"]]
            assert reference["sha256"] == _sha(data)
            assert 1 <= reference["startLine"] <= reference["endLine"] <= len(data.splitlines())
        for stage in ("before", "after"):
            assert item[stage]["status"] in {"covered", "partial", "missing", "excluded", "unknown"}
            assert item[stage]["reason"]
    assert (AUTHOR / "inventory-initial.json").is_file()
    assert (AUTHOR / "review.ru.md").is_file()


def test_packaged_excerpts_preserve_exact_source_bytes_and_ranges():
    with tarfile.open(EVIDENCE / "sources.tar.gz") as tar:
        sources = {member.name: tar.extractfile(member).read() for member in tar.getmembers()}
    candidate = AUTHOR / "candidate"
    provenance = _read(candidate / "evidence/sources.json")
    assert provenance["revision"] == REVISION
    paths = [entry["path"] for entry in provenance["entries"]]
    assert paths and len(paths) == len(set(paths))
    for entry in provenance["entries"]:
        source = sources[entry["sourcePath"]]
        assert _sha(source) == entry["sourceSha256"]
        lines = source.splitlines(keepends=True)
        assert 1 <= entry["startLine"] <= entry["endLine"] <= len(lines)
        expected = b"".join(lines[entry["startLine"] - 1 : entry["endLine"]])
        path = (candidate / entry["path"]).resolve()
        assert path.is_relative_to(candidate.resolve())
        assert path.read_bytes() == expected
        assert _sha(expected) == entry["excerptSha256"]


def test_preview_keeps_draft_authority_and_explicit_capability_index():
    candidate = AUTHOR / "candidate"
    manifest = yaml.safe_load((candidate / "specpm.yaml").read_text())
    assert manifest["preview_only"] is True
    declared = set()
    for entry in manifest["specs"]:
        path = (candidate / entry["path"]).resolve()
        assert path.is_relative_to(candidate.resolve())
        spec = yaml.safe_load(path.read_text())
        assert spec["metadata"]["status"] == "draft"
        declared.update(item["id"] for item in spec["provides"]["capabilities"])
        for evidence in spec["evidence"]:
            path = (candidate / evidence["path"]).resolve()
            assert path.is_relative_to(candidate.resolve()) and path.is_file()
    assert declared == set(manifest["index"]["provides"]["capabilities"])
    assert not manifest["index"]["provides"].get("intents")


def test_preview_passes_current_specpm_without_omitting_evidence():
    core = pytest.importorskip("specpm.core", reason="Run in the SpecPM integration job")
    candidate = AUTHOR / "candidate"
    result = core.validate_package(candidate)
    assert result["errors"] == []
    assert [warning["code"] for warning in result["warnings"]] == ["preview_only_package"]
    manifest = yaml.safe_load((candidate / "specpm.yaml").read_text())
    errors = []
    collected = set(core.collect_package_files(candidate, manifest, errors))
    assert errors == []
    actual = {str(path.relative_to(candidate)) for path in candidate.rglob("*") if path.is_file()}
    assert collected == actual


def test_original_worker_snapshot_is_preserved_before_main_corrections():
    corrections = _read(EVIDENCE / "review-corrections.json")
    receipt = _read(EVIDENCE / "verification.json")
    archive = EVIDENCE / corrections["originalAuthorArchive"]
    assert _sha(archive.read_bytes()) == corrections["originalAuthorArchiveSha256"]
    assert receipt["authorArtifactsStage"] == "main_reviewed_integration"
    assert receipt["postAuthorReview"]["sha256"] == _sha(
        (EVIDENCE / "review-corrections.json").read_bytes()
    )
    with tarfile.open(archive) as tar:
        actual = {}
        for member in tar.getmembers():
            assert member.isfile() and member.name not in actual
            path = PurePosixPath(member.name)
            assert not path.is_absolute() and ".." not in path.parts
            actual[member.name] = _sha(tar.extractfile(member).read())
    assert actual == corrections["originalAuthorArtifacts"]
    assert corrections["humanReview"] == "pending"


def test_coverage_labels_and_references_are_recorded_not_quality_scores():
    coverage = _read(AUTHOR / "capability-map.json")
    expected = {
        "make_http_requests": ("covered", "covered"),
        "configure_clients_and_requests": ("covered", "covered"),
        "serialize_and_transform_data": ("partial", "covered"),
        "attach_credentials_and_xsrf_tokens": ("partial", "covered"),
        "intercept_request_response_lifecycle": ("partial", "covered"),
        "cancel_and_bound_requests": ("covered", "covered"),
        "inspect_responses_and_errors": ("covered", "covered"),
        "observe_and_limit_transfer": ("partial", "covered"),
        "select_transport_and_runtime": ("partial", "covered"),
        "define_resilience_policy": ("excluded", "excluded"),
    }
    assert {
        item["id"]: (item["before"]["status"], item["after"]["status"])
        for item in coverage["items"]
    } == expected
    for item in coverage["items"]:
        for stage in ("before", "after"):
            assert item[stage]["fields"]
            for reference in item[stage]["fields"]:
                _assert_reference(reference)
    log = _read(AUTHOR / "work-log.json")
    frozen = next(
        entry
        for entry in log["phaseSequence"]
        if entry["phase"] == "inventory_initial_written_before_baseline"
    )
    assert frozen["sha256"] == _sha((AUTHOR / "inventory-initial.json").read_bytes())


@pytest.mark.parametrize(
    "reference",
    [
        "candidate/specs/main.spec.yaml:constraints.nonexistent_constraint",
        "candidate/evidence/not-present.md",
        "original/evidence/README-excerpt.md:lines 900000-900001",
    ],
)
def test_bad_coverage_references_are_rejected(reference):
    with pytest.raises(AssertionError):
        _assert_reference(reference)


def test_reviewed_preview_retains_prerequisite_and_separate_limit_meanings():
    spec = yaml.safe_load((AUTHOR / "candidate/specs/main.spec.yaml").read_text())
    constraints = {item["id"]: item["statement"] for item in spec["constraints"]}
    assert "ES6 Promise" in constraints["promise_runtime"]
    assert "polyfill" in constraints["promise_runtime"]
    assert "maxContentLength to bound response size" in constraints["body_and_decompression_limits"]
    assert (
        "maxBodyLength bounds the outgoing request body"
        in constraints["body_and_decompression_limits"]
    )
    adapters = (AUTHOR / "candidate/evidence/adapters.md").read_text()
    assert "config has been merged with defaults" in adapters
    assert "request transformers have run" in adapters
