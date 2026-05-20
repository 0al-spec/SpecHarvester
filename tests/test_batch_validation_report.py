from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.batch_validation import (
    BATCH_VALIDATION_REPORT_KIND,
    build_batch_validation_report,
    write_batch_validation_report,
)


def test_build_batch_validation_report_marks_complete_pinned_snapshot_high_confidence() -> None:
    report = build_batch_validation_report(
        batch_result=batch_result_fixture(),
        snapshots_by_id={
            "alpha": snapshot_fixture(
                file_count=2,
                skipped_file_count=0,
                package_manifest_count=1,
            )
        },
    )

    assert report["kind"] == BATCH_VALIDATION_REPORT_KIND
    assert report["summary"] == {
        "collectedCount": 1,
        "skippedCount": 1,
        "highConfidenceCount": 1,
        "mediumConfidenceCount": 0,
        "lowConfidenceCount": 0,
        "warningCount": 0,
        "errorCount": 0,
    }
    assert report["mode"] == "strict_public"
    assert report["skippedRecords"] == [{"id": "beta", "reason": "not_selected"}]
    record = report["records"][0]
    assert record["id"] == "alpha"
    assert record["confidence"] == "high"
    assert record["errors"] == []
    assert record["warnings"] == []
    assert record["evidence"]["licenseFileCount"] == 1
    assert "execution=none" in record["policyNotes"]
    assert "networkAccess=none" in record["policyNotes"]
    assert "packageScripts=not_run" in record["policyNotes"]


def test_build_batch_validation_report_records_medium_confidence_warnings() -> None:
    batch_result = batch_result_fixture()
    batch_result["collected"][0]["revision"] = None
    batch_result["collected"][0]["ref"] = "main"

    report = build_batch_validation_report(
        batch_result=batch_result,
        snapshots_by_id={
            "alpha": snapshot_fixture(
                file_count=1,
                skipped_file_count=2,
                package_manifest_count=0,
            )
        },
    )

    assert report["summary"]["mediumConfidenceCount"] == 1
    record = report["records"][0]
    assert record["confidence"] == "medium"
    assert [warning["code"] for warning in record["warnings"]] == [
        "source_ref_not_pinned_revision",
        "files_skipped",
        "no_package_manifests",
    ]


def test_build_batch_validation_report_errors_without_license_in_strict_public_mode() -> None:
    report = build_batch_validation_report(
        batch_result=batch_result_fixture(),
        snapshots_by_id={
            "alpha": snapshot_fixture(
                file_count=1,
                skipped_file_count=0,
                package_manifest_count=1,
                license_file_count=0,
            )
        },
    )

    assert report["status"] == "error"
    assert report["summary"]["errorCount"] == 1
    record = report["records"][0]
    assert record["confidence"] == "low"
    assert record["errors"] == [
        {
            "code": "missing_license_file",
            "message": "Strict public registry mode requires an allowlisted license-like file.",
        }
    ]
    assert "error:missing_license_file" in record["confidenceReasons"]


def test_build_batch_validation_report_allows_missing_license_in_relaxed_private_mode() -> None:
    report = build_batch_validation_report(
        batch_result=batch_result_fixture(),
        snapshots_by_id={
            "alpha": snapshot_fixture(
                file_count=1,
                skipped_file_count=0,
                package_manifest_count=1,
                license_file_count=0,
            )
        },
        strict_public=False,
    )

    assert report["status"] == "ok"
    assert report["mode"] == "relaxed_private"
    assert report["summary"]["errorCount"] == 0
    assert report["records"][0]["errors"] == []


def test_build_batch_validation_report_marks_empty_or_policy_mismatch_low_confidence() -> None:
    snapshot = snapshot_fixture(
        file_count=0,
        skipped_file_count=0,
        package_manifest_count=0,
    )
    snapshot["policy"]["execution"] = "unknown"

    report = build_batch_validation_report(
        batch_result=batch_result_fixture(),
        snapshots_by_id={"alpha": snapshot},
    )

    record = report["records"][0]
    assert record["confidence"] == "low"
    assert [warning["code"] for warning in record["warnings"]] == [
        "collector_policy_mismatch",
        "no_files_collected",
        "no_package_manifests",
    ]
    assert report["summary"]["lowConfidenceCount"] == 1


def test_write_batch_validation_report_uses_stable_json(tmp_path: Path) -> None:
    report_path = tmp_path / "batch-validation.json"
    report = build_batch_validation_report(
        batch_result=batch_result_fixture(),
        snapshots_by_id={
            "alpha": snapshot_fixture(
                file_count=2,
                skipped_file_count=0,
                package_manifest_count=1,
            )
        },
    )

    write_batch_validation_report(report_path, report)

    text = report_path.read_text(encoding="utf-8")
    assert text.endswith("\n")
    assert json.loads(text) == report


def batch_result_fixture() -> dict:
    return {
        "status": "ok",
        "input": "inputs",
        "outputRoot": "candidates",
        "selectedIds": ["alpha"],
        "collectedCount": 1,
        "skippedCount": 1,
        "collected": [
            {
                "id": "alpha",
                "repository": "https://github.com/example/alpha",
                "revision": "abc",
                "ref": None,
                "checkout": "/tmp/alpha",
                "packageId": "alpha.core",
                "labels": ["python"],
                "sourceManifest": {"path": "repos.yml", "entryIndex": 0},
                "output": "candidates/alpha/harvest.json",
                "fileCount": 2,
                "skippedFileCount": 0,
            }
        ],
        "skipped": [{"id": "beta", "reason": "not_selected"}],
    }


def snapshot_fixture(
    *,
    file_count: int,
    skipped_file_count: int,
    package_manifest_count: int,
    license_file_count: int = 1,
) -> dict:
    return {
        "kind": "SpecHarvesterEvidenceSnapshot",
        "schemaVersion": 1,
        "source": {
            "kind": "local_checkout",
            "label": "alpha",
            "repository": "https://github.com/example/alpha",
            "revision": "abc",
        },
        "policy": {
            "execution": "none",
            "networkAccess": "none",
            "packageScripts": "not_run",
            "contentAuthority": "untrusted_metadata",
        },
        "analyzerPolicy": {
            "networkAccess": "none",
            "packageScripts": "not_run",
            "allowedExecutions": ["none"],
        },
        "summary": {
            "fileCount": file_count,
            "skippedFileCount": skipped_file_count,
            "packageManifestCount": package_manifest_count,
            "licenseFileCount": license_file_count,
        },
    }
