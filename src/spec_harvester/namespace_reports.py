from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from spec_harvester.promoter import parse_yaml_scalar

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
class UpstreamRepositoryReference:
    owner: str
    name: str


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
    records: list[PackageNamespaceUpstreamRecord] = []
    issues: list[dict[str, str]] = []

    if accepted_root is not None:
        _collect_source_records(accepted_root, "accepted", records, issues)
    if candidates_root is not None:
        _collect_source_records(candidates_root, "candidate", records, issues)

    records.sort(key=lambda item: (item.source, item.path))
    return records, issues


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
    issues: list[dict[str, str]] = []
    for record in records:
        upstream_entries = [
            entry
            for entry in record.upstream_artifacts
            if entry.artifact_id == "upstream_repository"
        ]
        if not upstream_entries:
            issues.append(
                {
                    "path": record.path,
                    "packageId": record.package_id,
                    "packageVersion": record.package_version,
                    "code": "missing_upstream_repository",
                    "message": "No upstream_repository entry in foreignArtifacts.",
                }
            )
            continue

        if len(upstream_entries) > 1:
            issues.append(
                {
                    "path": record.path,
                    "packageId": record.package_id,
                    "packageVersion": record.package_version,
                    "code": "duplicate_upstream_repository_entries",
                    "message": "Multiple upstream_repository artifacts found.",
                }
            )

        for entry in upstream_entries:
            if not entry.uri:
                issues.append(
                    {
                        "path": record.path,
                        "packageId": record.package_id,
                        "packageVersion": record.package_version,
                        "code": "invalid_upstream_repository_uri",
                        "message": "upstream_repository artifact missing URI.",
                    }
                )
                continue
            upstream = parse_upstream_repository_reference(entry.uri)
            if upstream is None:
                issues.append(
                    {
                        "path": record.path,
                        "packageId": record.package_id,
                        "packageVersion": record.package_version,
                        "code": "invalid_upstream_repository_uri",
                        "message": f"Could not parse upstream owner from URI: {entry.uri}",
                    }
                )
                continue
            if not namespace_matches_upstream(record.namespace, upstream):
                issues.append(
                    {
                        "path": record.path,
                        "packageId": record.package_id,
                        "packageVersion": record.package_version,
                        "code": "upstream_namespace_mismatch",
                        "message": (
                            f"Package namespace `{record.namespace}` does not match inferred "
                            f"upstream owner `{upstream.owner}` or repository "
                            f"`{upstream.name}`."
                        ),
                    }
                )

    return sorted(issues, key=lambda item: (item["path"], item["code"]))


def namespace_matches_upstream(namespace: str, upstream: UpstreamRepositoryReference) -> bool:
    normalized_namespace = namespace.strip().lower()
    return normalized_namespace in {upstream.owner.lower(), upstream.name.lower()}


def parse_upstream_owner(uri: str) -> str | None:
    upstream = parse_upstream_repository_reference(uri)
    if upstream is None:
        return None
    return upstream.owner


def parse_upstream_repository_reference(uri: str) -> UpstreamRepositoryReference | None:
    text = uri.strip().strip("'\"")
    if text.startswith("git@github.com:"):
        body = text.removeprefix("git@github.com:")
        parts = body.strip("/").split("/")
    elif text.startswith("https://github.com/") or text.startswith("http://github.com/"):
        parsed = urlparse(text)
        parts = parsed.path.strip("/").split("/")
    else:
        return None

    if len(parts) < 2 or not parts[0] or not parts[1]:
        return None
    repository_name = strip_git_suffix(parts[1])
    if not repository_name:
        return None
    return UpstreamRepositoryReference(owner=parts[0], name=repository_name)


def strip_git_suffix(name: str) -> str:
    if name.endswith(".git"):
        return name.removesuffix(".git")
    return name


def _collect_source_records(
    source_root: Path,
    source: str,
    records: list[PackageNamespaceUpstreamRecord],
    issues: list[dict[str, str]],
) -> None:
    root = source_root.resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Source root does not exist or is not a directory: {root}")

    for manifest_path in sorted(root.rglob("specpm.yaml"), key=lambda item: str(item)):
        if manifest_path.is_symlink():
            issues.append(
                {
                    "path": str(manifest_path),
                    "code": "specpm_symlink",
                    "message": "Skip symlinked specpm.yaml in namespace/upstream report scan.",
                }
            )
            continue
        try:
            package = parse_specpm_namespace_upstream(manifest_path, source)
        except ValueError as exc:
            issues.append(
                {
                    "path": str(manifest_path),
                    "code": "invalid_specpm_manifest",
                    "message": str(exc),
                }
            )
            continue
        records.append(package)


def parse_specpm_namespace_upstream(
    manifest_path: Path,
    source: str,
) -> PackageNamespaceUpstreamRecord:
    metadata: dict[str, str] = {}
    artifacts: list[UpstreamArtifactRecord] = []

    parse_state = "root"
    current_artifact: dict[str, str] | None = None

    for raw_line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip(" "))
        text = line.strip()

        if indent == 0:
            if parse_state == "foreignArtifacts" and current_artifact is not None:
                artifacts.append(_normalize_artifact(current_artifact))
                current_artifact = None
            if text == "metadata:":
                parse_state = "metadata"
                continue
            if text == "foreignArtifacts:":
                parse_state = "foreignArtifacts"
                continue
            parse_state = "root"
            continue

        if parse_state == "metadata":
            if indent != 2 or ":" not in text:
                continue
            key, raw_value = text.split(":", 1)
            metadata[key.strip()] = parse_yaml_scalar(raw_value.strip())
            continue

        if parse_state == "foreignArtifacts":
            if indent == 2:
                if text.startswith("- "):
                    if current_artifact is not None:
                        artifacts.append(_normalize_artifact(current_artifact))
                    current_artifact = {}
                    text = text[2:].strip()
                    if ":" in text:
                        key, raw_value = text.split(":", 1)
                        current_artifact[key.strip()] = parse_yaml_scalar(raw_value.strip())
                    continue
                parse_state = "root"
                if current_artifact is not None:
                    artifacts.append(_normalize_artifact(current_artifact))
                    current_artifact = None
                continue

            if indent >= 4 and current_artifact is not None and ":" in text:
                key, raw_value = text.split(":", 1)
                current_artifact[key.strip()] = parse_yaml_scalar(raw_value.strip())
                continue

            if indent < 4:
                if current_artifact is not None:
                    artifacts.append(_normalize_artifact(current_artifact))
                    current_artifact = None
                parse_state = "root"

    if current_artifact is not None:
        artifacts.append(_normalize_artifact(current_artifact))

    package_id = metadata.get("id", "").strip()
    package_version = metadata.get("version", "").strip()
    if not package_id or not package_version:
        raise ValueError("specpm.yaml must contain metadata.id and metadata.version.")

    namespace = package_id.split(".")[0] if "." in package_id else package_id

    return PackageNamespaceUpstreamRecord(
        path=str(manifest_path),
        source=source,
        package_id=package_id,
        package_version=package_version,
        namespace=namespace,
        upstream_artifacts=tuple(artifacts),
    )


def _normalize_artifact(values: dict[str, str]) -> UpstreamArtifactRecord:
    artifact_id = str(values.get("id", "")).strip()
    if not artifact_id:
        artifact_id = str(values.get("artifact", "")).strip()

    uri = values.get("uri")
    uri_value = str(uri).strip() if uri is not None else ""
    role = values.get("role")
    role_value = str(role).strip() if role is not None else None
    revision = values.get("revision")
    revision_value = str(revision).strip() if revision is not None else None

    return UpstreamArtifactRecord(
        artifact_id=artifact_id,
        uri=uri_value,
        role=role_value,
        revision=revision_value,
    )


def write_namespace_upstream_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
