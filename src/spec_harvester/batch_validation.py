from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BATCH_VALIDATION_REPORT_KIND = "SpecHarvesterBatchValidationReport"
BATCH_VALIDATION_REPORT_SCHEMA_VERSION = 1

EXPECTED_POLICY = {
    "execution": "none",
    "networkAccess": "none",
    "packageScripts": "not_run",
    "contentAuthority": "untrusted_metadata",
}

TRUST_BOUNDARY_NOTES = [
    "Report generation only summarizes already prepared batch snapshots.",
    "No repository clone, fetch, package manager, package script, build tool, "
    "or analyzer execution is performed by the report step.",
    "Collected repository content remains untrusted static evidence until human "
    "review and SpecPM validation.",
]


def build_batch_validation_report(
    *,
    batch_result: dict[str, Any],
    snapshots_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    records = [
        validation_record(collected, snapshots_by_id[collected["id"]])
        for collected in batch_result["collected"]
    ]
    confidence_counts = {
        "high": sum(1 for record in records if record["confidence"] == "high"),
        "medium": sum(1 for record in records if record["confidence"] == "medium"),
        "low": sum(1 for record in records if record["confidence"] == "low"),
    }
    warning_count = sum(len(record["warnings"]) for record in records)

    return {
        "schemaVersion": BATCH_VALIDATION_REPORT_SCHEMA_VERSION,
        "kind": BATCH_VALIDATION_REPORT_KIND,
        "status": batch_result["status"],
        "input": batch_result["input"],
        "outputRoot": batch_result["outputRoot"],
        "selectedIds": batch_result["selectedIds"],
        "summary": {
            "collectedCount": len(records),
            "skippedCount": len(batch_result["skipped"]),
            "highConfidenceCount": confidence_counts["high"],
            "mediumConfidenceCount": confidence_counts["medium"],
            "lowConfidenceCount": confidence_counts["low"],
            "warningCount": warning_count,
        },
        "records": records,
        "skippedRecords": batch_result["skipped"],
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def validation_record(collected: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    summary = snapshot.get("summary", {})
    evidence = {
        "fileCount": int(summary.get("fileCount", 0)),
        "skippedFileCount": int(summary.get("skippedFileCount", 0)),
        "packageManifestCount": int(summary.get("packageManifestCount", 0)),
    }
    warnings = validation_warnings(collected, snapshot, evidence)
    confidence = confidence_level(warnings, evidence)
    return {
        "id": collected["id"],
        "repository": collected["repository"],
        "revision": collected["revision"],
        "ref": collected["ref"],
        "output": collected["output"],
        "sourceManifest": collected["sourceManifest"],
        "evidence": evidence,
        "confidence": confidence,
        "confidenceReasons": confidence_reasons(confidence, warnings, evidence),
        "policyNotes": policy_notes(snapshot),
        "warnings": warnings,
    }


def validation_warnings(
    collected: dict[str, Any],
    snapshot: dict[str, Any],
    evidence: dict[str, int],
) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    if policy_mismatches(snapshot):
        warnings.append(
            {
                "code": "collector_policy_mismatch",
                "message": "Snapshot policy does not match the safe static collection policy.",
            }
        )
    if collected["revision"] is None and collected["ref"] is not None:
        warnings.append(
            {
                "code": "source_ref_not_pinned_revision",
                "message": "Repository source used a ref instead of a pinned revision.",
            }
        )
    if evidence["fileCount"] == 0:
        warnings.append(
            {
                "code": "no_files_collected",
                "message": "Snapshot contains no collected allowlisted files.",
            }
        )
    if evidence["skippedFileCount"] > 0:
        warnings.append(
            {
                "code": "files_skipped",
                "message": "Snapshot skipped one or more allowlisted candidate files.",
            }
        )
    if evidence["packageManifestCount"] == 0:
        warnings.append(
            {
                "code": "no_package_manifests",
                "message": "Snapshot contains no recognized package manifest files.",
            }
        )
    return warnings


def policy_mismatches(snapshot: dict[str, Any]) -> dict[str, Any]:
    policy = snapshot.get("policy", {})
    return {
        key: policy.get(key)
        for key, expected in EXPECTED_POLICY.items()
        if policy.get(key) != expected
    }


def confidence_level(warnings: list[dict[str, str]], evidence: dict[str, int]) -> str:
    warning_codes = {warning["code"] for warning in warnings}
    if "collector_policy_mismatch" in warning_codes or evidence["fileCount"] == 0:
        return "low"
    if warnings:
        return "medium"
    return "high"


def confidence_reasons(
    confidence: str,
    warnings: list[dict[str, str]],
    evidence: dict[str, int],
) -> list[str]:
    if confidence == "high":
        return [
            "Snapshot policy matches safe static collection requirements.",
            "Snapshot has collected files and at least one package manifest.",
            "No review warnings were emitted.",
        ]
    reasons = [f"warning:{warning['code']}" for warning in warnings]
    if evidence["fileCount"] == 0 and "warning:no_files_collected" not in reasons:
        reasons.append("warning:no_files_collected")
    return reasons


def policy_notes(snapshot: dict[str, Any]) -> list[str]:
    policy = snapshot.get("policy", {})
    return [
        f"execution={policy.get('execution')}",
        f"networkAccess={policy.get('networkAccess')}",
        f"packageScripts={policy.get('packageScripts')}",
        f"contentAuthority={policy.get('contentAuthority')}",
    ]


def write_batch_validation_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
