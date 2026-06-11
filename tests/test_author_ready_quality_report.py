from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.producer_receipt import CandidateOutputFile
from spec_harvester.producer_reports import (
    AuthorReadyDraftQualityReport,
    AuthorReadyDraftQualityReportRequest,
    ProducerReportRequest,
    author_ready_stop_policy_summary,
    stop_policy_summary_from_diagnostics,
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


def test_author_ready_stop_policy_summary_stops_when_all_members_are_author_ready(
    tmp_path: Path,
) -> None:
    request = write_quality_fixture(
        tmp_path,
        validation={"status": "valid", "warningCount": 0, "errorCount": 0},
        diagnostics={"status": "clean", "entries": []},
    )
    report = AuthorReadyDraftQualityReport(request).payload()

    summary = author_ready_stop_policy_summary(
        [
            {
                "packageId": "example.demo",
                "qualityReportPath": "example.demo/author-ready-draft-quality-report.json",
                "qualityReport": report,
            }
        ]
    )

    assert summary["status"] == "author_ready_draft"
    assert summary["decision"] == "stop_for_author_review"
    assert summary["memberCounts"] == {
        "total": 1,
        "author_ready_draft": 1,
        "needs_regeneration": 0,
        "blocked": 0,
    }
    assert summary["members"][0]["decision"] == "stop_for_author_review"
    assert summary["blockingReasons"] == []
    assert summary["topAuthorActionItems"][0]["packageId"] == "example.demo"
    assert "not SpecPM registry acceptance" in " ".join(summary["nonAuthority"])


def test_author_ready_stop_policy_summary_continues_for_regeneration_candidates(
    tmp_path: Path,
) -> None:
    request = write_quality_fixture(
        tmp_path,
        validation={"status": "valid", "warningCount": 0, "errorCount": 0},
        diagnostics={"status": "clean", "entries": []},
        include_evidence=False,
    )
    report = AuthorReadyDraftQualityReport(request).payload()

    summary = author_ready_stop_policy_summary(
        [
            {
                "packageId": "example.demo",
                "qualityReportPath": "example.demo/author-ready-draft-quality-report.json",
                "qualityReport": report,
            }
        ]
    )

    assert summary["status"] == "needs_regeneration"
    assert summary["decision"] == "continue_generation"
    assert summary["memberCounts"]["needs_regeneration"] == 1
    assert summary["reviewableDimensions"][0]["packageIds"] == ["example.demo"]


def test_author_ready_stop_policy_summary_blocks_on_any_blocked_member(
    tmp_path: Path,
) -> None:
    ready_request = write_quality_fixture(
        tmp_path / "ready",
        validation={"status": "valid", "warningCount": 0, "errorCount": 0},
        diagnostics={"status": "clean", "entries": []},
    )
    blocked_request = write_quality_fixture(
        tmp_path / "blocked",
        validation={"status": "invalid", "warningCount": 0, "errorCount": 1},
        diagnostics={"status": "clean", "entries": []},
    )

    summary = author_ready_stop_policy_summary(
        [
            {
                "packageId": "example.ready",
                "qualityReportPath": "example.ready/author-ready-draft-quality-report.json",
                "qualityReport": AuthorReadyDraftQualityReport(ready_request).payload(),
            },
            {
                "packageId": "example.blocked",
                "qualityReportPath": "example.blocked/author-ready-draft-quality-report.json",
                "qualityReport": AuthorReadyDraftQualityReport(blocked_request).payload(),
            },
        ]
    )

    assert summary["status"] == "blocked"
    assert summary["decision"] == "blocked_until_inputs_change"
    assert summary["memberCounts"]["blocked"] == 1
    assert summary["memberCounts"]["author_ready_draft"] == 1
    assert summary["blockingReasons"] == [
        {
            "packageId": "example.blocked",
            "qualityReportPath": "example.blocked/author-ready-draft-quality-report.json",
            "reason": "hard_gate_failed",
        }
    ]


def test_stop_policy_summary_continues_when_clean_proposal_has_no_subjects() -> None:
    summary = stop_policy_summary_from_diagnostics(
        source_status="completed",
        error_count=0,
        warning_count=0,
        subject_count=0,
    )

    assert summary["status"] == "needs_regeneration"
    assert summary["decision"] == "continue_generation"
    assert summary["reason"] == "no_proposal_subjects"


def write_quality_fixture(
    root: Path,
    *,
    validation: dict[str, object],
    diagnostics: dict[str, object],
    include_evidence: bool = True,
) -> AuthorReadyDraftQualityReportRequest:
    (root / "specs").mkdir(parents=True)
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
