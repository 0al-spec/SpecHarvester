from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
import yaml

import spec_harvester.local_specpm_intake_bridge as intake_bridge
from spec_harvester.cli import main
from spec_harvester.local_review_decision_service import LocalReviewDecisionStore
from spec_harvester.local_specpm_intake_bridge import (
    LocalSpecPMIntakeBridgeOptions,
    build_local_specpm_intake_proposal,
)

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "SPECS/EVIDENCE/P53-T14/P53-T14_Portable_Handoff.tar.gz"
CATALOG = ROOT / "SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json"
DIGEST = "db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63"


def _record_decision(workspace: Path, disposition: str = "accept_for_intake") -> str:
    catalog = json.loads(CATALOG.read_text())
    candidate_id = catalog["items"][0]["candidateId"]
    reasons = {
        "accept_for_intake": "evidence_verified",
        "defer": "review_deferred",
    }
    store = LocalReviewDecisionStore(workspace, CATALOG)
    result = store.write(
        {
            "apiVersion": "spec-harvester.candidate-review-decision/v0",
            "kind": "SpecHarvesterCandidateReviewDecision",
            "authority": "local_review_decision_evidence_only",
            "binding": {
                "candidateId": candidate_id,
                "packetSha256": catalog["items"][0]["packetSha256"],
            },
            "disposition": disposition,
            "reviewer": "maintainer@example",
            "recordedAt": "2026-07-29T12:00:00Z",
            "reasonCode": reasons[disposition],
            "notes": "Reviewed against portable evidence.",
            "priorDecisionSha256": None,
        }
    )
    return result["candidateId"]


def _valid_specpm_report(candidate: Path) -> dict[str, Any]:
    manifest = yaml.safe_load((candidate / "specpm.yaml").read_text())
    spec_paths = [record["path"] for record in manifest["specs"]]
    return {
        "status": "warning_only",
        "error_count": 0,
        "warning_count": 1,
        "errors": [],
        "warnings": [
            {
                "severity": "warning",
                "code": "preview_only_package",
                "message": "Package remains preview-only.",
                "file": "specpm.yaml",
                "field": "preview_only",
            }
        ],
        "package_identity": {
            "package_id": manifest["metadata"]["id"],
            "name": manifest["metadata"]["name"],
            "version": manifest["metadata"]["version"],
        },
        "checked_files": ["specpm.yaml", *spec_paths],
        "capabilities": manifest["index"]["provides"]["capabilities"],
        "intents": manifest["index"]["provides"]["intents"],
        "intent_mappings": [],
    }


@pytest.fixture
def fake_specpm(monkeypatch: pytest.MonkeyPatch) -> list[Path]:
    validated: list[Path] = []

    def run(candidate: Path, **_: Any) -> dict[str, Any]:
        validated.append(candidate)
        return _valid_specpm_report(candidate)

    monkeypatch.setattr(intake_bridge, "_run_specpm_validation", run)
    return validated


def _options(tmp_path: Path, workspace: Path) -> LocalSpecPMIntakeBridgeOptions:
    return LocalSpecPMIntakeBridgeOptions(
        archive=ARCHIVE,
        expected_archive_sha256=DIGEST,
        catalog=CATALOG,
        review_workspace=workspace,
        output=tmp_path / "intake-proposal.json",
    )


def test_bridge_preflights_only_current_approved_candidates(
    tmp_path: Path, fake_specpm: list[Path]
) -> None:
    workspace = tmp_path / "review"
    candidate_id = _record_decision(workspace)
    result = build_local_specpm_intake_proposal(_options(tmp_path, workspace))
    payload = json.loads((tmp_path / "intake-proposal.json").read_text())

    assert result["approvedCandidateCount"] == 1
    assert result["specpmPreflightFailedCount"] == 0
    assert payload["summary"]["approvedCandidateCount"] == 1
    assert payload["summary"]["specpmPreflightPassedCount"] == len(fake_specpm)
    assert payload["candidates"][0]["candidateId"] == candidate_id
    assert payload["candidates"][0]["status"] == "specpm_preflight_passed"
    assert payload["candidates"][0]["reviewDecision"] == {
        "disposition": "accept_for_intake",
        "reasonCode": "evidence_verified",
        "reviewer": "maintainer@example",
        "recordedAt": "2026-07-29T12:00:00Z",
    }
    assert all(
        package["specpmReport"]["warningCount"] == 1
        for package in payload["candidates"][0]["packages"]
    )
    assert payload["registryMutationCount"] == 0
    assert not any(
        str(tmp_path) in json.dumps(package) for package in payload["candidates"][0]["packages"]
    )


def test_bridge_skips_non_approved_and_is_deterministic(
    tmp_path: Path, fake_specpm: list[Path]
) -> None:
    workspace = tmp_path / "review"
    _record_decision(workspace, disposition="defer")
    first = _options(tmp_path, workspace)
    build_local_specpm_intake_proposal(first)
    first_payload = first.output.read_bytes()
    second = LocalSpecPMIntakeBridgeOptions(
        **{**first.__dict__, "output": tmp_path / "second.json"}
    )
    build_local_specpm_intake_proposal(second)

    payload = json.loads(first_payload)
    assert payload["candidates"] == []
    assert payload["summary"]["skippedDispositionCounts"] == {"defer": 1}
    assert fake_specpm == []
    assert second.output.read_bytes() == first_payload


def test_bridge_records_invalid_specpm_package_as_failed_preflight(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace = tmp_path / "review"
    _record_decision(workspace)

    def invalid(candidate: Path, **_: Any) -> dict[str, Any]:
        report = _valid_specpm_report(candidate)
        report.update(
            {
                "status": "invalid",
                "error_count": 1,
                "warning_count": 0,
                "errors": [
                    {
                        "severity": "error",
                        "code": "invalid_test_package",
                        "message": "Synthetic validation failure.",
                        "file": "specpm.yaml",
                    }
                ],
                "warnings": [],
            }
        )
        return report

    monkeypatch.setattr(intake_bridge, "_run_specpm_validation", invalid)
    result = build_local_specpm_intake_proposal(_options(tmp_path, workspace))
    payload = json.loads((tmp_path / "intake-proposal.json").read_text())

    assert result["specpmPreflightFailedCount"] == result["packageCount"]
    assert payload["candidates"][0]["status"] == "specpm_preflight_failed"


def test_bridge_rejects_archive_or_decision_digest_drift(
    tmp_path: Path, fake_specpm: list[Path]
) -> None:
    workspace = tmp_path / "review"
    candidate_id = _record_decision(workspace)
    with pytest.raises(ValueError, match="archive SHA-256"):
        build_local_specpm_intake_proposal(
            LocalSpecPMIntakeBridgeOptions(
                **{**_options(tmp_path, workspace).__dict__, "expected_archive_sha256": "0" * 64}
            )
        )

    current_path = workspace / "decisions" / f"{candidate_id}.json"
    current = json.loads(current_path.read_text())
    current["binding"]["packetSha256"] = "0" * 64
    current_path.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")
    with pytest.raises(ValueError, match="packet digest is stale"):
        build_local_specpm_intake_proposal(_options(tmp_path, workspace))


def test_cli_writes_read_only_intake_proposal(tmp_path: Path, fake_specpm: list[Path]) -> None:
    workspace = tmp_path / "review"
    _record_decision(workspace)
    output = tmp_path / "cli-proposal.json"

    assert (
        main(
            [
                "build-local-specpm-intake-proposal",
                "--archive",
                str(ARCHIVE),
                "--expected-sha256",
                DIGEST,
                "--catalog",
                str(CATALOG),
                "--review-workspace",
                str(workspace),
                "--output",
                str(output),
            ]
        )
        == 0
    )
    assert json.loads(output.read_text())["registryMutationCount"] == 0


def test_specpm_process_boundary_passes_only_validate_arguments_and_normalizes_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    observed: dict[str, Any] = {}
    monkeypatch.setenv("PYTHONPATH", "/existing")

    def run(argv: list[str], **kwargs: Any) -> SimpleNamespace:
        observed["argv"] = argv
        observed["env"] = kwargs["env"]
        observed["timeout"] = kwargs["timeout"]
        kwargs["stdout"].write(json.dumps({"status": "valid"}).encode())
        kwargs["stderr"].write(b"bounded diagnostics")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", run)
    report = intake_bridge._run_specpm_validation(
        candidate,
        command="specpm --profile local",
        pythonpath="/specpm/src",
        timeout_seconds=7,
        max_report_bytes=1024,
    )

    assert observed["argv"] == [
        "specpm",
        "--profile",
        "local",
        "validate",
        str(candidate),
        "--json",
    ]
    assert observed["env"]["PYTHONPATH"] == f"/specpm/src:{'/existing'}"
    assert observed["timeout"] == 7
    assert report == {"status": "valid"}


@pytest.mark.parametrize(
    ("failure", "message"),
    [
        (FileNotFoundError(), "command was not found"),
        (subprocess.TimeoutExpired("specpm", 3), "exceeded 3 seconds"),
    ],
)
def test_specpm_process_boundary_rejects_startup_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: Exception,
    message: str,
) -> None:
    def run(*_: Any, **__: Any) -> SimpleNamespace:
        raise failure

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(ValueError, match=message):
        intake_bridge._run_specpm_validation(
            tmp_path,
            command="specpm",
            pythonpath=None,
            timeout_seconds=3,
            max_report_bytes=1024,
        )


@pytest.mark.parametrize(
    ("stdout", "returncode", "message"),
    [
        (b"not-json", 0, "did not return JSON"),
        (b"[]", 0, "must be an object"),
        (b'{"status":"valid"}', 2, "failed unexpectedly"),
    ],
)
def test_specpm_process_boundary_rejects_malformed_or_unexpected_results(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    stdout: bytes,
    returncode: int,
    message: str,
) -> None:
    def run(*_: Any, **kwargs: Any) -> SimpleNamespace:
        kwargs["stdout"].write(stdout)
        kwargs["stderr"].write(b"validator diagnostics")
        return SimpleNamespace(returncode=returncode)

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(ValueError, match=message):
        intake_bridge._run_specpm_validation(
            tmp_path,
            command="specpm",
            pythonpath=None,
            timeout_seconds=3,
            max_report_bytes=1024,
        )


def test_specpm_process_boundary_enforces_output_limit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def run(*_: Any, **kwargs: Any) -> SimpleNamespace:
        kwargs["stdout"].write(b"12345")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(ValueError, match="exceeds the configured byte limit"):
        intake_bridge._run_specpm_validation(
            tmp_path,
            command="specpm",
            pythonpath=None,
            timeout_seconds=3,
            max_report_bytes=4,
        )


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"status": "unknown"}, "status is invalid"),
        ({"error_count": True}, "issue counts are invalid"),
        ({"errors": [{}], "error_count": 1}, "entry is incomplete"),
        ({"warning_count": 2}, "counts do not match entries"),
        ({"package_identity": []}, "package identity is invalid"),
        ({"package_identity": {"package_id": "only"}}, "identity is incomplete"),
        ({"intent_mappings": {}}, "intent mappings are invalid"),
        ({"intent_mappings": [{}]}, "intent mapping is invalid"),
        ({"checked_files": ["../outside"]}, "path is unsafe"),
        ({"capabilities": [1]}, "capabilities is invalid"),
    ],
)
def test_specpm_report_normalization_rejects_malformed_contracts(
    change: dict[str, Any], message: str
) -> None:
    report: dict[str, Any] = {
        "status": "valid",
        "error_count": 0,
        "warning_count": 0,
        "errors": [],
        "warnings": [],
        "package_identity": {
            "package_id": "example.package",
            "name": "example",
            "version": "1.0.0",
        },
        "checked_files": ["specpm.yaml"],
        "capabilities": [],
        "intents": [],
        "intent_mappings": [],
    }
    report.update(change)
    with pytest.raises(ValueError, match=message):
        intake_bridge._normalized_specpm_report(report)


@pytest.mark.parametrize(
    ("path", "members", "message"),
    [
        ("../outside", {}, "path is unsafe"),
        ("specpm.yaml", {}, "outside the candidate package root"),
        ("candidate/specpm.yaml", {}, "missing from portable handoff"),
    ],
)
def test_candidate_reconstruction_rejects_unsafe_or_missing_files(
    tmp_path: Path,
    path: str,
    members: dict[str, bytes],
    message: str,
) -> None:
    packet = {"candidate": {"files": [{"path": path}]}}
    with pytest.raises(ValueError, match=message):
        intake_bridge._reconstruct_candidate("candidate-id", packet, members, tmp_path)
