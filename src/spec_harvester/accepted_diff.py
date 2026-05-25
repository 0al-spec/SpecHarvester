from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.specpm_manifest import SpecPackageManifest

ACCEPTED_CANDIDATE_DIFF_REPORT_KIND = "SpecHarvesterAcceptedCandidateDiffReport"
ACCEPTED_CANDIDATE_DIFF_REPORT_SCHEMA_VERSION = 1

TRUST_BOUNDARY_NOTES = [
    "Report generation reads local `specpm.yaml` metadata only.",
    "No SpecPM validation, repository code execution, package installation, network access, "
    "or analyzer execution occurs.",
    "The report is advisory and does not mutate candidate or accepted package content.",
]

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+([0-9A-Za-z.-]+))?$")


@dataclass(frozen=True)
class PackageDiffInputRecord:
    path: str
    source: str
    package_id: str
    package_version: str
    metadata: dict[str, str]
    intents: tuple[str, ...]
    capabilities: tuple[str, ...]
    upstream_artifacts: tuple[dict[str, str], ...]


def build_accepted_candidate_diff_report(
    *,
    accepted_root: Path,
    candidates_root: Path,
) -> dict[str, Any]:
    accepted_records, accepted_issues = collect_package_diff_records(accepted_root, "accepted")
    candidate_records, candidate_issues = collect_package_diff_records(candidates_root, "candidate")
    issues = accepted_issues + candidate_issues

    accepted_by_id = latest_accepted_by_package_id(accepted_records)
    comparisons = [
        build_candidate_comparison(candidate, accepted_by_id.get(candidate.package_id))
        for candidate in sorted(
            candidate_records,
            key=lambda item: (item.package_id, semver_sort_key(item.package_version), item.path),
        )
    ]

    return {
        "schemaVersion": ACCEPTED_CANDIDATE_DIFF_REPORT_SCHEMA_VERSION,
        "kind": ACCEPTED_CANDIDATE_DIFF_REPORT_KIND,
        "status": "partial" if issues else "ok",
        "summary": {
            "acceptedRecords": len(accepted_records),
            "candidateRecords": len(candidate_records),
            "comparedCount": sum(1 for item in comparisons if item["status"] != "new_package"),
            "newPackageCount": sum(1 for item in comparisons if item["status"] == "new_package"),
            "changedCount": sum(1 for item in comparisons if item["status"] == "changed"),
            "unchangedCount": sum(1 for item in comparisons if item["status"] == "unchanged"),
            "issueCount": len(issues),
        },
        "comparisons": comparisons,
        "issues": sorted(issues, key=lambda item: (item["path"], item["code"])),
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def collect_package_diff_records(
    source_root: Path,
    source: str,
) -> tuple[list[PackageDiffInputRecord], list[dict[str, str]]]:
    root = source_root.resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Source root does not exist or is not a directory: {root}")

    records: list[PackageDiffInputRecord] = []
    issues: list[dict[str, str]] = []
    for manifest_path in sorted(root.rglob("specpm.yaml"), key=lambda item: str(item)):
        if manifest_path.is_symlink():
            issues.append(
                {
                    "path": str(manifest_path),
                    "source": source,
                    "code": "specpm_symlink",
                    "message": "Skip symlinked specpm.yaml in accepted/candidate diff scan.",
                }
            )
            continue
        try:
            records.append(parse_specpm_diff_record(manifest_path, source))
        except ValueError as exc:
            issues.append(
                {
                    "path": str(manifest_path),
                    "source": source,
                    "code": "invalid_specpm_manifest",
                    "message": str(exc),
                }
            )

    return sorted(records, key=lambda item: (item.source, item.package_id, item.path)), issues


def parse_specpm_diff_record(manifest_path: Path, source: str) -> PackageDiffInputRecord:
    manifest = SpecPackageManifest.from_path(manifest_path)
    package_id, package_version = manifest.require_identity()

    return PackageDiffInputRecord(
        path=str(manifest_path),
        source=source,
        package_id=package_id,
        package_version=package_version,
        metadata=manifest.metadata_strings(),
        intents=manifest.intents,
        capabilities=manifest.capabilities,
        upstream_artifacts=tuple(
            sorted((artifact.as_dict() for artifact in manifest.artifacts), key=artifact_sort_key)
        ),
    )


def latest_accepted_by_package_id(
    records: list[PackageDiffInputRecord],
) -> dict[str, PackageDiffInputRecord]:
    latest: dict[str, PackageDiffInputRecord] = {}
    for record in records:
        current = latest.get(record.package_id)
        if current is None or semver_sort_key(record.package_version) > semver_sort_key(
            current.package_version
        ):
            latest[record.package_id] = record
    return latest


def build_candidate_comparison(
    candidate: PackageDiffInputRecord,
    accepted: PackageDiffInputRecord | None,
) -> dict[str, Any]:
    if accepted is None:
        return {
            "packageId": candidate.package_id,
            "oldPackageVersion": None,
            "newPackageVersion": candidate.package_version,
            "status": "new_package",
            "accepted": None,
            "candidate": record_reference(candidate),
            "changes": {
                "metadata": [],
                "intents": {"added": list(candidate.intents), "removed": []},
                "capabilities": {"added": list(candidate.capabilities), "removed": []},
                "upstreamArtifacts": {
                    "changed": bool(candidate.upstream_artifacts),
                    "old": [],
                    "new": list(candidate.upstream_artifacts),
                },
            },
        }

    changes = diff_records(accepted, candidate)
    status = "changed" if has_changes(changes) else "unchanged"
    return {
        "packageId": candidate.package_id,
        "oldPackageVersion": accepted.package_version,
        "newPackageVersion": candidate.package_version,
        "status": status,
        "accepted": record_reference(accepted),
        "candidate": record_reference(candidate),
        "changes": changes,
    }


def diff_records(
    accepted: PackageDiffInputRecord,
    candidate: PackageDiffInputRecord,
) -> dict[str, Any]:
    accepted_intents = set(accepted.intents)
    candidate_intents = set(candidate.intents)
    accepted_capabilities = set(accepted.capabilities)
    candidate_capabilities = set(candidate.capabilities)
    upstream_changed = accepted.upstream_artifacts != candidate.upstream_artifacts

    return {
        "metadata": diff_metadata(accepted.metadata, candidate.metadata),
        "intents": {
            "added": sorted(candidate_intents - accepted_intents),
            "removed": sorted(accepted_intents - candidate_intents),
        },
        "capabilities": {
            "added": sorted(candidate_capabilities - accepted_capabilities),
            "removed": sorted(accepted_capabilities - candidate_capabilities),
        },
        "upstreamArtifacts": {
            "changed": upstream_changed,
            "old": list(accepted.upstream_artifacts) if upstream_changed else [],
            "new": list(candidate.upstream_artifacts) if upstream_changed else [],
        },
    }


def diff_metadata(old: dict[str, str], new: dict[str, str]) -> list[dict[str, str | None]]:
    fields = sorted(set(old) | set(new))
    changes = []
    for field in fields:
        old_value = old.get(field)
        new_value = new.get(field)
        if old_value != new_value:
            changes.append({"field": field, "old": old_value, "new": new_value})
    return changes


def has_changes(changes: dict[str, Any]) -> bool:
    return bool(
        changes["metadata"]
        or changes["intents"]["added"]
        or changes["intents"]["removed"]
        or changes["capabilities"]["added"]
        or changes["capabilities"]["removed"]
        or changes["upstreamArtifacts"]["changed"]
    )


def record_reference(record: PackageDiffInputRecord) -> dict[str, str]:
    return {
        "path": record.path,
        "source": record.source,
        "packageId": record.package_id,
        "packageVersion": record.package_version,
    }


def semver_sort_key(version: str) -> tuple[tuple[int, int, int], int, tuple[Any, ...], str]:
    match = SEMVER_RE.match(version)
    if match is None:
        return ((-1, -1, -1), 0, (), version)
    major, minor, patch, prerelease, _build = match.groups()
    prerelease_items = tuple(parse_prerelease_item(item) for item in (prerelease or "").split("."))
    stable_rank = 1 if prerelease is None else 0
    return ((int(major), int(minor), int(patch)), stable_rank, prerelease_items, version)


def parse_prerelease_item(value: str) -> tuple[int, int | str]:
    if value.isdigit():
        return (0, int(value))
    return (1, value)


def artifact_sort_key(item: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        item.get("id", ""),
        item.get("uri", ""),
        item.get("role", ""),
        item.get("revision", ""),
    )


def write_accepted_candidate_diff_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
