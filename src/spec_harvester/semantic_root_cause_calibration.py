from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from spec_harvester.experimental_intent_policy import GENERIC_OBSERVED_INTENT_IDS
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

PLAN_API_VERSION = "spec-harvester.semantic-root-cause-calibration-plan/v0"
PLAN_KIND = "SpecHarvesterSemanticRootCauseCalibrationPlan"
CALIBRATION_API_VERSION = "spec-harvester.semantic-root-cause-calibration/v0"
CALIBRATION_KIND = "SpecHarvesterSemanticRootCauseCalibration"
TARGET_IDS = (
    "axios-axios",
    "n8n-io-n8n",
    "firecrawl-firecrawl",
    "bitcoin-bitcoin",
    "excalidraw-excalidraw",
    "openai-codex",
    "thedotmack-claude-mem",
    "angular-angular",
    "electron-electron",
    "freecodecamp-freecodecamp",
)
EXPECTED_PLAN_SHA256 = "376001a3ea1053afb5908bf1b7cb8125b95da4eebf2d76a6422e733f06844a11"
FALSE_NOVELTY_CODES = frozenset(
    {
        "experimental_intent_false_novelty_risk",
        "experimental_intent_retains_generic_reuse",
        "experimental_intent_overlaps_observed",
    }
)
ATTEMPT_BUDGET = {
    "providerMaxAttempts": 2,
    "jsonRepairMaxAttemptsPerProviderAttempt": 1,
    "timeoutSeconds": 300,
    "maxOutputBytes": 256 * 1024,
}
SUCCESS_CRITERIA = {
    "purposeAccuracyRate": {"operator": "greater_than_or_equal", "threshold": 0.85},
    "evidenceSupportedClaimRate": {
        "operator": "greater_than_or_equal",
        "threshold": 0.95,
    },
    "schemaValidProposalRate": {"operator": "equal", "threshold": 1.0},
    "reviewerEditBurdenRate": {
        "operator": "less_than_or_equal",
        "threshold": 0.25,
    },
    "requireGenericIntentReduction": True,
    "requireRepairedGenericCaseImprovement": True,
    "maximumFalseNoveltyCount": 0,
    "maximumDuplicateExperimentalIntentIdCount": 0,
    "maximumDuplicateExperimentalSemanticStemCount": 0,
}


def build_calibration_plan(
    *,
    source_manifest_dir: Path,
    source_root: Path,
    handoff_root: Path,
    readiness_evidence: Path,
    baseline_report_path: Path,
    baseline_archive_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], list[CampaignTarget], dict[str, dict[str, Any]]]:
    base_scope, all_targets = load_campaign_scope(
        source_manifest_dir=source_manifest_dir,
        source_root=source_root,
        handoff_root=handoff_root,
        readiness_evidence=readiness_evidence,
    )
    target_by_id = {target.repository_id: target for target in all_targets}
    if not set(TARGET_IDS) <= set(target_by_id):
        raise ValueError("P55-T10G frozen target is outside the retained corpus")

    report = _read_json(baseline_report_path)
    archive = report.get("archive")
    if (
        report.get("reportSha256") != _digest_without(report, "reportSha256")
        or not isinstance(archive, dict)
        or archive.get("sha256") != sha256_file(baseline_archive_path)
    ):
        raise ValueError("P55-T10C baseline report or archive binding is stale")
    _, members = _read_archive(
        LocalCandidateReviewCatalogOptions(
            archive=baseline_archive_path,
            expected_archive_sha256=archive["sha256"],
        )
    )
    archived_scope = _json_object(members.get("campaign-input.json", b""), "campaign-input.json")
    if archived_scope.get("taskId") != "P55-T10C" or archived_scope.get(
        "campaignInputSha256"
    ) != _digest_without(archived_scope, "campaignInputSha256"):
        raise ValueError("P55-T10C archived campaign input is stale")

    selected = [target_by_id[repository_id] for repository_id in TARGET_IDS]
    baseline_records: dict[str, dict[str, Any]] = {}
    bindings = []
    for target in selected:
        member = f"records/{target.repository_id}/campaign-record.json"
        record = _json_object(members.get(member, b""), member)
        _validate_baseline_record(record, archived_scope, target)
        baseline_records[target.repository_id] = record
        bindings.append(
            {
                **target.binding(),
                "baselineRecordSha256": record["recordSha256"],
                "baselineStatus": record["status"],
                "baselineGenericIntentIds": _generic_reuse(record),
                "baselineJsonRepairNeeded": _json_repair_needed(record),
            }
        )

    quality_policy = load_semantic_author_quality_policy()
    plan: dict[str, Any] = {
        "apiVersion": PLAN_API_VERSION,
        "kind": PLAN_KIND,
        "schemaVersion": 1,
        "authority": "maintainer_frozen_root_cause_calibration_plan",
        "taskId": "P55-T10G",
        "provider": {
            "providerId": CODEX_SPARK_MODEL,
            "modelId": CODEX_SPARK_MODEL,
            "transport": "codex_exec",
        },
        "baseline": {
            "taskId": "P55-T10C",
            "reportSha256": report["reportSha256"],
            "archiveSha256": archive["sha256"],
            "campaignInputSha256": archived_scope["campaignInputSha256"],
        },
        "currentInputBindings": {
            key: base_scope[key]
            for key in (
                "sourceManifestSha256",
                "handoffAggregateSha256",
                "p55T9AReadinessSha256",
                "specpmObservedIntentSnapshotSha256",
            )
        },
        "semanticQualityPolicySha256": quality_policy["policySha256"],
        "attemptBudget": ATTEMPT_BUDGET,
        "targets": bindings,
        "successCriteria": SUCCESS_CRITERIA,
        "executionBoundary": _execution_boundary(),
    }
    plan["planSha256"] = digest(plan)
    validate_calibration_plan(plan, require_frozen_identity=False)
    return plan, base_scope, selected, baseline_records


def validate_calibration_plan(
    plan: dict[str, Any], *, require_frozen_identity: bool = True
) -> None:
    if not isinstance(plan, dict):
        raise ValueError("P55-T10G calibration plan is invalid")
    targets = plan.get("targets")
    baseline = plan.get("baseline")
    current_bindings = plan.get("currentInputBindings")
    if (
        plan.get("apiVersion") != PLAN_API_VERSION
        or plan.get("kind") != PLAN_KIND
        or plan.get("schemaVersion") != 1
        or plan.get("taskId") != "P55-T10G"
        or plan.get("authority") != "maintainer_frozen_root_cause_calibration_plan"
        or plan.get("provider")
        != {
            "providerId": CODEX_SPARK_MODEL,
            "modelId": CODEX_SPARK_MODEL,
            "transport": "codex_exec",
        }
        or not isinstance(targets, list)
        or not all(isinstance(item, dict) for item in targets)
        or [item.get("repositoryId") for item in targets] != list(TARGET_IDS)
        or any(not _valid_target_binding(item) for item in targets)
        or not isinstance(baseline, dict)
        or baseline.get("taskId") != "P55-T10C"
        or set(baseline)
        != {
            "taskId",
            "reportSha256",
            "archiveSha256",
            "campaignInputSha256",
        }
        or any(not _sha256(baseline.get(key)) for key in set(baseline) - {"taskId"})
        or not isinstance(current_bindings, dict)
        or set(current_bindings)
        != {
            "sourceManifestSha256",
            "handoffAggregateSha256",
            "p55T9AReadinessSha256",
            "specpmObservedIntentSnapshotSha256",
        }
        or any(not _sha256(value) for value in current_bindings.values())
        or not _sha256(plan.get("semanticQualityPolicySha256"))
        or plan.get("attemptBudget") != ATTEMPT_BUDGET
        or plan.get("successCriteria") != SUCCESS_CRITERIA
        or plan.get("executionBoundary") != _execution_boundary()
        or plan.get("planSha256") != _digest_without(plan, "planSha256")
        or (require_frozen_identity and plan.get("planSha256") != EXPECTED_PLAN_SHA256)
    ):
        raise ValueError("P55-T10G calibration plan is invalid")


def write_calibration_plan(path: Path, plan: dict[str, Any]) -> None:
    validate_calibration_plan(plan)
    _write_json(path, plan)


def load_calibration_scope(
    *, plan_path: Path, **inputs: Any
) -> tuple[dict[str, Any], list[CampaignTarget], dict[str, dict[str, Any]], dict[str, Any]]:
    plan = _read_json(plan_path)
    validate_calibration_plan(plan)
    expected, base_scope, targets, baseline_records = build_calibration_plan(**inputs)
    if plan != expected:
        raise ValueError("P55-T10G frozen plan differs from current evidence bindings")
    scope = {
        **base_scope,
        "authority": "semantic_root_cause_calibration_proposal_only",
        "taskId": "P55-T10G",
        "repositoryCount": len(TARGET_IDS),
        "targets": [target.binding() for target in targets],
        "baseline": plan["baseline"],
        "successCriteria": plan["successCriteria"],
        "executionBoundary": _execution_boundary(),
    }
    scope["campaignInputSha256"] = digest(scope)
    return scope, targets, baseline_records, plan


def finalize_calibration(
    *,
    scope: dict[str, Any],
    targets: list[CampaignTarget],
    baseline_records: dict[str, dict[str, Any]],
    plan: dict[str, Any],
    work_root: Path,
    output_path: Path,
    archive_path: Path,
    purpose_assessment_path: Path,
) -> dict[str, Any]:
    records = []
    for target in targets:
        path = work_root / "records" / target.repository_id / "campaign-record.json"
        if not path.is_file():
            raise ValueError(f"P55-T10G calibration is incomplete: {target.repository_id}")
        record = _read_json(path)
        validate_campaign_record(record, scope, target)
        records.append(record)
    purpose_assessment = _read_json(purpose_assessment_path)
    _validate_purpose_assessment(purpose_assessment, records)
    report = _report(scope, plan, records, baseline_records, purpose_assessment)
    archive_sha256 = write_deterministic_archive(work_root, archive_path)
    report["archive"] = {
        "path": archive_path.name,
        "sha256": archive_sha256,
        "recordCount": len(records),
    }
    report["reportSha256"] = digest(report)
    _write_json(output_path, report)
    return report


def _report(
    scope: dict[str, Any],
    plan: dict[str, Any],
    records: list[dict[str, Any]],
    baseline_records: dict[str, dict[str, Any]],
    purpose_assessment: dict[str, Any],
) -> dict[str, Any]:
    completed = [record for record in records if record["status"] == "completed"]
    total = len(records)
    baseline_generic = sum(
        len(_generic_reuse(baseline_records[repository_id])) for repository_id in TARGET_IDS
    )
    current_generic = sum(len(_generic_reuse(record)) for record in completed)
    purpose_count = sum(item["purposeAccurate"] for item in purpose_assessment["assessments"])
    evidence_sum = sum(
        float(record["qualityReport"]["metrics"]["evidenceSupportRate"]) for record in completed
    )
    schema_count = sum(
        record["qualityReport"]["metrics"]["schemaValid"] is True for record in completed
    )
    purpose_by_id = {
        item["repositoryId"]: item["purposeAccurate"] for item in purpose_assessment["assessments"]
    }
    edit_required = sum(
        _requires_edit(record) or not purpose_by_id[record["repositoryId"]] for record in records
    )
    experimental_ids = [
        intent_id for record in completed for intent_id in record.get("experimentalIntentIds", [])
    ]
    stems = [".".join(intent_id.split(".")[:-1]) for intent_id in experimental_ids]
    false_novelty = sum(
        diagnostic.get("code") in FALSE_NOVELTY_CODES
        for record in completed
        for diagnostic in record["qualityReport"]["diagnostics"]
    )
    repaired_baseline_ids = {
        repository_id
        for repository_id, baseline in baseline_records.items()
        if _json_repair_needed(baseline) and _generic_reuse(baseline)
    }
    repaired_improved = sorted(
        record["repositoryId"]
        for record in records
        if record["repositoryId"] in repaired_baseline_ids and _repaired_case_improved(record)
    )
    metrics = {
        "purposeAccuracyRate": _rate(purpose_count, total),
        "evidenceSupportedClaimRate": round(evidence_sum / total, 4),
        "schemaValidProposalRate": _rate(schema_count, total),
        "reviewerEditBurdenRate": _rate(edit_required, total),
    }
    criteria = plan["successCriteria"]
    gates = {
        name: {
            **criteria[name],
            "value": metrics[name],
            "passed": _passes(metrics[name], criteria[name]),
        }
        for name in metrics
    }
    gates.update(
        {
            "genericIntentReduction": {
                "baseline": baseline_generic,
                "value": baseline_generic - current_generic,
                "passed": current_generic < baseline_generic,
            },
            "repairedGenericCaseImprovement": {
                "repositoryIds": repaired_improved,
                "passed": bool(repaired_improved),
            },
            "falseNovelty": {"value": false_novelty, "passed": false_novelty == 0},
            "duplicateExperimentalIntentIds": {
                "value": _duplicate_count(experimental_ids),
                "passed": _duplicate_count(experimental_ids) == 0,
            },
            "duplicateExperimentalSemanticStems": {
                "value": _duplicate_count(stems),
                "passed": _duplicate_count(stems) == 0,
            },
        }
    )
    comparisons = [
        _comparison(
            record,
            baseline_records[record["repositoryId"]],
            purpose_accurate=purpose_by_id[record["repositoryId"]],
        )
        for record in records
    ]
    passed = len(completed) == total and all(gate["passed"] for gate in gates.values())
    return {
        "apiVersion": CALIBRATION_API_VERSION,
        "kind": CALIBRATION_KIND,
        "schemaVersion": 1,
        "authority": "semantic_root_cause_calibration_evidence_only",
        "taskId": "P55-T10G",
        "planSha256": plan["planSha256"],
        "campaignInputSha256": scope["campaignInputSha256"],
        "provider": plan["provider"],
        "purposeAssessment": purpose_assessment,
        "summary": {
            "targetCount": total,
            "completedCount": len(completed),
            "failedCount": total - len(completed),
            "baselineGenericIntentReuseCount": baseline_generic,
            "currentGenericIntentReuseCount": current_generic,
            "genericIntentReductionCount": baseline_generic - current_generic,
            "jsonRepairRecordCount": sum(_json_repair_needed(record) for record in completed),
            "providerAttemptCount": sum(len(record.get("attempts", [])) for record in records),
            "failedProviderAttemptCount": sum(
                attempt.get("status") == "failed"
                for record in records
                for attempt in record.get("attempts", [])
            ),
            "experimentalIntentCount": len(experimental_ids),
            "falseNoveltyCount": false_novelty,
            "metrics": metrics,
            "gates": gates,
            "passed": passed,
            "p55T10HUnblocked": passed,
        },
        "comparisons": comparisons,
        "privacy": {
            "rawPromptsPersisted": False,
            "rawResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "credentialsPersisted": False,
            "machineLocalPathsPersisted": False,
        },
        "executionBoundary": _execution_boundary(),
    }


def _comparison(
    record: dict[str, Any], baseline: dict[str, Any], *, purpose_accurate: bool
) -> dict[str, Any]:
    diagnostics = (
        [item.get("code") for item in record.get("qualityReport", {}).get("diagnostics", [])]
        if record["status"] == "completed"
        else []
    )
    return {
        "repositoryId": record["repositoryId"],
        "baselineRecordSha256": baseline["recordSha256"],
        "currentRecordSha256": record["recordSha256"],
        "baselineStatus": baseline["status"],
        "currentStatus": record["status"],
        "baselineJsonRepairNeeded": _json_repair_needed(baseline),
        "currentJsonRepairNeeded": _json_repair_needed(record),
        "baselineGenericIntentIds": _generic_reuse(baseline),
        "currentGenericIntentIds": _generic_reuse(record),
        "currentExperimentalIntentIds": record.get("experimentalIntentIds", []),
        "currentQualityStatus": record.get("qualityReport", {}).get("status"),
        "currentDiagnosticCodes": sorted(code for code in diagnostics if isinstance(code, str)),
        "rootCause": _root_cause(record),
        "purposeAccurate": purpose_accurate,
        "reviewerEditRequired": _requires_edit(record) or not purpose_accurate,
    }


def _root_cause(record: dict[str, Any]) -> str:
    if record["status"] == "failed":
        failure_codes = " ".join(
            str(attempt.get("failureCode", "")) for attempt in record.get("attempts", [])
        )
        if "specific semantic purpose cannot use only a generic observed intent" in failure_codes:
            return "generic_only_contradiction"
        if "experimental intent identifier leaks candidate namespace" in failure_codes:
            return "experimental_intent_namespace"
        return str(record.get("failureStage") or "provider_or_schema_failure")
    diagnostics = {
        item.get("code") for item in record.get("qualityReport", {}).get("diagnostics", [])
    }
    if "specific_purpose_generic_only_contradiction" in diagnostics:
        return "generic_only_contradiction"
    if any(str(code).startswith("experimental_intent_") for code in diagnostics):
        return "experimental_intent_quality"
    if record["qualityReport"]["status"] == "eligible_for_calibration":
        return "no_blocking_quality_issue"
    return "semantic_quality_diagnostic"


def _validate_baseline_record(
    record: dict[str, Any], scope: dict[str, Any], target: CampaignTarget
) -> None:
    if (
        record.get("campaignInputSha256") != scope["campaignInputSha256"]
        or any(record.get(key) != value for key, value in target.binding().items())
        or record.get("status") not in {"completed", "failed"}
        or record.get("recordSha256") != _digest_without(record, "recordSha256")
    ):
        raise ValueError(f"P55-T10C baseline record binding is stale: {target.repository_id}")


def _validate_purpose_assessment(assessment: dict[str, Any], records: list[dict[str, Any]]) -> None:
    items = assessment.get("assessments") if isinstance(assessment, dict) else None
    expected_bindings = {record["repositoryId"]: record["recordSha256"] for record in records}
    if (
        assessment.get("apiVersion") != "spec-harvester.semantic-purpose-supervisor-assessment/v0"
        or assessment.get("kind") != "SpecHarvesterSemanticPurposeSupervisorAssessment"
        or assessment.get("authority") != "calibration_measurement_only"
        or not isinstance(items, list)
        or len(items) != len(TARGET_IDS)
        or [item.get("repositoryId") for item in items] != list(TARGET_IDS)
        or any(
            item.get("recordSha256") != expected_bindings.get(item.get("repositoryId"))
            or not isinstance(item.get("purposeAccurate"), bool)
            or not isinstance(item.get("rationale"), str)
            or not item["rationale"]
            for item in items
        )
        or assessment.get("acceptanceAuthorityGranted") is not False
        or assessment.get("assessmentSha256") != _digest_without(assessment, "assessmentSha256")
    ):
        raise ValueError("P55-T10G purpose assessment is invalid")


def _generic_reuse(record: dict[str, Any]) -> list[str]:
    return sorted(set(record.get("proposalReuseIntentIds", [])) & GENERIC_OBSERVED_INTENT_IDS)


def _json_repair_needed(record: dict[str, Any]) -> bool:
    return bool(
        record.get("status") == "completed"
        and record.get("semanticPass", {}).get("providerReceipt", {}).get("jsonRepairNeeded")
    )


def _requires_edit(record: dict[str, Any]) -> bool:
    return (
        record.get("status") != "completed"
        or record.get("qualityReport", {}).get("status") != "eligible_for_calibration"
    )


def _has_diagnostic(record: dict[str, Any], code: str) -> bool:
    return any(
        item.get("code") == code for item in record.get("qualityReport", {}).get("diagnostics", [])
    )


def _repaired_case_improved(record: dict[str, Any]) -> bool:
    if record.get("status") == "completed":
        return not _generic_reuse(record) or _has_diagnostic(
            record, "specific_purpose_generic_only_contradiction"
        )
    return _root_cause(record) == "generic_only_contradiction"


def _passes(value: float, rule: dict[str, Any]) -> bool:
    operator = rule["operator"]
    threshold = float(rule["threshold"])
    if operator == "greater_than_or_equal":
        return value >= threshold
    if operator == "less_than_or_equal":
        return value <= threshold
    if operator == "equal":
        return value == threshold
    raise ValueError(f"unsupported calibration gate operator: {operator}")


def _valid_target_binding(item: dict[str, Any]) -> bool:
    return (
        isinstance(item.get("revision"), str)
        and len(item["revision"]) == 40
        and _sha256(item.get("packetSha256"))
        and _sha256(item.get("baselineRecordSha256"))
        and isinstance(item.get("wave"), str)
        and bool(item["wave"])
        and isinstance(item.get("candidateId"), str)
        and bool(item["candidateId"])
        and item.get("baselineStatus") in {"completed", "failed"}
        and isinstance(item.get("baselineGenericIntentIds"), list)
        and all(
            isinstance(intent_id, str) and intent_id in GENERIC_OBSERVED_INTENT_IDS
            for intent_id in item["baselineGenericIntentIds"]
        )
        and isinstance(item.get("baselineJsonRepairNeeded"), bool)
    )


def _sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _duplicate_count(values: list[str]) -> int:
    return sum(count - 1 for count in Counter(values).values() if count > 1)


def _rate(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def _execution_boundary() -> dict[str, bool]:
    return {
        "repositoryCodeExecuted": False,
        "packageManagerInvoked": False,
        "candidateAccepted": False,
        "materializationPerformed": False,
        "canonicalIntentCreated": False,
        "specpmRegistryMutated": False,
        "publicationPerformed": False,
    }


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read calibration JSON {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"calibration JSON must be an object: {path.name}")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _digest_without(value: dict[str, Any], key: str) -> str:
    return hashlib.sha256(
        json.dumps(
            {name: item for name, item in value.items() if name != key},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
