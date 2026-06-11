from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.producer_receipt import CandidateOutputFile
from spec_harvester.producer_reports import (
    AuthorReadyDraftQualityReport,
    AuthorReadyDraftQualityReportRequest,
    ProducerReportRequest,
)


def test_author_ready_quality_report_blocks_invalid_validation(tmp_path: Path) -> None:
    request = write_quality_fixture(
        tmp_path,
        validation={"status": "invalid", "warningCount": 0, "errorCount": 1},
        diagnostics={"status": "clean", "entries": []},
    )

    report = AuthorReadyDraftQualityReport(request).payload()

    assert report["status"] == "blocked"
    assert report["authorReadyDraft"]["stopReason"] == "hard_gate_failed"
    assert gate_statuses(report)["producer_validation"] == "failed"
    assert "fix_producer_validation" in action_item_ids(report)


def test_author_ready_quality_report_needs_regeneration_without_evidence(
    tmp_path: Path,
) -> None:
    request = write_quality_fixture(
        tmp_path,
        validation={"status": "valid", "warningCount": 0, "errorCount": 0},
        diagnostics={"status": "clean", "entries": []},
        include_evidence=False,
    )

    report = AuthorReadyDraftQualityReport(request).payload()

    assert report["status"] == "needs_regeneration"
    assert report["authorReadyDraft"]["hardGateStatus"] == "review_required"
    assert gate_statuses(report)["evidence_links_present"] == "review_required"
    assert "complete_evidence_review" in action_item_ids(report)


def test_author_ready_quality_report_blocks_failed_diagnostics_status_without_entries(
    tmp_path: Path,
) -> None:
    request = write_quality_fixture(
        tmp_path,
        validation={"status": "valid", "warningCount": 0, "errorCount": 0},
        diagnostics={"status": "failed", "entries": []},
    )

    report = AuthorReadyDraftQualityReport(request).payload()

    assert report["status"] == "blocked"
    assert gate_statuses(report)["critical_diagnostics"] == "failed"
    assert "fix_critical_diagnostics" in action_item_ids(report)


def test_author_ready_quality_report_adds_action_item_for_diagnostics_warnings(
    tmp_path: Path,
) -> None:
    request = write_quality_fixture(
        tmp_path,
        validation={"status": "valid", "warningCount": 0, "errorCount": 0},
        diagnostics={"status": "warnings", "entries": []},
    )

    report = AuthorReadyDraftQualityReport(request).payload()

    assert report["status"] == "needs_regeneration"
    assert "review_diagnostics_warnings" in action_item_ids(report)


def test_author_ready_quality_report_blocks_missing_diagnostics_report(
    tmp_path: Path,
) -> None:
    request = write_quality_fixture(
        tmp_path,
        validation={"status": "valid", "warningCount": 0, "errorCount": 0},
        diagnostics={"status": "clean", "entries": []},
    )
    request.diagnostics_report_path.unlink()

    report = AuthorReadyDraftQualityReport(request).payload()

    assert report["status"] == "blocked"
    assert gate_statuses(report)["required_bundle_files"] == "failed"
    assert gate_statuses(report)["critical_diagnostics"] == "failed"
    assert "fix_required_bundle_files" in action_item_ids(report)


def test_author_ready_quality_report_requires_existing_evidence_file(
    tmp_path: Path,
) -> None:
    request = write_quality_fixture(
        tmp_path,
        validation={"status": "valid", "warningCount": 0, "errorCount": 0},
        diagnostics={"status": "clean", "entries": []},
    )
    (tmp_path / "harvest.json").unlink()

    report = AuthorReadyDraftQualityReport(request).payload()

    assert report["status"] == "needs_regeneration"
    assert gate_statuses(report)["evidence_links_present"] == "review_required"
    assert "review_evidence_links_present" in action_item_ids(report)


def write_quality_fixture(
    root: Path,
    *,
    validation: dict[str, object],
    diagnostics: dict[str, object],
    include_evidence: bool = True,
) -> AuthorReadyDraftQualityReportRequest:
    (root / "specs").mkdir()
    (root / "specpm.yaml").write_text("apiVersion: specpm.dev/v0.1\n", encoding="utf-8")
    (root / "specs" / "demo.spec.yaml").write_text(
        "apiVersion: specpm.dev/v0.1\n",
        encoding="utf-8",
    )
    output_files = [
        CandidateOutputFile(root=root, path="specpm.yaml", role="manifest"),
        CandidateOutputFile(root=root, path="specs/demo.spec.yaml", role="boundary_spec"),
        CandidateOutputFile(root=root, path="validation-report.json", role="validation_report"),
        CandidateOutputFile(root=root, path="diagnostics.json", role="diagnostics"),
    ]
    if include_evidence:
        (root / "harvest.json").write_text("{}", encoding="utf-8")
        output_files.append(CandidateOutputFile(root=root, path="harvest.json", role="evidence"))
    validation_path = root / "validation-report.json"
    diagnostics_path = root / "diagnostics.json"
    validation_path.write_text(json.dumps(validation), encoding="utf-8")
    diagnostics_path.write_text(json.dumps(diagnostics), encoding="utf-8")
    return AuthorReadyDraftQualityReportRequest(
        report=ProducerReportRequest(
            candidate_root=root,
            package_id="example.demo",
            package_version="0.1.0",
            package_api_version="specpm.dev/v0.1",
            spec_paths=("specs/demo.spec.yaml",),
            output_files=tuple(output_files),
        ),
        validation_report_path=validation_path,
        diagnostics_report_path=diagnostics_path,
    )


def gate_statuses(report: dict[str, object]) -> dict[str, str]:
    gates = report["hardGates"]
    assert isinstance(gates, list)
    return {str(gate["id"]): str(gate["status"]) for gate in gates if isinstance(gate, dict)}


def action_item_ids(report: dict[str, object]) -> set[str]:
    items = report["authorActionItems"]
    assert isinstance(items, list)
    return {str(item["id"]) for item in items if isinstance(item, dict)}
