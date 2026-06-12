from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.baseline_submission_handoff import (
    BASELINE_SUBMISSION_HANDOFF_API_VERSION,
    BASELINE_SUBMISSION_HANDOFF_KIND,
    MISSING_BASELINE_DIAGNOSTIC,
    BaselineSubmissionHandoffOptions,
    build_baseline_submission_handoff,
)
from spec_harvester.cli import main
from spec_harvester.fresh_candidate_refresh_run import (
    FreshCandidateRefreshRunOptions,
    build_fresh_candidate_refresh_run,
    write_fresh_candidate_refresh_run,
)
from spec_harvester.xyflow_package_set_smoke import (
    XyflowPackageSetSmokeOptions,
    run_xyflow_package_set_smoke,
)


def test_baseline_submission_handoff_records_missing_baseline_boundary(
    tmp_path: Path,
) -> None:
    fresh_run = write_fresh_run(tmp_path)
    prepare_report = write_prepare_report(tmp_path, missing_baseline=True)

    report = build_baseline_submission_handoff(
        BaselineSubmissionHandoffOptions(
            fresh_candidate_refresh_run=fresh_run,
            specpm_prepare_report=prepare_report,
        )
    )

    assert report["apiVersion"] == BASELINE_SUBMISSION_HANDOFF_API_VERSION
    assert report["kind"] == BASELINE_SUBMISSION_HANDOFF_KIND
    assert report["status"] == "first_submission_required"
    assert report["reason"] == "missing_current_generated_baseline"
    assert report["packageSet"]["id"] == "xyflow.workspace"
    assert report["packageSet"]["candidateCount"] == 4
    assert report["packageSet"]["contractFileCount"] == 8
    assert report["specpmPrepareReport"] == {
        "decisionReason": "refresh_prepare_requires_review",
        "decisionStatus": "manual_review_required",
        "diagnosticCode": MISSING_BASELINE_DIAGNOSTIC,
        "missingBaselineDiagnosticCount": 1,
        "sampleDiagnostics": [
            {
                "code": MISSING_BASELINE_DIAGNOSTIC,
                "field": "packageIds[0]",
                "message": "Current generated artifact has no contract files.",
            }
        ],
        "status": "missing_baseline",
    }
    assert report["baselineWorkflow"]["blockedRefreshDecision"] is True
    assert {item["id"] for item in report["baselineWorkflow"]["maintainerActions"]} == {
        "first_submission_review",
        "seed_baseline",
        "reject_or_request_regeneration",
    }
    assert report["authority"] == {
        "noRegistryMutation": True,
        "notRefreshDecision": True,
        "producerEvidenceAuthority": "evidence_only",
        "registryAuthority": "SpecPM maintainer review",
    }


def test_baseline_submission_handoff_without_prepare_report_is_unverified(
    tmp_path: Path,
) -> None:
    fresh_run = write_fresh_run(tmp_path)

    report = build_baseline_submission_handoff(
        BaselineSubmissionHandoffOptions(fresh_candidate_refresh_run=fresh_run)
    )

    assert report["status"] == "baseline_review_required"
    assert report["reason"] == "specpm_prepare_report_not_provided"
    assert report["specpmPrepareReport"] == {
        "diagnosticCode": MISSING_BASELINE_DIAGNOSTIC,
        "missingBaselineDiagnosticCount": 0,
        "status": "not_provided",
    }


def test_baseline_submission_handoff_rejects_non_missing_baseline_prepare_report(
    tmp_path: Path,
) -> None:
    fresh_run = write_fresh_run(tmp_path)
    prepare_report = write_prepare_report(tmp_path, missing_baseline=False)

    with pytest.raises(ValueError, match=MISSING_BASELINE_DIAGNOSTIC):
        build_baseline_submission_handoff(
            BaselineSubmissionHandoffOptions(
                fresh_candidate_refresh_run=fresh_run,
                specpm_prepare_report=prepare_report,
            )
        )


def test_baseline_submission_handoff_rejects_unsupported_fresh_run_schema_version(
    tmp_path: Path,
) -> None:
    fresh_run = write_fresh_run(tmp_path)
    payload = json.loads(fresh_run.read_text(encoding="utf-8"))
    payload["schemaVersion"] = 2
    fresh_run.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="schemaVersion"):
        build_baseline_submission_handoff(
            BaselineSubmissionHandoffOptions(fresh_candidate_refresh_run=fresh_run)
        )


def test_baseline_submission_handoff_cli_writes_report(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fresh_run = write_fresh_run(tmp_path)
    prepare_report = write_prepare_report(tmp_path, missing_baseline=True)
    output = tmp_path / "handoff" / "baseline-submission-handoff.json"

    exit_code = main(
        [
            "baseline-submission-handoff",
            "--fresh-candidate-refresh-run",
            str(fresh_run),
            "--specpm-prepare-report",
            str(prepare_report),
            "--output",
            str(output),
        ]
    )

    printed = json.loads(capsys.readouterr().out)
    written = json.loads(output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert printed == written
    assert written["status"] == "first_submission_required"
    assert written["specpmPrepareReport"]["diagnosticCode"] == MISSING_BASELINE_DIAGNOSTIC


def test_baseline_submission_handoff_cli_rejects_non_missing_baseline_report(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fresh_run = write_fresh_run(tmp_path)
    prepare_report = write_prepare_report(tmp_path, missing_baseline=False)

    exit_code = main(
        [
            "baseline-submission-handoff",
            "--fresh-candidate-refresh-run",
            str(fresh_run),
            "--specpm-prepare-report",
            str(prepare_report),
        ]
    )

    printed = json.loads(capsys.readouterr().out)
    assert exit_code == 2
    assert printed["status"] == "error"
    assert MISSING_BASELINE_DIAGNOSTIC in printed["message"]


def write_fresh_run(tmp_path: Path) -> Path:
    smoke = tmp_path / "xyflow-smoke"
    smoke_report = run_xyflow_package_set_smoke(XyflowPackageSetSmokeOptions(output=smoke))
    assert smoke_report["status"] == "passed"
    report = build_fresh_candidate_refresh_run(
        FreshCandidateRefreshRunOptions(
            bundle_set=smoke / "package-set",
            fresh_generated_root=tmp_path / "fresh-generated",
        )
    )
    output = tmp_path / "fresh-candidate-refresh-run.json"
    write_fresh_candidate_refresh_run(output, report)
    return output


def write_prepare_report(tmp_path: Path, *, missing_baseline: bool) -> Path:
    errors = []
    if missing_baseline:
        errors.append(
            {
                "code": MISSING_BASELINE_DIAGNOSTIC,
                "field": "packageIds[0]",
                "message": "Current generated artifact has no contract files.",
            }
        )
    else:
        errors.append(
            {
                "code": "refresh_decision_prepare_version_mismatch",
                "field": "version",
                "message": "Different failure, not a missing baseline.",
            }
        )
    report = {
        "decision": {
            "decision": {
                "status": "manual_review_required",
                "reason": "refresh_prepare_requires_review",
            }
        },
        "errors": errors,
    }
    output = tmp_path / f"prepare-report-{missing_baseline}.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output
