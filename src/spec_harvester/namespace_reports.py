from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.report_source_records import (
    ReportSourceIssuePolicy,
    SpecpmReportSourceRecords,
)
from spec_harvester.specpm_manifest import ManifestArtifact, SpecPackageManifest
from spec_harvester.upstream_issue_evaluation import (
    UpstreamIssuePolicy,
    namespace_matches_upstream,  # noqa: F401 - re-exported for existing callers.
    normalized_identifier_key,  # noqa: F401 - re-exported for existing callers.
    parse_upstream_owner,  # noqa: F401 - re-exported for existing callers.
    parse_upstream_repository_reference,  # noqa: F401 - re-exported for existing callers.
    upstream_issue_subjects,
)

NAMESPACE_UPSTREAM_REPORT_KIND = "SpecHarvesterNamespaceUpstreamReviewReport"
NAMESPACE_UPSTREAM_REPORT_SCHEMA_VERSION = 1

TRUST_BOUNDARY_NOTES = [
    "Report generation reads local `specpm.yaml` metadata only.",
    "No repository code execution, network access, dependency installation, "
    "or analyzer execution is performed.",
    "The report is advisory and does not update or validate any accepted content.",
]


@dataclass(frozen=True)
class UpstreamArtifactRecord:
    artifact_id: str
    uri: str
    role: str | None = None
    revision: str | None = None


@dataclass(frozen=True)
class PackageNamespaceUpstreamRecord:
    path: str
    source: str
    package_id: str
    package_version: str
    namespace: str
    upstream_artifacts: tuple[UpstreamArtifactRecord, ...]


def build_namespace_upstream_report(
    *,
    accepted_root: Path | None = None,
    candidates_root: Path | None = None,
) -> dict[str, Any]:
    if accepted_root is None and candidates_root is None:
        raise ValueError("At least one of accepted_root or candidates_root must be provided.")

    records, issues = collect_namespace_upstream_records(accepted_root, candidates_root)
    duplicate_namespaces = namespace_duplicates(records)

    upstream_checks = namespace_upstream_checks(records)
    issues.extend(upstream_checks)

    missing_upstream_count = sum(
        1 for issue in issues if issue["code"] == "missing_upstream_repository"
    )
    mismatch_count = sum(1 for issue in issues if issue["code"] == "upstream_namespace_mismatch")
    invalid_uri_count = sum(
        1 for issue in issues if issue["code"] == "invalid_upstream_repository_uri"
    )

    return {
        "schemaVersion": NAMESPACE_UPSTREAM_REPORT_SCHEMA_VERSION,
        "kind": NAMESPACE_UPSTREAM_REPORT_KIND,
        "status": "partial" if issues else "ok",
        "summary": {
            "records": len(records),
            "duplicateNamespaceCount": len(duplicate_namespaces),
            "missingUpstreamCount": missing_upstream_count,
            "upstreamMismatchCount": mismatch_count + invalid_uri_count,
            "issueCount": len(issues),
        },
        "records": [namespace_record_to_dict(record) for record in records],
        "duplicates": {
            "namespace": duplicate_namespaces,
        },
        "issues": issues,
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def collect_namespace_upstream_records(
    accepted_root: Path | None,
    candidates_root: Path | None,
) -> tuple[list[PackageNamespaceUpstreamRecord], list[dict[str, str]]]:
    return SpecpmReportSourceRecords(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
        parse_manifest=parse_specpm_namespace_upstream,
        issue_policy=ReportSourceIssuePolicy(
            symlink_message="Skip symlinked specpm.yaml in namespace/upstream report scan.",
        ),
        sort_key=lambda item: (item.source, item.path),
    ).collect()


def namespace_record_to_dict(record: PackageNamespaceUpstreamRecord) -> dict[str, Any]:
    return {
        "path": record.path,
        "source": record.source,
        "packageId": record.package_id,
        "packageVersion": record.package_version,
        "namespace": record.namespace,
        "upstreamArtifacts": [
            {
                "id": artifact.artifact_id,
                "uri": artifact.uri,
                **({"role": artifact.role} if artifact.role is not None else {}),
                **({"revision": artifact.revision} if artifact.revision is not None else {}),
            }
            for artifact in record.upstream_artifacts
        ],
    }


def namespace_duplicates(
    records: list[PackageNamespaceUpstreamRecord],
) -> list[dict[str, Any]]:
    namespace_map: dict[str, list[dict[str, str]]] = {}
    for record in records:
        namespace_map.setdefault(record.namespace, []).append(
            {
                "packageId": record.package_id,
                "packageVersion": record.package_version,
                "path": record.path,
                "source": record.source,
            }
        )

    duplicates: list[dict[str, Any]] = []
    for namespace, claimants in sorted(namespace_map.items(), key=lambda item: item[0]):
        if len(claimants) > 1:
            duplicates.append(
                {
                    "namespace": namespace,
                    "count": len(claimants),
                    "claimants": sorted(
                        claimants,
                        key=lambda item: (item["source"], item["packageId"], item["path"]),
                    ),
                }
            )
    return duplicates


def namespace_upstream_checks(
    records: list[PackageNamespaceUpstreamRecord],
) -> list[dict[str, str]]:
    policy = UpstreamIssuePolicy(
        missing_message="No upstream_repository entry in foreignArtifacts."
    )
    return policy.evaluate(upstream_issue_subjects(records))


def parse_specpm_namespace_upstream(
    manifest_path: Path,
    source: str,
) -> PackageNamespaceUpstreamRecord:
    manifest = SpecPackageManifest.from_path(manifest_path)
    package_id, package_version = manifest.require_identity()

    return PackageNamespaceUpstreamRecord(
        path=str(manifest_path),
        source=source,
        package_id=package_id,
        package_version=package_version,
        namespace=manifest.namespace(),
        upstream_artifacts=tuple(_normalize_artifact(artifact) for artifact in manifest.artifacts),
    )


def _normalize_artifact(artifact: ManifestArtifact) -> UpstreamArtifactRecord:
    return UpstreamArtifactRecord(
        artifact_id=artifact.artifact_id(),
        uri=artifact.uri(),
        role=artifact.role(),
        revision=artifact.revision(),
    )


def write_namespace_upstream_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
