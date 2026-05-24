from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.namespace_reports import (
    namespace_matches_upstream,
    parse_upstream_repository_reference,
)
from spec_harvester.promoter import parse_yaml_scalar

LICENSE_PROVENANCE_REPORT_KIND = "SpecHarvesterLicenseProvenanceRiskReport"
LICENSE_PROVENANCE_REPORT_SCHEMA_VERSION = 1

TRUST_BOUNDARY_NOTES = [
    "Report generation reads local `specpm.yaml` metadata only.",
    (
        "No repository code execution, dependency installation, "
        "network access, or analyzer execution is performed."
    ),
    "The report is advisory and does not mutate candidate or accepted package content.",
]

KNOWN_LICENSE_HINTS = {
    "apache-2.0",
    "apache-2.0-or-later",
    "bsd-2-clause",
    "bsd-3-clause",
    "bsd-4-clause",
    "cc0-1.0",
    "cc-by-1.0",
    "cc-by-2.0",
    "cc-by-3.0",
    "cc-by-4.0",
    "epl-2.0",
    "gpl-2.0",
    "gpl-2.0-only",
    "gpl-2.0-or-later",
    "gpl-3.0",
    "gpl-3.0-only",
    "gpl-3.0-or-later",
    "gpl-3.0+",
    "isc",
    "lgpl-2.1",
    "lgpl-2.1-only",
    "lgpl-2.1-or-later",
    "lgpl-3.0",
    "lgpl-3.0-only",
    "lgpl-3.0-or-later",
    "mit",
    "mpl-2.0",
    "unlicense",
}

LICENSE_FILE_BASENAMES = {"LICENSE", "COPYING"}
LICENSE_FILE_TEXT_EXTENSIONS = {"", ".txt", ".md", ".markdown", ".rst"}


@dataclass(frozen=True)
class LicenseProvenanceArtifact:
    artifact_id: str
    uri: str
    role: str | None = None


@dataclass(frozen=True)
class PackageLicenseProvenanceRecord:
    path: str
    source: str
    package_id: str
    package_version: str
    namespace: str
    license_name: str
    license_evidence: dict[str, Any] | None
    upstream_artifacts: tuple[LicenseProvenanceArtifact, ...]


def build_license_provenance_risk_report(
    *,
    accepted_root: Path | None = None,
    candidates_root: Path | None = None,
) -> dict[str, Any]:
    if accepted_root is None and candidates_root is None:
        raise ValueError("At least one of accepted_root or candidates_root must be provided.")

    records, issues = collect_license_provenance_records(accepted_root, candidates_root)
    license_checks = evaluate_license_risks(records)
    upstream_checks = evaluate_provenance_risks(records)
    issues.extend(license_checks)
    issues.extend(upstream_checks)

    risk_counts = {
        "high": sum(1 for issue in issues if issue.get("severity") == "high"),
        "medium": sum(1 for issue in issues if issue.get("severity") == "medium"),
        "low": sum(1 for issue in issues if issue.get("severity") == "low"),
    }

    issue_codes = sorted({issue["code"] for issue in issues})
    issue_counts = {
        code: sum(1 for issue in issues if issue["code"] == code) for code in issue_codes
    }

    return {
        "schemaVersion": LICENSE_PROVENANCE_REPORT_SCHEMA_VERSION,
        "kind": LICENSE_PROVENANCE_REPORT_KIND,
        "status": "partial" if issues else "ok",
        "summary": {
            "records": len(records),
            "riskScore": min(100, max(0, 100 - len(issues) * 7)),
            "issueCount": len(issues),
            "riskCounts": risk_counts,
            "issuesByCode": issue_counts,
        },
        "records": [license_provenance_record_to_dict(record) for record in records],
        "issues": issues,
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def collect_license_provenance_records(
    accepted_root: Path | None,
    candidates_root: Path | None,
) -> tuple[list[PackageLicenseProvenanceRecord], list[dict[str, str]]]:
    records: list[PackageLicenseProvenanceRecord] = []
    issues: list[dict[str, str]] = []

    if accepted_root is not None:
        _collect_source_records(accepted_root, "accepted", records, issues)
    if candidates_root is not None:
        _collect_source_records(candidates_root, "candidate", records, issues)

    records.sort(key=lambda item: (item.source, item.path))
    return records, issues


def license_provenance_record_to_dict(record: PackageLicenseProvenanceRecord) -> dict[str, Any]:
    return {
        "path": record.path,
        "source": record.source,
        "packageId": record.package_id,
        "packageVersion": record.package_version,
        "namespace": record.namespace,
        "license": record.license_name,
        **({"licenseEvidence": record.license_evidence} if record.license_evidence else {}),
        "upstreamArtifacts": [
            {
                "id": artifact.artifact_id,
                "uri": artifact.uri,
                **({"role": artifact.role} if artifact.role is not None else {}),
            }
            for artifact in record.upstream_artifacts
        ],
    }


def evaluate_license_risks(
    records: list[PackageLicenseProvenanceRecord],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for record in records:
        license_value = record.license_name.strip()
        if not license_value:
            issues.append(
                _report_issue(
                    record,
                    "missing_license",
                    "high",
                    "metadata.license is missing in specpm.yaml.",
                )
            )
            continue

        normalized = license_value.lower().strip()
        if normalized in {"unknown", "proprietary", "not specified", "unspecified", "n/a"}:
            evidence_source = license_evidence_source(record)
            if normalized == "unknown" and evidence_source == "absent":
                issues.append(
                    _report_issue(
                        record,
                        "absent_license_evidence",
                        "medium",
                        (
                            "License is UNKNOWN because no manifest license or "
                            "license-like file evidence was found."
                        ),
                    )
                )
                continue
            if normalized == "unknown" and evidence_source == "ambiguous_license_file":
                if has_collected_license_file_evidence(record):
                    issues.append(
                        _report_issue(
                            record,
                            "collected_unknown_license_evidence",
                            "low",
                            (
                                "License is UNKNOWN but standard collected license-file "
                                "evidence is present; deterministic SPDX classification "
                                "still needs review."
                            ),
                        )
                    )
                    continue
                issues.append(
                    _report_issue(
                        record,
                        "ambiguous_unknown_license",
                        "medium",
                        (
                            "License is UNKNOWN because license-like file evidence was "
                            "present but unclassified."
                        ),
                    )
                )
                continue
            issues.append(
                _report_issue(
                    record,
                    "unknown_license",
                    "medium",
                    f"License appears unspecified or proprietary: {license_value}",
                )
            )
            continue

        if _is_non_standard_license(normalized):
            issues.append(
                _report_issue(
                    record,
                    "non_standard_license",
                    "low",
                    f"License is not recognized as a common SPDX-like identifier: {license_value}",
                )
            )

    return sorted(issues, key=lambda item: (item["path"], item["code"]))


def license_evidence_source(record: PackageLicenseProvenanceRecord) -> str | None:
    evidence = record.license_evidence
    if not isinstance(evidence, dict):
        return None
    source = evidence.get("source")
    if isinstance(source, str) and source.strip():
        return source.strip()
    return None


def has_collected_license_file_evidence(record: PackageLicenseProvenanceRecord) -> bool:
    evidence = record.license_evidence
    if not isinstance(evidence, dict):
        return False
    paths = evidence.get("paths")
    if not isinstance(paths, list):
        return False
    return any(is_standard_license_evidence_path(path) for path in paths)


def is_standard_license_evidence_path(path: object) -> bool:
    if not isinstance(path, str) or not path.strip():
        return False
    candidate = Path(path.strip())
    name = candidate.name
    suffix = candidate.suffix.lower()
    if suffix not in LICENSE_FILE_TEXT_EXTENSIONS:
        return False
    stem = candidate.stem if suffix else name
    return stem.upper() in LICENSE_FILE_BASENAMES


def evaluate_provenance_risks(
    records: list[PackageLicenseProvenanceRecord],
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
                _report_issue(
                    record,
                    "missing_upstream_repository",
                    "medium",
                    "No upstream_repository artifact found in foreignArtifacts.",
                )
            )
            continue

        if len(upstream_entries) > 1:
            issues.append(
                _report_issue(
                    record,
                    "duplicate_upstream_repository_entries",
                    "low",
                    "Multiple upstream_repository artifacts found.",
                )
            )

        for entry in upstream_entries:
            if not entry.uri:
                issues.append(
                    _report_issue(
                        record,
                        "invalid_upstream_repository_uri",
                        "medium",
                        "upstream_repository artifact missing URI.",
                    )
                )
                continue

            upstream = parse_upstream_repository_reference(entry.uri)
            if upstream is None:
                if "github.com" in entry.uri.lower():
                    issues.append(
                        _report_issue(
                            record,
                            "invalid_upstream_repository_uri",
                            "medium",
                            f"Could not parse upstream owner from URI: {entry.uri}",
                        )
                    )
                else:
                    issues.append(
                        _report_issue(
                            record,
                            "non_github_upstream_repository",
                            "low",
                            f"Upstream URI is not a GitHub source: {entry.uri}",
                        )
                    )
                continue

            if not namespace_matches_upstream(record.namespace, upstream):
                issues.append(
                    _report_issue(
                        record,
                        "upstream_namespace_mismatch",
                        "low",
                        (
                            f"Package namespace `{record.namespace}` does not match inferred "
                            f"upstream owner `{upstream.owner}` or repository "
                            f"`{upstream.name}`."
                        ),
                    )
                )

            if "github.com" not in entry.uri.lower():
                issues.append(
                    _report_issue(
                        record,
                        "non_github_upstream_repository",
                        "low",
                        f"Upstream URI is not a GitHub source: {entry.uri}",
                    )
                )

    return sorted(issues, key=lambda item: (item["path"], item["code"]))


_SPDX_OPERATOR_PATTERN = re.compile(r"\s+(?:and|or|with)\s+", re.IGNORECASE)
_SPDX_EXCEPTION_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.+_-]*-exception(?:-[a-z0-9.+_-]+)?$")


def _is_non_standard_license(license_text: str) -> bool:
    normalized_license = license_text.strip().lower()
    if normalized_license in KNOWN_LICENSE_HINTS:
        return False

    no_paren = normalized_license.replace("(", " ").replace(")", " ").strip()
    if _SPDX_OPERATOR_PATTERN.search(no_paren):
        parts = [part.strip() for part in _SPDX_OPERATOR_PATTERN.split(no_paren)]
        if not parts:
            return True

        if any(not part for part in parts):
            return True

        operators = [m.group(0).strip().lower() for m in _SPDX_OPERATOR_PATTERN.finditer(no_paren)]
        if not operators:
            return True

        if any(operator == "with" for operator in operators):
            if len(parts) < 2:
                return True
            if parts[0] not in KNOWN_LICENSE_HINTS:
                return True
            return not all(_is_spdx_exception_term(part) for part in parts[1:])

        return any(part not in KNOWN_LICENSE_HINTS for part in parts)

    if any(prefix in no_paren for prefix in ("license:", "see", "file:", "http://", "https://")):
        return True

    if any(token in f" {normalized_license} " for token in (" with ", " or ", " and ")):
        return True

    return True


def _is_spdx_exception_term(term: str) -> bool:
    if term in KNOWN_LICENSE_HINTS:
        return True
    return bool(_SPDX_EXCEPTION_PATTERN.fullmatch(term))


def _report_issue(
    record: PackageLicenseProvenanceRecord,
    code: str,
    severity: str,
    message: str,
) -> dict[str, str]:
    return {
        "path": record.path,
        "packageId": record.package_id,
        "packageVersion": record.package_version,
        "code": code,
        "severity": severity,
        "message": message,
    }


def _collect_source_records(
    source_root: Path,
    source: str,
    records: list[PackageLicenseProvenanceRecord],
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
                    "severity": "low",
                    "message": "Skip symlinked specpm.yaml in license provenance risk scan.",
                }
            )
            continue

        try:
            package = parse_specpm_license_provenance(manifest_path, source)
        except ValueError as exc:
            issues.append(
                {
                    "path": str(manifest_path),
                    "code": "invalid_specpm_manifest",
                    "severity": "low",
                    "message": str(exc),
                }
            )
            continue
        records.append(package)


def parse_specpm_license_provenance(
    manifest_path: Path,
    source: str,
) -> PackageLicenseProvenanceRecord:
    metadata: dict[str, str] = {}
    license_evidence: dict[str, Any] | None = None
    artifacts: list[LicenseProvenanceArtifact] = []

    parse_state = "root"
    current_artifact: dict[str, str] | None = None
    collecting_license_evidence_paths = False

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
                collecting_license_evidence_paths = False
                continue
            if text == "foreignArtifacts:":
                parse_state = "foreignArtifacts"
                collecting_license_evidence_paths = False
                continue
            parse_state = "root"
            collecting_license_evidence_paths = False
            continue

        if parse_state == "metadata":
            if indent != 2 or ":" not in text:
                continue
            key, raw_value = text.split(":", 1)
            if key.strip() == "licenseEvidence" and not raw_value.strip():
                license_evidence = {}
                parse_state = "metadata_license_evidence"
                collecting_license_evidence_paths = False
                continue
            metadata[key.strip()] = parse_yaml_scalar(raw_value.strip())
            continue

        if parse_state == "metadata_license_evidence":
            if indent == 2:
                collecting_license_evidence_paths = False
                if ":" not in text:
                    parse_state = "metadata"
                    continue
                key, raw_value = text.split(":", 1)
                if key.strip() == "licenseEvidence" and not raw_value.strip():
                    license_evidence = {}
                    continue
                metadata[key.strip()] = parse_yaml_scalar(raw_value.strip())
                parse_state = "metadata"
                continue

            if license_evidence is None:
                license_evidence = {}

            if indent == 4 and ":" in text:
                key, raw_value = text.split(":", 1)
                key = key.strip()
                value = raw_value.strip()
                collecting_license_evidence_paths = False
                if key == "paths":
                    if value == "[]":
                        license_evidence["paths"] = []
                    elif value:
                        license_evidence["paths"] = [parse_yaml_scalar(value)]
                    else:
                        license_evidence["paths"] = []
                        collecting_license_evidence_paths = True
                    continue
                license_evidence[key] = parse_yaml_scalar(value)
                continue

            if indent == 6 and collecting_license_evidence_paths and text.startswith("- "):
                paths = license_evidence.setdefault("paths", [])
                if isinstance(paths, list):
                    paths.append(parse_yaml_scalar(text[2:].strip()))
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

    license_name = metadata.get("license", "").strip()
    namespace = package_id.split(".")[0] if "." in package_id else package_id

    return PackageLicenseProvenanceRecord(
        path=str(manifest_path),
        source=source,
        package_id=package_id,
        package_version=package_version,
        namespace=namespace,
        license_name=license_name,
        license_evidence=normalize_license_evidence(license_evidence),
        upstream_artifacts=tuple(artifacts),
    )


def normalize_license_evidence(evidence: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(evidence, dict) or not evidence:
        return None

    normalized: dict[str, Any] = {}
    source = evidence.get("source")
    if isinstance(source, str) and source.strip():
        normalized["source"] = source.strip()

    confidence = evidence.get("confidence")
    if isinstance(confidence, str) and confidence.strip():
        normalized["confidence"] = confidence.strip()

    paths = evidence.get("paths")
    if isinstance(paths, list):
        normalized["paths"] = sorted(str(path) for path in paths if str(path).strip())

    return normalized or None


def _normalize_artifact(values: dict[str, str]) -> LicenseProvenanceArtifact:
    artifact_id = str(values.get("id", "")).strip()
    if not artifact_id:
        artifact_id = str(values.get("artifact", "")).strip()
    uri = values.get("uri")
    uri_value = str(uri).strip() if uri is not None else ""
    role = values.get("role")
    role_value = str(role).strip() if role is not None else None

    return LicenseProvenanceArtifact(
        artifact_id=artifact_id,
        uri=uri_value,
        role=role_value,
    )


def write_license_provenance_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
