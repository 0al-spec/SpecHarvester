from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from spec_harvester.accepted_diff import (
    PackageDiffInputRecord,
    build_accepted_candidate_diff_report,
    parse_specpm_diff_record,
)

ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_KIND = (
    "SpecHarvesterAcceptedCandidateImpactClassificationReport"
)
ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_SCHEMA_VERSION = 1

TRUST_BOUNDARY_NOTES = [
    "Report generation reads local `specpm.yaml` metadata only.",
    "No repository code execution, dependency installation, network access, "
    "or analyzer execution is performed.",
    (
        "The report is advisory and does not update, validate, or mutate accepted "
        "or candidate package content."
    ),
]


def build_accepted_candidate_impact_report(
    *,
    accepted_root: Path,
    candidates_root: Path,
) -> dict[str, Any]:
    diff_report = build_accepted_candidate_diff_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    records: list[dict[str, Any]] = [
        build_impact_record(
            comparison,
        )
        for comparison in diff_report["comparisons"]
    ]

    return {
        "schemaVersion": ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_SCHEMA_VERSION,
        "kind": ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_KIND,
        "status": diff_report["status"],
        "summary": _build_summary(
            records,
            diff_report["summary"]["issueCount"],
        ),
        "comparisons": records,
        "issues": diff_report["issues"],
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def build_impact_record(
    comparison: dict[str, Any],
) -> dict[str, Any]:
    changes = comparison["changes"]
    capability_changes = changes["capabilities"]
    intent_changes = changes["intents"]

    metadata_bucket = _classify_metadata(comparison)
    provenance_bucket = _classify_provenance(changes["upstreamArtifacts"])
    interface_bucket = _classify_interface(
        capability_changes=capability_changes,
        intent_changes=intent_changes,
    )
    capability_bucket = _classify_claim_bucket(
        added=capability_changes["added"],
        removed=capability_changes["removed"],
    )
    intent_bucket = _classify_claim_bucket(
        added=intent_changes["added"],
        removed=intent_changes["removed"],
    )

    changed_claims = sorted(set(interface_bucket["added"] + interface_bucket["removed"]))

    return {
        "packageId": comparison["packageId"],
        "oldPackageVersion": comparison["oldPackageVersion"],
        "newPackageVersion": comparison["newPackageVersion"],
        "status": comparison["status"],
        "accepted": comparison["accepted"],
        "candidate": comparison["candidate"],
        "impact": {
            "metadata": metadata_bucket,
            "interface": interface_bucket,
            "license": _classify_license(metadata_bucket),
            "provenance": provenance_bucket,
            "capability": capability_bucket,
            "intent": intent_bucket,
        },
        "changedClaims": changed_claims,
    }


def _classify_metadata(
    comparison: dict[str, Any],
) -> dict[str, Any]:
    metadata_changes = list(comparison["changes"]["metadata"])

    if comparison["status"] == "new_package":
        manifest = _read_manifest_record(Path(comparison["candidate"]["path"]))
        metadata_changes = [
            {"field": key, "old": None, "new": manifest.metadata.get(key)}
            for key in sorted(manifest.metadata)
        ]
    return {
        "changed": bool(metadata_changes),
        "items": sorted(
            [change["field"] for change in metadata_changes],
            key=lambda item: str(item),
        ),
    }


def _classify_license(metadata_bucket: dict[str, Any]) -> dict[str, Any]:
    license_fields = [
        item for item in metadata_bucket["items"] if item.lower().startswith("license")
    ]
    return {
        "changed": bool(license_fields),
        "items": sorted(license_fields),
    }


def _classify_interface(
    *,
    capability_changes: dict[str, list[str]],
    intent_changes: dict[str, list[str]],
) -> dict[str, Any]:
    added = [f"capability:{item}" for item in capability_changes["added"]] + [
        f"intent:{item}" for item in intent_changes["added"]
    ]
    removed = [f"capability:{item}" for item in capability_changes["removed"]] + [
        f"intent:{item}" for item in intent_changes["removed"]
    ]
    return {
        "changed": bool(added or removed),
        "added": sorted(added),
        "removed": sorted(removed),
    }


def _classify_claim_bucket(
    *,
    added: list[str],
    removed: list[str],
) -> dict[str, Any]:
    return {
        "changed": bool(added or removed),
        "added": sorted(added),
        "removed": sorted(removed),
    }


def _classify_provenance(upstream_artifacts: dict[str, Any]) -> dict[str, Any]:
    old_artifacts = sorted(
        upstream_artifacts["old"],
        key=_artifact_sort_key,
    )
    new_artifacts = sorted(
        upstream_artifacts["new"],
        key=_artifact_sort_key,
    )

    old_counts = Counter(_artifact_signature(item) for item in old_artifacts)
    new_counts = Counter(_artifact_signature(item) for item in new_artifacts)
    removed_signatures: list[str] = []
    for signature, count in old_counts.items():
        delta = count - new_counts.get(signature, 0)
        removed_signatures.extend([signature] * max(delta, 0))

    added_signatures: list[str] = []
    for signature, count in new_counts.items():
        delta = count - old_counts.get(signature, 0)
        added_signatures.extend([signature] * max(delta, 0))

    old_items_by_signature: dict[str, list[dict[str, str]]] = {}
    new_items_by_signature: dict[str, list[dict[str, str]]] = {}
    for item in old_artifacts:
        old_items_by_signature.setdefault(_artifact_signature(item), []).append(item)
    for item in new_artifacts:
        new_items_by_signature.setdefault(_artifact_signature(item), []).append(item)

    removed: list[dict[str, str]] = []
    for signature in removed_signatures:
        removed.extend(old_items_by_signature.get(signature, []))
    added: list[dict[str, str]] = []
    for signature in added_signatures:
        added.extend(new_items_by_signature.get(signature, []))

    # Preserve stable ordering across runs for identical reports.
    removed.sort(key=_artifact_sort_key)
    added.sort(key=_artifact_sort_key)

    # Preserve deterministic provenance order and surface all details as plain objects.
    return {
        "changed": bool(added or removed),
        "added": added,
        "removed": removed,
    }


def _artifact_signature(item: dict[str, str]) -> str:
    return "|".join(
        (
            str(item.get("id", "")),
            str(item.get("uri", "")),
            str(item.get("role", "")),
            str(item.get("revision", "")),
        )
    )


def _artifact_sort_key(item: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        item.get("id", ""),
        item.get("uri", ""),
        item.get("role", ""),
        item.get("revision", ""),
    )


def _read_manifest_record(path: Path) -> PackageDiffInputRecord:
    return parse_specpm_diff_record(path, "candidate")


def _build_summary(
    records: list[dict[str, Any]],
    issue_count: int,
) -> dict[str, Any]:
    return {
        "recordCount": len(records),
        "metadataImpactCount": sum(1 for item in records if item["impact"]["metadata"]["changed"]),
        "interfaceImpactCount": sum(
            1 for item in records if item["impact"]["interface"]["changed"]
        ),
        "licenseImpactCount": sum(1 for item in records if item["impact"]["license"]["changed"]),
        "provenanceImpactCount": sum(
            1 for item in records if item["impact"]["provenance"]["changed"]
        ),
        "capabilityImpactCount": sum(
            1 for item in records if item["impact"]["capability"]["changed"]
        ),
        "intentImpactCount": sum(1 for item in records if item["impact"]["intent"]["changed"]),
        "changedCount": sum(1 for item in records if item["status"] == "changed"),
        "newPackageCount": sum(1 for item in records if item["status"] == "new_package"),
        "unchangedCount": sum(1 for item in records if item["status"] == "unchanged"),
        "issueCount": issue_count,
    }


def write_accepted_candidate_impact_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
