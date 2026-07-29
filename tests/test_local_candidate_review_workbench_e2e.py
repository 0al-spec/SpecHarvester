from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml

import spec_harvester.local_specpm_intake_bridge as intake_bridge
from spec_harvester.cli import main
from spec_harvester.local_candidate_review_workbench_e2e import (
    HOSTILE_MARKER,
    LocalCandidateReviewWorkbenchE2EOptions,
    _wave_records,
    build_local_candidate_review_workbench_e2e,
)

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "SPECS/EVIDENCE/P53-T14/P53-T14_Portable_Handoff.tar.gz"
CATALOG = ROOT / "SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json"
DETAILS = ROOT / "SPECS/EVIDENCE/P54-T5/P54-T5_Candidate_Review_Details.json"
DIGEST = "db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63"


def _specpm_report(candidate: Path) -> dict[str, Any]:
    manifest = yaml.safe_load((candidate / "specpm.yaml").read_text())
    return {
        "status": "warning_only",
        "error_count": 0,
        "warning_count": 1,
        "errors": [],
        "warnings": [
            {
                "code": "preview_only_package",
                "message": "Package remains preview-only.",
                "file": "specpm.yaml",
            }
        ],
        "package_identity": {
            "package_id": manifest["metadata"]["id"],
            "name": manifest["metadata"]["name"],
            "version": manifest["metadata"]["version"],
        },
        "checked_files": [
            "specpm.yaml",
            *[record["path"] for record in manifest["specs"]],
        ],
        "capabilities": manifest["index"]["provides"]["capabilities"],
        "intents": manifest["index"]["provides"]["intents"],
        "intent_mappings": [],
    }


@pytest.fixture
def fake_specpm(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        intake_bridge,
        "_run_specpm_validation",
        lambda candidate, **_: _specpm_report(candidate),
    )


def _options(tmp_path: Path) -> LocalCandidateReviewWorkbenchE2EOptions:
    return LocalCandidateReviewWorkbenchE2EOptions(
        archive=ARCHIVE,
        expected_archive_sha256=DIGEST,
        catalog=CATALOG,
        details=DETAILS,
        output=tmp_path / "workbench-e2e.json",
    )


def test_workbench_e2e_validates_full_corpus_and_security_boundaries(
    tmp_path: Path, fake_specpm: None
) -> None:
    result = build_local_candidate_review_workbench_e2e(_options(tmp_path))
    report = json.loads((tmp_path / "workbench-e2e.json").read_text())

    assert result == {
        "status": "passed",
        "candidateCount": 100,
        "representativeReviewCount": 4,
        "specpmPreflightFailedCount": 0,
        "output": str(tmp_path / "workbench-e2e.json"),
    }
    assert report["corpus"] == {
        "candidateCount": 100,
        "comparisonCount": 100,
        "detailCount": 100,
        "waveCounts": {
            "wave-1": 25,
            "wave-2": 25,
            "wave-3": 25,
            "wave-4": 25,
        },
    }
    assert {record["disposition"] for record in report["representativeReviews"]} == {
        "accept_for_intake",
        "request_revision",
        "defer",
        "do_not_promote",
    }
    assert report["decisionLifecycle"]["restartHydrationPassed"] is True
    assert report["decisionLifecycle"]["interruptedWriteLeftPartialState"] is False
    assert report["browserSecurity"]["hostileMarkerPersistedAsInertText"] is True
    assert report["browserSecurity"]["candidateRenderingPrimitive"] == "textContent"
    assert report["serviceSecurity"] == {
        "candidateOriginStatus": 403,
        "invalidCsrfStatus": 403,
        "reviewerOriginStatus": 201,
    }
    assert report["specpmIntake"]["approvedCandidateCount"] == 1
    assert report["specpmIntake"]["registryMutationCount"] == 0
    assert report["registryMutationCount"] == 0
    assert "path_traversal_rejected" in report["negativeChecks"]
    assert "detail_digest_drift_rejected" in report["negativeChecks"]
    assert HOSTILE_MARKER not in json.dumps(report)


def test_workbench_e2e_is_deterministic(tmp_path: Path, fake_specpm: None) -> None:
    first = _options(tmp_path)
    build_local_candidate_review_workbench_e2e(first)
    first_bytes = first.output.read_bytes()
    second = LocalCandidateReviewWorkbenchE2EOptions(
        **{**first.__dict__, "output": tmp_path / "second.json"}
    )
    build_local_candidate_review_workbench_e2e(second)

    assert second.output.read_bytes() == first_bytes


def test_workbench_e2e_rejects_stale_source_bundle(tmp_path: Path, fake_specpm: None) -> None:
    catalog = json.loads(CATALOG.read_text())
    catalog["sourceBundleSha256"] = "0" * 64
    catalog_path = tmp_path / "catalog.json"
    catalog_path.write_text(json.dumps(catalog))
    options = LocalCandidateReviewWorkbenchE2EOptions(
        **{**_options(tmp_path).__dict__, "catalog": catalog_path}
    )

    with pytest.raises(ValueError, match="catalog source bundle digest is stale"):
        build_local_candidate_review_workbench_e2e(options)


def test_wave_records_reject_incomplete_or_unknown_wave() -> None:
    details = json.loads(DETAILS.read_text())
    details["details"][0]["sections"][0]["content"] = json.dumps({"wave": "wave-unknown"})
    with pytest.raises(ValueError, match="wave provenance is unknown"):
        _wave_records(details)

    details = json.loads(DETAILS.read_text())
    details["details"].pop()
    with pytest.raises(ValueError, match="wave coverage is incomplete"):
        _wave_records(details)


def test_workbench_e2e_cli(tmp_path: Path, fake_specpm: None, capsys: Any) -> None:
    output = tmp_path / "cli-e2e.json"
    assert (
        main(
            [
                "validate-local-candidate-review-workbench",
                "--archive",
                str(ARCHIVE),
                "--expected-sha256",
                DIGEST,
                "--catalog",
                str(CATALOG),
                "--details",
                str(DETAILS),
                "--output",
                str(output),
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["candidateCount"] == 100
    assert json.loads(output.read_text())["status"] == "passed"
