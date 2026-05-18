from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SMOKE_TRIAGE_SUMMARY_KIND = "SpecHarvesterLocalSmokeTriageSummary"
SMOKE_TRIAGE_SUMMARY_SCHEMA_VERSION = 1

TRUST_BOUNDARY_NOTES = [
    "Summary generation reads existing local smoke JSON reports only.",
    (
        "No repository code execution, package installation, network access, "
        "or analyzer execution is performed."
    ),
    (
        "The summary is advisory and does not mutate candidates, accepted packages, "
        "or detailed reports."
    ),
]


def build_smoke_triage_summary(
    *,
    batch_validation: Path,
    governance_claims: Path,
    namespace_upstream: Path,
    license_provenance: Path,
) -> dict[str, Any]:
    batch_report = read_json_report(batch_validation)
    duplicate_report = read_json_report(governance_claims)
    namespace_report = read_json_report(namespace_upstream)
    license_report = read_json_report(license_provenance)

    batch_summary = dict_summary(batch_report)
    duplicate_summary = dict_summary(duplicate_report)
    namespace_summary = dict_summary(namespace_report)
    license_summary = dict_summary(license_report)

    batch_warning_count = int_value(batch_summary, "warningCount")
    duplicate_claim_count = int_value(duplicate_summary, "duplicateIntentCount") + int_value(
        duplicate_summary, "duplicateCapabilityCount"
    )
    namespace_issue_count = int_value(namespace_summary, "issueCount")
    license_issue_count = int_value(license_summary, "issueCount")
    total_issue_count = (
        batch_warning_count + duplicate_claim_count + namespace_issue_count + license_issue_count
    )

    return {
        "schemaVersion": SMOKE_TRIAGE_SUMMARY_SCHEMA_VERSION,
        "kind": SMOKE_TRIAGE_SUMMARY_KIND,
        "status": "attention_required" if total_issue_count else "ok",
        "summary": {
            "batchWarningCount": batch_warning_count,
            "duplicateClaimCount": duplicate_claim_count,
            "namespaceIssueCount": namespace_issue_count,
            "licenseIssueCount": license_issue_count,
            "totalIssueCount": total_issue_count,
        },
        "reports": {
            "batchValidation": {
                "path": str(batch_validation),
                "status": str(batch_report.get("status", "unknown")),
                "collectedCount": int_value(batch_summary, "collectedCount"),
                "skippedCount": int_value(batch_summary, "skippedCount"),
                "warningCount": batch_warning_count,
            },
            "duplicateClaims": {
                "path": str(governance_claims),
                "status": str(duplicate_report.get("status", "unknown")),
                "duplicateIntentCount": int_value(duplicate_summary, "duplicateIntentCount"),
                "duplicateCapabilityCount": int_value(
                    duplicate_summary, "duplicateCapabilityCount"
                ),
                "issueCount": int_value(duplicate_summary, "issueCount"),
            },
            "namespaceUpstream": {
                "path": str(namespace_upstream),
                "status": str(namespace_report.get("status", "unknown")),
                "duplicateNamespaceCount": int_value(namespace_summary, "duplicateNamespaceCount"),
                "missingUpstreamCount": int_value(namespace_summary, "missingUpstreamCount"),
                "upstreamMismatchCount": int_value(namespace_summary, "upstreamMismatchCount"),
                "issueCount": namespace_issue_count,
            },
            "licenseProvenance": {
                "path": str(license_provenance),
                "status": str(license_report.get("status", "unknown")),
                "issueCount": license_issue_count,
                "riskCounts": dict_value(license_summary, "riskCounts"),
                "issuesByCode": dict_value(license_summary, "issuesByCode"),
            },
        },
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def read_json_report(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON report at {path}: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"JSON report must be an object: {path}")
    return payload


def dict_summary(report: dict[str, Any]) -> dict[str, Any]:
    summary = report.get("summary")
    if isinstance(summary, dict):
        return summary
    return {}


def int_value(values: dict[str, Any], key: str) -> int:
    value = values.get(key, 0)
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    return 0


def dict_value(values: dict[str, Any], key: str) -> dict[str, Any]:
    value = values.get(key)
    if isinstance(value, dict):
        return {str(item_key): value[item_key] for item_key in sorted(value)}
    return {}


def write_smoke_triage_summary(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
