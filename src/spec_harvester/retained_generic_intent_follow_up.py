from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from spec_harvester.experimental_intent_policy import (
    GENERIC_OBSERVED_INTENT_IDS,
    load_experimental_intent_decision_policy,
)
from spec_harvester.local_candidate_review_catalog import (
    LocalCandidateReviewCatalogOptions,
    _json_object,
    _read_archive,
)
from spec_harvester.retained_corpus_semantic_campaign import (
    CODEX_SPARK_MODEL,
    CampaignTarget,
    digest,
    load_campaign_scope,
    sha256_file,
    validate_campaign_record,
    write_deterministic_archive,
)
from spec_harvester.semantic_proposal_quality import load_semantic_author_quality_policy

FOLLOW_UP_API_VERSION = "spec-harvester.retained-generic-intent-follow-up/v0"
FOLLOW_UP_KIND = "SpecHarvesterRetainedGenericIntentFollowUp"
PLAN_API_VERSION = "spec-harvester.retained-generic-intent-follow-up-plan/v0"
PLAN_KIND = "SpecHarvesterRetainedGenericIntentFollowUpPlan"
REVIEW_SAMPLE_API_VERSION = "spec-harvester.semantic-follow-up-review-sample/v0"
REVIEW_SAMPLE_KIND = "SpecHarvesterSemanticFollowUpReviewSample"
EXPECTED_TARGET_COUNT = 46
EXPECTED_GENERIC_REFERENCE_COUNT = 48
FALSE_NOVELTY_CODES = frozenset(
    {
        "experimental_intent_false_novelty_risk",
        "experimental_intent_retains_generic_reuse",
        "experimental_intent_overlaps_observed",
    }
)


def build_follow_up_plan(
    *,
    source_manifest_dir: Path,
    source_root: Path,
    handoff_root: Path,
    readiness_evidence: Path,
    baseline_report_path: Path,
    baseline_archive_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], list[CampaignTarget], dict[str, dict[str, Any]]]:
    baseline_scope, all_targets = load_campaign_scope(
        source_manifest_dir=source_manifest_dir,
        source_root=source_root,
        handoff_root=handoff_root,
        readiness_evidence=readiness_evidence,
    )
    baseline_report = _read_json(baseline_report_path)
    if baseline_report.get("reportSha256") != _digest_without(baseline_report, "reportSha256"):
        raise ValueError("P55-T10 baseline report digest is stale")
    archive = baseline_report.get("archive")
    if (
        baseline_report.get("campaignInputSha256") != baseline_scope["campaignInputSha256"]
        or not isinstance(archive, dict)
        or archive.get("recordCount") != 100
        or archive.get("sha256") != sha256_file(baseline_archive_path)
    ):
        raise ValueError("P55-T10 baseline report or archive binding is stale")
    _, members = _read_archive(
        LocalCandidateReviewCatalogOptions(
            archive=baseline_archive_path,
            expected_archive_sha256=archive["sha256"],
        )
    )
    archived_scope = _json_object(members.get("campaign-input.json", b""), "campaign-input.json")
    if archived_scope != baseline_scope:
        raise ValueError("P55-T10 archived campaign input differs from reconstructed scope")

    target_by_id = {target.repository_id: target for target in all_targets}
    baseline_records: dict[str, dict[str, Any]] = {}
    selected_targets: list[CampaignTarget] = []
    target_bindings: list[dict[str, Any]] = []
    for target in all_targets:
        member_name = f"records/{target.repository_id}/campaign-record.json"
        record = _json_object(members.get(member_name, b""), member_name)
        validate_campaign_record(record, baseline_scope, target)
        baseline_records[target.repository_id] = record
        if not set(record.get("proposalReuseIntentIds", [])) & GENERIC_OBSERVED_INTENT_IDS:
            continue
        selected_targets.append(target)
        target_bindings.append(
            {
                **target.binding(),
                "baselineRecordSha256": record["recordSha256"],
                "baselineGenericIntentIds": sorted(
                    set(record["proposalReuseIntentIds"]) & GENERIC_OBSERVED_INTENT_IDS
                ),
            }
        )
    generic_reference_count = sum(len(item["baselineGenericIntentIds"]) for item in target_bindings)
    if (
        len(baseline_records) != 100
        or len(selected_targets) != EXPECTED_TARGET_COUNT
        or generic_reference_count != EXPECTED_GENERIC_REFERENCE_COUNT
    ):
        raise ValueError(
            "P55-T10 baseline does not contain 46 repositories with 48 generic references"
        )
    if any(target.repository_id not in target_by_id for target in selected_targets):
        raise ValueError("P55-T10 generic-reuse target is outside the retained corpus")

    decision_policy = load_experimental_intent_decision_policy()
    quality_policy = load_semantic_author_quality_policy()
    plan: dict[str, Any] = {
        "apiVersion": PLAN_API_VERSION,
        "kind": PLAN_KIND,
        "schemaVersion": 1,
        "authority": "maintainer_frozen_generic_intent_follow_up_plan",
        "taskId": "P55-T10C",
        "provider": {
            "providerId": CODEX_SPARK_MODEL,
            "modelId": CODEX_SPARK_MODEL,
            "transport": "codex_exec",
        },
        "baseline": {
            "reportSha256": baseline_report["reportSha256"],
            "archiveSha256": archive["sha256"],
            "campaignInputSha256": baseline_scope["campaignInputSha256"],
        },
        "policies": {
            "experimentalIntentDecisionPolicySha256": decision_policy["policySha256"],
            "semanticQualityPolicySha256": quality_policy["policySha256"],
        },
        "attemptBudget": {
            "providerMaxAttempts": 2,
            "jsonRepairMaxAttemptsPerProviderAttempt": 1,
            "timeoutSeconds": 300,
            "maxOutputBytes": 256 * 1024,
        },
        "targets": target_bindings,
        "genericReferenceCount": EXPECTED_GENERIC_REFERENCE_COUNT,
        "successCriteria": {
            "requireAllTargetsTerminal": True,
            "maximumFalseNoveltyCount": 0,
            "maximumDuplicateExperimentalIntentIdCount": 0,
            "maximumDuplicateExperimentalSemanticStemCount": 0,
            "minimumRepresentativeReviewSampleCount": 8,
        },
        "executionBoundary": _execution_boundary(),
    }
    plan["planSha256"] = digest(plan)
    return plan, baseline_scope, selected_targets, baseline_records


def write_follow_up_plan(path: Path, plan: dict[str, Any]) -> None:
    validate_follow_up_plan(plan)
    _write_json(path, plan)


def validate_follow_up_plan(plan: dict[str, Any]) -> None:
    if (
        not isinstance(plan, dict)
        or plan.get("apiVersion") != PLAN_API_VERSION
        or plan.get("kind") != PLAN_KIND
        or plan.get("schemaVersion") != 1
        or plan.get("authority") != "maintainer_frozen_generic_intent_follow_up_plan"
        or plan.get("taskId") != "P55-T10C"
        or plan.get("provider")
        != {
            "providerId": CODEX_SPARK_MODEL,
            "modelId": CODEX_SPARK_MODEL,
            "transport": "codex_exec",
        }
    ):
        raise ValueError("P55-T10C follow-up plan identity is invalid")
    targets = plan.get("targets")
    if (
        not isinstance(targets, list)
        or len(targets) != EXPECTED_TARGET_COUNT
        or len({item.get("repositoryId") for item in targets if isinstance(item, dict)})
        != EXPECTED_TARGET_COUNT
        or plan.get("genericReferenceCount") != EXPECTED_GENERIC_REFERENCE_COUNT
    ):
        raise ValueError("P55-T10C follow-up target set is invalid")
    if plan.get("attemptBudget") != {
        "providerMaxAttempts": 2,
        "jsonRepairMaxAttemptsPerProviderAttempt": 1,
        "timeoutSeconds": 300,
        "maxOutputBytes": 256 * 1024,
    }:
        raise ValueError("P55-T10C follow-up attempt budget is invalid")
    if plan.get("successCriteria") != {
        "requireAllTargetsTerminal": True,
        "maximumFalseNoveltyCount": 0,
        "maximumDuplicateExperimentalIntentIdCount": 0,
        "maximumDuplicateExperimentalSemanticStemCount": 0,
        "minimumRepresentativeReviewSampleCount": 8,
    }:
        raise ValueError("P55-T10C follow-up success criteria are invalid")
    if plan.get("executionBoundary") != _execution_boundary():
        raise ValueError("P55-T10C follow-up execution boundary is invalid")
    if plan.get("planSha256") != _digest_without(plan, "planSha256"):
        raise ValueError("P55-T10C follow-up plan digest is stale")


def load_follow_up_scope(
    *,
    plan_path: Path,
    source_manifest_dir: Path,
    source_root: Path,
    handoff_root: Path,
    readiness_evidence: Path,
    baseline_report_path: Path,
    baseline_archive_path: Path,
) -> tuple[dict[str, Any], list[CampaignTarget], dict[str, dict[str, Any]]]:
    plan = _read_json(plan_path)
    validate_follow_up_plan(plan)
    expected, baseline_scope, targets, baseline_records = build_follow_up_plan(
        source_manifest_dir=source_manifest_dir,
        source_root=source_root,
        handoff_root=handoff_root,
        readiness_evidence=readiness_evidence,
        baseline_report_path=baseline_report_path,
        baseline_archive_path=baseline_archive_path,
    )
    if plan != expected:
        raise ValueError("P55-T10C frozen plan differs from current baseline bindings")
    scope: dict[str, Any] = {
        "apiVersion": FOLLOW_UP_API_VERSION,
        "kind": FOLLOW_UP_KIND,
        "schemaVersion": 1,
        "authority": "semantic_follow_up_proposal_only",
        "taskId": "P55-T10C",
        "provider": baseline_scope["provider"],
        "targetCount": EXPECTED_TARGET_COUNT,
        "baseline": plan["baseline"],
        "policies": plan["policies"],
        "attemptBudget": plan["attemptBudget"],
        "successCriteria": plan["successCriteria"],
        "targets": plan["targets"],
        "inputProjection": baseline_scope["inputProjection"],
        "executionBoundary": _execution_boundary(),
    }
    scope["campaignInputSha256"] = digest(scope)
    return scope, targets, baseline_records


def finalize_follow_up(
    *,
    scope: dict[str, Any],
    targets: list[CampaignTarget],
    baseline_records: dict[str, dict[str, Any]],
    work_root: Path,
    output_path: Path,
    archive_path: Path,
    review_sample_path: Path,
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for target in targets:
        path = work_root / "records" / target.repository_id / "campaign-record.json"
        record = _read_json(path)
        validate_campaign_record(record, scope, target)
        records.append(record)
    if len(records) != EXPECTED_TARGET_COUNT:
        raise ValueError("P55-T10C follow-up is incomplete")

    archive_sha256 = write_deterministic_archive(work_root, archive_path)
    comparison = compare_follow_up(baseline_records, records)
    sample = build_representative_review_sample(scope, records)
    _write_json(review_sample_path, sample)
    criteria = scope["successCriteria"]
    transition_ready = (
        comparison["completedCount"] + comparison["failedCount"] == EXPECTED_TARGET_COUNT
        and comparison["falseNoveltyCount"] <= criteria["maximumFalseNoveltyCount"]
        and comparison["duplicateExperimentalIntentIdCount"]
        <= criteria["maximumDuplicateExperimentalIntentIdCount"]
        and comparison["duplicateExperimentalSemanticStemCount"]
        <= criteria["maximumDuplicateExperimentalSemanticStemCount"]
        and len(sample["items"]) >= criteria["minimumRepresentativeReviewSampleCount"]
    )
    report: dict[str, Any] = {
        "apiVersion": FOLLOW_UP_API_VERSION,
        "kind": FOLLOW_UP_KIND,
        "schemaVersion": 1,
        "authority": "semantic_follow_up_evidence_only",
        "taskId": "P55-T10C",
        "campaignInputSha256": scope["campaignInputSha256"],
        "baseline": scope["baseline"],
        "policies": scope["policies"],
        "provider": scope["provider"],
        "summary": comparison,
        "archive": {
            "path": archive_path.name,
            "sha256": archive_sha256,
            "recordCount": len(records),
        },
        "review": {
            "samplePath": review_sample_path.name,
            "sampleSha256": sha256_file(review_sample_path),
            "sampleCount": len(sample["items"]),
            "maintainerDecisionCount": 0,
            "status": "awaiting_explicit_maintainer_review",
        },
        "decision": {
            "p55T11TechnicallyReady": transition_ready,
            "p55T11Unblocked": False,
            "blockedOn": ["explicit_representative_maintainer_review"],
            "thresholdsRedefined": False,
        },
        "privacy": {
            "rawPromptsPersisted": False,
            "rawResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "credentialsPersisted": False,
            "machineLocalPathsPersisted": False,
        },
        "executionBoundary": _execution_boundary(),
        "recordIndex": [
            {
                "repositoryId": record["repositoryId"],
                "candidateId": record["candidateId"],
                "status": record["status"],
                "recordSha256": record["recordSha256"],
            }
            for record in records
        ],
    }
    report["reportSha256"] = digest(report)
    _write_json(output_path, report)
    return report


def compare_follow_up(
    baseline_records: dict[str, dict[str, Any]], records: list[dict[str, Any]]
) -> dict[str, Any]:
    completed = [record for record in records if record["status"] == "completed"]
    failed = [record for record in records if record["status"] == "failed"]
    quality_counts = Counter(record["qualityReport"]["status"] for record in completed)
    baseline_generic_count = sum(
        intent_id in GENERIC_OBSERVED_INTENT_IDS
        for record in records
        for intent_id in baseline_records[record["repositoryId"]]["proposalReuseIntentIds"]
    )
    follow_up_generic_count = sum(
        intent_id in GENERIC_OBSERVED_INTENT_IDS
        for record in completed
        for intent_id in record["proposalReuseIntentIds"]
    ) + sum(
        intent_id in GENERIC_OBSERVED_INTENT_IDS
        for record in failed
        for intent_id in baseline_records[record["repositoryId"]]["proposalReuseIntentIds"]
    )
    experimental_ids = [
        intent_id for record in completed for intent_id in record["experimentalIntentIds"]
    ]
    stems = [".".join(intent_id.split(".")[:-1]) for intent_id in experimental_ids]
    false_novelty = sum(
        bool(
            {item["code"] for item in record["qualityReport"]["diagnostics"]} & FALSE_NOVELTY_CODES
        )
        for record in completed
    )
    evidence_supported_experimental = sum(
        len(record["experimentalIntentIds"])
        for record in completed
        if record["qualityReport"]["status"] != "rejected"
        and record["qualityReport"]["metrics"]["schemaValid"] is True
        and record["qualityReport"]["metrics"]["evidenceSupportRate"] == 1.0
    )
    edit_required = sum(
        record["qualityReport"]["status"] == "rejected"
        or bool(set(record["proposalReuseIntentIds"]) & GENERIC_OBSERVED_INTENT_IDS)
        or bool(
            {item["code"] for item in record["qualityReport"]["diagnostics"]} & FALSE_NOVELTY_CODES
        )
        for record in completed
    ) + len(failed)
    duration_ms = sum(attempt["durationMs"] for record in records for attempt in record["attempts"])
    usage: Counter[str] = Counter()
    for record in completed:
        usage.update(
            {
                key: value
                for key, value in record["semanticPass"]["providerReceipt"].get("usage", {}).items()
                if isinstance(value, int) and not isinstance(value, bool)
            }
        )
    return {
        "targetCount": len(records),
        "completedCount": len(completed),
        "failedCount": len(failed),
        "qualityStatusCounts": dict(sorted(quality_counts.items())),
        "baselineGenericIntentReuseCount": baseline_generic_count,
        "followUpGenericIntentReuseCount": follow_up_generic_count,
        "genericIntentReductionCount": baseline_generic_count - follow_up_generic_count,
        "experimentalIntentCount": len(experimental_ids),
        "evidenceSupportedExperimentalIntentCount": evidence_supported_experimental,
        "falseNoveltyCount": false_novelty,
        "duplicateExperimentalIntentIdCount": _duplicate_count(experimental_ids),
        "duplicateExperimentalSemanticStemCount": _duplicate_count(stems),
        "providerAttemptCount": sum(len(record["attempts"]) for record in records),
        "failedProviderAttemptCount": sum(
            attempt["status"] == "failed" for record in records for attempt in record["attempts"]
        ),
        "jsonRepairRecordCount": sum(
            record["semanticPass"]["providerReceipt"]["jsonRepairNeeded"] for record in completed
        ),
        "estimatedReviewerEditRequiredCount": edit_required,
        "estimatedReviewerEditBurdenRate": round(edit_required / len(records), 4),
        "durationMs": duration_ms,
        "tokenUsage": dict(sorted(usage.items())),
        "cost": {"status": "unavailable_from_codex_exec_receipts"},
    }


def build_representative_review_sample(
    scope: dict[str, Any], records: list[dict[str, Any]]
) -> dict[str, Any]:
    strata: dict[str, list[dict[str, Any]]] = {
        "experimental_proposal": [],
        "retained_generic_reuse": [],
        "quality_rejected": [],
        "recovered_provider_attempt": [],
    }
    for record in sorted(records, key=lambda item: item["repositoryId"]):
        if record["status"] != "completed":
            continue
        if record["experimentalIntentIds"]:
            strata["experimental_proposal"].append(record)
        if set(record["proposalReuseIntentIds"]) & GENERIC_OBSERVED_INTENT_IDS:
            strata["retained_generic_reuse"].append(record)
        if record["qualityReport"]["status"] == "rejected":
            strata["quality_rejected"].append(record)
        if any(item["status"] == "failed" for item in record["attempts"]):
            strata["recovered_provider_attempt"].append(record)
    selected: list[tuple[str, dict[str, Any]]] = []
    used: set[str] = set()
    for stratum, candidates in strata.items():
        for record in candidates:
            if record["repositoryId"] not in used:
                selected.append((stratum, record))
                used.add(record["repositoryId"])
                break
    for stratum, candidates in strata.items():
        for record in candidates:
            if len(selected) >= 8:
                break
            if record["repositoryId"] not in used:
                selected.append((stratum, record))
                used.add(record["repositoryId"])
    if len(selected) < 8:
        for record in sorted(records, key=lambda item: item["repositoryId"]):
            if record["repositoryId"] not in used:
                selected.append(("coverage_fill", record))
                used.add(record["repositoryId"])
            if len(selected) >= 8:
                break
    sample: dict[str, Any] = {
        "apiVersion": REVIEW_SAMPLE_API_VERSION,
        "kind": REVIEW_SAMPLE_KIND,
        "schemaVersion": 1,
        "authority": "maintainer_review_queue_only",
        "taskId": "P55-T10C",
        "campaignInputSha256": scope["campaignInputSha256"],
        "items": [
            {
                "repositoryId": record["repositoryId"],
                "candidateId": record["candidateId"],
                "stratum": stratum,
                "recordSha256": record["recordSha256"],
                "qualityStatus": record.get("qualityReport", {}).get("status"),
                "proposalReuseIntentIds": record.get("proposalReuseIntentIds", []),
                "experimentalIntentIds": record.get("experimentalIntentIds", []),
                "providerAttemptCount": len(record.get("attempts", [])),
                "workbenchCursor": record["candidateId"],
                "reviewStatus": "awaiting_explicit_maintainer_review",
            }
            for stratum, record in selected
        ],
        "executionBoundary": _execution_boundary(),
    }
    sample["sampleSha256"] = digest(sample)
    return sample


def _duplicate_count(values: list[str]) -> int:
    counts = Counter(values)
    return sum(count - 1 for count in counts.values() if count > 1)


def _execution_boundary() -> dict[str, bool]:
    return {
        "repositoryCodeExecuted": False,
        "packageManagerInvoked": False,
        "reviewerDecisionCreated": False,
        "materializationPerformed": False,
        "canonicalizationPerformed": False,
        "specpmMutated": False,
        "registryMutated": False,
        "publicationPerformed": False,
    }


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read P55-T10C JSON: {path.name}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"P55-T10C JSON must be an object: {path.name}")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _digest_without(value: dict[str, Any], key: str) -> str:
    return digest({name: item for name, item in value.items() if name != key})
