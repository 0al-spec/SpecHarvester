"""Tests for real_repo_quality_report module."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.real_repo_quality_report import (
    QUALITY_REPORT_KIND,
    QUALITY_REPORT_SCHEMA_VERSION,
    RATING_PARTIAL,
    RATING_STRONG,
    RATING_UNSCORED,
    RATING_WEAK,
    RETRY_DEGRADED,
    RETRY_IMPROVED,
    RETRY_NOT_ATTEMPTED,
    RETRY_UNCHANGED,
    SPECPM_FAILED,
    SPECPM_NOT_RUN,
    SPECPM_PASSED,
    SPECPM_SKIPPED,
    VERDICT_FAIL,
    VERDICT_PASS,
    VERDICT_REVIEW,
    VERDICT_UNSCORED,
    _derive_analyzer_coverage,
    _derive_capability_rating,
    _derive_intent_rating,
    _derive_overall_verdict,
    _derive_retry_outcome,
    _derive_specpm_status,
    _extract_token_usage,
    build_package_quality_record,
    build_quality_report,
    write_quality_report,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_json(path: Path, data: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def _ok_step(name: str) -> dict:
    return {"step": name, "status": "ok"}


def _fail_step(name: str) -> dict:
    return {"step": name, "status": "failed"}


def _skipped_step(name: str) -> dict:
    return {"step": name, "status": "skipped"}


# ---------------------------------------------------------------------------
# Schema constants
# ---------------------------------------------------------------------------


def test_schema_version_and_kind() -> None:
    assert QUALITY_REPORT_SCHEMA_VERSION == 1
    assert QUALITY_REPORT_KIND == "SpecHarvesterRealRepositoryQualityReport"


# ---------------------------------------------------------------------------
# _derive_intent_rating
# ---------------------------------------------------------------------------


def test_intent_rating_dry_run() -> None:
    rating, notes = _derive_intent_rating([], None, dry_run=True)
    assert rating == RATING_UNSCORED
    assert "dry_run" in notes


def test_intent_rating_draft_step_missing() -> None:
    rating, _ = _derive_intent_rating([], None, dry_run=False)
    assert rating == RATING_WEAK


def test_intent_rating_draft_step_failed() -> None:
    rating, _ = _derive_intent_rating([_fail_step("draft")], None, dry_run=False)
    assert rating == RATING_WEAK


def test_intent_rating_draft_json_missing() -> None:
    rating, _ = _derive_intent_rating([_ok_step("draft")], None, dry_run=False)
    assert rating == RATING_WEAK


def test_intent_rating_no_intent_field() -> None:
    rating, _ = _derive_intent_rating([_ok_step("draft")], {"candidate": {}}, dry_run=False)
    assert rating == RATING_WEAK


def test_intent_rating_partial_no_evidence() -> None:
    draft = {"candidate": {"intent": "Process HTTP requests"}}
    rating, notes = _derive_intent_rating([_ok_step("draft")], draft, dry_run=False)
    assert rating == RATING_PARTIAL
    assert "evidenceSources" in notes


def test_intent_rating_strong_with_evidence() -> None:
    draft = {
        "candidate": {
            "intent": "Process HTTP requests",
            "evidenceSources": ["README.md"],
        }
    }
    rating, notes = _derive_intent_rating([_ok_step("draft")], draft, dry_run=False)
    assert rating == RATING_STRONG
    assert "1 evidence" in notes


def test_intent_rating_top_level_intent() -> None:
    """Draft JSON may have intent at the top level (not nested under 'candidate')."""
    draft = {"intent": "Do something", "evidenceSources": ["a.md", "b.md"]}
    rating, _ = _derive_intent_rating([_ok_step("draft")], draft, dry_run=False)
    assert rating == RATING_STRONG


# ---------------------------------------------------------------------------
# _derive_capability_rating
# ---------------------------------------------------------------------------


def test_capability_rating_dry_run() -> None:
    rating, _ = _derive_capability_rating([], None, dry_run=True)
    assert rating == RATING_UNSCORED


def test_capability_rating_no_draft_step() -> None:
    rating, _ = _derive_capability_rating([], None, dry_run=False)
    assert rating == RATING_WEAK


def test_capability_rating_empty_capabilities() -> None:
    draft = {"candidate": {"capabilities": []}}
    rating, _ = _derive_capability_rating([_ok_step("draft")], draft, dry_run=False)
    assert rating == RATING_WEAK


def test_capability_rating_all_with_evidence() -> None:
    draft = {
        "candidate": {
            "capabilities": [
                {"name": "fetch", "evidenceSources": ["README.md"]},
                {"name": "parse", "evidenceSources": ["docs/api.md"]},
            ]
        }
    }
    rating, notes = _derive_capability_rating([_ok_step("draft")], draft, dry_run=False)
    assert rating == RATING_STRONG
    assert "all 2" in notes


def test_capability_rating_partial_evidence() -> None:
    draft = {
        "candidate": {
            "capabilities": [
                {"name": "fetch", "evidenceSources": ["README.md"]},
                {"name": "parse"},
            ]
        }
    }
    rating, notes = _derive_capability_rating([_ok_step("draft")], draft, dry_run=False)
    assert rating == RATING_PARTIAL
    assert "1/2" in notes


def test_capability_rating_no_evidence() -> None:
    draft = {
        "candidate": {
            "capabilities": [{"name": "fetch"}, {"name": "parse"}],
        }
    }
    rating, _ = _derive_capability_rating([_ok_step("draft")], draft, dry_run=False)
    assert rating == RATING_WEAK


# ---------------------------------------------------------------------------
# _derive_specpm_status
# ---------------------------------------------------------------------------


def test_specpm_not_run() -> None:
    status, _ = _derive_specpm_status([])
    assert status == SPECPM_NOT_RUN


def test_specpm_passed() -> None:
    status, _ = _derive_specpm_status([_ok_step("specpm")])
    assert status == SPECPM_PASSED


def test_specpm_failed() -> None:
    status, notes = _derive_specpm_status([_fail_step("specpm")])
    assert status == SPECPM_FAILED
    assert "failed" in notes


def test_specpm_skipped() -> None:
    status, _ = _derive_specpm_status([_skipped_step("specpm")])
    assert status == SPECPM_SKIPPED


# ---------------------------------------------------------------------------
# _derive_retry_outcome
# ---------------------------------------------------------------------------


def test_retry_not_attempted_no_specnode_step() -> None:
    outcome, _ = _derive_retry_outcome([], None)
    assert outcome == RETRY_NOT_ATTEMPTED


def test_retry_degraded_specnode_failed() -> None:
    outcome, _ = _derive_retry_outcome([_fail_step("specnode")], None)
    assert outcome == RETRY_DEGRADED


def test_retry_unchanged_no_result_file() -> None:
    outcome, _ = _derive_retry_outcome([_ok_step("specnode")], None)
    assert outcome == RETRY_UNCHANGED


def test_retry_unchanged_zero_retries() -> None:
    outcome, _ = _derive_retry_outcome([_ok_step("specnode")], {"retryCount": 0})
    assert outcome == RETRY_UNCHANGED


def test_retry_improved() -> None:
    outcome, notes = _derive_retry_outcome(
        [_ok_step("specnode")], {"retryCount": 2, "improved": True}
    )
    assert outcome == RETRY_IMPROVED
    assert "2 retry" in notes


def test_retry_unchanged_with_retries_no_improvement() -> None:
    outcome, _ = _derive_retry_outcome([_ok_step("specnode")], {"retryCount": 1, "improved": False})
    assert outcome == RETRY_UNCHANGED


# ---------------------------------------------------------------------------
# _extract_token_usage
# ---------------------------------------------------------------------------


def test_token_usage_none_when_no_result() -> None:
    usage = _extract_token_usage(None)
    assert usage == {"prompt": None, "completion": None}


def test_token_usage_from_standard_keys() -> None:
    result = {"tokenUsage": {"prompt": 512, "completion": 256}}
    usage = _extract_token_usage(result)
    assert usage == {"prompt": 512, "completion": 256}


def test_token_usage_from_alternate_keys() -> None:
    result = {"usage": {"input_tokens": 100, "output_tokens": 50}}
    usage = _extract_token_usage(result)
    assert usage == {"prompt": 100, "completion": 50}


def test_token_usage_missing_fields() -> None:
    usage = _extract_token_usage({"tokenUsage": {}})
    assert usage == {"prompt": None, "completion": None}


# ---------------------------------------------------------------------------
# _derive_analyzer_coverage
# ---------------------------------------------------------------------------


def test_analyzer_coverage_dry_run() -> None:
    rating, _, used = _derive_analyzer_coverage(None, dry_run=True)
    assert rating == RATING_UNSCORED
    assert used == []


def test_analyzer_coverage_no_harvest() -> None:
    rating, _, used = _derive_analyzer_coverage(None, dry_run=False)
    assert rating == RATING_UNSCORED
    assert used == []


def test_analyzer_coverage_no_analyzers() -> None:
    rating, _, used = _derive_analyzer_coverage({"files": []}, dry_run=False)
    assert rating == RATING_WEAK
    assert used == []


def test_analyzer_coverage_one_type() -> None:
    harvest = {"files": [{"pythonPublicApi": {"symbols": []}}]}
    rating, notes, used = _derive_analyzer_coverage(harvest, dry_run=False)
    assert rating == RATING_PARTIAL
    assert "pythonPublicApi" in used


def test_analyzer_coverage_two_types() -> None:
    harvest = {
        "files": [
            {"pythonPublicApi": {"symbols": []}},
            {"semanticEvidence": {"clusters": []}},
        ]
    }
    rating, _, used = _derive_analyzer_coverage(harvest, dry_run=False)
    assert rating == RATING_STRONG
    assert len(used) == 2


def test_analyzer_coverage_unknown_analyzer_type_detected() -> None:
    """An unknown/new analyzer output field (dict-valued) is detected generically."""
    harvest = {
        "files": [
            {"rustPublicApi": {"functions": ["foo", "bar"]}},
            {"semanticEvidence": {"clusters": []}},
        ]
    }
    rating, notes, used = _derive_analyzer_coverage(harvest, dry_run=False)
    assert rating == RATING_STRONG
    assert "rustPublicApi" in used
    assert "semanticEvidence" in used


def test_analyzer_coverage_non_analyzer_dict_fields_ignored() -> None:
    """Standard file metadata keys (path, digest, etc.) are not counted as analyzers."""
    harvest = {
        "files": [
            {
                "path": "src/main.rs",
                "digest": "abc123",
                "size": 1024,
                "language": "Rust",
                "encoding": "utf-8",
                "skipped": False,
            }
        ]
    }
    rating, _, used = _derive_analyzer_coverage(harvest, dry_run=False)
    assert rating == RATING_WEAK
    assert used == []


def test_analyzer_coverage_empty_dict_field_not_counted() -> None:
    """Empty dict-valued fields are not counted as analyzer output."""
    harvest = {"files": [{"pythonPublicApi": {}}]}
    rating, _, used = _derive_analyzer_coverage(harvest, dry_run=False)
    assert rating == RATING_WEAK
    assert used == []


# ---------------------------------------------------------------------------
# _derive_overall_verdict
# ---------------------------------------------------------------------------


def test_overall_verdict_dry_run() -> None:
    verdict = _derive_overall_verdict(
        intent_rating=RATING_STRONG,
        cap_rating=RATING_STRONG,
        specpm_status=SPECPM_PASSED,
        dry_run=True,
    )
    assert verdict == VERDICT_UNSCORED


def test_overall_verdict_all_unscored() -> None:
    verdict = _derive_overall_verdict(
        intent_rating=RATING_UNSCORED,
        cap_rating=RATING_UNSCORED,
        specpm_status=SPECPM_NOT_RUN,
        dry_run=False,
    )
    assert verdict == VERDICT_UNSCORED


def test_overall_verdict_pass() -> None:
    verdict = _derive_overall_verdict(
        intent_rating=RATING_STRONG,
        cap_rating=RATING_PARTIAL,
        specpm_status=SPECPM_PASSED,
        dry_run=False,
    )
    assert verdict == VERDICT_PASS


def test_overall_verdict_fail_specpm_failed() -> None:
    verdict = _derive_overall_verdict(
        intent_rating=RATING_STRONG,
        cap_rating=RATING_STRONG,
        specpm_status=SPECPM_FAILED,
        dry_run=False,
    )
    assert verdict == VERDICT_FAIL


def test_overall_verdict_fail_weak_intent() -> None:
    verdict = _derive_overall_verdict(
        intent_rating=RATING_WEAK,
        cap_rating=RATING_STRONG,
        specpm_status=SPECPM_PASSED,
        dry_run=False,
    )
    assert verdict == VERDICT_FAIL


def test_overall_verdict_review_weak_caps() -> None:
    verdict = _derive_overall_verdict(
        intent_rating=RATING_PARTIAL,
        cap_rating=RATING_WEAK,
        specpm_status=SPECPM_PASSED,
        dry_run=False,
    )
    assert verdict == VERDICT_REVIEW


def test_overall_verdict_pass_specpm_not_run() -> None:
    verdict = _derive_overall_verdict(
        intent_rating=RATING_STRONG,
        cap_rating=RATING_STRONG,
        specpm_status=SPECPM_NOT_RUN,
        dry_run=False,
    )
    assert verdict == VERDICT_PASS


# ---------------------------------------------------------------------------
# build_package_quality_record
# ---------------------------------------------------------------------------


def test_build_package_quality_record_dry_run() -> None:
    pkg_record: dict = {
        "id": "my-pkg",
        "packageId": "com.example.my-pkg",
        "steps": [],
    }
    record = build_package_quality_record(
        pkg_record, candidate_dir=None, dry_run=True, human_review_notes="manual note"
    )
    assert record["id"] == "my-pkg"
    assert record["overallVerdict"] == VERDICT_UNSCORED
    assert record["humanReviewNotes"] == "manual note"
    assert record["tokenUsage"] == {"prompt": None, "completion": None}


def test_build_package_quality_record_with_candidate_files(tmp_path: Path) -> None:
    candidate_dir = tmp_path / "my-pkg"
    candidate_dir.mkdir()
    _write_json(
        candidate_dir / "draft.json",
        {
            "candidate": {
                "intent": "A great package",
                "evidenceSources": ["README.md"],
                "capabilities": [
                    {"name": "parse", "evidenceSources": ["api.md"]},
                ],
            }
        },
    )
    _write_json(
        candidate_dir / "harvest.json",
        {
            "files": [
                {"pythonPublicApi": {"symbols": []}},
                {"semanticEvidence": {"clusters": []}},
            ]
        },
    )

    pkg_record: dict = {
        "id": "my-pkg",
        "packageId": "com.example.my-pkg",
        "steps": [_ok_step("draft"), _ok_step("specpm")],
    }
    record = build_package_quality_record(
        pkg_record,
        candidate_dir=candidate_dir,
        dry_run=False,
    )
    assert record["intentAccuracy"] == RATING_STRONG
    assert record["capabilityEvidenceQuality"] == RATING_STRONG
    assert record["specpmStatus"] == SPECPM_PASSED
    assert record["retryOutcome"] == RETRY_NOT_ATTEMPTED
    assert record["analyzerCoverage"] == RATING_STRONG
    assert record["overallVerdict"] == VERDICT_PASS


# ---------------------------------------------------------------------------
# build_quality_report
# ---------------------------------------------------------------------------


def _minimal_run_report(tmp_path: Path, *, dry_run: bool = False) -> dict:
    return {
        "status": "ok",
        "out": str(tmp_path / "output"),
        "inputs": str(tmp_path / "inputs"),
        "dryRun": dry_run,
        "packages": [
            {
                "id": "pkg-a",
                "packageId": None,
                "steps": [],
            }
        ],
    }


def test_build_quality_report_schema_fields(tmp_path: Path) -> None:
    report = build_quality_report(_minimal_run_report(tmp_path))
    assert report["schemaVersion"] == QUALITY_REPORT_SCHEMA_VERSION
    assert report["kind"] == QUALITY_REPORT_KIND
    assert report["packageCount"] == 1
    assert "summary" in report
    assert "packages" in report
    assert "trustBoundary" in report


def test_build_quality_report_summary_counts(tmp_path: Path) -> None:
    report = build_quality_report(_minimal_run_report(tmp_path, dry_run=True))
    assert report["summary"]["unscoredCount"] == 1
    assert report["summary"]["passCount"] == 0


def test_build_quality_report_human_notes_injected(tmp_path: Path) -> None:
    run_report = _minimal_run_report(tmp_path)
    report = build_quality_report(run_report, human_notes={"pkg-a": "looks good"})
    assert report["packages"][0]["humanReviewNotes"] == "looks good"


def test_build_quality_report_candidates_root_override(tmp_path: Path) -> None:
    run_report = _minimal_run_report(tmp_path)
    override = tmp_path / "override"
    report = build_quality_report(run_report, candidates_root=override)
    assert report["candidatesRoot"] == str(override)


# ---------------------------------------------------------------------------
# write_quality_report
# ---------------------------------------------------------------------------


def test_write_quality_report_roundtrip(tmp_path: Path) -> None:
    report = build_quality_report(_minimal_run_report(tmp_path, dry_run=True))
    out_path = tmp_path / "quality-report.json"
    write_quality_report(out_path, report)
    loaded = json.loads(out_path.read_text(encoding="utf-8"))
    assert loaded["kind"] == QUALITY_REPORT_KIND


def test_write_quality_report_creates_parent_dirs(tmp_path: Path) -> None:
    report = {"kind": QUALITY_REPORT_KIND, "schemaVersion": 1}
    out_path = tmp_path / "nested" / "dir" / "report.json"
    write_quality_report(out_path, report)
    assert out_path.exists()


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------


def test_cli_quality_report_help(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["quality-report", "--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "quality-report" in captured.out or "run-report" in captured.out


def test_cli_quality_report_dry_run(tmp_path: Path, capsys) -> None:
    run_report = _minimal_run_report(tmp_path, dry_run=True)
    run_report_path = tmp_path / "run-report.json"
    _write_json(run_report_path, run_report)

    result = main(["quality-report", "--run-report", str(run_report_path)])
    assert result == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["kind"] == QUALITY_REPORT_KIND
    assert data["dryRun"] is True


def test_cli_quality_report_output_written(tmp_path: Path, capsys) -> None:
    run_report = _minimal_run_report(tmp_path, dry_run=True)
    run_report_path = tmp_path / "run-report.json"
    out_path = tmp_path / "quality-report.json"
    _write_json(run_report_path, run_report)

    main(
        [
            "quality-report",
            "--run-report",
            str(run_report_path),
            "--output",
            str(out_path),
        ]
    )
    assert out_path.exists()
    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert data["schemaVersion"] == QUALITY_REPORT_SCHEMA_VERSION


def test_cli_quality_report_notes_parsed(tmp_path: Path, capsys) -> None:
    run_report = _minimal_run_report(tmp_path, dry_run=True)
    run_report_path = tmp_path / "run-report.json"
    _write_json(run_report_path, run_report)

    main(
        [
            "quality-report",
            "--run-report",
            str(run_report_path),
            "--notes",
            "id=pkg-a,notes=needs review",
        ]
    )
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["packages"][0]["humanReviewNotes"] == "needs review"


def test_cli_quality_report_notes_with_comma_in_text(tmp_path: Path, capsys) -> None:
    """Commas inside the notes text must not truncate the value."""
    run_report = _minimal_run_report(tmp_path, dry_run=True)
    run_report_path = tmp_path / "run-report.json"
    _write_json(run_report_path, run_report)

    main(
        [
            "quality-report",
            "--run-report",
            str(run_report_path),
            "--notes",
            "id=pkg-a,notes=good intent, but thin evidence",
        ]
    )
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["packages"][0]["humanReviewNotes"] == "good intent, but thin evidence"


def test_cli_quality_report_notes_from_file(tmp_path: Path, capsys) -> None:
    run_report = _minimal_run_report(tmp_path, dry_run=True)
    run_report_path = tmp_path / "run-report.json"
    _write_json(run_report_path, run_report)

    notes_file = tmp_path / "notes.json"
    _write_json(notes_file, {"pkg-a": "file note"})

    main(
        [
            "quality-report",
            "--run-report",
            str(run_report_path),
            "--notes",
            f"@{notes_file}",
        ]
    )
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["packages"][0]["humanReviewNotes"] == "file note"


def test_cli_quality_report_invalid_json(tmp_path: Path, capsys) -> None:
    bad_path = tmp_path / "bad.json"
    bad_path.write_text("not json", encoding="utf-8")

    result = main(["quality-report", "--run-report", str(bad_path)])
    assert result == 2
