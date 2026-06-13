from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.source_manifest import read_repository_source_manifests

ROOT = Path(__file__).resolve().parents[1]


def assert_current_next_task(next_text: str) -> None:
    if "# Next Task: P31-T2 Selected Candidate Handoff Proposal Helper" in next_text:
        assert_p31_t1_last_archived(next_text)
        assert_p30_t5_recent(next_text)
        assert_p31_t1_recent(next_text)
        assert_phase_31_t2_active(next_text)
        return

    if "# Next Task: P31-T1 Selected Candidate Handoff Proposal Contract" in next_text:
        assert_p30_t5_last_archived(next_text)
        assert_p30_t5_recent(next_text)
        assert_phase_31_t1_active(next_text)
        return

    if "# Next Task: Phase 30 Complete" in next_text:
        assert_p30_t5_last_archived(next_text)
        assert_p29_t6_recent(next_text)
        assert_p30_t1_recent(next_text)
        assert_p30_t2_recent(next_text)
        assert_p30_t3_recent(next_text)
        assert_p30_t4_recent(next_text)
        assert_p30_t5_recent(next_text)
        assert_phase_30_complete(next_text)
        return

    if "# Next Task: P30-T5 Selected Candidate Handoff Dry Run" in next_text:
        assert_p30_t4_last_archived(next_text)
        assert_p29_t6_recent(next_text)
        assert_p30_t1_recent(next_text)
        assert_p30_t2_recent(next_text)
        assert_p30_t3_recent(next_text)
        assert_p30_t4_recent(next_text)
        assert_phase_30_t5_active(next_text)
        return

    if "# Next Task: P30-T4 Candidate-Layer Triage Report" in next_text:
        assert_p30_t3_last_archived(next_text)
        assert_p29_t6_recent(next_text)
        assert_p30_t1_recent(next_text)
        assert_p30_t2_recent(next_text)
        assert_p30_t3_recent(next_text)
        assert_phase_30_t4_active(next_text)
        return

    if "# Next Task: P30-T3 Live LM Studio Limited Corpus Batch" in next_text:
        assert_p30_t2_last_archived(next_text)
        assert_p29_t6_recent(next_text)
        assert_p30_t1_recent(next_text)
        assert_p30_t2_recent(next_text)
        assert_phase_30_t3_active(next_text)
        return

    if "# Next Task: P30-T2 Deterministic Limited Corpus Batch" in next_text:
        assert_p30_t1_last_archived(next_text)
        assert_p29_t6_recent(next_text)
        assert_p30_t1_recent(next_text)
        assert_phase_30_t2_active(next_text)
        return

    if "# Next Task: P30-T1 Limited Popular-Library Corpus Plan" in next_text:
        assert_p29_t6_last_archived(next_text)
        assert_p29_t6_recent(next_text)
        assert_phase_30_t1_active(next_text)
        return

    if "# Next Task: P29-T6 Corpus Quality Gate After Fallbacks" in next_text:
        assert_p29_t5_last_archived(next_text)
        assert_p29_t1_recent(next_text)
        assert_p29_t2_recent(next_text)
        assert_p29_t3_recent(next_text)
        assert_p29_t4_recent(next_text)
        assert_p29_t5_recent(next_text)
        assert_phase_29_t6_active(next_text)
        return

    if "# Next Task: Phase 29 Complete" in next_text:
        assert_p29_t6_last_archived(next_text)
        assert_p29_t1_recent(next_text)
        assert_p29_t2_recent(next_text)
        assert_p29_t3_recent(next_text)
        assert_p29_t4_recent(next_text)
        assert_p29_t5_recent(next_text)
        assert_p29_t6_recent(next_text)
        assert_phase_29_complete(next_text)
        return

    if "# Next Task: P29-T5 LM Studio JSON Repair and Retry" in next_text:
        assert_p29_t4_last_archived(next_text)
        assert_p29_t1_recent(next_text)
        assert_p29_t2_recent(next_text)
        assert_p29_t3_recent(next_text)
        assert_p29_t4_recent(next_text)
        assert_phase_29_t5_active(next_text)
        return

    if "# Next Task: P29-T4 Single-Package Candidate Fallback" in next_text:
        assert_p29_t3_last_archived(next_text)
        assert_p29_t1_recent(next_text)
        assert_p29_t2_recent(next_text)
        assert_p29_t3_recent(next_text)
        assert_phase_29_t4_active(next_text)
        return

    if "# Next Task: P29-T3 Corpus Baseline and Gap Report" in next_text:
        assert_p29_t2_last_archived(next_text)
        assert_p29_t1_recent(next_text)
        assert_p29_t2_recent(next_text)
        assert_phase_29_t3_active(next_text)
        return

    if "# Next Task: P29-T2 SpecPM Candidate-Layer Intake Policy" in next_text:
        assert_p29_t1_last_archived(next_text)
        assert_p29_t1_recent(next_text)
        assert_phase_29_t2_active(next_text)
        return

    assert_p26_t5_archived(next_text)
    assert_p27_t1_recent(next_text)
    assert_p27_t2_recent(next_text)
    assert_p27_t3_recent(next_text)
    if "# Next Task: P27-T4 Author Review Viewer and Handoff Checklist" in next_text:
        assert_p27_t3_last_archived(next_text)
        assert_phase_27_t4_active(next_text)
        return

    if "# Next Task: P27-T5 Real Repository Author-Ready Draft Calibration Matrix" in next_text:
        assert_p27_t4_last_archived(next_text)
        assert_p27_t4_recent(next_text)
        assert_phase_27_t5_active(next_text)
        return

    if "# Next Task: P28-T3 Second Real Repository Refresh Compare Run" in next_text:
        assert_p28_t2_last_archived(next_text)
        assert_p27_t4_recent(next_text)
        assert_p27_t5_recent(next_text)
        assert_p28_t1_recent(next_text)
        assert_p28_t2_recent(next_text)
        assert_phase_28_t3_active(next_text)
        return

    if "# Next Task: P28 Follow-Up Selection" in next_text:
        assert_p28_t3_last_archived(next_text)
        assert_p27_t4_recent(next_text)
        assert_p27_t5_recent(next_text)
        assert_p28_t1_recent(next_text)
        assert_p28_t2_recent(next_text)
        assert_p28_t3_recent(next_text)
        assert_phase_28_follow_up_active(next_text)
        return

    if "# Next Task: P28-T4 Package-Set Role Selection Profiles" in next_text:
        assert_p28_t3_last_archived(next_text)
        assert_p27_t4_recent(next_text)
        assert_p27_t5_recent(next_text)
        assert_p28_t1_recent(next_text)
        assert_p28_t2_recent(next_text)
        assert_p28_t3_recent(next_text)
        assert_phase_28_t4_active(next_text)
        return

    if "# Next Task: P28-T5 First-Submission or Seeded-Baseline Workflow" in next_text:
        assert_p28_t4_last_archived(next_text)
        assert_p27_t4_recent(next_text)
        assert_p27_t5_recent(next_text)
        assert_p28_t1_recent(next_text)
        assert_p28_t2_recent(next_text)
        assert_p28_t3_recent(next_text)
        assert_p28_t4_recent(next_text)
        assert_phase_28_t5_active(next_text)
        return

    if "# Next Task: Phase 28 Complete" in next_text:
        assert_p28_t5_last_archived(next_text)
        assert_p27_t4_recent(next_text)
        assert_p27_t5_recent(next_text)
        assert_p28_t1_recent(next_text)
        assert_p28_t2_recent(next_text)
        assert_p28_t3_recent(next_text)
        assert_p28_t4_recent(next_text)
        assert_p28_t5_recent(next_text)
        assert_phase_28_complete(next_text)
        return

    if "# Next Task: P29-T1 Autonomous Candidate Batch Runner" in next_text:
        assert_p28_t5_last_archived(next_text)
        assert_p27_t4_recent(next_text)
        assert_p27_t5_recent(next_text)
        assert_p28_t1_recent(next_text)
        assert_p28_t2_recent(next_text)
        assert_p28_t3_recent(next_text)
        assert_p28_t4_recent(next_text)
        assert_p28_t5_recent(next_text)
        assert_phase_29_t1_active(next_text)
        return

    assert_p27_t5_last_archived(next_text)
    assert_p27_t4_recent(next_text)
    assert_p27_t5_recent(next_text)
    assert_phase_27_complete(next_text)


def assert_p27_t3_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P27-T3 Author-Ready Stop Policy Summary" in next_text


def assert_p27_t4_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P27-T4 Author Review Viewer and Handoff Checklist" in next_text


def assert_p27_t5_last_archived(next_text: str) -> None:
    assert (
        "**Last Archived:** P27-T5 Real Repository Author-Ready Draft Calibration Matrix"
        in next_text
    )


def assert_p28_t2_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P28-T2 Real Xyflow Refresh Compare Run" in next_text


def assert_p28_t3_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P28-T3 Second Real Repository Refresh Compare Run" in next_text


def assert_p28_t4_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P28-T4 Package-Set Role Selection Profiles" in next_text


def assert_p28_t5_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P28-T5 First-Submission or Seeded-Baseline Workflow" in next_text


def assert_p29_t1_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P29-T1 Autonomous Candidate Batch Runner" in next_text


def assert_p29_t2_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P29-T2 SpecPM Candidate-Layer Intake Policy" in next_text


def assert_p29_t3_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P29-T3 Corpus Baseline and Gap Report" in next_text


def assert_p29_t4_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P29-T4 Single-Package Candidate Fallback" in next_text


def assert_p29_t5_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P29-T5 LM Studio JSON Repair and Retry" in next_text


def assert_p29_t6_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P29-T6 Corpus Quality Gate After Fallbacks" in next_text


def assert_p30_t1_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P30-T1 Limited Popular-Library Corpus Plan" in next_text


def assert_p30_t2_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P30-T2 Deterministic Limited Corpus Batch" in next_text


def assert_p30_t3_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P30-T3 Live LM Studio Limited Corpus Batch" in next_text


def assert_p30_t4_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P30-T4 Candidate-Layer Triage Report" in next_text


def assert_p30_t5_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P30-T5 Selected Candidate Handoff Dry Run" in next_text


def assert_p31_t1_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P31-T1 Selected Candidate Handoff Proposal Contract" in next_text


def assert_p26_t5_archived(next_text: str) -> None:
    assert "SpecHarvesterPackageSetAIDraftProposal" in next_text
    assert "LLM + schema" in next_text
    assert "selected members" in next_text
    assert "exclusions" in next_text
    assert "contains" in next_text


def assert_p27_t1_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P27-T1` documented the author-ready draft quality bar" in next_text
    assert "valid starter package" in next_text
    assert "repository authors" in next_text
    assert "final accepted specification" in normalized


def assert_p27_t2_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P27-T2` added `author-ready-draft-quality-report.json`" in next_text
    assert "authorReadyDraft" in next_text
    assert "quality_report" in next_text
    assert "author action items" in normalized


def assert_p27_t3_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P27-T3` added a deterministic stop-policy summary" in next_text
    assert "authorReadyDraftSummary" in next_text
    assert "stopPolicySummary" in next_text
    assert "stop_for_author_review" in next_text
    assert "continue_generation" in next_text
    assert "blocked_until_inputs_change" in next_text
    assert "single draft" in normalized
    assert "AI enrichment" in normalized


def assert_p27_t4_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P27-T4` added author review checklists" in next_text
    assert "authorReview" in next_text
    assert "weak claims" in next_text
    assert "evidence gaps" in next_text
    assert "recommended edits" in next_text
    assert "member action summaries" in normalized


def assert_phase_27_t4_active(next_text: str) -> None:
    assert "# Next Task: P27-T4 Author Review Viewer and Handoff Checklist" in next_text
    assert "**Status:** In Progress" in next_text
    assert "author review checklists" in next_text
    assert "weak claim" in next_text
    assert "evidence-gap" in next_text
    assert "recommended edits" in next_text


def assert_p27_t5_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P27-T5` added `SpecHarvesterAuthorReadyCalibrationMatrix`" in next_text
    assert "SpecHarvesterAuthorReadyCalibrationMatrix" in next_text
    assert "author-ready-calibration-matrix" in next_text
    assert "totalEstimatedAuthorEdits" in next_text
    assert "calibrationVerdict" in next_text
    assert "author_curation_ready" in normalized


def assert_phase_27_t5_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P27-T5 Real Repository Author-Ready Draft Calibration Matrix" in next_text
    assert "**Status:** In Progress" in next_text
    assert "real-repository author-ready draft calibration matrix" in next_text
    assert "author edits" in next_text
    assert "curated specs" in normalized


def assert_phase_27_complete(next_text: str) -> None:
    assert "# Next Task: Phase 27 Complete" in next_text
    assert "**Status:** Phase Complete" in next_text
    assert "Author-Ready Valid Drafts" in next_text


def assert_p28_t1_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P28-T1` added `SpecHarvesterFreshCandidateRefreshRun`" in next_text
    assert "fresh-candidate-refresh-run" in next_text
    assert "prepare-refresh-decision" in next_text
    assert "publishing packages" in normalized
    assert "maintainer review" in normalized


def assert_p28_t2_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P28-T2` ran real `xyflow`" in next_text
    assert "a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd" in next_text
    assert "no_update_required" in next_text
    assert "no_contract_delta" in next_text
    assert "8 generated contract-file digests" in normalized


def assert_p28_t3_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    plain = normalized.replace("`", "")
    assert "`P28-T3` ran real `TanStack/query`" in next_text
    assert "feb1efd804c1262106f72c8adc1d82a8ce9cfbb0" in next_text
    assert "tanstack_query.workspace" in next_text
    assert "39 candidates" in plain
    assert "38 contains relation proposals" in plain
    assert "78 fresh contract files" in plain
    assert "refresh_decision_prepare_current_contract_files_missing" in next_text
    assert "missing-baseline" in normalized


def assert_p28_t4_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    plain = normalized.replace("`", "")
    assert "`P28-T4` added package-set role selection profiles" in next_text
    assert "--role-profile generic_monorepo" in normalized
    assert "workspace and member_package roles" in plain
    assert "39 candidates" in plain
    assert "38 contains relation proposals" in plain


def assert_p28_t5_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    plain = normalized.replace("`", "")
    assert "`P28-T5` added `SpecHarvesterBaselineSubmissionHandoff`" in next_text
    assert "baseline-submission-handoff" in next_text
    assert "first_submission_required" in next_text
    assert "refresh_decision_prepare_current_contract_files_missing" in next_text
    assert "first_submission_review" in next_text
    assert "seed_baseline" in next_text
    assert "reject_or_request_regeneration" in next_text
    assert "notRefreshDecision: true" in normalized
    assert "39 candidates" in plain
    assert "78 contract files" in plain
    assert "39 missing-baseline diagnostics" in plain


def assert_phase_28_t3_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P28-T3 Second Real Repository Refresh Compare Run" in next_text
    assert "**Status:** In Progress" in next_text
    assert "second package-set-capable repository" in normalized
    assert "not calibrated only against `xyflow`" in normalized


def assert_phase_28_follow_up_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P28 Follow-Up Selection" in next_text
    assert "**Status:** Review Pending" in next_text
    assert "role selection" in normalized
    assert "first-submission or seeded-baseline workflow" in normalized


def assert_phase_28_t4_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P28-T4 Package-Set Role Selection Profiles" in next_text
    assert "**Status:** In Progress" in next_text
    assert "generic monorepos" in normalized
    assert "--role member_package" in normalized
    assert "declarative" in normalized
    assert "P28-T5" in next_text
    assert "first-submission or seeded-baseline workflow" in normalized


def assert_phase_28_t5_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P28-T5 First-Submission or Seeded-Baseline Workflow" in next_text
    assert "**Status:** In Progress" in next_text
    assert "refresh_decision_prepare_current_contract_files_missing" in next_text
    assert "first-submission or seeded-baseline evidence" in normalized
    assert "failed registry refresh" in normalized
    assert "producer evidence is not SpecPM acceptance" in normalized


def assert_phase_28_complete(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: Phase 28 Complete" in next_text
    assert "**Status:** Phase Complete" in next_text
    assert "SpecPM Refresh Compare Handoff is complete" in next_text
    assert "fresh generated-root layout" in normalized
    assert "`xyflow` smoke" in next_text
    assert "real `TanStack/query`" in next_text
    assert "generic monorepos" in normalized
    assert "SpecHarvesterBaselineSubmissionHandoff" in next_text
    assert "SpecPM-side intake policy/preflight" in normalized


def assert_phase_29_t1_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P29-T1 Autonomous Candidate Batch Runner" in next_text
    assert "**Status:** Selected" in next_text
    assert "autonomous candidate batch runner" in normalized
    assert "workspace inventory" in normalized
    assert "public interface indexes" in normalized
    assert "LM Studio/OpenAI-compatible provider" in normalized
    assert "autonomous popular-library scraping" in normalized
    assert "must not clone repositories" in normalized
    assert "accepted SpecPM truth" in normalized


def assert_p29_t1_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P29-T1` added `autonomous-candidate-batch`" in next_text
    assert "SpecHarvesterAutonomousCandidateBatchReport" in next_text
    assert "autonomous_popular_mvp" in next_text
    assert "openai/gpt-oss-20b" in next_text
    assert "AI draft `completed`" in normalized
    assert "AI enrichment `completed`" in normalized
    assert "`xyflow` smoke" in next_text
    assert "4 candidates" in normalized
    assert "3 relations" in normalized
    assert "stop_for_author_review" in next_text
    assert "AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md" in next_text
    assert "single-package fallback" in normalized
    assert "JSON repair/retry" in normalized


def assert_phase_29_t2_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P29-T2 SpecPM Candidate-Layer Intake Policy" in next_text
    assert "**Status:** In Progress" in next_text
    assert "SpecPM-facing candidate-layer intake policy" in normalized
    assert "autonomous batch output" in normalized
    assert "AI draft/enrichment proposals" in normalized
    assert "without turning producer output into registry authority" in normalized
    assert "P29-T4" in next_text
    assert "P29-T5" in next_text
    assert "P29-T6" in next_text


def assert_p29_t2_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P29-T2` documented" in next_text
    assert "AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md" in next_text
    assert "AutonomousCandidateIntakePolicy" in next_text
    assert "candidate_layer_review_required" in next_text
    assert "needs_regeneration" in next_text
    assert "not_for_intake" in next_text
    assert "producer_preview_evidence_only" in next_text
    assert "SpecHarvesterPackageSetAIDraftProposal" in next_text
    assert "SpecHarvesterPackageSetAIEnrichmentProposal" in next_text
    assert "accept packages" in normalized
    assert "remove `preview_only`" in next_text
    assert "publish registry metadata" in normalized


def assert_p29_t3_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P29-T3` recorded the Flask, Gin, and xyflow corpus baseline" in next_text
    assert "AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md" in next_text
    assert "AutonomousCandidateCorpusBaseline" in next_text
    assert "SpecHarvesterAutonomousCandidateCorpusBaseline" in next_text
    assert "deterministic `--skip-ai` outcomes" in next_text
    assert "live LM Studio statuses" in normalized
    assert "pipelineHealth: deterministic_pipeline_passed" in next_text
    assert "candidateQuality: needs_follow_up" in next_text
    assert "single_package_fallback_needed" in next_text
    assert "stop_for_author_review" in next_text
    assert "ai_json_repair_needed" in next_text


def assert_phase_29_t3_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P29-T3 Corpus Baseline and Gap Report" in next_text
    assert "**Status:** In Progress" in next_text
    assert "Flask, Gin, and xyflow" in next_text
    assert "deterministic `--skip-ai` outcomes" in next_text
    assert "live LM Studio outcome" in normalized
    assert "candidate counts" in normalized
    assert "relation counts" in normalized
    assert "single_package_fallback_needed" in next_text
    assert "ai_json_repair_needed" in next_text
    assert "no generated preview candidate is promoted to SpecPM acceptance" in normalized


def assert_phase_29_t4_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P29-T4 Single-Package Candidate Fallback" in next_text
    assert "**Status:** In Progress" in next_text
    assert "single-package candidate fallback" in normalized
    assert "Flask and Gin" in next_text
    assert "deterministic evidence and public interface indexes" in normalized
    assert "package-set drafting selects no workspace members" in normalized
    assert "one preview candidate" in normalized
    assert "preview_only" in next_text
    assert "producer_preview_evidence_only" in next_text
    assert "avoid inventing `contains` relations" in next_text
    assert "SpecPM registry acceptance out of scope" in normalized


def assert_p29_t4_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P29-T4` implemented the deterministic single-package candidate fallback" in next_text
    assert "SINGLE_PACKAGE_CANDIDATE_FALLBACK.md" in next_text
    assert "SinglePackageCandidateFallback" in next_text
    assert "flask.core" in next_text
    assert "gin.core" in next_text
    assert "0` relation proposals" in next_text
    assert "single_package_source_manifest_fallback" in next_text
    assert "preview_only" in next_text
    assert "producer_preview_evidence_only" in next_text
    assert "producer receipt" in normalized
    assert "author-ready quality report" in normalized
    assert "SpecPM registry acceptance" in normalized


def assert_phase_29_t5_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P29-T5 LM Studio JSON Repair and Retry" in next_text
    assert "**Status:** In Progress" in next_text
    assert "LM Studio/OpenAI-compatible JSON repair/retry" in normalized
    assert "malformed local model output" in normalized
    assert "no-raw-response persistence boundary" in normalized
    assert "structured diagnostics" in normalized
    assert "repair attempt counts" in normalized
    assert "raw prompts, raw provider responses, secrets, and chain-of-thought" in normalized
    assert "needs_regeneration" in next_text


def assert_p29_t5_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P29-T5` implemented bounded LM Studio/OpenAI-compatible JSON repair/retry" in next_text
    assert "package-set AI draft and enrichment proposal generation" in normalized
    assert "jsonRepairNeeded" in next_text
    assert "jsonRepairAttemptCount" in next_text
    assert "jsonRepairStatus" in next_text
    assert "ai_json_repair_needed" in next_text
    assert "ai_json_repair_exhausted" in next_text
    assert "diagnosticCodes" in next_text
    assert "jsonRepair" in next_text
    assert "raw prompts, raw provider responses, secrets, or chain-of-thought" in normalized


def assert_phase_29_t6_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P29-T6 Corpus Quality Gate After Fallbacks" in next_text
    assert "**Status:** In Progress" in next_text
    assert "mixed local Flask/Gin/xyflow corpus" in normalized
    assert "at least one reviewable preview candidate" in normalized
    assert "deterministic preflight" in normalized
    assert "live LM Studio status" in normalized
    assert "larger popular-library scraping" in normalized


def assert_p29_t6_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P29-T6` recorded the post-mitigation corpus quality gate" in next_text
    assert "AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md" in next_text
    assert "AutonomousCandidateCorpusQualityGate" in next_text
    assert "SpecHarvesterAutonomousCandidateCorpusQualityGate" in next_text
    assert "flask.core" in next_text
    assert "gin.core" in next_text
    assert "xyflow.workspace" in next_text
    assert "ready_for_limited_popular_library_scraping" in next_text
    assert "deterministic preflight passed" in normalized
    assert "openai/gpt-oss-20b" in next_text
    assert "excluded_package_unknown" in next_text
    assert "package_set_id_missing" in next_text
    assert "JSON repair `not_needed`" in next_text
    assert "producer_preview_evidence_only" in next_text
    assert "preview_only" in next_text
    assert "not automatic SpecPM acceptance" in normalized


def assert_phase_29_complete(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: Phase 29 Complete" in next_text
    assert "**Status:** Phase Complete" in next_text
    assert "Autonomous Candidate Harvest MVP is complete" in next_text
    assert "valid starter packages" in normalized
    assert "limited popular-library scraping" in normalized
    assert "candidate-layer review" in normalized
    assert "not accepted registry truth" in normalized
    assert "select the next phase" in normalized


def assert_phase_30_t1_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P30-T1 Limited Popular-Library Corpus Plan" in next_text
    assert "**Status:** Selected" in next_text
    assert "Phase 30. Limited Popular-Library Scraping Batch" in next_text
    assert "P29-T6 Corpus Quality Gate After Fallbacks" in next_text
    assert "ready_for_limited_popular_library_scraping" in next_text
    assert "flask.core" in next_text
    assert "gin.core" in next_text
    assert "xyflow.workspace" in next_text
    assert "producer_preview_evidence_only" in next_text
    assert "preview_only" in next_text
    assert "not automatic SpecPM acceptance" in normalized
    assert "source-manifest shape" in normalized
    assert "selection criteria" in normalized
    assert "operator runbook" in normalized
    assert "non-authority boundaries" in normalized


def assert_p30_t1_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P30-T1` defined the limited popular-library corpus plan" in next_text
    assert "LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md" in next_text
    assert "LimitedPopularLibraryCorpusPlan" in next_text
    assert "inputs/limited-popular-libraries/repositories.yml" in next_text
    assert "flask.core" in next_text
    assert "gin.core" in next_text
    assert "xyflow.workspace" in next_text
    assert "cupertino.core" in next_text
    assert "navigation-split-view.core" in next_text
    assert "docc2context.core" in next_text
    assert "source-manifest shape" in normalized
    assert "selection criteria" in normalized
    assert "operator runbook" in normalized
    assert "stop conditions" in normalized
    assert "candidate-layer triage states" in normalized
    assert "non-authority boundaries" in normalized


def assert_phase_30_t2_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P30-T2 Deterministic Limited Corpus Batch" in next_text
    assert "**Status:**" in next_text
    assert "In Progress" in next_text or "Selected" in next_text
    assert "Phase 30. Limited Popular-Library Scraping Batch" in next_text
    assert "deterministic `--skip-ai` path" in next_text
    assert "collection, candidate, relation" in normalized
    assert "preflight, and stop-policy outcomes" in normalized


def assert_p30_t2_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P30-T2` recorded the deterministic limited popular-library corpus run" in next_text
    assert "LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md" in next_text
    assert "SpecHarvesterLimitedPopularLibraryDeterministicBatch" in next_text
    assert "ready_for_live_lm_studio_limited_corpus" in next_text
    assert "6 repositories" in normalized
    assert "9 preview candidates" in normalized
    assert "3 relation proposals" in normalized
    assert "navigation_split_view.core" in next_text
    assert "package_id_hint_mismatch" in next_text
    assert "producer_preview_evidence_only" in next_text
    assert "not SpecPM acceptance" in normalized


def assert_phase_30_t3_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P30-T3 Live LM Studio Limited Corpus Batch" in next_text
    assert "**Status:**" in next_text
    assert "In Progress" in next_text or "Selected" in next_text
    assert "Phase 30. Limited Popular-Library Scraping Batch" in next_text
    assert "live LM Studio" in normalized
    assert "openai/gpt-oss-20b" in next_text
    assert "deterministic P30-T2 baseline" in normalized
    assert "cost" in normalized
    assert "repair" in normalized
    assert "non-authority boundaries" in normalized


def assert_p30_t3_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P30-T3` recorded the live LM Studio limited corpus run" in next_text
    assert "LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md" in next_text
    assert "SpecHarvesterLimitedPopularLibraryLiveLMStudioBatch" in next_text
    assert "ready_for_candidate_layer_triage" in next_text
    assert "openai/gpt-oss-20b" in next_text
    assert "6 repositories" in normalized
    assert "9 preview candidates" in normalized
    assert "3 relation proposals" in normalized
    assert "AI draft" in normalized
    assert "2 completed" in normalized
    assert "4 warning" in normalized
    assert "AI enrichment" in normalized
    assert "5 completed" in normalized
    assert "1 warning" in normalized
    assert "JSON repair" in normalized
    assert "not_needed" in next_text
    assert "138700" in next_text
    assert "excluded_package_unknown" in next_text
    assert "package_set_id_missing" in next_text
    assert "refined_summary_missing" in next_text
    assert "package_id_hint_mismatch" in next_text
    assert "producer_preview_evidence_only" in next_text
    assert "not SpecPM acceptance" in normalized


def assert_phase_30_t4_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P30-T4 Candidate-Layer Triage Report" in next_text
    assert "**Status:**" in next_text
    assert "In Progress" in next_text or "Selected" in next_text
    assert "Phase 30. Limited Popular-Library Scraping Batch" in next_text
    assert "candidate-layer triage report" in normalized
    assert "candidate_layer_review_required" in next_text
    assert "needs_regeneration" in next_text
    assert "blocked" in next_text
    assert "not_for_intake" in next_text
    assert "excluded_package_unknown" in next_text
    assert "package_set_id_missing" in next_text
    assert "refined_summary_missing" in next_text
    assert "package_id_hint_mismatch" in next_text


def assert_p30_t4_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P30-T4` recorded the candidate-layer triage report" in next_text
    assert "LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md" in next_text
    assert "SpecHarvesterLimitedPopularLibraryCandidateLayerTriage" in next_text
    assert "ready_for_selected_handoff_dry_run" in next_text
    assert "flask.core" in next_text
    assert "gin.core" in next_text
    assert "docc2context.core" in next_text
    assert "candidate_layer_review_required" in next_text
    assert "needs_regeneration" in next_text
    assert "3 selected" in normalized
    assert "6 deferred" in normalized
    assert "excluded_package_unknown" in next_text
    assert "package_set_id_missing" in next_text
    assert "refined_summary_missing" in next_text
    assert "package_id_hint_mismatch" in next_text
    assert "producer_preview_evidence_only" in next_text
    assert "not SpecPM acceptance" in normalized


def assert_phase_30_t5_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P30-T5 Selected Candidate Handoff Dry Run" in next_text
    assert "**Status:**" in next_text
    assert "In Progress" in next_text or "Selected" in next_text
    assert "Phase 30. Limited Popular-Library Scraping Batch" in next_text
    assert "SpecPM handoff dry-run evidence" in normalized
    assert "flask.core" in next_text
    assert "gin.core" in next_text
    assert "docc2context.core" in next_text
    assert "preview_only" in next_text
    assert "producer_preview_evidence_only" in next_text
    assert "external registry acceptance authority" in normalized


def assert_p30_t5_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P30-T5` recorded the selected handoff dry run" in next_text
    assert "LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md" in next_text
    assert "SpecHarvesterLimitedPopularLibrarySelectedHandoffDryRun" in next_text
    assert "selected_handoff_dry_run_ready" in next_text
    assert "flask.core" in next_text
    assert "gin.core" in next_text
    assert "docc2context.core" in next_text
    assert "3 selected" in normalized
    assert "6 deferred" in normalized
    assert "producer preflight" in normalized
    assert "static viewer" in normalized
    assert "external_required" in next_text
    assert "producer_preview_evidence_only" in next_text
    assert "not SpecPM acceptance" in normalized


def assert_phase_30_complete(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: Phase 30 Complete" in next_text
    assert "**Status:** Phase Complete" in next_text
    assert "Limited Popular-Library Scraping Batch is complete" in next_text
    assert "deterministic evidence" in normalized
    assert "live LM Studio evidence" in normalized
    assert "candidate-layer triage" in normalized
    assert "selected handoff dry run" in normalized
    assert "not accepted registry truth" in normalized


def assert_phase_31_t1_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P31-T1 Selected Candidate Handoff Proposal Contract" in next_text
    assert "**Status:** Selected" in next_text
    assert "Phase 31. Selected Candidate SpecPM Intake Handoff" in next_text
    assert "SpecHarvesterSelectedCandidateHandoffProposal" in next_text
    assert "portable proposal contract" in normalized
    assert "preview_only" in next_text
    assert "producer_preview_evidence_only" in next_text
    assert "external SpecPM acceptance authority" in normalized


def assert_p31_t1_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P31-T1` defined `SpecHarvesterSelectedCandidateHandoffProposal`" in next_text
    assert "SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md" in next_text
    assert "selected-candidate-handoff-proposal/v0" in next_text
    assert "flask.core" in next_text
    assert "gin.core" in next_text
    assert "docc2context.core" in next_text
    assert "3 selected" in normalized
    assert "6 deferred" in normalized
    assert "required evidence roles" in normalized
    assert "external_required" in next_text
    assert "not SpecPM acceptance" in normalized


def assert_phase_31_t2_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P31-T2 Selected Candidate Handoff Proposal Helper" in next_text
    assert "**Status:** Selected" in next_text
    assert "producer helper" in normalized
    assert "JSON and Markdown handoff artifacts" in normalized
    assert "selected candidate bundles" in normalized
    assert "producer preflight reports" in normalized
    assert "static viewer outputs" in normalized
    assert "SpecPM acceptance out of scope" in normalized


def test_analyzer_sandbox_requirements_docs_cover_required_controls() -> None:
    github_doc = ROOT / "docs" / "ANALYZER_SANDBOX_REQUIREMENTS.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "AnalyzerSandboxRequirements.md"
    )

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "execution: none",
            "metadata_tool_only",
            "build_tool_sandboxed",
            "no network",
            "no package scripts",
            "no harvested dependency installation",
            "no secret access",
            "pinned analyzer",
            "bounded filesystem",
            "deterministic output",
            "source digest evidence",
            "diagnostics",
            "audit log",
            "collect-local",
            "untrusted evidence",
        ):
            assert required in text


def test_docc_topics_link_analyzer_sandbox_requirements() -> None:
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    trust_boundary = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "TrustBoundary.md"

    assert "<doc:AnalyzerSandboxRequirements>" in root_page.read_text(encoding="utf-8")
    assert "<doc:AnalyzerSandboxRequirements>" in trust_boundary.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_trusted_classifier_evaluation() -> None:
    github_doc = ROOT / "docs" / "TRUSTED_CLASSIFIER_EVALUATION.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "TrustedClassifierEvaluation.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    trust_boundary = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "TrustBoundary.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "classifierPolicy",
            "ProjectProfile",
            "manifest-first",
            "advisory untrusted metadata",
            "go-enry",
            "Syft",
            "ScanCode",
            "Universal Ctags",
            "Tree-sitter",
            "pinned tool version",
            "no network",
            "no package scripts",
            "no harvested dependency installation",
            "source digest evidence",
        ):
            assert required in text

    assert "TRUSTED_CLASSIFIER_EVALUATION.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:TrustedClassifierEvaluation>" in root_page.read_text(encoding="utf-8")
    assert "<doc:TrustedClassifierEvaluation>" in trust_boundary.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_project_profile_analyzer_orchestration() -> None:
    github_doc = ROOT / "docs" / "BATCH_COLLECTION.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "BatchCollection.md"
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc, architecture_doc, architecture_docc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "--emit-interface-indexes",
            "ProjectProfile.analyzerPlan",
            "public-interface-index.json",
            "spec_harvester.python_public_api",
            "spec_harvester.js_ts_public_api",
            "spec_harvester.go_public_api",
            "spec_harvester.swift_public_api",
            "manifest_only",
            "advisory",
            "kind: public_interface_index",
            "artifactKind: SpecHarvesterPublicInterfaceIndex",
            "SpecPM `0.2.0+`",
        ):
            assert required in text

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "--emit-interface-indexes",
            "--analyzer-cache-dir",
            "PublicInterfaceIndex",
            "does not install dependencies",
            "run package scripts",
            "execute checkout files",
            "contact networks",
            "kind: public_interface_index",
            "artifactKind: SpecHarvesterPublicInterfaceIndex",
            "SpecPM `0.2.0+`",
        ):
            assert required in text


def test_docc_and_github_docs_cover_language_neutral_semantic_extraction() -> None:
    github_doc = ROOT / "docs" / "LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LanguageNeutralSemanticExtraction.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "semanticHints",
            "language-neutral",
            "README",
            "API contract",
            "OpenAPI",
            "schema validation",
            "workflow automation",
            "developer tooling",
            "web framework",
            "documentation knowledge base",
            "semantic_intent_static_evidence",
            "declared SpecPM support targets",
            "provides.capabilities.<capability_id>",
            "provides.capabilities.intentIds",
            "intent.web.framework_surface",
            "intent.api.contract_surface",
            "intent.metadata.schema_validation",
            "manifest-poor",
            "raw documentation bodies",
        ):
            assert required in text

    assert "LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:LanguageNeutralSemanticExtraction>" in root_page.read_text(encoding="utf-8")
    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "semanticHints" in text
        assert "intent.web.framework_surface" in text
        assert "intent.api.contract_surface" in text
        assert "provides.capabilities.<capability_id>" in text
        assert "provides.capabilities.intentIds" in text
        assert "raw documentation" in text


def test_docc_and_github_docs_cover_static_spec_renderer() -> None:
    github_doc = ROOT / "docs" / "STATIC_SPEC_RENDERER.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "StaticSpecRenderer.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "render-spec-site",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "spec-package.json",
            "SpecPM remains",
            "validation and registry authority",
            "no package code execution",
            "no package scripts",
            "no dependency installation",
            "no network probes",
            "no browser-side YAML parsing",
            "SpecHarvesterStaticSpecPackage",
            "standalone viewer",
        ):
            assert required in text

    assert "STATIC_SPEC_RENDERER.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:StaticSpecRenderer>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_producer_candidate_bundle_plan() -> None:
    github_doc = ROOT / "docs" / "PRODUCER_CANDIDATE_BUNDLE.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProducerCandidateBundle.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    workplan = ROOT / "SPECS" / "Workplan.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecPM Producer Candidate Bundle Contract",
            "candidate/",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "apiVersion: specpm.receipts/v0",
            "kind: SpecPMProducerReceipt",
            "receiptProfile: generated_spec_package_v0",
            "configuration.digest",
            "outputs[]",
            "SHA-256",
            "self-hash problem",
            "humanReview.status: approved",
            "maintainer override",
            "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md"
            if path == github_doc
            else "SpecPMRegistryAcceptanceDecision",
            "privacy.secretsIncluded",
            "unstable generated ID",
            "evidence references",
            "namespace",
            "Producer receipts are evidence, not authority",
            "SPECPM_SHARED_FIXTURE_POLICY.md"
            if path == github_doc
            else "SpecPMSharedFixturePolicy",
        ):
            assert required in normalized

        assert "producer-receipt.json` must not appear in `outputs[]" in text

    assert "PRODUCER_CANDIDATE_BUNDLE.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:ProducerCandidateBundle>" in root_page.read_text(encoding="utf-8")

    workplan_text = workplan.read_text(encoding="utf-8")
    assert "apiVersion: specpm.receipts/v0" in workplan_text
    assert "kind: SpecPMProducerReceipt" in workplan_text
    assert "apiVersion: specpm.producer_receipt/v1" not in workplan_text


def test_docc_and_github_docs_cover_specpm_handoff_guide() -> None:
    github_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecHarvester produces an evidence-rich candidate",
            "SpecPM validates package shape",
            "public index publishes only reviewed sources",
            "candidate/",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "spec-harvester collect-local",
            "spec-harvester draft",
            "preflight-candidate-bundle",
            "render-spec-site",
            'kind": "SpecPMProducerReceipt',
            'receiptProfile": "generated_spec_package_v0',
            "producer-receipt.json` must not appear in `outputs[]",
            "humanReview.status: approved",
            "maintainer override",
            "SpecHarvester evidence can support the decision",
            "It cannot make the decision",
            "registryAcceptanceDecision.status: external_required",
            "SpecPMRegistryAcceptanceDecision",
            "Shared Fixture Policy",
        ):
            assert required in normalized

    assert "SPECPM_HANDOFF.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecPMHandoff>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_specpm_shared_fixture_policy() -> None:
    github_doc = ROOT / "docs" / "SPECPM_SHARED_FIXTURE_POLICY.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMSharedFixturePolicy.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecPM Shared Fixture Policy",
            "SpecPM contract fixture",
            "SpecHarvester generated fixture",
            "reviewable drift check",
            "generated_spec_package_v0",
            "exact SpecPM commit SHA",
            "root of trust",
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "producer preflight",
            "static viewer",
            "proposal body evidence links",
            "Silent drift is not acceptable" if path == github_doc else "silently drift",
            "does not make generated",
        ):
            assert required in normalized

    assert "SPECPM_SHARED_FIXTURE_POLICY.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecPMSharedFixturePolicy>" in root_page.read_text(encoding="utf-8")
    assert "shared fixture policy" in roadmap.read_text(encoding="utf-8")
    workplan_text = workplan.read_text(encoding="utf-8")
    assert "`P23-T2` Define a shared cross-repository fixture policy" in workplan_text
    assert "- [x] `P23-T2`" in workplan_text
    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_specpm_ci_preflight_gate_support() -> None:
    github_doc = ROOT / "docs" / "SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecPMCiPreflightGateSupport.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    proposal_doc = ROOT / "docs" / "SPECPM_PROPOSAL_AUTOMATION.md"
    docc_proposal = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProposalAutomation.md"
    )
    handoff_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    shared_fixture_doc = ROOT / "docs" / "SPECPM_SHARED_FIXTURE_POLICY.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecPM CI Preflight Gate Support",
            "future optional SpecPM CI preflight",
            "stable producer evidence layout",
            "SpecPM maintainer review",
            "registry acceptance decision",
            "producerEvidenceLinks",
            "pathScope",
            "accepted_source_bundle",
            "producer_receipt",
            "validation_report",
            "diagnostics",
            "producer_preflight",
            "static_viewer",
            "accepted_source_diff",
            "humanReview.requiredFor",
            "public_index_acceptance",
            "repo_relative",
            "workflow_artifact",
            "pull_request",
            "A pass is not acceptance" if path == docc_doc else "does not require SpecPM",
        ):
            assert required in normalized

    assert "SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecPMCiPreflightGateSupport>" in root_page.read_text(encoding="utf-8")
    assert "SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md" in proposal_doc.read_text(encoding="utf-8")
    assert "<doc:SpecPMCiPreflightGateSupport>" in docc_proposal.read_text(encoding="utf-8")
    assert "SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md" in handoff_doc.read_text(encoding="utf-8")
    assert "SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md" in shared_fixture_doc.read_text(encoding="utf-8")
    assert "optional SpecPM CI preflight gate" in roadmap.read_text(encoding="utf-8")
    workplan_text = workplan.read_text(encoding="utf-8")
    assert "`P23-T3` Add SpecHarvester-side support" in workplan_text
    assert "- [x] `P23-T3`" in workplan_text
    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_specpm_registry_acceptance_decision() -> None:
    github_doc = ROOT / "docs" / "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecPMRegistryAcceptanceDecision.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    proposal_doc = ROOT / "docs" / "SPECPM_PROPOSAL_AUTOMATION.md"
    docc_proposal = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProposalAutomation.md"
    )
    handoff_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    producer_bundle_doc = ROOT / "docs" / "PRODUCER_CANDIDATE_BUNDLE.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecPM Registry Acceptance Decision Record",
            "external registry acceptance decision record",
            "SpecPMRegistryAcceptanceDecision",
            "public_index_acceptance",
            "external_required",
            "evidence_only",
            "pending",
            "approved",
            "rejected",
            "override",
            "withdrawn",
            "SpecHarvester receipt says approved",
            "must not be the root of trust for approval",
        ):
            assert required in normalized

    assert "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecPMRegistryAcceptanceDecision>" in root_page.read_text(encoding="utf-8")
    assert "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md" in proposal_doc.read_text(encoding="utf-8")
    assert "<doc:SpecPMRegistryAcceptanceDecision>" in docc_proposal.read_text(encoding="utf-8")
    assert "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md" in handoff_doc.read_text(encoding="utf-8")
    assert "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md" in producer_bundle_doc.read_text(
        encoding="utf-8"
    )
    assert "external SpecPM registry acceptance decision" in roadmap.read_text(encoding="utf-8")
    workplan_text = workplan.read_text(encoding="utf-8")
    assert "`P23-T4` Integrate a future external registry acceptance decision" in workplan_text
    assert "- [x] `P23-T4`" in workplan_text
    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_specpm_package_set_alignment() -> None:
    github_doc = ROOT / "docs" / "SPECPM_PACKAGE_SET_ALIGNMENT.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMPackageSetAlignment.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecPM Package Set Alignment",
            "Package Sets",
            "Package Relations",
            "Package Set Search",
            "Package Set Registry Metadata",
            "SpecHarvester Monorepo Discovery",
            "Multi-Package Producer Intake",
            "Xyflow Package Set Reference",
            "workspace inventory",
            "package-set candidates",
            "scoped member",
            "relation proposals",
            "bundle-set preflight",
            "static viewer",
            "xyflow.workspace",
            "xyflow.system",
            "xyflow.react",
            "xyflow.svelte",
            "producer_observed",
            "package_id",
            "P25-T2",
            "P25-T7",
            "package script execution",
            "trust inheritance",
        ):
            assert required in normalized

    assert "SPECPM_PACKAGE_SET_ALIGNMENT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecPMPackageSetAlignment>" in root_page.read_text(encoding="utf-8")
    assert "Package-set contract alignment is documented" in roadmap.read_text(encoding="utf-8")
    workplan_text = workplan.read_text(encoding="utf-8")
    assert "`P25-T1` Align SpecHarvester planning" in workplan_text
    assert "- [x] `P25-T1`" in workplan_text
    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_workspace_inventory() -> None:
    github_doc = ROOT / "docs" / "WORKSPACE_INVENTORY.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "WorkspaceInventory.md"
    batch_doc = ROOT / "docs" / "BATCH_COLLECTION.md"
    batch_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "BatchCollection.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "workspace-inventory.json",
            "spec-harvester.workspace-inventory/v0",
            "SpecHarvesterWorkspaceInventory",
            "--emit-workspace-inventory",
            "repository URL",
            "exact revision",
            "workspace manifests",
            "include patterns",
            "package manifest paths",
            "proposed SpecPM package IDs",
            "package roles",
            "digest-backed evidence references",
            "producer evidence",
            "not a SpecPM registry payload",
            "xyflow.workspace",
            "xyflow.system",
            "xyflow.react",
            "xyflow.svelte",
            "P25-T3",
            "preflight-bundle-set",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (batch_doc, batch_docc):
        text = path.read_text(encoding="utf-8")
        assert "--emit-workspace-inventory" in text
        assert "workspace-inventory.json" in text
        assert "SpecHarvesterWorkspaceInventory" in text

    assert "WORKSPACE_INVENTORY.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:WorkspaceInventory>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_package_set_drafting() -> None:
    github_doc = ROOT / "docs" / "PACKAGE_SET_DRAFTING.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageSetDrafting.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workspace_doc = ROOT / "docs" / "WORKSPACE_INVENTORY.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "draft-package-set",
            "workspace-inventory.json",
            "package-set-draft.json",
            "package-relation-proposals.json",
            "spec-harvester.package-set-draft/v0",
            "SpecHarvesterPackageSetDraft",
            "xyflow.workspace",
            "xyflow.system",
            "xyflow.react",
            "xyflow.svelte",
            "preview_only",
            "skipped[]",
            "role_not_selected_for_initial_package_set_draft",
            "P25-T4",
            "preflight-bundle-set",
            "not namespace authority",
            "does not execute package scripts",
            "role selection profiles",
            "--role-profile generic_monorepo",
            "workspace/member package-set",
            "selection.roleProfile",
            "custom",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (workflow_doc, workspace_doc):
        text = path.read_text(encoding="utf-8")
        assert "draft-package-set" in text
        assert "package-set-draft.json" in text

    assert "PACKAGE_SET_DRAFTING.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:PackageSetDrafting>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_package_relation_proposals() -> None:
    github_doc = ROOT / "docs" / "PACKAGE_RELATION_PROPOSALS.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageRelationProposals.md"
    )
    package_set_doc = ROOT / "docs" / "PACKAGE_SET_DRAFTING.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workspace_doc = ROOT / "docs" / "WORKSPACE_INVENTORY.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "package-relation-proposals.json",
            "spec-harvester.package-relation-proposals/v0",
            "SpecHarvesterPackageRelationProposals",
            "contains",
            "xyflow.workspace contains xyflow.system",
            "xyflow.workspace contains xyflow.react",
            "xyflow.workspace contains xyflow.svelte",
            "reviewStatus: producer_observed",
            "workspace-inventory.json",
            "package-set-draft.json",
            "does not hash itself",
            "not SpecPM accepted registry metadata",
            "trust inheritance",
            "preflight-bundle-set",
            "render-package-set-site",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (package_set_doc, workflow_doc, workspace_doc):
        assert "package-relation-proposals.json" in path.read_text(encoding="utf-8")

    assert "PACKAGE_RELATION_PROPOSALS.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:PackageRelationProposals>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_bundle_set_preflight() -> None:
    github_doc = ROOT / "docs" / "BUNDLE_SET_PREFLIGHT.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "BundleSetPreflight.md"
    package_set_doc = ROOT / "docs" / "PACKAGE_SET_DRAFTING.md"
    relation_doc = ROOT / "docs" / "PACKAGE_RELATION_PROPOSALS.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "preflight-bundle-set",
            "package-set-draft.json",
            "package-relation-proposals.json",
            "spec-harvester.bundle-set-preflight/v0",
            "SpecHarvesterBundleSetPreflightReport",
            "candidate `packageId`",
            "preflight-candidate-bundle",
            "relation source and target",
            "workspace inventory",
            "does not accept packages",
            "does not accept relations",
            "package managers",
            "render-package-set-site",
            "P25-T7",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (package_set_doc, relation_doc, workflow_doc):
        assert "preflight-bundle-set" in path.read_text(encoding="utf-8")

    assert "BUNDLE_SET_PREFLIGHT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:BundleSetPreflight>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_package_set_viewer() -> None:
    github_doc = ROOT / "docs" / "PACKAGE_SET_VIEWER.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageSetViewer.md"
    package_set_doc = ROOT / "docs" / "PACKAGE_SET_DRAFTING.md"
    relation_doc = ROOT / "docs" / "PACKAGE_RELATION_PROPOSALS.md"
    preflight_doc = ROOT / "docs" / "BUNDLE_SET_PREFLIGHT.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "render-package-set-site",
            "package-set-draft.json",
            "package-relation-proposals.json",
            "bundle-set-preflight.json",
            "package-set.json",
            "SpecHarvesterStaticPackageSet",
            "spec-harvester.static-package-set-renderer/v0",
            "authorReadyDraftSummary",
            "authorReview",
            "author review checklist",
            "weak claim",
            "evidence-gap",
            "recommended edits",
            "member action",
            "member package cards",
            "relation proposal badges",
            "result scope examples",
            "producer-observed review status",
            "producer_observed",
            "does not accept packages",
            "does not accept relations",
            "P25-T7",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (package_set_doc, relation_doc, preflight_doc, workflow_doc, workflow_docc):
        text = " ".join(path.read_text(encoding="utf-8").split())
        assert "render-package-set-site" in text
        assert "member package cards" in text
        assert "relation proposal badges" in text

    assert "PACKAGE_SET_VIEWER.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:PackageSetViewer>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_xyflow_package_set_smoke() -> None:
    github_doc = ROOT / "docs" / "XYFLOW_PACKAGE_SET_SMOKE.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "XyflowPackageSetSmoke.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    alignment_doc = ROOT / "docs" / "SPECPM_PACKAGE_SET_ALIGNMENT.md"
    alignment_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMPackageSetAlignment.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "xyflow-package-set-smoke",
            "collect-batch --emit-workspace-inventory",
            "draft-package-set",
            "preflight-bundle-set",
            "render-package-set-site",
            "workspace-inventory.json",
            "package-set-draft.json",
            "package-relation-proposals.json",
            "bundle-set-preflight.json",
            "viewer/package-set.json",
            "xyflow-package-set-smoke.json",
            "spec-harvester.xyflow-package-set-smoke/v0",
            "SpecHarvesterXyflowPackageSetSmokeReport",
            "xyflow.workspace",
            "xyflow.system",
            "xyflow.react",
            "xyflow.svelte",
            "xyflow.workspace contains xyflow.system",
            "xyflow.workspace contains xyflow.react",
            "xyflow.workspace contains xyflow.svelte",
            "xyflow.cli",
            "xyflow.e2e",
            "xyflow.react_examples",
            "xyflow.svelte_examples",
            "does not fetch the real",
            "run package scripts",
            "run package managers",
            "accept packages",
            "accept relations",
            "publish registry metadata",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "XYFLOW_PACKAGE_SET_SMOKE.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:XyflowPackageSetSmoke>" in root_page.read_text(encoding="utf-8")
    for path in (workflow_doc, alignment_doc, alignment_docc):
        text = path.read_text(encoding="utf-8")
        assert "xyflow-package-set-smoke" in text
        assert "xyflow-package-set-smoke.json" in text
        assert "viewer/package-set.json" in text


def test_docc_and_github_docs_cover_package_set_handoff_proposal() -> None:
    github_doc = ROOT / "docs" / "PACKAGE_SET_HANDOFF_PROPOSAL.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageSetHandoffProposal.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    proposal_doc = ROOT / "docs" / "SPECPM_PROPOSAL_AUTOMATION.md"
    proposal_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProposalAutomation.md"
    )
    handoff_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    handoff_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "package-set-handoff-proposal",
            "package-set-draft.json",
            "package-relation-proposals.json",
            "bundle-set-preflight.json",
            "SpecHarvesterPackageSetHandoffProposal",
            "spec-harvester.package-set-handoff-proposal/v0",
            "package_set_draft",
            "package_relation_proposals",
            "bundle_set_preflight",
            "package_set_viewer",
            "member_candidate_bundle",
            "member_manifest",
            "member_producer_receipt",
            "member_quality_report",
            "package_relation_summary",
            "authorReadyDraftSummary",
            "authorReview",
            "Author Review Checklist",
            "Weak Claims and Evidence Gaps",
            "Recommended Edits",
            "Weak claims",
            "Evidence gaps",
            "Recommended edits",
            "stop_for_author_review",
            "registryAcceptanceDecision.status: external_required",
            "public_index_acceptance",
            "package_relation_acceptance",
            "does not accept packages",
            "accept relations",
            "replace SpecPM maintainer review",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (proposal_doc, proposal_docc, handoff_doc, handoff_docc):
        text = path.read_text(encoding="utf-8")
        assert "package-set-handoff-proposal" in text
        assert "external_required" in text

    assert "PACKAGE_SET_HANDOFF_PROPOSAL.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:PackageSetHandoffProposal>" in root_page.read_text(encoding="utf-8")
    workplan_text = workplan.read_text(encoding="utf-8")
    assert "`P26-T1` Add a package-set handoff proposal artifact" in workplan_text
    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_package_set_ai_enrichment() -> None:
    github_doc = ROOT / "docs" / "PACKAGE_SET_AI_ENRICHMENT.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageSetAIEnrichment.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    handoff_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    handoff_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    workplan = ROOT / "SPECS" / "Workplan.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "package-set-ai-enrichment-proposal",
            "SpecHarvesterPackageSetAIEnrichmentProposal",
            "spec-harvester.package-set-ai-enrichment/v0",
            "openai/gpt-oss-20b",
            "refinedSummary",
            "capabilities",
            "interfaces",
            "evidencePaths",
            "model_evidence_path_unsupported",
            "stopPolicySummary",
            "stop_for_author_review",
            "continue_generation",
            "blocked_until_inputs_change",
            "proposal evidence only",
            "does not mutate",
            "accept packages",
            "accept relations",
            "publish registry metadata",
            "CI must not require",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (handoff_doc, handoff_docc):
        text = path.read_text(encoding="utf-8")
        assert "package-set-ai-enrichment-proposal" in text
        assert "SpecHarvesterPackageSetAIEnrichmentProposal" in text
        assert "model_evidence_path_unsupported" in text

    assert "PACKAGE_SET_AI_ENRICHMENT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:PackageSetAIEnrichment>" in root_page.read_text(encoding="utf-8")
    assert "`P26-T4` Add proposal-only package-set AI enrichment" in workplan.read_text(
        encoding="utf-8"
    )


def test_docc_and_github_docs_cover_fresh_candidate_refresh_run() -> None:
    github_doc = ROOT / "docs" / "FRESH_CANDIDATE_REFRESH_RUN.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "FreshCandidateRefreshRun.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    handoff_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    handoff_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    package_set_handoff = ROOT / "docs" / "PACKAGE_SET_HANDOFF_PROPOSAL.md"
    package_set_handoff_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageSetHandoffProposal.md"
    )
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        plain = normalized.replace("`", "")
        for required in (
            "fresh-candidate-refresh-run",
            "SpecHarvesterFreshCandidateRefreshRun",
            "spec-harvester.fresh-candidate-refresh-run/v0",
            "specpm-public-index-generated-root/v0",
            "<package_id>/<version>/specpm.yaml",
            "specs/*.spec.yaml",
            "specpm producer-bundle prepare-refresh-decision",
            "refresh-decision.json",
            "prepare-report.json",
            "preflight-report.json",
            "producerEvidenceAuthority: evidence_only",
            "noRegistryMutation: true",
            "no_update_required",
            "no_contract_delta",
            "8 generated contract-file digests",
            "TanStack/query",
            "feb1efd804c1262106f72c8adc1d82a8ce9cfbb0",
            "refresh_decision_prepare_current_contract_files_missing",
            "manual_review_required",
            "first-submission",
            "seeded-baseline workflow",
            "does not publish packages",
            "replace SpecPM maintainer review",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"
        assert "39 candidates" in plain, f"TanStack/query candidate count missing in {path}"
        assert "38 contains relation proposals" in plain, (
            f"TanStack/query relation count missing in {path}"
        )
        assert "78 contract files" in plain, f"TanStack/query contract file count missing in {path}"

    for path in (handoff_doc, handoff_docc, package_set_handoff, package_set_handoff_docc):
        text = path.read_text(encoding="utf-8")
        assert "fresh-candidate-refresh-run" in text
        assert "prepare-refresh-decision" in text

    assert "FRESH_CANDIDATE_REFRESH_RUN.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:FreshCandidateRefreshRun>" in root_page.read_text(encoding="utf-8")
    assert "SpecHarvesterFreshCandidateRefreshRun" in roadmap.read_text(encoding="utf-8")
    assert "FreshCandidateRefreshRun" in roadmap_docc.read_text(encoding="utf-8")
    assert "`P28-T1` Add a fresh candidate refresh run contract" in workplan.read_text(
        encoding="utf-8"
    )
    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_baseline_submission_handoff() -> None:
    github_doc = ROOT / "docs" / "BASELINE_SUBMISSION_HANDOFF.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "BaselineSubmissionHandoff.md"
    )
    specpm_handoff = ROOT / "docs" / "SPECPM_HANDOFF.md"
    specpm_handoff_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    )
    fresh_doc = ROOT / "docs" / "FRESH_CANDIDATE_REFRESH_RUN.md"
    fresh_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "FreshCandidateRefreshRun.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "baseline-submission-handoff",
            "SpecHarvesterBaselineSubmissionHandoff",
            "spec-harvester.baseline-submission-handoff/v0",
            "refresh_decision_prepare_current_contract_files_missing",
            "first_submission_required",
            "baseline_review_required",
            "first_submission_review",
            "seed_baseline",
            "reject_or_request_regeneration",
            "producerEvidenceAuthority: evidence_only",
            "noRegistryMutation: true",
            "notRefreshDecision: true",
            "baseline seeding",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (specpm_handoff, specpm_handoff_docc, fresh_doc, fresh_docc):
        text = path.read_text(encoding="utf-8")
        assert "baseline-submission-handoff" in text
        assert "SpecHarvesterBaselineSubmissionHandoff" in text or (
            "<doc:BaselineSubmissionHandoff>" in text
        )

    assert "BASELINE_SUBMISSION_HANDOFF.md" in docs_index.read_text(encoding="utf-8")
    root_text = root_page.read_text(encoding="utf-8")
    assert "docs/BASELINE_SUBMISSION_HANDOFF.md" in root_text
    assert "<doc:BaselineSubmissionHandoff>" in root_text
    assert "SpecHarvesterBaselineSubmissionHandoff" in roadmap.read_text(encoding="utf-8")
    assert "SpecHarvesterBaselineSubmissionHandoff" in roadmap_docc.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_author_ready_draft_quality_bar() -> None:
    github_doc = ROOT / "docs" / "AUTHOR_READY_DRAFT_QUALITY_BAR.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "AuthorReadyDraftQualityBar.md"
    )
    package_set_ai_draft = ROOT / "docs" / "PACKAGE_SET_AI_DRAFT_PROPOSAL.md"
    package_set_ai_draft_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageSetAIDraftProposal.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "valid starter package",
            "author-ready draft",
            "SpecHarvester -> valid author-ready draft",
            "author + agent -> semantic completion and curation",
            "SpecPM -> validation, registry acceptance, and public index authority",
            "specpm validate",
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "preview",
            "author action items",
            "evidence gaps",
            "not a numeric guarantee of correctness",
            "authorReadyDraftSummary",
            "stop_for_author_review",
            "continue_generation",
            "blocked_until_inputs_change",
            "validation",
            "evidenceCoverage",
            "repositorySpecificity",
            "packageTopology",
            "claimConservatism",
            "authorActionability",
            "authorityBoundary",
            "framework encyclopedia",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "AUTHOR_READY_DRAFT_QUALITY_BAR.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyDraftQualityBar>" in docc_root.read_text(encoding="utf-8")
    assert "AUTHOR_READY_DRAFT_QUALITY_BAR.md" in package_set_ai_draft.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyDraftQualityBar>" in package_set_ai_draft_docc.read_text(
        encoding="utf-8"
    )

    roadmap_text = roadmap.read_text(encoding="utf-8")
    roadmap_docc_text = roadmap_docc.read_text(encoding="utf-8")
    assert "Milestone 5: Author-Ready Valid Drafts" in roadmap_text
    assert "valid starter package" in roadmap_text
    assert "Author-Ready Valid Drafts" in roadmap_docc_text
    assert "<doc:AuthorReadyDraftQualityBar>" in roadmap_docc_text

    workplan_text = workplan.read_text(encoding="utf-8")
    assert "Phase 27. Author-Ready Valid Drafts" in workplan_text
    for task_id in ("P27-T1", "P27-T2", "P27-T3", "P27-T4", "P27-T5"):
        assert f"`{task_id}`" in workplan_text
    assert "- [x] `P27-T1`" in workplan_text
    assert "- [x] `P27-T2`" in workplan_text
    assert "- [x] `P27-T3`" in workplan_text
    assert "- [x] `P27-T4`" in workplan_text
    assert "- [x] `P27-T5`" in workplan_text
    assert "author_ready_draft" in workplan_text
    assert "needs_regeneration" in workplan_text
    assert "blocked" in workplan_text

    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_author_ready_draft_quality_report() -> None:
    github_doc = ROOT / "docs" / "AUTHOR_READY_DRAFT_QUALITY_REPORT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AuthorReadyDraftQualityReport.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    producer_doc = ROOT / "docs" / "PRODUCER_CANDIDATE_BUNDLE.md"
    handoff_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    package_set_handoff = ROOT / "docs" / "PACKAGE_SET_HANDOFF_PROPOSAL.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "author-ready-draft-quality-report.json",
            "spec-harvester.author-ready-draft-quality/v0",
            "SpecHarvesterAuthorReadyDraftQualityReport",
            "authorReadyDraft.status",
            "author_ready_draft",
            "needs_regeneration",
            "blocked",
            "hardGates",
            "producer_validation",
            "critical_diagnostics",
            "required_bundle_files",
            "producer_receipt_planned",
            "evidence_links_present",
            "authority_boundary",
            "dimensions",
            "authorActionItems",
            "authorReadyDraftSummary",
            "stop_for_author_review",
            "continue_generation",
            "blocked_until_inputs_change",
            "quality_report",
            "not SpecPM registry acceptance",
            "not maintainer approval",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "AUTHOR_READY_DRAFT_QUALITY_REPORT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyDraftQualityReport>" in docc_root.read_text(encoding="utf-8")
    assert "quality_report" in producer_doc.read_text(encoding="utf-8")
    assert "author-ready-draft-quality-report.json" in handoff_doc.read_text(encoding="utf-8")
    assert "member_quality_report" in package_set_handoff.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_author_ready_calibration_matrix() -> None:
    github_doc = ROOT / "docs" / "AUTHOR_READY_CALIBRATION_MATRIX.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AuthorReadyCalibrationMatrix.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"
    quality_doc = ROOT / "docs" / "REAL_REPOSITORY_QUALITY_REPORT.md"
    quality_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "RealRepositoryQualityReport.md"
    )
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "author-ready-calibration-matrix",
            "quality-report.json",
            "spec-harvester.author-ready-calibration-matrix/v0",
            "SpecHarvesterAuthorReadyCalibrationMatrix",
            "estimatedAuthorEdits",
            "editCategories",
            "authorReadyStatus",
            "reviewPriority",
            "generatorFollowUpReasons",
            "calibrationVerdict",
            "author_curation_ready",
            "mixed_author_ready",
            "generator_follow_up_recommended",
            "blocked_inputs_present",
            "cupertino",
            "navigation-split-view",
            "xyflow",
            "flask",
            "gin",
            "docc2context",
            ".smoke/",
            "must not be committed",
            "SpecPM acceptance",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "AUTHOR_READY_CALIBRATION_MATRIX.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyCalibrationMatrix>" in docc_root.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyCalibrationMatrix>" in workflow_docc.read_text(encoding="utf-8")
    assert "AUTHOR_READY_CALIBRATION_MATRIX.md" in quality_doc.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyCalibrationMatrix>" in quality_docc.read_text(encoding="utf-8")
    assert "author-ready calibration matrix" in roadmap.read_text(encoding="utf-8")
    assert "AuthorReadyCalibrationMatrix" in roadmap_docc.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_governance_report_broad_intent_filtering() -> None:
    github_doc = ROOT / "docs" / "GOVERNANCE_REPORTS.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "GovernanceReports.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Broad language-neutral semantic intents",
            "API contract",
            "metadata schema validation",
            "workflow automation",
            "developer tooling",
            "documentation",
            "public repository metadata",
            "records",
            "duplicate findings",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"


def test_docc_and_github_docs_cover_specnode_integration_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    trust_doc = ROOT / "docs" / "TRUST_BOUNDARY.md"
    trust_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "TrustBoundary.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterSpecNodeArtifactBundle",
            "SpecNodeRefinementJob",
            "candidatePatchProposal",
            "usageReceipt",
            "modelFilesystemAccess: none",
            "modelShellAccess: none",
            "modelNetworkAccess: provider_only",
            "allowedTools",
            "candidateMutation: proposal_only",
            "rawSourceAccess: none",
            "secretAccess: none",
            "proposal_only",
            "ProjectProfile",
            "PublicInterfaceIndex",
            "public-interface-index.json",
            "harvest.json",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "no authority",
            "cannot run shell commands",
            "mutate files",
            "read raw repository source",
            "read secrets",
            "install dependencies",
            "run package scripts",
            "expand network access",
            "SpecPM validation",
            "human review",
        ):
            assert required in text
        assert '"attempts": []' not in text

    assert "SPECNODE_INTEGRATION_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeIntegrationContract>" in root_page.read_text(encoding="utf-8")

    for path in (architecture_doc, architecture_docc, trust_doc, trust_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNode" in text
        assert "SpecHarvesterSpecNodeArtifactBundle" in text
        assert "SpecNodeRefinementJob" in text
        assert "modelFilesystemAccess: none" in text
        assert "modelShellAccess: none" in text

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNode" in text
        assert "SpecHarvesterSpecNodeArtifactBundle" in text
        assert "SpecNodeRefinementJob" in text
        assert "candidatePatchProposal" in text
        assert "usageReceipt" in text


def test_docc_and_github_docs_cover_refine_preview_planning_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_REFINE_PREVIEW_CONTRACT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinePreviewContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterRefinePreviewPlan",
            "refine-preview",
            "compactModelInput",
            "harvestSummary",
            "projectProfile",
            "publicInterfaceSummary",
            "semanticEvidenceIndex",
            "validationSummaries",
            "draftCandidateMetadata",
            "artifactDigests",
            "promptBudget",
            "maxPromptBytes",
            "maxPromptTokens",
            "maxPublicSymbols",
            "maxSemanticClusters",
            "truncationPolicy",
            "redactionPolicy",
            "rawRepositorySource: excluded",
            "documentationBodies: excluded",
            "providerLogs: excluded",
            "arbitraryPrompts: excluded",
            "modelFilesystemAccess: none",
            "modelShellAccess: none",
            "candidateMutation: proposal_only",
            "SpecHarvesterSpecNodeArtifactBundle",
            "SpecNodeRefinementJob",
            "harvest.json",
            "ProjectProfile",
            "PublicInterfaceIndex",
            "public-interface-index.json",
            "SpecHarvesterEvidenceSnapshot",
            "does not execute models",
            "deterministic local planning step",
            "perform network fetches",
        ):
            assert required in text

    assert "SPECNODE_REFINE_PREVIEW_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeRefinePreviewContract>" in root_page.read_text(encoding="utf-8")

    for path in (integration_doc, integration_docc, architecture_doc, architecture_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecHarvesterRefinePreviewPlan" in text
        assert "compactModelInput" in text

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecHarvesterRefinePreviewPlan" in text
        assert "compactModelInput" in text
        assert "PublicInterfaceIndex" in text


def test_docc_and_github_docs_cover_specnode_refinement_prompt_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_REFINEMENT_PROMPT_CONTRACT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinementPromptContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    refine_doc = ROOT / "docs" / "SPECNODE_REFINE_PREVIEW_CONTRACT.md"
    refine_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinePreviewContract.md"
    )
    provider_doc = ROOT / "docs" / "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md"
    provider_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderAdapterContract.md"
    )
    patch_doc = ROOT / "docs" / "SPECNODE_PATCH_PROPOSAL_CONTRACT.md"
    patch_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodePatchProposalContract.md"
    )
    smoke_doc = ROOT / "docs" / "SPECNODE_PROVIDER_SMOKE_COVERAGE.md"
    smoke_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderSmokeCoverage.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecNodeRefinementPromptContract",
            "promptContractVersion",
            "SpecNodeRefinementPromptTemplate",
            "SpecNodeRefinementPromptInput",
            "SpecNodeRefinementPromptInstructions",
            "compactModelInput",
            "SpecHarvesterRefinePreviewPlan",
            "SpecNodeRefinementResult",
            "SpecNodeCandidatePatchProposal",
            "SpecNodeRejectionReason",
            "response_format.type: json_schema",
            "response_format.type: json_object",
            "generate_specpm",
            "target package behavior",
            "evidence_reference_rules",
            "negative_claim_policy",
            "confidence_calibration",
            "Evidence Reference Rules",
            "Negative-Claim Policy",
            "Confidence Calibration",
            "unknown IDs",
            "collapsed ranges",
            "invented evidence references",
            "no network calls",
            "no authentication",
            "chain-of-thought",
            "provider logs",
            "raw repository source",
            "arbitrary prompts",
            "modelFilesystemAccess: none",
            "modelShellAccess: none",
            "candidateMutation: proposal_only",
            "schema validation",
            "SpecPM validation",
            "human review",
        ):
            assert required in text

    assert "SPECNODE_REFINEMENT_PROMPT_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeRefinementPromptContract>" in root_page.read_text(encoding="utf-8")

    for path in (
        refine_doc,
        refine_docc,
        provider_doc,
        provider_docc,
        patch_doc,
        patch_docc,
        smoke_doc,
        smoke_docc,
        architecture_doc,
        architecture_docc,
        workflow_doc,
        workflow_docc,
    ):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeRefinementPromptContract" in text
            or "SPECNODE_REFINEMENT_PROMPT_CONTRACT.md" in text
        )

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "target-package intent inference" in text
        assert "unsupported negative claims" in text
        assert "overconfident" in text


def test_docc_and_github_docs_cover_specnode_semantic_review_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_SEMANTIC_REVIEW_CONTRACT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeSemanticReviewContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    prompt_doc = ROOT / "docs" / "SPECNODE_REFINEMENT_PROMPT_CONTRACT.md"
    prompt_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinementPromptContract.md"
    )
    patch_doc = ROOT / "docs" / "SPECNODE_PATCH_PROPOSAL_CONTRACT.md"
    patch_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodePatchProposalContract.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecNodeSemanticReviewContract",
            "semanticReviewContractVersion",
            "SpecNodeSemanticReviewJob",
            "SpecNodeSemanticReviewRubric",
            "SpecNodeSemanticReviewResult",
            "SpecNodeSemanticReviewFinding",
            "SpecNodeSemanticReviewVerdict",
            "SpecNodeRefinementResult",
            "compactModelInput",
            "response_format.type: json_schema",
            "response_format.type: json_object",
            "approve",
            "needs_revision",
            "reject",
            "wrong_package_intent",
            "unsupported_capability_claim",
            "missing_evidence_reference",
            "overconfident_confidence_score",
            "unsafe_negative_claim",
            "schema_policy_mismatch",
            "authority_boundary_violation",
            "prompt_contract_violation",
            "generate_specpm",
            "firstPassPromptTranscript: excluded",
            "chainOfThought: excluded",
            "firstPassProviderLogs: excluded",
            "providerLogs: excluded",
            "rawRepositorySource: excluded",
            "arbitraryPrompts: excluded",
            "candidateMutation: none",
            "candidatePatchProposal",
            "operations",
            "retryDirective",
            "rawUnifiedDiff",
            "shellCommand",
            "networkFetch",
            "providerCall",
            "packageManagerCommand",
            "testRunnerCommand",
            "buildToolCommand",
            "direct file writes",
            "reviewed_refinement_result",
            "semantic_evidence_index",
            "human review",
        ):
            assert required in text

    assert "SPECNODE_SEMANTIC_REVIEW_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeSemanticReviewContract>" in root_page.read_text(encoding="utf-8")

    for path in (
        integration_doc,
        integration_docc,
        prompt_doc,
        prompt_docc,
        patch_doc,
        patch_docc,
        architecture_doc,
        architecture_docc,
        workflow_doc,
        workflow_docc,
    ):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeSemanticReviewContract" in text
            or "SPECNODE_SEMANTIC_REVIEW_CONTRACT.md" in text
        )

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeSemanticReviewRubric" in text
        assert "SpecNodeSemanticReviewFinding" in text
        assert "wrong_package_intent" in text
        assert "authority_boundary_violation" in text
        assert "direct file writes" in text


def test_docc_and_github_docs_cover_specnode_retry_orchestration_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinementRetryOrchestration.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    semantic_doc = ROOT / "docs" / "SPECNODE_SEMANTIC_REVIEW_CONTRACT.md"
    semantic_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeSemanticReviewContract.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecNodeRefinementRetryOrchestrationContract",
            "retryOrchestrationContractVersion",
            "SpecNodeRefinementRetryRun",
            "SpecNodeRefinementRetryPolicy",
            "SpecNodeRefinementRetryAttempt",
            "SpecNodeRetryDirectiveSet",
            "SpecNodeRetryDirective",
            "SpecNodeRetryContext",
            "SpecNodeRefinementResult",
            "SpecNodeSemanticReviewResult",
            "SpecNodeSemanticReviewFinding",
            "maxAttempts",
            "attemptCount",
            "artifactReuse: same_bundle_and_preview_plan",
            "sourceBundleDigest",
            "sourcePreviewPlanDigest",
            "sourceSemanticReviewResultDigest",
            "sourceFindingId",
            "boundedInstruction",
            "rawTextPropagation: forbidden",
            "candidateOutputAuthority: proposal_only",
            "approved",
            "retry_scheduled",
            "retry_limit_reached",
            "needs_revision",
            "reject",
            "refocus_target_package_intent",
            "remove_or_evidence_capability_claim",
            "add_evidence_reference_or_drop_claim",
            "lower_confidence_or_add_evidence",
            "remove_unsupported_negative_claim",
            "align_with_schema_policy",
            "remove_authority_request",
            "restore_prompt_contract_boundary",
            "raw repository source",
            "provider logs",
            "first-pass prompt transcripts",
            "chain-of-thought",
            "candidatePatchProposal",
            "operations",
            "retryDirective",
            "rawUnifiedDiff",
            "shellCommand",
            "networkFetch",
            "providerCall",
            "packageManagerCommand",
            "testRunnerCommand",
            "buildToolCommand",
            "direct file writes",
            "SpecPM validation",
            "human review",
        ):
            assert required in text

    assert "SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeRefinementRetryOrchestration>" in root_page.read_text(encoding="utf-8")

    for path in (
        integration_doc,
        integration_docc,
        semantic_doc,
        semantic_docc,
        architecture_doc,
        architecture_docc,
        workflow_doc,
        workflow_docc,
    ):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeRefinementRetryOrchestration" in text
            or "SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md" in text
        )

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeRefinementRetryRun" in text
        assert "SpecNodeRetryDirective" in text
        assert "sourceBundleDigest" in text
        assert "sourcePreviewPlanDigest" in text
        assert "maxAttempts" in text


def test_docc_and_github_docs_cover_specnode_provider_adapter_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderAdapterContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    refine_doc = ROOT / "docs" / "SPECNODE_REFINE_PREVIEW_CONTRACT.md"
    refine_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinePreviewContract.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecNodeOpenAICompatibleProviderAdapter",
            "SpecNodeProviderDiscoveryResult",
            "SpecNodeProviderHealth",
            "SpecNodeModelListing",
            "SpecNodeGenerationPolicy",
            "SpecNodeProviderUsageReceipt",
            "OpenAI-compatible",
            "LM Studio",
            "lm_studio",
            "http://127.0.0.1:1234",
            "http://localhost:1234",
            "baseUrl",
            "defaultHeaders",
            "authPolicy",
            "endpointAllowlist",
            "/v1/models",
            "/v1/chat/completions",
            "Endpoint joining rule",
            "localhost_only",
            "allowRemoteEndpoints",
            "modelNetworkAccess: provider_only",
            "toolNetworkAccess: none",
            "timeoutPolicy",
            "retryPolicy",
            "maxBackoffSeconds",
            "temperature",
            "maxOutputTokens",
            "promptBudget",
            "maxPromptTokens",
            "maxPromptBytes",
            "inputTokens",
            "outputTokens",
            "totalTokens",
            "responseSha256",
            "redactionPolicy",
            "allowedTools: []",
            "modelFilesystemAccess: none",
            "modelShellAccess: none",
            "rawSourceAccess: none",
            "secretAccess: none",
            "candidateMutation: proposal_only",
            "SpecHarvesterRefinePreviewPlan",
            "usageReceipt",
            "SpecHarvester does not contact providers",
            "explicit operator opt-in",
            "openai/gpt-oss-20b",
            "response_format.type: json_schema",
            "SpecNodeRefinementResult",
            "response_format.type: json_object",
            "json_object",
            "<|message|>",
            "multiple objects",
            "raw repository source",
            "provider logs",
        ):
            assert required in text

    assert "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeProviderAdapterContract>" in root_page.read_text(encoding="utf-8")

    for path in (integration_doc, integration_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeOpenAICompatibleProviderAdapter" in text
        assert "SpecNodeProviderUsageReceipt" in text
        assert "timeoutPolicy" in text
        assert "retryPolicy" in text
        assert "SpecHarvester" in text

    for path in (refine_doc, refine_docc, architecture_doc, architecture_docc):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeProviderAdapterContract" in text
            or "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md" in text
        )
        assert "SpecNodeOpenAICompatibleProviderAdapter" in text

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeProviderAdapterContract" in text
            or "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md" in text
        )
        assert "SpecNodeOpenAICompatibleProviderAdapter" in text
        assert "/v1/models" in text
        assert "/v1/chat/completions" in text
        assert "SpecHarvester does not contact providers" in text


def test_docc_and_github_docs_cover_specnode_patch_proposal_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_PATCH_PROPOSAL_CONTRACT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodePatchProposalContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    refine_doc = ROOT / "docs" / "SPECNODE_REFINE_PREVIEW_CONTRACT.md"
    refine_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinePreviewContract.md"
    )
    provider_doc = ROOT / "docs" / "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md"
    provider_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderAdapterContract.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecNodeCandidatePatchProposal",
            "candidatePatchProposal",
            "SpecNodeCandidatePatchOperation",
            "SpecNodeProposalProvenance",
            "SpecNodeProposalUsageReceipt",
            "SpecNodeProviderUsageReceipt",
            "SpecNodeRejectionReason",
            "reviewNotes",
            "usageReceipt",
            "SpecNodeRefinementResult",
            "SpecNodeRefinementJob",
            "baseCandidateDigest",
            "sourceJobDigest",
            "sourcePreviewPlanDigest",
            "sourceArtifactDigests",
            "providerReceiptDigest",
            "policyDigest",
            "promptBudget",
            "redactionPolicy",
            "inputTokens",
            "outputTokens",
            "totalTokens",
            "responseSha256",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "expectedCurrentValueSha256",
            "targetPointer",
            "evidenceRefs",
            "add_field",
            "replace_field",
            "remove_field",
            "append_unique",
            "replace_list_item_by_id",
            "remove_list_item_by_id",
            "rawUnifiedDiff",
            "fullFileReplacement",
            "shellCommand",
            "gitCommand",
            "networkFetch",
            "providerCall",
            "packageManagerCommand",
            "testRunnerCommand",
            "buildToolCommand",
            "direct file writes",
            "raw repository source",
            "provider logs",
            "insufficient_evidence",
            "prompt_budget_exceeded",
            "provider_unavailable",
            "model_output_invalid",
            "policy_violation",
            "unsupported_candidate_shape",
            "schema_validation_failed",
            "safety_boundary_triggered",
            "SpecPM validation",
        ):
            assert required in text

    assert "SPECNODE_PATCH_PROPOSAL_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodePatchProposalContract>" in root_page.read_text(encoding="utf-8")

    for path in (integration_doc, integration_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeCandidatePatchProposal" in text
        assert "SpecNodeProposalUsageReceipt" in text
        assert "SpecNodeRejectionReason" in text
        assert "validation-before-apply" in text

    for path in (refine_doc, refine_docc, provider_doc, provider_docc):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodePatchProposalContract" in text or "SPECNODE_PATCH_PROPOSAL_CONTRACT.md" in text
        )

    for path in (architecture_doc, architecture_docc, workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeCandidatePatchProposal" in text
        assert "SpecNodeRejectionReason" in text
        assert "direct file writes" in text


def test_docc_and_github_docs_cover_specnode_provider_smoke_coverage() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_PROVIDER_SMOKE_COVERAGE.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderSmokeCoverage.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    refine_doc = ROOT / "docs" / "SPECNODE_REFINE_PREVIEW_CONTRACT.md"
    refine_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinePreviewContract.md"
    )
    provider_doc = ROOT / "docs" / "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md"
    provider_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderAdapterContract.md"
    )
    patch_doc = ROOT / "docs" / "SPECNODE_PATCH_PROPOSAL_CONTRACT.md"
    patch_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodePatchProposalContract.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecNodeProviderSmokeRun",
            "SpecNode-compatible provider",
            "SpecHarvesterSpecNodeArtifactBundle",
            "SpecHarvesterRefinePreviewPlan",
            "SpecNodeRefinementJob",
            "SpecNodeRefinementResult",
            "SpecNodeCandidatePatchProposal",
            "SpecNodeRejectionReason",
            "provider_unavailable",
            "compactModelInput",
            "weak-model",
            "rawRepositorySource: excluded",
            "documentationBodies: excluded",
            "dependencyDirectories: excluded",
            "providerLogs: excluded",
            "secrets: excluded",
            "arbitraryPrompts: excluded",
            "usageReceipt",
            "SpecNodeProviderUsageReceipt",
            "requiresSchemaValidation: true",
            "requiresHumanReview: true",
            "requiresSpecPMValidationAfterApply: true",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "rawUnifiedDiff",
            "fullFileReplacement",
            "shellCommand",
            "gitCommand",
            "networkFetch",
            "providerCall",
            "packageManagerCommand",
            "testRunnerCommand",
            "buildToolCommand",
            "direct file writes",
            "does not call LM Studio",
            "does not mutate candidate files",
            "manual live smoke",
            "scripts/specnode_live_retry_smoke.py",
            "SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE",
            "SPECHARVESTER_LM_STUDIO_BASE_URL",
            "SPECHARVESTER_SPECNODE_MODEL",
            "localhost",
            "127.0.0.1",
            "::1",
            "run_specnode_refinement_retry_orchestration",
            "SpecNodeRetryDirectiveSet",
            "SpecNodeRetryContext",
            "retry context",
            "token usage",
            "openai/gpt-oss-20b",
            "response_format.type: json_schema",
            "response_format.type: json_object",
            "parse_specnode_model_json_object",
            "<|message|>",
            "multiple object payloads",
            "trailing non-JSON text",
        ):
            assert required in text

    assert "SPECNODE_PROVIDER_SMOKE_COVERAGE.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeProviderSmokeCoverage>" in root_page.read_text(encoding="utf-8")

    for path in (
        integration_doc,
        integration_docc,
        refine_doc,
        refine_docc,
        provider_doc,
        provider_docc,
        patch_doc,
        patch_docc,
        architecture_doc,
        architecture_docc,
        workflow_doc,
        workflow_docc,
    ):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeProviderSmokeCoverage" in text or "SPECNODE_PROVIDER_SMOKE_COVERAGE.md" in text
        )

    for path in (architecture_doc, architecture_docc, workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeProviderSmokeRun" in text
        assert "SpecNodeRefinementResult" in text
        assert "provider_unavailable" in text


def test_docc_and_github_docs_cover_accepted_candidate_impact_classification() -> None:
    github_doc = ROOT / "docs" / "ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_REPORTS.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AcceptedCandidateImpactClassificationReports.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "accepted-candidate-impact-classification-report",
            "metadata",
            "interface",
            "license",
            "provenance",
            "capability",
            "intent",
        ):
            assert required in text

    assert "<doc:AcceptedCandidateImpactClassificationReports>" in root_page.read_text(
        encoding="utf-8"
    )
    assert "ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_REPORTS.md" in docs_index.read_text(
        encoding="utf-8"
    )


def test_docc_and_github_docs_cover_license_provenance_issue_classes() -> None:
    github_doc = ROOT / "docs" / "LICENSE_PROVENANCE_RISK_REPORTS.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LicenseProvenanceRiskReports.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterLicenseProvenanceRiskReport",
            "absent_license_evidence",
            "ambiguous_unknown_license",
            "collected_unknown_license_evidence",
            "LICENSE.txt",
            "COPYING.rst",
            "licenseEvidence",
            "governance-license-provenance-report",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "LICENSE_PROVENANCE_RISK_REPORTS.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:LicenseProvenanceRiskReports>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_code_duplication_reports() -> None:
    github_doc = ROOT / "docs" / "CODE_DUPLICATION_REPORTS.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "CodeDuplicationReports.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterCodeDuplicationReport",
            "code-duplication-report",
            "--backend pylint",
            "--backend jscpd",
            "jscpd-report.json",
            "MIT",
            "npm",
            "supply-chain",
            "R0801",
            "--fail-on-duplicates",
            "advisory",
            "No repository code execution",
            "No imports from scanned modules",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "CODE_DUPLICATION_REPORTS.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:CodeDuplicationReports>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_architecture_lint_guardrails() -> None:
    github_doc = ROOT / "docs" / "ARCHITECTURE_LINT_GUARDRAILS.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ArchitectureLintGuardrails.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterArchitectureLintReport",
            "architecture-lint",
            "--fail-on-issues",
            "Helper",
            "constructor",
            "static/class",
            "specpm.yaml",
            "No repository code execution",
            "No imports from scanned modules",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "ARCHITECTURE_LINT_GUARDRAILS.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:ArchitectureLintGuardrails>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_procedural_style_report() -> None:
    github_doc = ROOT / "docs" / "PROCEDURAL_STYLE_REPORT.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProceduralStyleReport.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterProceduralStyleReport",
            "procedural-style-report",
            "--fail-on-hotspots",
            "topLevelFunctionSpan",
            "behaviorRichClassCount",
            "dtoOnlyClassCount",
            "largestTopLevelFunctions",
            "advisory",
            "No repository code execution",
            "No imports from scanned modules",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "PROCEDURAL_STYLE_REPORT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:ProceduralStyleReport>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_eo_refactoring_strategy() -> None:
    github_doc = ROOT / "docs" / "EO_REFACTORING_STRATEGY.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "EORefactoringStrategy.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "behavior-rich objects",
            "ELEGANT_OBJECTS_STYLE.md",
            "AGENTS.md",
            "top-level function",
            "DTO-only dataclasses",
            "characterization tests",
            "SpecNode",
            "Stop Conditions",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "EO_REFACTORING_STRATEGY.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:EORefactoringStrategy>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_accepted_package_update_proposals() -> None:
    github_doc = ROOT / "docs" / "ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AcceptedPackageUpdateProposals.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    workflow_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "accepted-package-update-proposal",
            "sourceRevision",
            "evidenceDigests",
            "producerEvidenceLinks",
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "oldPackageVersion",
            "newPackageVersion",
            "changedClaims",
            "validationStatus",
            "reviewerNotes",
            "updateKind",
            "accepted source bundle",
            "accepted-source pull request diff",
            "registryAcceptanceDecision",
            "external_required",
            "SpecPMRegistryAcceptanceDecision",
        ):
            assert required in text

    assert "<doc:AcceptedPackageUpdateProposals>" in root_page.read_text(encoding="utf-8")
    assert "<doc:AcceptedPackageUpdateProposals>" in workflow_page.read_text(encoding="utf-8")
    assert "ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md" in docs_index.read_text(encoding="utf-8")


def test_specpm_proposal_automation_links_producer_bundle_evidence() -> None:
    workflow = (ROOT / ".github" / "workflows" / "propose-to-specpm.yml").read_text(
        encoding="utf-8"
    )
    github_doc = (ROOT / "docs" / "SPECPM_PROPOSAL_AUTOMATION.md").read_text(encoding="utf-8")
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProposalAutomation.md"
    ).read_text(encoding="utf-8")
    handoff_doc = (ROOT / "docs" / "SPECPM_HANDOFF.md").read_text(encoding="utf-8")
    docc_handoff = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    ).read_text(encoding="utf-8")
    workplan = (ROOT / "SPECS" / "Workplan.md").read_text(encoding="utf-8")
    next_task = (ROOT / "SPECS" / "INPROGRESS" / "next.md").read_text(encoding="utf-8")

    for required in (
        "Build producer evidence artifacts",
        "preflight-candidate-bundle",
        "producer-preflight-report.json",
        "render-spec-site",
        "Upload producer evidence artifacts",
        "actions/upload-artifact@v4",
        "Producer Bundle Evidence",
        "producer-receipt.json",
        "validation-report.json",
        "diagnostics.json",
        "Static viewer evidence",
        "Accepted-source diff",
        "producerEvidenceLinks",
        '"pathScope": "repo_relative"',
        '"pathScope": "workflow_artifact"',
        '"pathScope": "pull_request"',
        "registryAcceptanceDecision",
        '"status": "external_required"',
        '"producerReceiptAuthority": "evidence_only"',
    ):
        assert required in workflow

    for text in (github_doc, docc_doc, handoff_doc, docc_handoff):
        for required in (
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "producer preflight",
            "static viewer",
            "accepted-source diff",
            "review evidence",
            "registryAcceptanceDecision",
            "external_required",
        ):
            assert required in text

    assert "P23-T1" in workplan
    assert "P23-T2" in workplan
    assert "proposal artifacts and SpecPM pull" in workplan
    assert_current_next_task(next_task)


def test_specpm_proposal_automation_supports_package_set_dry_run_boundary() -> None:
    workflow = (ROOT / ".github" / "workflows" / "propose-to-specpm.yml").read_text(
        encoding="utf-8"
    )
    github_doc = (ROOT / "docs" / "SPECPM_PROPOSAL_AUTOMATION.md").read_text(encoding="utf-8")
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProposalAutomation.md"
    ).read_text(encoding="utf-8")

    for required in (
        "proposal_kind",
        "single_package",
        "package_set",
        "package_set_bundle_dir",
        "package_set_viewer_dir",
        'default: ""',
        "xyflow-package-set-smoke",
        "Build package-set handoff evidence artifacts",
        "package-set-handoff-proposal",
        "package-set-handoff-proposal.json",
        "package-set-handoff-proposal.md",
        "Upload package-set handoff evidence artifacts",
        "specpm-package-set-proposal-evidence",
        "package_set proposal mode is dry-run artifact generation only",
        "steps.config.outputs.proposal_kind == 'package_set'",
        "steps.config.outputs.proposal_kind == 'single_package'",
        "does not use \\`SPECPM_PROPOSAL_TOKEN\\`",
        "does not create a SpecPM PR",
    ):
        assert required in workflow

    for text in (" ".join(github_doc.split()), " ".join(docc_doc.split())):
        for required in (
            "proposal_kind: package_set",
            "package_set_bundle_dir",
            "package_set_viewer_dir",
            "xyflow-package-set-smoke",
            "committed or downloaded artifacts",
            "package-set-handoff-proposal.json",
            "package-set-handoff-proposal.md",
            "specpm-package-set-proposal-evidence",
            "create_pr=false",
            "SPECPM_PROPOSAL_TOKEN",
            "untrusted",
            "does not create a SpecPM PR",
            "review evidence only",
        ):
            assert required in text


def test_local_smoke_fixture_docs_cover_reproducible_controls() -> None:
    github_doc = ROOT / "docs" / "LOCAL_SMOKE_FIXTURES.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "LocalSmokeFixtures.md"
    docs_index = ROOT / "docs" / "README.md"
    root_readme = ROOT / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    gitignore = ROOT / ".gitignore"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            ".smoke/inputs",
            ".smoke/output",
            "Cupertino".lower(),
            "xyflow",
            "docc2context",
            "Puzzle".lower(),
            "collect-batch",
            "--relaxed-private",
            "batch-validation.json",
            "staged git changes",
            "missing_license_file",
            "multi-language smoke matrix",
            "synthetic",
            "npm",
            "SPM",
            "Gradle/Maven",
            "Go modules",
            "Composer",
            "CMake",
            "Xcode/CocoaPods",
            "RubyGems",
            "Python packaging",
            "documentation-first",
            "manifest-poor",
            "ProjectProfile",
            "semanticHints",
            "semantic_intent_static_evidence",
            "Flask",
            "Gin",
            "LICENSE.txt",
            "popular-smoke",
            "--emit-interface-indexes",
            "public-interface-index.json",
            "SpecPM validation",
            "preview_only_package",
            "unknown_evidence_kind",
            "evidence_support_target_unknown",
            "smoke-triage-summary",
            "governance-upstream-report",
            "governance-license-provenance-report",
            "generated smoke outputs",
            "Do not install harvested dependencies",
            "Do not run harvested package scripts",
            "Do not execute harvested repository code",
        ):
            assert required in text

    assert "LOCAL_SMOKE_FIXTURES.md" in docs_index.read_text(encoding="utf-8")
    assert "LOCAL_SMOKE_FIXTURES.md" in root_readme.read_text(encoding="utf-8")
    assert "<doc:LocalSmokeFixtures>" in docc_root.read_text(encoding="utf-8")

    ignored_paths = gitignore.read_text(encoding="utf-8")
    assert ".smoke/" in ignored_paths
    assert "smoke-inputs/" in ignored_paths
    assert "smoke-output*/" in ignored_paths


def test_real_repository_refinement_validation_docs_cover_boundaries() -> None:
    github_doc = ROOT / "docs" / "REAL_REPOSITORY_REFINEMENT_VALIDATION.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "RealRepositoryRefinementValidation.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvester-side",
            "external SpecNode contract boundary",
            "SpecNode runtime",
            "provider discovery",
            "model execution",
            "provider lifecycle",
            "packageId",
            "--relaxed-private",
            ".smoke/inputs",
            ".smoke/output",
            "source-manifests",
            "collect-batch",
            "--emit-interface-indexes",
            "draft",
            "smoke-triage-summary",
            "ProjectProfile",
            "PublicInterfaceIndex",
            "semanticEvidenceIndex",
            "SpecHarvesterSpecNodeArtifactBundle",
            "SpecHarvesterRefinePreviewPlan",
            "SpecNodeRefinementRetryRun",
            "SpecPM validation",
            "intent accuracy",
            "capability/evidence support",
            "token usage",
            "Platform",
            "workspace catalog",
            ".0al",
            "Do not install harvested dependencies",
            "Do not run harvested package scripts",
            "Do not execute harvested repository code",
            "Do not commit generated candidates",
        ):
            assert required in text

    assert "REAL_REPOSITORY_REFINEMENT_VALIDATION.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:RealRepositoryRefinementValidation>" in docc_root.read_text(encoding="utf-8")

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "RealRepositoryRefinementValidation" in text
        assert "SpecHarvester-side" in text
        assert "provider-specific orchestration" in text


def test_real_repository_quality_report_docs_cover_required_fields() -> None:
    github_doc = ROOT / "docs" / "REAL_REPOSITORY_QUALITY_REPORT.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "RealRepositoryQualityReport.md"
    )
    docs_index = ROOT / "docs" / "README.md"

    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "quality-report",
            "intentAccuracy",
            "capabilityEvidenceQuality",
            "specpmStatus",
            "retryOutcome",
            "tokenUsage",
            "analyzerCoverage",
            "public-interface-index.json",
            "SpecHarvesterPublicInterfaceIndex",
            "publicInterfaceIndex",
            "humanReviewNotes",
            "overallVerdict",
            "strong",
            "partial",
            "weak",
            "unscored",
            "passed",
            "failed",
            "not_run",
            "not_attempted",
            "improved",
            "pass",
            "review",
            "fail",
            "--run-report",
            "draft-summary.json",
            "candidateDir",
            "must not be committed",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "REAL_REPOSITORY_QUALITY_REPORT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:RealRepositoryQualityReport>" in docc_root.read_text(encoding="utf-8")


def test_real_repository_refinement_validation_runner_docs_cover_execution_entrypoint() -> None:
    github_doc = ROOT / "docs" / "REAL_REPOSITORY_REFINEMENT_VALIDATION_RUNNER.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "RealRepositoryRefinementValidationRunner.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "run_real_repository_validation.py",
            "degraded",
            "optional",
            "local-only",
            "run-report.json",
            "draft-summary.json",
            "quality-report",
        ):
            assert required in text

    assert "REAL_REPOSITORY_REFINEMENT_VALIDATION_RUNNER.md" in docs_index.read_text(
        encoding="utf-8"
    )
    assert "<doc:RealRepositoryRefinementValidationRunner>" in workflow_docc.read_text(
        encoding="utf-8"
    )
    assert "<doc:RealRepositoryRefinementValidationRunner>" in docc_root.read_text(encoding="utf-8")


def test_real_repository_local_validation_matrix_docs_cover_observed_results() -> None:
    github_doc = ROOT / "docs" / "REAL_REPOSITORY_LOCAL_VALIDATION_MATRIX.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "RealRepositoryLocalValidationMatrix.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "P16-T5",
            "Delta from P15-T4",
            "cupertino",
            "navigation-split-view",
            "xyflow",
            "flask",
            "gin",
            "docc2context",
            "attention_required",
            "duplicate intent",
            "LICENSE.txt",
            "collected_unknown_license_evidence",
            "navigation_split_view",
            "public-interface-index.json counted",
            "namespaceIssueCount=0",
            "5 total advisory issues",
            "SpecPM validation",
            ".smoke/",
            "No harvested package scripts",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "REAL_REPOSITORY_LOCAL_VALIDATION_MATRIX.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:RealRepositoryLocalValidationMatrix>" in docc_root.read_text(encoding="utf-8")
    assert "<doc:RealRepositoryLocalValidationMatrix>" in workflow_docc.read_text(encoding="utf-8")


def test_autonomous_candidate_batch_docs_cover_local_lm_studio_boundary() -> None:
    github_doc = ROOT / "docs" / "AUTONOMOUS_CANDIDATE_BATCH.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "AutonomousCandidateBatch.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "autonomous-candidate-batch",
            "SpecHarvesterAutonomousCandidateBatchReport",
            "LM Studio",
            "openai/gpt-oss-20b",
            "--skip-ai",
            "autonomous_popular_mvp",
            "preview_only",
            "does not clone repositories",
            "execute harvested code",
            "install dependencies",
            "SpecPM remains",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "AUTONOMOUS_CANDIDATE_BATCH.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:AutonomousCandidateBatch>" in docc_root.read_text(encoding="utf-8")
    assert "Autonomous Candidate Harvest MVP" in roadmap.read_text(encoding="utf-8")
    assert "Autonomous Candidate Harvest MVP" in roadmap_docc.read_text(encoding="utf-8")


def test_autonomous_candidate_intake_policy_docs_cover_specpm_review_boundary() -> None:
    github_doc = ROOT / "docs" / "AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AutonomousCandidateIntakePolicy.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    handoff = ROOT / "docs" / "SPECPM_HANDOFF.md"
    handoff_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    autonomous_batch = ROOT / "docs" / "AUTONOMOUS_CANDIDATE_BATCH.md"
    autonomous_batch_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "AutonomousCandidateBatch.md"
    )
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Autonomous Candidate Intake Policy",
            "SpecHarvesterAutonomousCandidateBatchReport",
            "SpecHarvesterPackageSetAIDraftProposal",
            "SpecHarvesterPackageSetAIEnrichmentProposal",
            "bundle-set-preflight.json",
            "authorReadyDraftSummary",
            "stopPolicySummary",
            "candidate_layer_review_required",
            "needs_regeneration",
            "blocked",
            "not_for_intake",
            "producer_preview_evidence_only",
            "provider receipts",
            "privacy flags",
            "candidate count",
            "relation count",
            "accept packages",
            "accept relations",
            "seed baselines",
            "remove `preview_only`",
            "publish registry metadata",
            "single_package_fallback_needed",
            "ai_json_repair_needed",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:AutonomousCandidateIntakePolicy>" in docc_root.read_text(encoding="utf-8")
    assert "AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md" in handoff.read_text(encoding="utf-8")
    assert "<doc:AutonomousCandidateIntakePolicy>" in handoff_docc.read_text(encoding="utf-8")
    assert "AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md" in autonomous_batch.read_text(encoding="utf-8")
    assert "<doc:AutonomousCandidateIntakePolicy>" in autonomous_batch_docc.read_text(
        encoding="utf-8"
    )
    assert "AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md" in roadmap.read_text(encoding="utf-8")
    assert "AutonomousCandidateIntakePolicy" in roadmap_docc.read_text(encoding="utf-8")


def test_autonomous_candidate_tech_debt_plan_docs_cover_corpus_followups() -> None:
    github_doc = ROOT / "docs" / "AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AutonomousCandidateTechDebtPlan.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Autonomous Candidate Technical Debt Plan",
            "flask",
            "gin",
            "xyflow",
            "single-package repositories",
            "single-package candidate fallback",
            "LM Studio JSON Repair and Retry",
            "malformed JSON",
            "P29-T3",
            "P29-T4",
            "P29-T5",
            "P29-T6",
            "preview_only",
            "producer-side preview evidence",
            "single_package_fallback_needed",
            "ai_json_repair_needed",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:AutonomousCandidateTechDebtPlan>" in docc_root.read_text(encoding="utf-8")
    assert "single-package candidate fallback" in roadmap.read_text(encoding="utf-8")
    assert "JSON repair/retry" in roadmap.read_text(encoding="utf-8")
    assert "AutonomousCandidateTechDebtPlan" in roadmap_docc.read_text(encoding="utf-8")

    workplan_text = workplan.read_text(encoding="utf-8")
    for task_id in ("P29-T3", "P29-T4", "P29-T5", "P29-T6"):
        assert f"`{task_id}`" in workplan_text
    assert "single-package repositories" in workplan_text
    assert "Local LM Studio JSON failures" in workplan_text

    assert_current_next_task(next_task.read_text(encoding="utf-8"))


def test_autonomous_candidate_corpus_baseline_fixture_records_gap_outcomes() -> None:
    fixture = (
        ROOT
        / "tests"
        / "fixtures"
        / "autonomous_candidate_corpus_baseline"
        / "flask-gin-xyflow.example.json"
    )
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    assert payload["apiVersion"] == "spec-harvester.autonomous-candidate-corpus-baseline/v0"
    assert payload["kind"] == "SpecHarvesterAutonomousCandidateCorpusBaseline"
    assert payload["schemaVersion"] == 1
    assert payload["authority"] == "producer_preview_evidence_only"
    assert payload["corpus"]["id"] == "local-flask-gin-xyflow"
    assert payload["corpus"]["repositories"] == ["flask", "gin", "xyflow"]
    assert payload["source"]["provider"] == "lm_studio"
    assert payload["source"]["model"] == "openai/gpt-oss-20b"
    assert payload["summary"] == {
        "deterministicPassedCount": 3,
        "deterministicFailedCount": 0,
        "liveLmStudioFailedCount": 1,
        "repositoryCount": 3,
    }

    by_id = {item["id"]: item for item in payload["repositoryResults"]}
    assert set(by_id) == {"flask", "gin", "xyflow"}

    for repo_id, package_id, revision in (
        ("flask", "flask.core", "954f5684e4841aad84a8eec7ace7b81a0d3f6831"),
        ("gin", "gin.core", "5f4f9643258dc2a65e684b63f12c8d543c936c67"),
    ):
        result = by_id[repo_id]
        assert result["packageId"] == package_id
        assert result["revision"] == revision
        assert result["deterministic"] == {
            "status": "passed",
            "candidateCount": 0,
            "relationCount": 0,
            "preflight": "passed",
        }
        assert result["authorReadyDecision"] == "blocked_until_inputs_change"
        assert result["gapCodes"] == ["single_package_fallback_needed"]
        assert result["liveLmStudio"]["status"] == "needs_regeneration"
        assert result["liveLmStudio"]["aiDraft"] == "completed"
        assert result["liveLmStudio"]["aiEnrichment"] == "completed"
        assert result["liveLmStudio"]["proposalSubjectCount"] == 0

    xyflow = by_id["xyflow"]
    assert xyflow["packageId"] == "xyflow.workspace"
    assert xyflow["revision"] == "a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd"
    assert xyflow["deterministic"] == {
        "status": "passed",
        "candidateCount": 4,
        "relationCount": 3,
        "preflight": "passed",
    }
    assert xyflow["authorReadyDecision"] == "stop_for_author_review"
    assert xyflow["gapCodes"] == ["ai_json_repair_needed"]
    assert xyflow["liveLmStudio"]["status"] == "needs_regeneration"
    assert xyflow["liveLmStudio"]["aiDraft"] == "failed"
    assert xyflow["liveLmStudio"]["aiEnrichment"] == "not_run_after_ai_draft_failure"
    assert xyflow["liveLmStudio"]["proposalSubjectCount"] == 4
    assert xyflow["liveLmStudio"]["diagnostics"][0]["code"] == "model_output_invalid_json"

    non_authority = " ".join(payload["nonAuthority"])
    assert "review evidence only" in non_authority
    assert "not SpecPM registry acceptance" in non_authority
    assert "does not publish packages or relations" in non_authority
    assert "does not remove preview_only" in non_authority
    assert payload["productVerdict"]["pipelineHealth"] == "deterministic_pipeline_passed"
    assert payload["productVerdict"]["candidateQuality"] == "needs_follow_up"


def test_autonomous_candidate_corpus_baseline_docs_cover_mixed_corpus_verdict() -> None:
    github_doc = ROOT / "docs" / "AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AutonomousCandidateCorpusBaseline.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    intake = ROOT / "docs" / "AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md"
    intake_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AutonomousCandidateIntakePolicy.md"
    )
    tech_debt = ROOT / "docs" / "AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md"
    tech_debt_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AutonomousCandidateTechDebtPlan.md"
    )

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Autonomous Candidate Corpus Baseline",
            "SpecHarvesterAutonomousCandidateCorpusBaseline",
            "local-flask-gin-xyflow",
            "flask.core",
            "gin.core",
            "xyflow.workspace",
            "954f5684e4841aad84a8eec7ace7b81a0d3f6831",
            "5f4f9643258dc2a65e684b63f12c8d543c936c67",
            "a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd",
            "single_package_fallback_needed",
            "ai_json_repair_needed",
            "blocked_until_inputs_change",
            "stop_for_author_review",
            "model_output_invalid_json",
            "deterministic_pipeline_passed",
            "needs_follow_up",
            "producer_preview_evidence_only",
            "preview_only",
            "no generated preview candidate is promoted to SpecPM acceptance",
            "P29-T4",
            "P29-T5",
            "P29-T6",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:AutonomousCandidateCorpusBaseline>" in docc_root.read_text(encoding="utf-8")
    assert "AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md" in roadmap.read_text(encoding="utf-8")
    assert "AutonomousCandidateCorpusBaseline" in roadmap_docc.read_text(encoding="utf-8")
    assert "AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md" in intake.read_text(encoding="utf-8")
    assert "AutonomousCandidateCorpusBaseline" in intake_docc.read_text(encoding="utf-8")
    assert "AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md" in tech_debt.read_text(encoding="utf-8")
    assert "AutonomousCandidateCorpusBaseline" in tech_debt_docc.read_text(encoding="utf-8")


def test_autonomous_candidate_corpus_quality_gate_fixture_records_post_mitigation_outcome() -> None:
    fixture = (
        ROOT
        / "tests"
        / "fixtures"
        / "autonomous_candidate_corpus_quality_gate"
        / "flask-gin-xyflow-post-fallbacks.example.json"
    )
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    assert payload["apiVersion"] == "spec-harvester.autonomous-candidate-corpus-quality-gate/v0"
    assert payload["kind"] == "SpecHarvesterAutonomousCandidateCorpusQualityGate"
    assert payload["schemaVersion"] == 1
    assert payload["authority"] == "producer_preview_evidence_only"
    assert payload["corpus"]["id"] == "local-flask-gin-xyflow-post-fallbacks"
    assert payload["corpus"]["repositories"] == ["flask", "gin", "xyflow"]
    assert payload["source"]["provider"] == "lm_studio"
    assert payload["source"]["model"] == "openai/gpt-oss-20b"
    assert payload["source"]["jsonRepairMaxAttempts"] == 1
    assert payload["source"]["deterministicReportDigest"].startswith("sha256:")
    assert payload["source"]["liveLmStudioReportDigest"].startswith("sha256:")
    assert payload["summary"] == {
        "deterministicPassedCount": 3,
        "deterministicReviewableCandidateRepositoryCount": 3,
        "jsonRepairExhaustedCount": 0,
        "jsonRepairNeededCount": 0,
        "liveLmStudioFailedCount": 0,
        "liveLmStudioPassedCount": 3,
        "repositoryCount": 3,
    }

    by_id = {item["id"]: item for item in payload["repositoryResults"]}
    assert set(by_id) == {"flask", "gin", "xyflow"}

    expected = {
        "flask": ("flask.core", ["flask.core"], 1, 0, ["excluded_package_unknown"]),
        "gin": ("gin.core", ["gin.core"], 1, 0, ["excluded_package_unknown"]),
        "xyflow": (
            "xyflow.workspace",
            ["xyflow.react", "xyflow.svelte", "xyflow.system", "xyflow.workspace"],
            4,
            3,
            ["package_set_id_missing"],
        ),
    }
    for repo_id, (
        package_id,
        candidate_ids,
        candidate_count,
        relation_count,
        draft_codes,
    ) in expected.items():
        result = by_id[repo_id]
        assert result["packageId"] == package_id
        assert result["deterministic"]["candidateIds"] == candidate_ids
        assert result["deterministic"]["candidateCount"] == candidate_count
        assert result["deterministic"]["relationCount"] == relation_count
        assert result["deterministic"]["preflight"] == "passed"
        assert result["deterministic"]["reviewablePreviewCandidate"] is True
        assert result["deterministic"]["authorReadyDecision"] == "stop_for_author_review"
        assert result["liveLmStudio"]["status"] == "passed"
        assert result["liveLmStudio"]["aiDraft"] == "warning"
        assert result["liveLmStudio"]["aiDraftDiagnosticCodes"] == draft_codes
        assert result["liveLmStudio"]["aiDraftJsonRepair"]["status"] == "not_needed"
        assert result["liveLmStudio"]["aiEnrichment"] == "completed"
        assert result["liveLmStudio"]["aiEnrichmentDiagnosticCodes"] == []
        assert result["liveLmStudio"]["aiEnrichmentJsonRepair"]["status"] == "not_needed"
        assert result["qualityGate"]["status"] == "passed"
        assert result["qualityGate"]["blockingGapCodes"] == []

    non_authority = " ".join(payload["nonAuthority"])
    assert "review evidence only" in non_authority
    assert "not SpecPM registry acceptance" in non_authority
    assert "does not accept packages or relations" in non_authority
    assert "does not remove preview_only" in non_authority
    assert payload["productVerdict"]["status"] == "ready_for_limited_popular_library_scraping"
    assert payload["productVerdict"]["pipelineHealth"] == "deterministic_and_live_lm_studio_passed"
    assert (
        payload["productVerdict"]["candidateQuality"]
        == "valid_starter_packages_require_author_review"
    )


def test_autonomous_candidate_corpus_quality_gate_docs_cover_readiness_verdict() -> None:
    github_doc = ROOT / "docs" / "AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AutonomousCandidateCorpusQualityGate.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    tech_debt = ROOT / "docs" / "AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md"
    tech_debt_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AutonomousCandidateTechDebtPlan.md"
    )

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Autonomous Candidate Corpus Quality Gate",
            "SpecHarvesterAutonomousCandidateCorpusQualityGate",
            "local-flask-gin-xyflow-post-fallbacks",
            "flask.core",
            "gin.core",
            "xyflow.workspace",
            "954f5684e4841aad84a8eec7ace7b81a0d3f6831",
            "5f4f9643258dc2a65e684b63f12c8d543c936c67",
            "a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd",
            "stop_for_author_review",
            "openai/gpt-oss-20b",
            "jsonRepairMaxAttempts",
            "excluded_package_unknown",
            "package_set_id_missing",
            "ready_for_limited_popular_library_scraping",
            "producer_preview_evidence_only",
            "preview_only",
            "not automatic SpecPM acceptance"
            if path == github_doc
            else "producer preview evidence",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:AutonomousCandidateCorpusQualityGate>" in docc_root.read_text(encoding="utf-8")
    assert "AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md" in roadmap.read_text(encoding="utf-8")
    assert "AutonomousCandidateCorpusQualityGate" in roadmap_docc.read_text(encoding="utf-8")
    assert "AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md" in tech_debt.read_text(encoding="utf-8")
    assert "AutonomousCandidateCorpusQualityGate" in tech_debt_docc.read_text(encoding="utf-8")


def test_limited_popular_library_corpus_plan_docs_and_manifest_are_aligned() -> None:
    github_doc = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryCorpusPlan.md"
    )
    manifest = ROOT / "inputs" / "limited-popular-libraries" / "repositories.yml"
    generic_manifest = ROOT / "inputs" / "repositories.example.yml"
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Limited Popular-Library Corpus Plan",
            "ready_for_limited_popular_library_scraping",
            "inputs/limited-popular-libraries/repositories.yml",
            "operator-provided local public checkouts",
            "producer_preview_evidence_only",
            "preview_only",
            "accepted SpecPM truth",
            "flask.core",
            "gin.core",
            "xyflow.workspace",
            "cupertino.core",
            "navigation-split-view.core",
            "docc2context.core",
            "candidate_layer_review_required",
            "needs_regeneration",
            "blocked",
            "not_for_intake",
            "json-repair-max-attempts 1",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    records = read_repository_source_manifests(ROOT / "inputs", include_disabled=True)
    by_path = {}
    for record in records:
        by_path.setdefault(record["sourceManifest"]["path"], []).append(record)

    limited_records = read_repository_source_manifests(
        ROOT / "inputs" / "limited-popular-libraries",
        include_disabled=True,
    )
    limited = limited_records
    assert [record["id"] for record in limited] == [
        "flask",
        "gin",
        "xyflow",
        "cupertino",
        "navigation-split-view",
        "docc2context",
    ]
    assert {record["packageId"] for record in limited} == {
        "flask.core",
        "gin.core",
        "xyflow.workspace",
        "cupertino.core",
        "navigation-split-view.core",
        "docc2context.core",
    }
    assert all(record["revision"] for record in limited)
    assert all(record["checkout"] for record in limited)
    assert all("seed_corpus" in record["labels"] for record in limited)
    assert by_path["repositories.example.yml"][0]["id"] == "xyflow-example"
    assert generic_manifest.read_text(encoding="utf-8").startswith("# Minimal source list")
    assert manifest.read_text(encoding="utf-8").startswith(
        "# P30-T1 limited popular-library seed corpus."
    )

    assert "LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:LimitedPopularLibraryCorpusPlan>" in docc_root.read_text(encoding="utf-8")
    assert "Milestone 10: Limited Popular-Library Scraping Batch" in roadmap.read_text(
        encoding="utf-8"
    )
    assert "LimitedPopularLibraryCorpusPlan" in roadmap_docc.read_text(encoding="utf-8")
    workplan_text = workplan.read_text(encoding="utf-8")
    assert "Phase 30. Limited Popular-Library Scraping Batch" in workplan_text
    for task_id in ("P30-T1", "P30-T2", "P30-T3", "P30-T4", "P30-T5"):
        assert f"`{task_id}`" in workplan_text
    assert "- [x] `P30-T1`" in workplan_text
    assert_current_next_task(next_task.read_text(encoding="utf-8"))


def test_limited_popular_library_deterministic_batch_fixture_records_p30_t2_outcome() -> None:
    fixture = (
        ROOT
        / "tests"
        / "fixtures"
        / "limited_popular_library_deterministic_batch"
        / "p30-t2-limited-popular-libraries.example.json"
    )
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    assert payload["apiVersion"] == (
        "spec-harvester.limited-popular-library-deterministic-batch/v0"
    )
    assert payload["kind"] == "SpecHarvesterLimitedPopularLibraryDeterministicBatch"
    assert payload["schemaVersion"] == 1
    assert payload["authority"] == "producer_preview_evidence_only"
    assert payload["corpus"]["id"] == "p30-limited-popular-libraries"
    assert payload["corpus"]["manifestPath"] == "inputs/limited-popular-libraries/repositories.yml"
    assert payload["corpus"]["repositories"] == [
        "flask",
        "gin",
        "xyflow",
        "cupertino",
        "navigation-split-view",
        "docc2context",
    ]
    assert payload["source"]["mode"] == "skip_ai"
    assert payload["source"]["batchReportDigest"].startswith("sha256:")
    assert payload["source"]["batchValidationReportDigest"].startswith("sha256:")
    assert payload["summary"] == {
        "aiDraftSkippedCount": 6,
        "aiEnrichmentSkippedCount": 6,
        "candidateCount": 9,
        "collectedCount": 6,
        "failedRepositoryCount": 0,
        "passedPreflightCount": 6,
        "processedCount": 6,
        "relationCount": 3,
        "repositoryCount": 6,
        "reviewFindingCount": 1,
        "skippedPackageCount": 7,
    }

    by_id = {item["id"]: item for item in payload["repositoryResults"]}
    assert set(by_id) == {
        "flask",
        "gin",
        "xyflow",
        "cupertino",
        "navigation-split-view",
        "docc2context",
    }

    expected = {
        "flask": ("flask.core", ["flask.core"], 1, 0, 0, "complete"),
        "gin": ("gin.core", ["gin.core"], 1, 0, 0, "complete"),
        "xyflow": (
            "xyflow.workspace",
            ["xyflow.react", "xyflow.svelte", "xyflow.system", "xyflow.workspace"],
            4,
            3,
            7,
            "partial",
        ),
        "cupertino": ("cupertino.core", ["cupertino.core"], 1, 0, 0, "complete"),
        "navigation-split-view": (
            "navigation-split-view.core",
            ["navigation_split_view.core"],
            1,
            0,
            0,
            "complete",
        ),
        "docc2context": ("docc2context.core", ["docc2context.core"], 1, 0, 0, "complete"),
    }
    for repo_id, (
        manifest_package_id,
        candidate_ids,
        candidate_count,
        relation_count,
        skipped_count,
        interface_status,
    ) in expected.items():
        result = by_id[repo_id]
        assert result["status"] == "passed"
        assert result["collectionStatus"] == "collected"
        assert result["manifestPackageId"] == manifest_package_id
        assert result["candidateIds"] == candidate_ids
        assert result["packageSetDraftStatus"] == "ok"
        assert result["preflight"]["status"] == "passed"
        assert result["preflight"]["candidateCount"] == candidate_count
        assert result["preflight"]["relationCount"] == relation_count
        assert result["preflight"]["errorCount"] == 0
        assert result["preflight"]["warningCount"] == 0
        assert result["skippedPackageCount"] == skipped_count
        assert result["authorReadyStatus"] == "author_ready_draft"
        assert result["authorReadyDecision"] == "stop_for_author_review"
        assert result["aiDraft"] == "skipped"
        assert result["aiEnrichment"] == "skipped"
        assert result["interfaceIndex"]["status"] == interface_status

    navigation = by_id["navigation-split-view"]
    assert navigation["candidateLayerFindings"] == [
        {
            "id": "package_id_hint_mismatch",
            "severity": "review",
            "summary": (
                "The manifest packageId hint uses navigation-split-view.core, while "
                "deterministic drafting normalized the generated candidate id to "
                "navigation_split_view.core."
            ),
        }
    ]

    non_authority = " ".join(payload["nonAuthority"])
    assert "review evidence only" in non_authority
    assert "did not execute AI draft or enrichment providers" in non_authority
    assert "not SpecPM registry acceptance" in non_authority
    assert "does not accept packages" in non_authority
    assert "does not accept relations" in non_authority
    assert "does not seed baselines" in non_authority
    assert "does not remove preview_only" in non_authority
    assert "does not publish registry metadata" in non_authority
    assert payload["productVerdict"]["status"] == "ready_for_live_lm_studio_limited_corpus"
    assert payload["productVerdict"]["pipelineHealth"] == "deterministic_pipeline_passed"
    assert (
        payload["productVerdict"]["candidateQuality"]
        == "valid_starter_packages_require_author_review"
    )


def test_limited_popular_library_deterministic_batch_docs_cover_p30_t2_verdict() -> None:
    github_doc = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryDeterministicBatch.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    corpus_plan = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md"
    corpus_plan_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryCorpusPlan.md"
    )

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Limited Popular-Library Deterministic Batch",
            "SpecHarvesterLimitedPopularLibraryDeterministicBatch",
            "spec-harvester.limited-popular-library-deterministic-batch/v0",
            "producer_preview_evidence_only",
            "inputs/limited-popular-libraries/repositories.yml",
            "flask.core",
            "gin.core",
            "xyflow.workspace",
            "cupertino.core",
            "navigation-split-view.core",
            "navigation_split_view.core",
            "docc2context.core",
            "9",
            "3",
            "stop_for_author_review",
            "package_id_hint_mismatch",
            "ready_for_live_lm_studio_limited_corpus",
            "skip-ai",
            "not a SpecPM intake decision",
            "remove `preview_only`" if path == github_doc else "preview_only",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md" in docs_index.read_text(
        encoding="utf-8"
    )
    assert "<doc:LimitedPopularLibraryDeterministicBatch>" in docc_root.read_text(encoding="utf-8")
    assert "LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md" in roadmap.read_text(encoding="utf-8")
    assert "LimitedPopularLibraryDeterministicBatch" in roadmap_docc.read_text(encoding="utf-8")
    assert "LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md" in corpus_plan.read_text(
        encoding="utf-8"
    )
    assert "LimitedPopularLibraryDeterministicBatch" in corpus_plan_docc.read_text(encoding="utf-8")


def test_limited_popular_library_live_lm_studio_batch_fixture_records_p30_t3_outcome() -> None:
    fixture = (
        ROOT
        / "tests"
        / "fixtures"
        / "limited_popular_library_live_lm_studio_batch"
        / "p30-t3-limited-popular-libraries.example.json"
    )
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    assert payload["apiVersion"] == "spec-harvester.limited-popular-library-live-lm-studio-batch/v0"
    assert payload["kind"] == "SpecHarvesterLimitedPopularLibraryLiveLMStudioBatch"
    assert payload["schemaVersion"] == 1
    assert payload["authority"] == "producer_preview_evidence_only"
    assert payload["corpus"]["id"] == "p30-limited-popular-libraries"
    assert payload["corpus"]["manifestPath"] == "inputs/limited-popular-libraries/repositories.yml"
    assert payload["corpus"]["repositories"] == [
        "flask",
        "gin",
        "xyflow",
        "cupertino",
        "navigation-split-view",
        "docc2context",
    ]
    assert payload["deterministicBaseline"] == {
        "apiVersion": "spec-harvester.limited-popular-library-deterministic-batch/v0",
        "fixturePath": (
            "tests/fixtures/limited_popular_library_deterministic_batch/"
            "p30-t2-limited-popular-libraries.example.json"
        ),
        "status": "ready_for_live_lm_studio_limited_corpus",
        "summary": {
            "candidateCount": 9,
            "passedPreflightCount": 6,
            "relationCount": 3,
            "repositoryCount": 6,
        },
    }
    assert payload["provider"] == {
        "baseUrl": "http://127.0.0.1:1234",
        "chainOfThoughtPersisted": False,
        "jsonRepairMaxAttempts": 1,
        "model": "openai/gpt-oss-20b",
        "name": "lm_studio",
        "rawPromptPersisted": False,
        "rawResponsePersisted": False,
    }
    assert payload["source"]["mode"] == "local_lm_studio"
    assert payload["source"]["runRoot"] == "/tmp/specharvester-p30-t3.f7iGn0/live-lm-studio"
    assert payload["source"]["batchReportDigest"].startswith("sha256:")
    assert payload["source"]["batchValidationReportDigest"].startswith("sha256:")
    assert payload["summary"] == {
        "aiDraftCompletedCount": 2,
        "aiDraftProposalCount": 6,
        "aiDraftWarningCount": 4,
        "aiEnrichmentCompletedCount": 5,
        "aiEnrichmentProposalCount": 6,
        "aiEnrichmentWarningCount": 1,
        "candidateCount": 9,
        "collectedCount": 6,
        "failedRepositoryCount": 0,
        "jsonRepairExhaustedCount": 0,
        "jsonRepairNeededCount": 0,
        "passedPreflightCount": 6,
        "processedCount": 6,
        "providerDraftTotalTokens": 28316,
        "providerEnrichmentTotalTokens": 110384,
        "providerTotalTokens": 138700,
        "relationCount": 3,
        "repositoryCount": 6,
    }

    by_id = {item["id"]: item for item in payload["repositoryResults"]}
    assert set(by_id) == {
        "flask",
        "gin",
        "xyflow",
        "cupertino",
        "navigation-split-view",
        "docc2context",
    }

    expected = {
        "flask": (
            "flask.core",
            ["flask.core"],
            1,
            0,
            "warning",
            ["excluded_package_unknown"],
            2024,
            "completed",
            [],
            1,
            8308,
        ),
        "gin": (
            "gin.core",
            ["gin.core"],
            1,
            0,
            "warning",
            ["excluded_package_unknown"],
            5831,
            "completed",
            [],
            1,
            15656,
        ),
        "xyflow": (
            "xyflow.workspace",
            ["xyflow.react", "xyflow.svelte", "xyflow.system", "xyflow.workspace"],
            4,
            3,
            "warning",
            ["package_set_id_missing"],
            6199,
            "completed",
            [],
            4,
            48341,
        ),
        "cupertino": (
            "cupertino.core",
            ["cupertino.core"],
            1,
            0,
            "completed",
            [],
            5479,
            "warning",
            ["refined_summary_missing"],
            1,
            14836,
        ),
        "navigation-split-view": (
            "navigation-split-view.core",
            ["navigation_split_view.core"],
            1,
            0,
            "warning",
            ["package_set_id_missing"],
            4400,
            "completed",
            [],
            1,
            11634,
        ),
        "docc2context": (
            "docc2context.core",
            ["docc2context.core"],
            1,
            0,
            "completed",
            [],
            4383,
            "completed",
            [],
            1,
            11609,
        ),
    }
    for repo_id, (
        manifest_package_id,
        candidate_ids,
        candidate_count,
        relation_count,
        draft_status,
        draft_codes,
        draft_tokens,
        enrichment_status,
        enrichment_codes,
        enrichment_proposals,
        enrichment_tokens,
    ) in expected.items():
        result = by_id[repo_id]
        assert result["status"] == "passed"
        assert result["manifestPackageId"] == manifest_package_id
        assert result["candidateIds"] == candidate_ids
        assert result["preflight"] == {
            "candidateCount": candidate_count,
            "errorCount": 0,
            "relationCount": relation_count,
            "status": "passed",
            "warningCount": 0,
        }
        assert result["authorReadyStatus"] == "author_ready_draft"
        assert result["authorReadyDecision"] == "stop_for_author_review"
        assert result["aiDraft"]["status"] == draft_status
        assert result["aiDraft"]["diagnosticCodes"] == draft_codes
        assert result["aiDraft"]["jsonRepairStatus"] == "not_needed"
        assert result["aiDraft"]["providerTotalTokens"] == draft_tokens
        assert result["aiEnrichment"]["status"] == enrichment_status
        assert result["aiEnrichment"]["diagnosticCodes"] == enrichment_codes
        assert result["aiEnrichment"]["jsonRepairStatus"] == "not_needed"
        assert result["aiEnrichment"]["proposalCount"] == enrichment_proposals
        assert result["aiEnrichment"]["providerTotalTokens"] == enrichment_tokens

    assert by_id["xyflow"]["skippedPackageCount"] == 7
    assert by_id["navigation-split-view"]["candidateLayerFindings"] == [
        {
            "id": "package_id_hint_mismatch",
            "severity": "review",
            "summary": (
                "The manifest packageId hint uses navigation-split-view.core, while "
                "deterministic drafting normalized the generated candidate id to "
                "navigation_split_view.core."
            ),
        }
    ]

    non_authority = " ".join(payload["nonAuthority"])
    assert "review evidence only" in non_authority
    assert "proposal-only and not registry truth" in non_authority
    assert "not SpecPM registry acceptance" in non_authority
    assert "does not accept packages" in non_authority
    assert "does not accept relations" in non_authority
    assert "does not seed baselines" in non_authority
    assert "does not remove preview_only" in non_authority
    assert "does not publish registry metadata" in non_authority
    assert payload["productVerdict"]["status"] == "ready_for_candidate_layer_triage"
    assert payload["productVerdict"]["pipelineHealth"] == "deterministic_and_live_lm_studio_passed"
    assert (
        payload["productVerdict"]["candidateQuality"]
        == "valid_starter_packages_with_ai_review_findings"
    )


def test_limited_popular_library_live_lm_studio_batch_docs_cover_p30_t3_verdict() -> None:
    github_doc = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryLiveLMStudioBatch.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    corpus_plan = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md"
    corpus_plan_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryCorpusPlan.md"
    )
    deterministic = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md"
    deterministic_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryDeterministicBatch.md"
    )

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Limited Popular-Library Live LM Studio Batch",
            "SpecHarvesterLimitedPopularLibraryLiveLMStudioBatch",
            "spec-harvester.limited-popular-library-live-lm-studio-batch/v0",
            "producer_preview_evidence_only",
            "openai/gpt-oss-20b",
            "jsonRepairMaxAttempts",
            "rawPromptPersisted: false",
            "rawResponsePersisted: false",
            "chainOfThoughtPersisted: false",
            "Flask",
            "Gin",
            "xyflow",
            "Cupertino",
            "NavigationSplitView",
            "docc2context",
            "excluded_package_unknown",
            "package_set_id_missing",
            "refined_summary_missing",
            "package_id_hint_mismatch",
            "ready_for_candidate_layer_triage",
            "138700",
            "not SpecPM handoff" if path == github_doc else "candidate-layer triage",
            "remove `preview_only`" if path == github_doc else "preview_only",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md" in docs_index.read_text(
        encoding="utf-8"
    )
    assert "<doc:LimitedPopularLibraryLiveLMStudioBatch>" in docc_root.read_text(encoding="utf-8")
    assert "LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md" in roadmap.read_text(encoding="utf-8")
    assert "LimitedPopularLibraryLiveLMStudioBatch" in roadmap_docc.read_text(encoding="utf-8")
    assert "LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md" in corpus_plan.read_text(
        encoding="utf-8"
    )
    assert "LimitedPopularLibraryLiveLMStudioBatch" in corpus_plan_docc.read_text(encoding="utf-8")
    assert "LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md" in deterministic.read_text(
        encoding="utf-8"
    )
    assert "LimitedPopularLibraryLiveLMStudioBatch" in deterministic_docc.read_text(
        encoding="utf-8"
    )


def test_limited_popular_library_candidate_layer_triage_fixture_records_p30_t4_outcome() -> None:
    fixture = (
        ROOT
        / "tests"
        / "fixtures"
        / "limited_popular_library_candidate_layer_triage"
        / "p30-t4-limited-popular-libraries.example.json"
    )
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    assert (
        payload["apiVersion"] == "spec-harvester.limited-popular-library-candidate-layer-triage/v0"
    )
    assert payload["kind"] == "SpecHarvesterLimitedPopularLibraryCandidateLayerTriage"
    assert payload["schemaVersion"] == 1
    assert payload["authority"] == "producer_preview_evidence_only"
    assert payload["corpus"]["id"] == "p30-limited-popular-libraries"
    assert payload["corpus"]["manifestPath"] == "inputs/limited-popular-libraries/repositories.yml"
    assert payload["corpus"]["repositories"] == [
        "flask",
        "gin",
        "xyflow",
        "cupertino",
        "navigation-split-view",
        "docc2context",
    ]
    assert payload["inputs"]["deterministicFixture"] == {
        "kind": "SpecHarvesterLimitedPopularLibraryDeterministicBatch",
        "path": (
            "tests/fixtures/limited_popular_library_deterministic_batch/"
            "p30-t2-limited-popular-libraries.example.json"
        ),
        "status": "ready_for_live_lm_studio_limited_corpus",
    }
    assert payload["inputs"]["liveLmStudioFixture"] == {
        "kind": "SpecHarvesterLimitedPopularLibraryLiveLMStudioBatch",
        "path": (
            "tests/fixtures/limited_popular_library_live_lm_studio_batch/"
            "p30-t3-limited-popular-libraries.example.json"
        ),
        "status": "ready_for_candidate_layer_triage",
    }
    assert payload["summary"] == {
        "blockedCandidateCount": 0,
        "candidateLayerReviewRequiredCount": 3,
        "deferredCandidateCount": 6,
        "findingBlockedCount": 0,
        "findingCandidateLayerReviewRequiredCount": 2,
        "findingNeedsRegenerationCount": 4,
        "findingNotForIntakeCount": 0,
        "needsRegenerationCandidateCount": 6,
        "notForIntakeCandidateCount": 0,
        "p30T5SelectedCandidateCount": 3,
        "previewCandidateCount": 9,
        "relationProposalCount": 3,
        "repositoryCount": 6,
        "uniqueFindingCodeCount": 4,
    }
    assert payload["selectedForP30T5"] == ["flask.core", "gin.core", "docc2context.core"]
    assert payload["productVerdict"] == {
        "candidateQuality": "selected_candidates_ready_for_dry_run_handoff",
        "pipelineHealth": "deterministic_and_live_evidence_triaged",
        "status": "ready_for_selected_handoff_dry_run",
        "summary": (
            "Proceed to P30-T5 only for selected candidate-layer review packages. "
            "Defer package-set and warning-bearing candidates until targeted "
            "regeneration or explicit maintainer approval resolves their findings."
        ),
    }

    assert set(payload["triagePolicy"]) == {
        "candidate_layer_review_required",
        "needs_regeneration",
        "blocked",
        "not_for_intake",
    }

    candidates = {item["id"]: item for item in payload["triagedCandidates"]}
    assert list(candidates) == [
        "flask.core",
        "gin.core",
        "xyflow.workspace",
        "xyflow.react",
        "xyflow.svelte",
        "xyflow.system",
        "cupertino.core",
        "navigation_split_view.core",
        "docc2context.core",
    ]
    selected = {
        candidate_id
        for candidate_id, candidate in candidates.items()
        if candidate["p30T5Selected"] is True
    }
    assert selected == {"flask.core", "gin.core", "docc2context.core"}
    review_required = {
        candidate_id
        for candidate_id, candidate in candidates.items()
        if candidate["classification"] == "candidate_layer_review_required"
    }
    assert review_required == {"flask.core", "gin.core", "docc2context.core"}
    needs_regeneration = {
        candidate_id
        for candidate_id, candidate in candidates.items()
        if candidate["classification"] == "needs_regeneration"
    }
    assert needs_regeneration == {
        "xyflow.workspace",
        "xyflow.react",
        "xyflow.svelte",
        "xyflow.system",
        "cupertino.core",
        "navigation_split_view.core",
    }
    assert candidates["flask.core"]["findingCodes"] == ["excluded_package_unknown"]
    assert candidates["gin.core"]["findingCodes"] == ["excluded_package_unknown"]
    assert candidates["docc2context.core"]["findingCodes"] == []
    assert candidates["navigation_split_view.core"]["findingCodes"] == [
        "package_set_id_missing",
        "package_id_hint_mismatch",
    ]
    assert all(candidates[item]["p30T5Selected"] is False for item in needs_regeneration)

    findings = {item["code"]: item for item in payload["triageFindings"]}
    assert set(findings) == {
        "excluded_package_unknown",
        "package_set_id_missing",
        "refined_summary_missing",
        "package_id_hint_mismatch",
    }
    assert findings["excluded_package_unknown"]["classification"] == (
        "candidate_layer_review_required"
    )
    assert findings["excluded_package_unknown"]["count"] == 2
    assert findings["excluded_package_unknown"]["affectedCandidateIds"] == [
        "flask.core",
        "gin.core",
    ]
    for code in (
        "package_set_id_missing",
        "refined_summary_missing",
        "package_id_hint_mismatch",
    ):
        assert findings[code]["classification"] == "needs_regeneration"
    assert findings["package_set_id_missing"]["count"] == 2
    assert findings["refined_summary_missing"]["affectedCandidateIds"] == ["cupertino.core"]
    assert findings["package_id_hint_mismatch"]["affectedCandidateIds"] == [
        "navigation_split_view.core"
    ]

    non_authority = " ".join(payload["nonAuthority"])
    assert "review evidence only" in non_authority
    assert "not SpecPM registry acceptance" in non_authority
    assert "does not accept packages" in non_authority
    assert "does not accept relations" in non_authority
    assert "does not seed baselines" in non_authority
    assert "does not remove preview_only" in non_authority
    assert "does not publish registry metadata" in non_authority
    assert "does not treat AI output as canonical" in non_authority


def test_limited_popular_library_candidate_layer_triage_docs_cover_p30_t4_verdict() -> None:
    github_doc = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryCandidateLayerTriage.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    corpus_plan = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md"
    corpus_plan_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryCorpusPlan.md"
    )
    deterministic = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md"
    deterministic_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryDeterministicBatch.md"
    )
    live = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md"
    live_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryLiveLMStudioBatch.md"
    )

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Limited Popular-Library Candidate-Layer Triage",
            "SpecHarvesterLimitedPopularLibraryCandidateLayerTriage",
            "spec-harvester.limited-popular-library-candidate-layer-triage/v0",
            "producer_preview_evidence_only",
            "candidate_layer_review_required",
            "needs_regeneration",
            "blocked",
            "not_for_intake",
            "flask.core",
            "gin.core",
            "xyflow.workspace",
            "xyflow.react",
            "xyflow.svelte",
            "xyflow.system",
            "cupertino.core",
            "navigation_split_view.core",
            "docc2context.core",
            "excluded_package_unknown",
            "package_set_id_missing",
            "refined_summary_missing",
            "package_id_hint_mismatch",
            "ready_for_selected_handoff_dry_run",
            "P30-T5",
            "remove `preview_only`" if path == github_doc else "preview_only",
            "accept packages",
            "accept relations",
            "publish registry metadata",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md" in docs_index.read_text(
        encoding="utf-8"
    )
    assert "<doc:LimitedPopularLibraryCandidateLayerTriage>" in docc_root.read_text(
        encoding="utf-8"
    )
    assert "LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md" in roadmap.read_text(
        encoding="utf-8"
    )
    assert "LimitedPopularLibraryCandidateLayerTriage" in roadmap_docc.read_text(encoding="utf-8")
    assert "LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md" in corpus_plan.read_text(
        encoding="utf-8"
    )
    assert "LimitedPopularLibraryCandidateLayerTriage" in corpus_plan_docc.read_text(
        encoding="utf-8"
    )
    assert "LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md" in deterministic.read_text(
        encoding="utf-8"
    )
    assert "LimitedPopularLibraryCandidateLayerTriage" in deterministic_docc.read_text(
        encoding="utf-8"
    )
    assert "LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md" in live.read_text(encoding="utf-8")
    assert "LimitedPopularLibraryCandidateLayerTriage" in live_docc.read_text(encoding="utf-8")


def test_limited_popular_library_selected_handoff_dry_run_fixture_records_p30_t5_outcome() -> None:
    fixture = (
        ROOT
        / "tests"
        / "fixtures"
        / "limited_popular_library_selected_handoff_dry_run"
        / "p30-t5-limited-popular-libraries.example.json"
    )
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    assert (
        payload["apiVersion"]
        == "spec-harvester.limited-popular-library-selected-handoff-dry-run/v0"
    )
    assert payload["kind"] == "SpecHarvesterLimitedPopularLibrarySelectedHandoffDryRun"
    assert payload["schemaVersion"] == 1
    assert payload["authority"] == "producer_preview_evidence_only"
    assert payload["corpus"]["id"] == "p30-limited-popular-libraries"
    assert payload["inputs"]["deterministicFixture"] == {
        "kind": "SpecHarvesterLimitedPopularLibraryDeterministicBatch",
        "path": (
            "tests/fixtures/limited_popular_library_deterministic_batch/"
            "p30-t2-limited-popular-libraries.example.json"
        ),
        "status": "ready_for_live_lm_studio_limited_corpus",
    }
    assert payload["inputs"]["liveLmStudioFixture"] == {
        "kind": "SpecHarvesterLimitedPopularLibraryLiveLMStudioBatch",
        "path": (
            "tests/fixtures/limited_popular_library_live_lm_studio_batch/"
            "p30-t3-limited-popular-libraries.example.json"
        ),
        "status": "ready_for_candidate_layer_triage",
    }
    assert payload["inputs"]["candidateLayerTriageFixture"] == {
        "kind": "SpecHarvesterLimitedPopularLibraryCandidateLayerTriage",
        "path": (
            "tests/fixtures/limited_popular_library_candidate_layer_triage/"
            "p30-t4-limited-popular-libraries.example.json"
        ),
        "status": "ready_for_selected_handoff_dry_run",
    }
    assert payload["run"] == {
        "commands": [
            "spec-harvester preflight-candidate-bundle <candidate>",
            "spec-harvester render-spec-site --candidate <candidate> --output <viewer>",
        ],
        "runRoot": "/tmp/specharvester-p30-t5-selected-handoff",
        "sourceCandidateRoot": "/tmp/specharvester-p30-t3.f7iGn0/live-lm-studio/package-sets",
    }
    assert payload["summary"] == {
        "deferredCandidateCount": 6,
        "passedPreflightCount": 3,
        "registryMutationCount": 0,
        "selectedCandidateCount": 3,
        "specpmPullRequestCreated": False,
        "viewerRenderedCount": 3,
    }
    assert payload["productVerdict"] == {
        "candidateQuality": "selected_preview_candidates_have_preflight_and_viewer_evidence",
        "pipelineHealth": "selected_preflight_and_viewer_generation_passed",
        "status": "selected_handoff_dry_run_ready",
        "summary": (
            "Dry-run evidence is ready for future SpecPM review for flask.core, "
            "gin.core, and docc2context.core only. The selected candidates remain "
            "preview-only producer evidence and are not accepted registry truth."
        ),
    }

    selected = {item["id"]: item for item in payload["selectedCandidates"]}
    assert list(selected) == ["flask.core", "gin.core", "docc2context.core"]
    deferred = {item["id"]: item for item in payload["deferredCandidates"]}
    assert set(deferred) == {
        "xyflow.workspace",
        "xyflow.react",
        "xyflow.svelte",
        "xyflow.system",
        "cupertino.core",
        "navigation_split_view.core",
    }
    assert all(item["reason"] == "needs_regeneration" for item in deferred.values())
    assert all(item["p30T5Selected"] is False for item in deferred.values())

    def sha256(value: str) -> str:
        return f"sha256:{value}"

    expected_file_digests = {
        "flask.core": {
            "specpm.yaml": sha256(
                "2b4a1c4d9aaeef5efbb8424fe3f748d7895551a7d852814c7ce3d163e789630f"
            ),
            "specs/flask.spec.yaml": sha256(
                "309b518b319fff5a2cdc1ca9abb9432919621a3fa327e20e3e3357592b1c2ad1"
            ),
            "producer-receipt.json": sha256(
                "23f56cb23d477fab8a3b11b62348751d4ea2306522b6642ce330432107bde6fe"
            ),
            "validation-report.json": sha256(
                "8e3e1ae6266cdd039ced62c59b701dba0abf47b881362e57ae94991b0c561eed"
            ),
            "diagnostics.json": sha256(
                "62da575a03f6be1773a4b783185a7ff29d392cf499e29e96955cf2e9123f0713"
            ),
            "author-ready-draft-quality-report.json": (
                sha256("75bf9010e50638a26eb62f3f6ff936a8882b10ff176a793378a60d9fcfbb469d")
            ),
        },
        "gin.core": {
            "specpm.yaml": sha256(
                "501be249e4d10598e069da3e12a6bc43af7de8084b725b0768acb6b7d167d3a4"
            ),
            "specs/gin.spec.yaml": sha256(
                "99e4520b4465f4d524bfa50ca54dccc57cafde7fad56b56261b3eb16ebc29506"
            ),
            "producer-receipt.json": sha256(
                "b47be79ba1c0fa137d2e80b58514e08360b615109c5469a5a9ca56c545f4cd0c"
            ),
            "validation-report.json": sha256(
                "b3bf292e36a8f2c038dd04aad0b80a825f959aa63882e92df4f489fbf2c6d16a"
            ),
            "diagnostics.json": sha256(
                "7406004edcf4366c3ed7dbc62c63c4f58b782aff5874ac84127f31fafec399dd"
            ),
            "author-ready-draft-quality-report.json": (
                sha256("622e6f05fd78d32dd56ab202067a0e0e07b30d521284904e769390409e9d1576")
            ),
        },
        "docc2context.core": {
            "specpm.yaml": sha256(
                "1ff2ff07c56e842543aa1b5c8dd42592d0d4d161330d8e53048f9b04f7dd06d8"
            ),
            "specs/docc2context.spec.yaml": (
                sha256("fe4227c16ebe8bd72c94a53b856aa31e4253036b60bec4a1bc63fb975639955b")
            ),
            "producer-receipt.json": sha256(
                "ed359c0063bbba5750cc0e448577f346f33ea4bd4ad2c33be38f2186890f1a6b"
            ),
            "validation-report.json": sha256(
                "315cb32df1087655b93bff7473b113a174a8784e1db38788ae7b28ed79f7b287"
            ),
            "diagnostics.json": sha256(
                "a7e06d36283586e3d9d9a2a5a6edf8e0515e08532dcd577943ac98bf006e5d9e"
            ),
            "author-ready-draft-quality-report.json": (
                sha256("1eca3f7727b99e4799604cca32f1f294110a2682cd9f344a8983e27902dae588")
            ),
        },
    }
    expected_preflight_digests = {
        "flask.core": sha256("836abcf074a43cfa84526cb992eab0a6b7c1354e34bd0d275e407606d46787f7"),
        "gin.core": sha256("e6738829bed9b409eff3df6a5cfe1524cda6b1762a352779e78154439490547f"),
        "docc2context.core": (
            sha256("7d0e119e59c56397d42b28922dfe281fa77a6b06b899663e1a27e2ba2918a282")
        ),
    }
    expected_viewer_digests = {
        "flask.core": {
            "index": sha256("3feea0d6acb3a2809f732bd81ee760e05d7a6f33d607ecc0a9e5a1180e5287c3"),
            "specPackage": sha256(
                "06667c14b9c90a8988a35f8c99f530cfd36edd84297a5b3fe23c2aa2aa172d84"
            ),
        },
        "gin.core": {
            "index": sha256("e15ef3f031a0e11196f11ff76593af985eb24ad016cb5b3eb313a4f3fb09557d"),
            "specPackage": sha256(
                "c9d3e34021d6eba53f96aa92939ec2cebb64a44173b34782971f2f18ad2b93b0"
            ),
        },
        "docc2context.core": {
            "index": sha256("4baee2a08ed2d996d633a81863a5b0097fed3736df4595027c4d452605dbf804"),
            "specPackage": sha256(
                "d6ad8328a2300d0f5f6e3c89895182e28c5f28d43cbc71d4dc40d4be3c67d81a"
            ),
        },
    }

    for candidate_id, candidate in selected.items():
        assert candidate["p30T5Selected"] is True
        assert candidate["previewOnly"] is True
        assert candidate["triageClassification"] == "candidate_layer_review_required"
        assert candidate["handoffRecommendation"] == "ready_for_specpm_dry_run_review"
        assert candidate["registryAcceptanceDecision"] == {
            "producerAuthority": "evidence_only",
            "requiredFor": "public_index_acceptance",
            "status": "external_required",
        }
        assert candidate["producerPreflight"]["status"] == "passed"
        assert candidate["producerPreflight"]["warningCount"] == 0
        assert candidate["producerPreflight"]["errorCount"] == 0
        assert candidate["producerPreflight"]["diagnosticCount"] == 0
        assert (
            candidate["producerPreflight"]["reportDigest"]
            == expected_preflight_digests[candidate_id]
        )
        assert candidate["viewer"]["status"] == "ok"
        assert candidate["viewer"]["indexDigest"] == expected_viewer_digests[candidate_id]["index"]
        assert (
            candidate["viewer"]["specPackageDigest"]
            == expected_viewer_digests[candidate_id]["specPackage"]
        )
        required_files = {item["path"]: item for item in candidate["requiredFiles"]}
        assert set(required_files) == set(expected_file_digests[candidate_id])
        assert {item["role"] for item in candidate["requiredFiles"]} == {
            "manifest",
            "boundary_spec",
            "producer_receipt",
            "validation_report",
            "diagnostics",
            "quality_report",
        }
        assert {
            path: item["digest"] for path, item in required_files.items()
        } == expected_file_digests[candidate_id]

    non_authority = " ".join(payload["nonAuthority"])
    assert "review evidence only" in non_authority
    assert "not SpecPM registry acceptance" in non_authority
    assert "does not accept packages" in non_authority
    assert "does not accept relations" in non_authority
    assert "does not seed baselines" in non_authority
    assert "does not remove preview_only" in non_authority
    assert "does not publish registry metadata" in non_authority
    assert "does not create a SpecPM pull request" in non_authority
    assert payload["notExecuted"] == [
        "prepare-accepted-entry",
        "accepted-package-update-proposal",
        "SpecPM pull request creation",
        "registry mutation",
        "relation acceptance",
        "baseline seeding",
        "preview_only removal",
    ]


def test_limited_popular_library_selected_handoff_dry_run_docs_cover_p30_t5_verdict() -> None:
    github_doc = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibrarySelectedHandoffDryRun.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    handoff = ROOT / "docs" / "SPECPM_HANDOFF.md"
    handoff_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    corpus_plan = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md"
    corpus_plan_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryCorpusPlan.md"
    )
    triage = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md"
    triage_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryCandidateLayerTriage.md"
    )
    live = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md"
    live_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibraryLiveLMStudioBatch.md"
    )

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Limited Popular-Library Selected Handoff Dry Run",
            "SpecHarvesterLimitedPopularLibrarySelectedHandoffDryRun",
            "spec-harvester.limited-popular-library-selected-handoff-dry-run/v0",
            "producer_preview_evidence_only",
            "flask.core",
            "gin.core",
            "docc2context.core",
            "xyflow.workspace",
            "xyflow.react",
            "xyflow.svelte",
            "xyflow.system",
            "cupertino.core",
            "navigation_split_view.core",
            "selected_handoff_dry_run_ready",
            "producer-side preflight",
            "static viewer",
            "SHA-256",
            "author-ready-draft-quality-report.json",
            "external_required",
            "needs_regeneration",
            "prepare-accepted-entry",
            "accepted-package-update-proposal",
            "SpecPM pull request",
            "preview_only",
            "accept packages",
            "accept relations",
            "publish registry metadata",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md" in docs_index.read_text(
        encoding="utf-8"
    )
    assert "<doc:LimitedPopularLibrarySelectedHandoffDryRun>" in docc_root.read_text(
        encoding="utf-8"
    )
    assert "LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md" in roadmap.read_text(
        encoding="utf-8"
    )
    assert "LimitedPopularLibrarySelectedHandoffDryRun" in roadmap_docc.read_text(encoding="utf-8")
    assert "LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md" in handoff.read_text(
        encoding="utf-8"
    )
    assert "LimitedPopularLibrarySelectedHandoffDryRun" in handoff_docc.read_text(encoding="utf-8")
    assert "LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md" in corpus_plan.read_text(
        encoding="utf-8"
    )
    assert "LimitedPopularLibrarySelectedHandoffDryRun" in corpus_plan_docc.read_text(
        encoding="utf-8"
    )
    assert "LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md" in triage.read_text(
        encoding="utf-8"
    )
    assert "LimitedPopularLibrarySelectedHandoffDryRun" in triage_docc.read_text(encoding="utf-8")
    assert "LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md" in live.read_text(encoding="utf-8")
    assert "LimitedPopularLibrarySelectedHandoffDryRun" in live_docc.read_text(encoding="utf-8")


def test_selected_candidate_handoff_proposal_fixture_records_p31_t1_contract() -> None:
    fixture = (
        ROOT
        / "tests"
        / "fixtures"
        / "selected_candidate_handoff_proposal"
        / "p31-t1-selected-candidate-handoff.example.json"
    )
    payload = json.loads(fixture.read_text(encoding="utf-8"))

    assert payload["apiVersion"] == "spec-harvester.selected-candidate-handoff-proposal/v0"
    assert payload["kind"] == "SpecHarvesterSelectedCandidateHandoffProposal"
    assert payload["schemaVersion"] == 1
    assert payload["authority"] == "producer_preview_evidence_only"
    assert payload["summary"] == {
        "deferredCandidateCount": 6,
        "registryMutationCount": 0,
        "requiredEvidenceRoleCount": 11,
        "selectedCandidateCount": 3,
        "specpmPullRequestCreated": False,
    }
    assert payload["source"]["triageFixture"] == {
        "apiVersion": "spec-harvester.limited-popular-library-candidate-layer-triage/v0",
        "kind": "SpecHarvesterLimitedPopularLibraryCandidateLayerTriage",
        "path": (
            "tests/fixtures/limited_popular_library_candidate_layer_triage/"
            "p30-t4-limited-popular-libraries.example.json"
        ),
        "status": "ready_for_selected_handoff_dry_run",
    }
    assert payload["source"]["selectedDryRunFixture"] == {
        "apiVersion": "spec-harvester.limited-popular-library-selected-handoff-dry-run/v0",
        "kind": "SpecHarvesterLimitedPopularLibrarySelectedHandoffDryRun",
        "path": (
            "tests/fixtures/limited_popular_library_selected_handoff_dry_run/"
            "p30-t5-limited-popular-libraries.example.json"
        ),
        "status": "selected_handoff_dry_run_ready",
    }

    required_roles = {item["role"]: item for item in payload["requiredEvidenceRoles"]}
    assert list(required_roles) == [
        "candidate_bundle",
        "manifest",
        "boundary_spec",
        "producer_receipt",
        "validation_report",
        "diagnostics",
        "quality_report",
        "producer_preflight",
        "static_viewer",
        "static_viewer_payload",
        "selected_handoff_dry_run",
    ]
    assert all(item["required"] is True for item in required_roles.values())
    assert required_roles["manifest"]["path"] == "specpm.yaml"
    assert required_roles["boundary_spec"]["path"] == "specs/*.spec.yaml"
    assert required_roles["producer_preflight"]["path"] == "preflight/<package_id>.json"
    assert required_roles["static_viewer_payload"]["path"] == (
        "viewer/<package_id>/spec-package.json"
    )

    selected = {item["id"]: item for item in payload["selectedCandidates"]}
    assert list(selected) == ["flask.core", "gin.core", "docc2context.core"]
    deferred = {item["id"]: item for item in payload["deferredCandidates"]}
    assert set(deferred) == {
        "xyflow.workspace",
        "xyflow.react",
        "xyflow.svelte",
        "xyflow.system",
        "cupertino.core",
        "navigation_split_view.core",
    }
    assert all(item["reason"] == "needs_regeneration" for item in deferred.values())
    assert all(
        item["handoffStatus"] == "excluded_from_selected_handoff" for item in deferred.values()
    )

    for candidate in selected.values():
        assert candidate["previewOnly"] is True
        assert candidate["triageClassification"] == "candidate_layer_review_required"
        assert candidate["maintainerAction"] == "review_for_possible_specpm_intake"
        assert candidate["producerPreflight"]["status"] == "passed"
        assert candidate["producerPreflight"]["warningCount"] == 0
        assert candidate["producerPreflight"]["errorCount"] == 0
        assert candidate["staticViewer"]["status"] == "ok"
        assert candidate["registryAcceptanceDecision"] == {
            "producerAuthority": "evidence_only",
            "requiredFor": "public_index_acceptance",
            "status": "external_required",
        }
        evidence_roles = {item["role"] for item in candidate["evidenceLinks"]}
        assert evidence_roles == set(required_roles)
        digest_roles = {
            item["role"]
            for item in candidate["evidenceLinks"]
            if item["role"] != "candidate_bundle" and item["role"] != "selected_handoff_dry_run"
        }
        assert all(
            item["digest"].startswith("sha256:")
            for item in candidate["evidenceLinks"]
            if item["role"] in digest_roles
        )

    assert payload["futureConsumerBoundary"] == {
        "producerCanAccept": False,
        "specpmMayAcceptAfterMaintainerReview": True,
        "specpmMayPreflight": True,
    }
    assert (
        "Verify every required evidence role and digest before trusting the handoff."
        in (payload["maintainerChecklist"])
    )
    non_authority = " ".join(payload["nonAuthority"])
    assert "review evidence only" in non_authority
    assert "not SpecPM registry acceptance" in non_authority
    assert "does not accept packages" in non_authority
    assert "does not accept relations" in non_authority
    assert "does not seed baselines" in non_authority
    assert "does not remove preview_only" in non_authority
    assert "does not publish registry metadata" in non_authority
    assert "does not create a SpecPM pull request" in non_authority
    assert payload["notExecuted"] == [
        "prepare-accepted-entry",
        "accepted-package-update-proposal",
        "SpecPM pull request creation",
        "registry mutation",
        "relation acceptance",
        "baseline seeding",
        "preview_only removal",
    ]


def test_selected_candidate_handoff_proposal_docs_cover_p31_t1_contract() -> None:
    github_doc = ROOT / "docs" / "SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SelectedCandidateHandoffProposal.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    handoff = ROOT / "docs" / "SPECPM_HANDOFF.md"
    handoff_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    selected_dry_run = ROOT / "docs" / "LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md"
    selected_dry_run_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LimitedPopularLibrarySelectedHandoffDryRun.md"
    )

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Selected Candidate Handoff Proposal",
            "SpecHarvesterSelectedCandidateHandoffProposal",
            "spec-harvester.selected-candidate-handoff-proposal/v0",
            "producer_preview_evidence_only",
            "flask.core",
            "gin.core",
            "docc2context.core",
            "xyflow.workspace",
            "xyflow.react",
            "xyflow.svelte",
            "xyflow.system",
            "cupertino.core",
            "navigation_split_view.core",
            "candidate_bundle",
            "manifest",
            "boundary_spec",
            "producer_receipt",
            "validation_report",
            "diagnostics",
            "quality_report",
            "producer_preflight",
            "static_viewer",
            "static_viewer_payload",
            "selected_handoff_dry_run",
            "SHA-256",
            "external_required",
            "previewOnly: true",
            "preview_only",
            "needs_regeneration",
            "SpecPM-side preflight",
            "prepare-accepted-entry",
            "accepted-package-update-proposal",
            "SpecPM pull request",
            "accept packages",
            "accept relations",
            "seed baselines",
            "publish registry metadata",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SelectedCandidateHandoffProposal>" in docc_root.read_text(encoding="utf-8")
    assert "SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md" in roadmap.read_text(encoding="utf-8")
    assert "SelectedCandidateHandoffProposal" in roadmap_docc.read_text(encoding="utf-8")
    assert "SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md" in handoff.read_text(encoding="utf-8")
    assert "SelectedCandidateHandoffProposal" in handoff_docc.read_text(encoding="utf-8")
    assert "SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md" in selected_dry_run.read_text(encoding="utf-8")
    assert "SelectedCandidateHandoffProposal" in selected_dry_run_docc.read_text(encoding="utf-8")


def test_single_package_candidate_fallback_docs_cover_producer_boundary() -> None:
    github_doc = ROOT / "docs" / "SINGLE_PACKAGE_CANDIDATE_FALLBACK.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SinglePackageCandidateFallback.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    autonomous_batch = ROOT / "docs" / "AUTONOMOUS_CANDIDATE_BATCH.md"
    autonomous_batch_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "AutonomousCandidateBatch.md"
    )
    tech_debt = ROOT / "docs" / "AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md"
    tech_debt_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AutonomousCandidateTechDebtPlan.md"
    )
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Single-Package Candidate Fallback",
            "autonomous-candidate-batch",
            "workspace-inventory.json",
            "flask.core",
            "gin.core",
            "0 relation proposals",
            "harvest.json",
            "public-interface-index.json",
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "author-ready-draft-quality-report.json",
            "single_package_source_manifest_fallback",
            "single_package",
            "does not invent `contains` relations",
            "producer_preview_evidence_only",
            "preview_only",
            "no SpecPM acceptance",
            "P29-T5",
            "P29-T6",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "SINGLE_PACKAGE_CANDIDATE_FALLBACK.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SinglePackageCandidateFallback>" in docc_root.read_text(encoding="utf-8")
    assert "SINGLE_PACKAGE_CANDIDATE_FALLBACK.md" in autonomous_batch.read_text(encoding="utf-8")
    assert "SinglePackageCandidateFallback" in autonomous_batch_docc.read_text(encoding="utf-8")
    assert "SINGLE_PACKAGE_CANDIDATE_FALLBACK.md" in tech_debt.read_text(encoding="utf-8")
    assert "SinglePackageCandidateFallback" in tech_debt_docc.read_text(encoding="utf-8")
    assert "SINGLE_PACKAGE_CANDIDATE_FALLBACK.md" in roadmap.read_text(encoding="utf-8")
    assert "SinglePackageCandidateFallback" in roadmap_docc.read_text(encoding="utf-8")
