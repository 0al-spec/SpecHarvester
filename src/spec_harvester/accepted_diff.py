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


@dataclass(frozen=True)
class PackageDiffSource:
    root: Path
    source: str

    def records_and_issues(self) -> tuple[list[PackageDiffInputRecord], list[dict[str, str]]]:
        root = self.root.resolve()
        if not root.exists() or not root.is_dir():
            raise ValueError(f"Source root does not exist or is not a directory: {root}")

        records: list[PackageDiffInputRecord] = []
        issues: list[dict[str, str]] = []
        for manifest_path in sorted(root.rglob("specpm.yaml"), key=lambda item: str(item)):
            if manifest_path.is_symlink():
                issues.append(self.symlink_issue(manifest_path))
                continue
            try:
                records.append(self.record(manifest_path))
            except ValueError as exc:
                issues.append(self.invalid_manifest_issue(manifest_path, exc))

        return sorted(records, key=lambda item: (item.source, item.package_id, item.path)), issues

    def record(self, manifest_path: Path) -> PackageDiffInputRecord:
        return parse_specpm_diff_record(manifest_path, self.source)

    def symlink_issue(self, manifest_path: Path) -> dict[str, str]:
        return {
            "path": str(manifest_path),
            "source": self.source,
            "code": "specpm_symlink",
            "message": "Skip symlinked specpm.yaml in accepted/candidate diff scan.",
        }

    def invalid_manifest_issue(self, manifest_path: Path, error: ValueError) -> dict[str, str]:
        return {
            "path": str(manifest_path),
            "source": self.source,
            "code": "invalid_specpm_manifest",
            "message": str(error),
        }


@dataclass(frozen=True)
class AcceptedPackageVersions:
    records: tuple[PackageDiffInputRecord, ...]

    def latest_by_package_id(self) -> dict[str, PackageDiffInputRecord]:
        latest: dict[str, PackageDiffInputRecord] = {}
        for record in self.records:
            current = latest.get(record.package_id)
            if current is None or semver_sort_key(record.package_version) > semver_sort_key(
                current.package_version
            ):
                latest[record.package_id] = record
        return latest


@dataclass(frozen=True)
class PackageRecordDiff:
    accepted: PackageDiffInputRecord
    candidate: PackageDiffInputRecord

    def changes(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata_changes(),
            "intents": self.intent_changes(),
            "capabilities": self.capability_changes(),
            "upstreamArtifacts": self.upstream_artifact_changes(),
        }

    def has_changes(self) -> bool:
        return has_changes(self.changes())

    def metadata_changes(self) -> list[dict[str, str | None]]:
        return diff_metadata(self.accepted.metadata, self.candidate.metadata)

    def intent_changes(self) -> dict[str, list[str]]:
        accepted_intents = set(self.accepted.intents)
        candidate_intents = set(self.candidate.intents)
        return {
            "added": sorted(candidate_intents - accepted_intents),
            "removed": sorted(accepted_intents - candidate_intents),
        }

    def capability_changes(self) -> dict[str, list[str]]:
        accepted_capabilities = set(self.accepted.capabilities)
        candidate_capabilities = set(self.candidate.capabilities)
        return {
            "added": sorted(candidate_capabilities - accepted_capabilities),
            "removed": sorted(accepted_capabilities - candidate_capabilities),
        }

    def upstream_artifact_changes(self) -> dict[str, Any]:
        upstream_changed = self.accepted.upstream_artifacts != self.candidate.upstream_artifacts
        return {
            "changed": upstream_changed,
            "old": list(self.accepted.upstream_artifacts) if upstream_changed else [],
            "new": list(self.candidate.upstream_artifacts) if upstream_changed else [],
        }


@dataclass(frozen=True)
class CandidateComparison:
    candidate: PackageDiffInputRecord
    accepted: PackageDiffInputRecord | None

    def as_dict(self) -> dict[str, Any]:
        if self.accepted is None:
            return self.new_package()

        delta = PackageRecordDiff(self.accepted, self.candidate)
        changes = delta.changes()
        status = "changed" if has_changes(changes) else "unchanged"
        return {
            "packageId": self.candidate.package_id,
            "oldPackageVersion": self.accepted.package_version,
            "newPackageVersion": self.candidate.package_version,
            "status": status,
            "accepted": record_reference(self.accepted),
            "candidate": record_reference(self.candidate),
            "changes": changes,
        }

    def new_package(self) -> dict[str, Any]:
        return {
            "packageId": self.candidate.package_id,
            "oldPackageVersion": None,
            "newPackageVersion": self.candidate.package_version,
            "status": "new_package",
            "accepted": None,
            "candidate": record_reference(self.candidate),
            "changes": {
                "metadata": [],
                "intents": {"added": list(self.candidate.intents), "removed": []},
                "capabilities": {"added": list(self.candidate.capabilities), "removed": []},
                "upstreamArtifacts": {
                    "changed": bool(self.candidate.upstream_artifacts),
                    "old": [],
                    "new": list(self.candidate.upstream_artifacts),
                },
            },
        }


@dataclass(frozen=True)
class AcceptedCandidateDiffReport:
    accepted_root: Path
    candidates_root: Path

    def report(self) -> dict[str, Any]:
        accepted_records, accepted_issues = PackageDiffSource(
            self.accepted_root, "accepted"
        ).records_and_issues()
        candidate_records, candidate_issues = PackageDiffSource(
            self.candidates_root, "candidate"
        ).records_and_issues()
        issues = accepted_issues + candidate_issues
        comparisons = self.comparisons(accepted_records, candidate_records)

        return {
            "schemaVersion": ACCEPTED_CANDIDATE_DIFF_REPORT_SCHEMA_VERSION,
            "kind": ACCEPTED_CANDIDATE_DIFF_REPORT_KIND,
            "status": "partial" if issues else "ok",
            "summary": self.summary(accepted_records, candidate_records, comparisons, issues),
            "comparisons": comparisons,
            "issues": self.sorted_issues(issues),
            "trustBoundary": TRUST_BOUNDARY_NOTES,
        }

    def comparisons(
        self,
        accepted_records: list[PackageDiffInputRecord],
        candidate_records: list[PackageDiffInputRecord],
    ) -> list[dict[str, Any]]:
        accepted_by_id = AcceptedPackageVersions(tuple(accepted_records)).latest_by_package_id()
        return [
            CandidateComparison(candidate, accepted_by_id.get(candidate.package_id)).as_dict()
            for candidate in sorted(
                candidate_records,
                key=lambda item: (
                    item.package_id,
                    semver_sort_key(item.package_version),
                    item.path,
                ),
            )
        ]

    def summary(
        self,
        accepted_records: list[PackageDiffInputRecord],
        candidate_records: list[PackageDiffInputRecord],
        comparisons: list[dict[str, Any]],
        issues: list[dict[str, str]],
    ) -> dict[str, int]:
        return {
            "acceptedRecords": len(accepted_records),
            "candidateRecords": len(candidate_records),
            "comparedCount": sum(1 for item in comparisons if item["status"] != "new_package"),
            "newPackageCount": sum(1 for item in comparisons if item["status"] == "new_package"),
            "changedCount": sum(1 for item in comparisons if item["status"] == "changed"),
            "unchangedCount": sum(1 for item in comparisons if item["status"] == "unchanged"),
            "issueCount": len(issues),
        }

    def sorted_issues(self, issues: list[dict[str, str]]) -> list[dict[str, str]]:
        return sorted(issues, key=lambda item: (item["path"], item["code"]))


@dataclass(frozen=True)
class AcceptedCandidateDiffReportWriter:
    path: Path
    report: dict[str, Any]

    def write(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


def build_accepted_candidate_diff_report(
    *,
    accepted_root: Path,
    candidates_root: Path,
) -> dict[str, Any]:
    return AcceptedCandidateDiffReport(accepted_root, candidates_root).report()


def collect_package_diff_records(
    source_root: Path,
    source: str,
) -> tuple[list[PackageDiffInputRecord], list[dict[str, str]]]:
    return PackageDiffSource(source_root, source).records_and_issues()


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
    return AcceptedPackageVersions(tuple(records)).latest_by_package_id()


def build_candidate_comparison(
    candidate: PackageDiffInputRecord,
    accepted: PackageDiffInputRecord | None,
) -> dict[str, Any]:
    return CandidateComparison(candidate, accepted).as_dict()


def diff_records(
    accepted: PackageDiffInputRecord,
    candidate: PackageDiffInputRecord,
) -> dict[str, Any]:
    return PackageRecordDiff(accepted, candidate).changes()


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
    AcceptedCandidateDiffReportWriter(path, report).write()
