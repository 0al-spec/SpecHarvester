from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.smoke_triage import build_smoke_triage_summary


def test_build_smoke_triage_summary_groups_report_signals(tmp_path: Path) -> None:
    batch = write_json(
        tmp_path / "batch-validation.json",
        {
            "kind": "SpecHarvesterBatchValidationReport",
            "status": "ok",
            "summary": {
                "collectedCount": 4,
                "skippedCount": 0,
                "warningCount": 1,
            },
        },
    )
    governance = write_json(
        tmp_path / "governance-claims.json",
        {
            "kind": "SpecHarvesterGovernanceDuplicateClaimReport",
            "status": "partial",
            "summary": {
                "records": 4,
                "duplicateIntentCount": 2,
                "duplicateCapabilityCount": 1,
                "issueCount": 1,
            },
        },
    )
    namespace = write_json(
        tmp_path / "namespace-upstream.json",
        {
            "kind": "SpecHarvesterNamespaceUpstreamReviewReport",
            "status": "ok",
            "summary": {
                "records": 4,
                "duplicateNamespaceCount": 0,
                "missingUpstreamCount": 0,
                "upstreamMismatchCount": 0,
                "issueCount": 0,
            },
        },
    )
    license_report = write_json(
        tmp_path / "license-provenance.json",
        {
            "kind": "SpecHarvesterLicenseProvenanceRiskReport",
            "status": "partial",
            "summary": {
                "records": 4,
                "issueCount": 1,
                "riskCounts": {"high": 0, "medium": 1, "low": 0},
                "issuesByCode": {"absent_license_evidence": 1},
            },
        },
    )

    summary = build_smoke_triage_summary(
        batch_validation=batch,
        governance_claims=governance,
        namespace_upstream=namespace,
        license_provenance=license_report,
    )

    assert summary["kind"] == "SpecHarvesterLocalSmokeTriageSummary"
    assert summary["status"] == "attention_required"
    assert summary["summary"] == {
        "batchWarningCount": 1,
        "duplicateClaimCount": 3,
        "duplicateIssueCount": 1,
        "namespaceIssueCount": 0,
        "licenseIssueCount": 1,
        "totalIssueCount": 6,
    }
    assert summary["reports"]["batchValidation"]["path"] == str(batch)
    assert summary["reports"]["duplicateClaims"]["duplicateIntentCount"] == 2
    assert summary["reports"]["duplicateClaims"]["issueCount"] == 1
    assert summary["reports"]["licenseProvenance"]["issuesByCode"] == {"absent_license_evidence": 1}


def test_cli_smoke_triage_summary_writes_output_file(tmp_path: Path) -> None:
    batch = write_json(
        tmp_path / "batch-validation.json",
        {"status": "ok", "summary": {"collectedCount": 1, "warningCount": 0}},
    )
    governance = write_json(
        tmp_path / "governance-claims.json",
        {
            "status": "ok",
            "summary": {
                "duplicateIntentCount": 0,
                "duplicateCapabilityCount": 0,
                "issueCount": 0,
            },
        },
    )
    namespace = write_json(
        tmp_path / "namespace-upstream.json",
        {
            "status": "ok",
            "summary": {
                "duplicateNamespaceCount": 0,
                "missingUpstreamCount": 0,
                "upstreamMismatchCount": 0,
                "issueCount": 0,
            },
        },
    )
    license_report = write_json(
        tmp_path / "license-provenance.json",
        {
            "status": "ok",
            "summary": {
                "issueCount": 0,
                "riskCounts": {"high": 0, "medium": 0, "low": 0},
                "issuesByCode": {},
            },
        },
    )
    output = tmp_path / "smoke-triage.json"

    exit_code = main(
        [
            "smoke-triage-summary",
            "--batch-validation",
            str(batch),
            "--governance-claims",
            str(governance),
            "--namespace-upstream",
            str(namespace),
            "--license-provenance",
            str(license_report),
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["status"] == "ok"
    assert payload["summary"]["totalIssueCount"] == 0


def write_json(path: Path, payload: dict[str, object]) -> Path:
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    return path
