from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Generic, TypeVar

RecordT = TypeVar("RecordT")


@dataclass(frozen=True)
class ReportSourceIssuePolicy:
    symlink_message: str
    symlink_severity: str | None = None
    invalid_manifest_severity: str | None = None

    def symlink_issue(self, path: Path) -> dict[str, str]:
        return self._issue(
            path=path,
            code="specpm_symlink",
            message=self.symlink_message,
            severity=self.symlink_severity,
        )

    def invalid_manifest_issue(self, path: Path, exc: ValueError) -> dict[str, str]:
        return self._issue(
            path=path,
            code="invalid_specpm_manifest",
            message=str(exc),
            severity=self.invalid_manifest_severity,
        )

    def _issue(
        self,
        *,
        path: Path,
        code: str,
        message: str,
        severity: str | None,
    ) -> dict[str, str]:
        issue = {
            "path": str(path),
            "code": code,
            "message": message,
        }
        if severity is not None:
            issue["severity"] = severity
        return issue


@dataclass(frozen=True)
class SpecpmReportSourceRecords(Generic[RecordT]):
    accepted_root: Path | None
    candidates_root: Path | None
    parse_manifest: Callable[[Path, str], RecordT]
    issue_policy: ReportSourceIssuePolicy
    sort_key: Callable[[RecordT], tuple[str, str]]

    def collect(self) -> tuple[list[RecordT], list[dict[str, str]]]:
        records: list[RecordT] = []
        issues: list[dict[str, str]] = []

        if self.accepted_root is not None:
            self._collect_root(self.accepted_root, "accepted", records, issues)
        if self.candidates_root is not None:
            self._collect_root(self.candidates_root, "candidate", records, issues)

        records.sort(key=self.sort_key)
        return records, issues

    def _collect_root(
        self,
        source_root: Path,
        source: str,
        records: list[RecordT],
        issues: list[dict[str, str]],
    ) -> None:
        root = source_root.resolve()
        if not root.exists() or not root.is_dir():
            raise ValueError(f"Source root does not exist or is not a directory: {root}")

        for manifest_path in sorted(root.rglob("specpm.yaml"), key=lambda item: str(item)):
            if manifest_path.is_symlink():
                issues.append(self.issue_policy.symlink_issue(manifest_path))
                continue
            try:
                records.append(self.parse_manifest(manifest_path, source))
            except ValueError as exc:
                issues.append(self.issue_policy.invalid_manifest_issue(manifest_path, exc))
