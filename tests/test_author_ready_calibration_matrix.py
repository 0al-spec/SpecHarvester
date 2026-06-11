from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.author_ready_calibration_matrix import (
    AUTHOR_READY_CALIBRATION_KIND,
    STATUS_AUTHOR_READY,
    STATUS_BLOCKED,
    STATUS_NEEDS_REGENERATION,
    build_author_ready_calibration_matrix,
    write_author_ready_calibration_matrix,
)
from spec_harvester.cli import main


def test_author_ready_calibration_matrix_builds_summary() -> None:
    matrix = build_author_ready_calibration_matrix(quality_report_fixture())

    assert matrix["kind"] == AUTHOR_READY_CALIBRATION_KIND
    assert matrix["summary"]["packageCount"] == 3
    assert matrix["summary"]["authorReadyDraftCount"] == 1
    assert matrix["summary"]["needsRegenerationCount"] == 1
    assert matrix["summary"]["blockedCount"] == 1
    assert matrix["summary"]["totalEstimatedAuthorEdits"] == 13
    assert matrix["summary"]["editCategoryCounts"]["intent_summary"] == 2
    assert matrix["summary"]["editCategoryCounts"]["validation"] == 2
    assert matrix["summary"]["calibrationVerdict"] == "blocked_inputs_present"
    analyzer_follow_up = next(
        item
        for item in matrix["repeatedGeneratorFollowUps"]
        if item["reason"] == "missing_analyzer_coverage"
    )
    assert analyzer_follow_up["followUpRecommended"] is True


def test_author_ready_calibration_matrix_honors_author_notes() -> None:
    matrix = build_author_ready_calibration_matrix(
        quality_report_fixture(),
        author_notes={
            "packages": {
                "pkg-review": {
                    "estimatedAuthorEdits": 1,
                    "editCategories": ["summary_wording"],
                    "authorReadyStatus": STATUS_AUTHOR_READY,
                    "notes": "Author only needs wording cleanup.",
                }
            }
        },
    )

    row = next(package for package in matrix["packages"] if package["id"] == "pkg-review")
    assert row["authorReadyStatus"] == STATUS_AUTHOR_READY
    assert row["estimatedAuthorEdits"] == 1
    assert row["editCategories"] == ["summary_wording"]
    assert row["humanReviewNotes"] == "Author only needs wording cleanup."


def test_author_ready_calibration_matrix_status_derivation() -> None:
    rows = build_author_ready_calibration_matrix(quality_report_fixture())["packages"]
    by_id = {row["id"]: row for row in rows}

    assert by_id["pkg-pass"]["authorReadyStatus"] == STATUS_AUTHOR_READY
    assert by_id["pkg-review"]["authorReadyStatus"] == STATUS_NEEDS_REGENERATION
    assert by_id["pkg-fail"]["authorReadyStatus"] == STATUS_BLOCKED
    assert by_id["pkg-fail"]["reviewPriority"] == "blocking"


def test_write_author_ready_calibration_matrix_roundtrip(tmp_path: Path) -> None:
    matrix = build_author_ready_calibration_matrix(quality_report_fixture())
    out = tmp_path / "nested" / "author-ready-calibration-matrix.json"

    write_author_ready_calibration_matrix(out, matrix)

    assert json.loads(out.read_text(encoding="utf-8"))["kind"] == AUTHOR_READY_CALIBRATION_KIND


def test_cli_author_ready_calibration_matrix_writes_output(tmp_path: Path, capsys) -> None:
    quality_report = tmp_path / "quality-report.json"
    output = tmp_path / "author-ready-calibration-matrix.json"
    write_json(quality_report, quality_report_fixture())

    result = main(
        [
            "author-ready-calibration-matrix",
            "--quality-report",
            str(quality_report),
            "--output",
            str(output),
        ]
    )

    assert result == 0
    assert output.exists()
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["kind"] == AUTHOR_READY_CALIBRATION_KIND


def test_cli_author_ready_calibration_matrix_reads_author_notes(
    tmp_path: Path,
    capsys,
) -> None:
    quality_report = tmp_path / "quality-report.json"
    author_notes = tmp_path / "author-notes.json"
    write_json(quality_report, quality_report_fixture())
    write_json(author_notes, {"pkg-pass": {"estimatedAuthorEdits": 2}})

    result = main(
        [
            "author-ready-calibration-matrix",
            "--quality-report",
            str(quality_report),
            "--author-notes",
            str(author_notes),
        ]
    )

    assert result == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    row = next(package for package in data["packages"] if package["id"] == "pkg-pass")
    assert row["estimatedAuthorEdits"] == 2


def test_cli_author_ready_calibration_matrix_missing_quality_report_errors(
    tmp_path: Path,
    capsys,
) -> None:
    result = main(
        [
            "author-ready-calibration-matrix",
            "--quality-report",
            str(tmp_path / "missing.json"),
        ]
    )

    assert result == 2
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["status"] == "error"
    assert "Cannot read quality report" in data["message"]


def quality_report_fixture() -> dict:
    return {
        "kind": "SpecHarvesterRealRepositoryQualityReport",
        "runReport": "/tmp/run-report.json",
        "packages": [
            {
                "id": "pkg-pass",
                "packageId": "pkg.pass",
                "intentAccuracy": "strong",
                "capabilityEvidenceQuality": "strong",
                "analyzerCoverage": "strong",
                "specpmStatus": "passed",
                "retryOutcome": "not_attempted",
                "overallVerdict": "pass",
                "humanReviewNotes": "",
            },
            {
                "id": "pkg-review",
                "packageId": "pkg.review",
                "intentAccuracy": "partial",
                "capabilityEvidenceQuality": "partial",
                "analyzerCoverage": "weak",
                "specpmStatus": "skipped",
                "retryOutcome": "not_attempted",
                "overallVerdict": "review",
                "humanReviewNotes": "Needs author review.",
            },
            {
                "id": "pkg-fail",
                "packageId": "pkg.fail",
                "intentAccuracy": "weak",
                "capabilityEvidenceQuality": "weak",
                "analyzerCoverage": "weak",
                "specpmStatus": "failed",
                "retryOutcome": "degraded",
                "overallVerdict": "fail",
                "humanReviewNotes": "",
            },
        ],
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
