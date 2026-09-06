"""Integrity checks for the retained v2 experiment, not a utility score."""

import hashlib
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import pytest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "SPECS/EVIDENCE/P56-T4"
REPORT = json.loads((EVIDENCE / "generation-report.json").read_text())
PREPARATION = json.loads((EVIDENCE / "preparation.json").read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def test_five_original_outcomes_preserve_protocol_and_limits():
    assert REPORT["protocol"] == "p56-exploratory-authoring/v2"
    assert REPORT["humanReview"] == "pending"
    assert REPORT["utilityVerdict"] is None
    assert REPORT["publicationAuthorized"] is False
    assert len(REPORT["repositories"]) == 5
    assert {r["repository"] for r in REPORT["repositories"]} == {
        "openai/codex",
        "bitcoin/bitcoin",
        "rtk-ai/rtk",
        "axios/axios",
        "n8n-io/n8n",
    }
    for row, source in zip(REPORT["repositories"], PREPARATION["repositories"], strict=True):
        assert row["revision"] == source["revision"]
        assert row["model"] == "gpt-5.6-luna"
        assert row["reasoningEffort"] == "medium"
        assert row["attempts"] == 1
        assert row["repairAttempts"] == 0
        assert row["usage"] is None
        assert row["errorCount"] == 0
        assert row["previewOnly"] is True
        assert row["sourceUnchanged"] is True
        assert row["sourceChanges"] == []
        assert row["sourceSnapshotSha256After"] == row["sourceSnapshotSha256Before"]
        assert row["runtimeIsolationProven"] is False
        assert 0 < row["observedAuthorSeconds"] < 600
        assert row["humanReview"] == "pending"
    assert sum(r["warningCount"] for r in REPORT["repositories"]) == 7


def test_archive_is_bound_safe_and_preserves_every_original_file():
    archive = EVIDENCE / REPORT["archive"]["path"]
    assert sha(archive.read_bytes()) == REPORT["archive"]["sha256"]
    with tarfile.open(archive) as tar:
        actual = {}
        for member in tar.getmembers():
            path = PurePosixPath(member.name)
            assert not path.is_absolute() and ".." not in path.parts
            assert member.isfile() and member.name not in actual
            data = tar.extractfile(member).read()
            assert b"/Users/" not in data
            assert not member.uname and not member.gname
            actual[member.name] = sha(data)
        assert actual == REPORT["archive"]["members"]
        for row in REPORT["repositories"]:
            base = f"records/{row['repositoryId']}"
            receipt = json.loads(tar.extractfile(f"{base}/original/receipt.json").read())
            assert all(row[key] == value for key, value in receipt.items())
            source = next(
                r for r in PREPARATION["repositories"] if r["repository"] == row["repository"]
            )
            assert actual[f"{base}/readme/README.md"] == source["readmeSha256"]
            prefix = f"records/{row['repositoryId']}/original/candidate/"
            files = {p.removeprefix(prefix): h for p, h in actual.items() if p.startswith(prefix)}
            assert files == row["files"]
            assert (
                sha(json.dumps(files, sort_keys=True, separators=(",", ":")).encode())
                == row["candidateSha256"]
            )
    for name, field in (
        ("preparation.json", "preparationSha256"),
        ("baseline-lock.json", "baselineLockSha256"),
    ):
        assert sha((EVIDENCE / name).read_bytes()) == REPORT[field]
    assert PREPARATION["baselineLockSha256"] == REPORT["baselineLockSha256"]
    assert (
        sha((ROOT / "docs/P56_T3A_Exploratory_Pilot_Protocol.md").read_bytes())
        == PREPARATION["protocolSha256"]
    )


def test_known_quality_defects_are_not_hidden_by_schema_success():
    rows = {r["repositoryId"]: r for r in REPORT["repositories"]}
    assert rows["rtk-ai-rtk"]["omittedFromSpecPMPackage"] == ["evidence/source-notes.md"]
    assert "Material evidence fidelity defect" in rows["rtk-ai-rtk"]["sourceIntegrityFindings"][0]
    assert rows["bitcoin-bitcoin"]["warningCount"] == 2
    assert rows["n8n-io-n8n"]["warningCount"] == 2
    assert REPORT["status"] == "completed_with_review_findings"


def test_baselines_and_pins_match_retained_bytes():
    benchmark = json.loads((ROOT / "SPECS/EVIDENCE/P56-T1/benchmark.json").read_text())
    expected = {r["repository"]: r["revision"] for r in benchmark["repositories"]}
    assert {r["repository"]: r["revision"] for r in REPORT["repositories"]} == expected
    lock = json.loads((EVIDENCE / "baseline-lock.json").read_text())
    assert len(lock["repositories"]) == 5
    selected = datetime.fromisoformat(lock["selectedAt"])
    for row in REPORT["repositories"]:
        started = datetime.strptime(row["startedAt"], "%Y-%m-%d %H:%M:%S UTC").replace(
            tzinfo=timezone.utc
        )
        assert selected < started
    archives = {}
    for key, item in lock["archives"].items():
        path = ROOT / item["path"]
        assert sha(path.read_bytes()) == item["sha256"]
        with tarfile.open(path) as tar:
            archives[key] = {
                m.name: sha(tar.extractfile(m).read()) for m in tar.getmembers() if m.isfile()
            }
    for item in lock["repositories"].values():
        assert item["retainedRevision"] == expected[item["repository"]]
        prefix = item["candidateMemberPrefix"]
        actual = {
            p.removeprefix(prefix): h
            for p, h in archives[item["candidateArchive"]].items()
            if p.startswith(prefix)
        }
        assert actual == item["candidateFiles"]
        assert (
            sha(json.dumps(actual, sort_keys=True, separators=(",", ":")).encode())
            == item["candidateSetSha256"]
        )
        assert (
            archives[item["semanticArchive"]][item["semanticMember"]]
            == item["semanticRecordSha256"]
        )


def test_originals_with_independent_specpm_validator(tmp_path):
    core = pytest.importorskip("specpm.core")
    with tarfile.open(EVIDENCE / REPORT["archive"]["path"]) as tar:
        for row in REPORT["repositories"]:
            candidate = tmp_path / row["repositoryId"]
            prefix = f"records/{row['repositoryId']}/original/candidate/"
            for member in tar.getmembers():
                if not member.name.startswith(prefix):
                    continue
                relative = PurePosixPath(member.name.removeprefix(prefix))
                assert member.isfile() and not relative.is_absolute() and ".." not in relative.parts
                target = candidate / str(relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(tar.extractfile(member).read())
            result = core.validate_package(candidate)
            retained = json.loads(
                tar.extractfile(f"records/{row['repositoryId']}/original/validation.json").read()
            )
            assert result["errors"] == retained["errors"]
            assert result["warnings"] == retained["warnings"]
            assert len(result["errors"]) == row["errorCount"]
            assert len(result["warnings"]) == row["warningCount"]
