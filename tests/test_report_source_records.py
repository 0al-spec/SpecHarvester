from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from spec_harvester.report_source_records import (
    ReportSourceIssuePolicy,
    SpecpmReportSourceRecords,
)


@dataclass(frozen=True)
class SourceRecord:
    path: str
    source: str


def test_specpm_report_source_records_collects_and_reports_issues(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    valid = accepted_root / "valid" / "specpm.yaml"
    invalid = accepted_root / "invalid" / "specpm.yaml"
    candidate = candidates_root / "valid" / "specpm.yaml"
    target = tmp_path / "target-specpm.yaml"
    symlink = accepted_root / "linked" / "specpm.yaml"
    for path in (valid, invalid, candidate, symlink):
        path.parent.mkdir(parents=True, exist_ok=True)
    valid.write_text("metadata:\n  id: valid.core\n", encoding="utf-8")
    invalid.write_text("invalid", encoding="utf-8")
    candidate.write_text("metadata:\n  id: candidate.core\n", encoding="utf-8")
    target.write_text("metadata:\n  id: linked.core\n", encoding="utf-8")
    symlink.symlink_to(target)

    records, issues = SpecpmReportSourceRecords(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
        parse_manifest=parse_test_manifest,
        issue_policy=ReportSourceIssuePolicy(
            symlink_message="Skip linked manifest.",
            symlink_severity="low",
            invalid_manifest_severity="low",
        ),
        sort_key=lambda item: (item.source, item.path),
    ).collect()

    assert [record.source for record in records] == ["accepted", "candidate"]
    assert [Path(record.path).name for record in records] == ["specpm.yaml", "specpm.yaml"]
    assert {issue["code"] for issue in issues} == {
        "invalid_specpm_manifest",
        "specpm_symlink",
    }
    assert {issue["severity"] for issue in issues} == {"low"}
    assert any(issue["message"] == "Skip linked manifest." for issue in issues)
    assert any(issue["message"] == "broken manifest" for issue in issues)


def test_specpm_report_source_records_rejects_missing_root(tmp_path: Path) -> None:
    collector = SpecpmReportSourceRecords(
        accepted_root=tmp_path / "missing",
        candidates_root=None,
        parse_manifest=parse_test_manifest,
        issue_policy=ReportSourceIssuePolicy(symlink_message="Skip linked manifest."),
        sort_key=lambda item: (item.source, item.path),
    )

    with pytest.raises(ValueError, match="Source root does not exist or is not a directory"):
        collector.collect()


def parse_test_manifest(path: Path, source: str) -> SourceRecord:
    if path.parent.name == "invalid":
        raise ValueError("broken manifest")
    return SourceRecord(path=str(path), source=source)
