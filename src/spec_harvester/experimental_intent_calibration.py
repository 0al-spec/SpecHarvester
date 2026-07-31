from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from spec_harvester.controlled_calibration import git_dirty_status, git_head
from spec_harvester.experimental_intent_policy import (
    load_experimental_intent_decision_policy,
)
from spec_harvester.semantic_author_input_pack import (
    SemanticAuthorInputPackOptions,
    build_semantic_author_input_pack,
)
from spec_harvester.semantic_author_pass import (
    SemanticAuthorPassError,
    SemanticAuthorPassOptions,
    SemanticAuthorProvider,
    contains_semantic_focus_term,
    run_semantic_author_pass,
)
from spec_harvester.semantic_proposal_quality import (
    evaluate_semantic_proposal_quality,
    load_semantic_author_quality_policy,
)
from spec_harvester.source_manifest import read_repository_source_manifests

CALIBRATION_API_VERSION = "spec-harvester.experimental-intent-calibration/v0"
CALIBRATION_KIND = "SpecHarvesterExperimentalIntentCalibration"
EXPECTED_REPOSITORY_IDS = (
    "rtk-ai-rtk",
    "openai-codex",
    "burntsushi-ripgrep",
    "thedotmack-claude-mem",
)
FALSE_NOVELTY_CODES = {
    "experimental_intent_false_novelty_risk",
    "experimental_intent_retains_generic_reuse",
}


@dataclass(frozen=True)
class ExperimentalIntentCalibrationOptions:
    timeout_seconds: float = 240.0
    provider_max_attempts: int = 2
    json_repair_max_attempts: int = 1
    max_output_bytes: int = 256 * 1024


def load_calibration_plan(path: Path) -> dict[str, Any]:
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read experimental intent calibration plan: {exc}") from exc
    validate_calibration_plan(plan)
    return plan


def validate_calibration_plan(plan: dict[str, Any]) -> None:
    if not isinstance(plan, dict):
        raise ValueError("experimental intent calibration plan must be an object")
    if (
        plan.get("apiVersion") != "spec-harvester.experimental-intent-calibration-plan/v0"
        or plan.get("kind") != "SpecHarvesterExperimentalIntentCalibrationPlan"
        or plan.get("schemaVersion") != 1
        or plan.get("authority") != "maintainer_frozen_target_calibration_plan"
        or plan.get("taskId") != "P55-T10B"
        or plan.get("provider")
        != {
            "providerId": "gpt-5.3-codex-spark",
            "modelId": "gpt-5.3-codex-spark",
            "transport": "codex_exec",
        }
    ):
        raise ValueError("experimental intent calibration plan identity is invalid")
    targets = plan.get("targets")
    if plan.get("targetRubric") != {
        "path": "tests/fixtures/targeted_semantic_calibration/p55-t9-target-rubric.example.json",
        "sha256": "3346390190767c20c8067c0aa3dc71860173d044c4175afda88d27387e6c34ff",
    }:
        raise ValueError("experimental intent calibration rubric binding is invalid")
    if (
        not isinstance(targets, list)
        or [item.get("repositoryId") for item in targets if isinstance(item, dict)]
        != list(EXPECTED_REPOSITORY_IDS)
        or any(item.get("expectedDecision") != "experimental_required" for item in targets)
    ):
        raise ValueError("experimental intent calibration target set is invalid")
    if plan.get("attemptBudget") != {
        "providerMaxAttempts": 2,
        "jsonRepairMaxAttemptsPerProviderAttempt": 1,
    }:
        raise ValueError("experimental intent calibration attempt budget is invalid")
    if plan.get("successCriteria") != {
        "minimumEvidenceSupportedExperimentalIntentCount": 1,
        "maximumFalseNoveltyCount": 0,
        "maximumDuplicateExperimentalIntentIdCount": 0,
        "requireAllTargetsTerminal": True,
        "requireFrozenQualityGates": True,
    }:
        raise ValueError("experimental intent calibration success criteria are invalid")
    boundary = plan.get("executionBoundary")
    if not isinstance(boundary, dict) or any(boundary.values()):
        raise ValueError("experimental intent calibration execution boundary is invalid")
    if plan.get("planSha256") != digest_without(plan, "planSha256"):
        raise ValueError("experimental intent calibration plan digest is stale")


def run_experimental_intent_calibration(
    *,
    plan_path: Path,
    rubric_path: Path,
    candidate_root: Path,
    source_root: Path,
    source_manifest_dir: Path,
    provider: SemanticAuthorProvider,
    output_path: Path,
    options: ExperimentalIntentCalibrationOptions | None = None,
) -> dict[str, Any]:
    options = options or ExperimentalIntentCalibrationOptions()
    plan = load_calibration_plan(plan_path)
    _validate_options(options, plan)
    if (
        provider.provider_id != plan["provider"]["providerId"]
        or getattr(provider, "model", plan["provider"]["modelId"]) != plan["provider"]["modelId"]
    ):
        raise ValueError("calibration provider or model does not match the frozen plan")
    rubric = _load_rubric(rubric_path, plan)
    quality_policy = load_semantic_author_quality_policy()
    decision_policy = load_experimental_intent_decision_policy()
    if plan["qualityPolicySha256"] != quality_policy["policySha256"]:
        raise ValueError("calibration quality policy binding is stale")
    if plan["decisionPolicySha256"] != decision_policy["policySha256"]:
        raise ValueError("calibration decision policy binding is stale")
    revisions = _source_revisions(source_manifest_dir)
    targets_by_id = {target["repositoryId"]: target for target in rubric["targets"]}
    records: list[dict[str, Any]] = []
    for target_plan in plan["targets"]:
        repository_id = target_plan["repositoryId"]
        target = targets_by_id[repository_id]
        source = source_root / repository_id
        _validate_source_checkout(source, revisions[repository_id])
        candidate = _resolve_candidate(candidate_root, repository_id, target["candidateDirectory"])
        records.append(
            _run_target(
                target=target,
                expected_decision=target_plan["expectedDecision"],
                candidate=candidate,
                source=source,
                provider=provider,
                options=options,
            )
        )
    summary = summarize_calibration(records, quality_policy)
    criteria = plan["successCriteria"]
    unblocked = (
        summary["completedCount"] == len(EXPECTED_REPOSITORY_IDS)
        and all(item["passed"] for item in summary["frozenQualityGates"].values())
        and summary["evidenceSupportedExperimentalIntentCount"]
        >= criteria["minimumEvidenceSupportedExperimentalIntentCount"]
        and summary["falseNoveltyCount"] <= criteria["maximumFalseNoveltyCount"]
        and summary["duplicateExperimentalIntentIdCount"]
        <= criteria["maximumDuplicateExperimentalIntentIdCount"]
    )
    report = {
        "apiVersion": CALIBRATION_API_VERSION,
        "kind": CALIBRATION_KIND,
        "schemaVersion": 1,
        "authority": "targeted_calibration_evidence_only",
        "taskId": "P55-T10B",
        "planSha256": plan["planSha256"],
        "rubricSha256": canonical_digest(rubric),
        "qualityPolicySha256": quality_policy["policySha256"],
        "decisionPolicySha256": decision_policy["policySha256"],
        "sourceManifestSha256": hashlib.sha256(
            (source_manifest_dir / "repositories.yml").read_bytes()
        ).hexdigest(),
        "sourceRevisions": revisions,
        "provider": plan["provider"],
        "scope": {
            "fullFrozenTargetSet": True,
            "repositoryIds": list(EXPECTED_REPOSITORY_IDS),
        },
        "summary": summary,
        "records": records,
        "decision": {
            "p55T10CUnblocked": unblocked,
            "thresholdsRedefined": False,
            "maintainerDecisionRecorded": False,
        },
        "privacy": {
            "rawPromptsPersisted": False,
            "rawResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "credentialsPersisted": False,
            "machineLocalPathsPersisted": False,
        },
        "executionBoundary": {
            "repositoryCodeExecuted": False,
            "packageManagerInvoked": False,
            "materializationPerformed": False,
            "canonicalizationPerformed": False,
            "specpmMutated": False,
            "registryMutated": False,
            "publicationPerformed": False,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def target_metrics(
    target: dict[str, Any],
    semantic_pass: dict[str, Any],
    quality: dict[str, Any],
    expected_decision: str,
) -> dict[str, Any]:
    proposal = semantic_pass["proposal"]
    claims = proposal["claims"]
    claims_by_id = {claim["id"]: claim for claim in claims}
    purpose = " ".join(claim["text"] for claim in claims if claim["kind"] == "purpose")
    purpose_matches = [
        any(contains_semantic_focus_term(purpose, term) for term in group)
        for group in target["purposeConceptGroups"]
    ]
    purpose_accurate = all(purpose_matches)
    experiments = [
        item for item in proposal["intentDecisions"] if item["state"] == "proposed_experimental"
    ]
    reuses = [item for item in proposal["intentDecisions"] if item["state"] == "proposed_reuse"]
    nearby_differentiated = bool(experiments) and all(
        item["nearbyIntentIds"]
        and len(item["nearbyIntentIds"]) == len(item["nearbyIntentClaimIds"])
        and all(
            claims_by_id.get(claim_id, {}).get("kind") == "nearby_intent_difference"
            for claim_id in item["nearbyIntentClaimIds"]
        )
        for item in experiments
    )
    evidence_supported_experimental = sum(
        purpose_accurate
        and nearby_differentiated
        and claims_by_id[item["userNeedClaimId"]]["evidence"]
        and all(claims_by_id[claim_id]["evidence"] for claim_id in item["nearbyIntentClaimIds"])
        and all(claims_by_id[claim_id]["evidence"] for claim_id in item["nonGoalClaimIds"])
        for item in experiments
    )
    diagnostic_codes = {item["code"] for item in quality["diagnostics"]}
    false_novelty = bool(diagnostic_codes & FALSE_NOVELTY_CODES)
    justified_reuse_count = sum(
        claims_by_id[item["rationaleClaimId"]]["kind"] == "nearby_intent_difference"
        and bool(claims_by_id[item["rationaleClaimId"]]["evidence"])
        for item in reuses
    )
    edit_reasons = []
    if not purpose_accurate:
        edit_reasons.append("purpose_inaccurate")
    if not quality["metrics"]["schemaValid"] or quality["metrics"]["evidenceSupportRate"] < 0.95:
        edit_reasons.append("schema_or_evidence_invalid")
    if expected_decision == "experimental_required" and not evidence_supported_experimental:
        edit_reasons.append("experimental_intent_missing_or_unsupported")
    if false_novelty:
        edit_reasons.append("false_novelty")
    return {
        "purposeAccurate": purpose_accurate,
        "purposeConceptGroupMatches": purpose_matches,
        "schemaValid": quality["metrics"]["schemaValid"],
        "evidenceSupportRate": quality["metrics"]["evidenceSupportRate"],
        "observedIntentReuseCount": len(reuses),
        "justifiedReuseCount": justified_reuse_count,
        "experimentalIntentCount": len(experiments),
        "evidenceSupportedExperimentalIntentCount": evidence_supported_experimental,
        "nearbyIntentDifferentiated": nearby_differentiated,
        "falseNovelty": false_novelty,
        "reviewerEditReasons": edit_reasons,
        "reviewerEditBurdenRate": round(len(edit_reasons) / 4, 4),
    }


def summarize_calibration(
    records: list[dict[str, Any]], quality_policy: dict[str, Any]
) -> dict[str, Any]:
    completed = [record for record in records if record["status"] == "completed"]
    total = len(records)

    def rate(name: str) -> float:
        return round(sum(bool(item["metrics"][name]) for item in completed) / total, 4)

    def average(name: str) -> float:
        return round(sum(float(item["metrics"][name]) for item in completed) / total, 4)

    failed_count = total - len(completed)
    metrics = {
        "purposeAccuracyRate": rate("purposeAccurate"),
        "evidenceSupportedClaimRate": average("evidenceSupportRate"),
        "schemaValidProposalRate": rate("schemaValid"),
        "reviewerEditBurdenRate": round(
            (
                sum(float(item["metrics"]["reviewerEditBurdenRate"]) for item in completed)
                + failed_count
            )
            / total,
            4,
        ),
    }
    frozen_gates = {
        name: {**rule, "value": metrics[name], "passed": _passes(metrics[name], rule)}
        for name, rule in quality_policy["metrics"].items()
    }
    experimental_ids = [
        decision["intentId"]
        for record in completed
        for decision in record["intentDecisions"]
        if decision["state"] == "proposed_experimental"
    ]
    stems = [".".join(intent_id.split(".")[:-1]) for intent_id in experimental_ids]
    return {
        "targetCount": total,
        "completedCount": len(completed),
        "failedCount": failed_count,
        "providerAttemptCount": sum(item["providerAttemptCount"] for item in records),
        "metrics": metrics,
        "frozenQualityGates": frozen_gates,
        "experimentalIntentProposalRate": round(
            sum(item["metrics"]["experimentalIntentCount"] > 0 for item in completed) / total,
            4,
        ),
        "evidenceSupportedExperimentalIntentCount": sum(
            item["metrics"]["evidenceSupportedExperimentalIntentCount"] for item in completed
        ),
        "justifiedReuseCount": sum(item["metrics"]["justifiedReuseCount"] for item in completed),
        "nearbyIntentDifferentiationRate": rate("nearbyIntentDifferentiated"),
        "falseNoveltyCount": sum(item["metrics"]["falseNovelty"] for item in completed),
        "duplicateExperimentalIntentIdCount": _duplicate_count(experimental_ids),
        "duplicateExperimentalSemanticStemCount": _duplicate_count(stems),
    }


def observed_catalog(manifest: dict[str, Any]) -> dict[str, Any]:
    intent_ids = sorted(
        item
        for item in manifest.get("index", {}).get("provides", {}).get("intents", [])
        if isinstance(item, str)
    )
    content = {
        "sourcePath": "generated/observed-intents.json",
        "intents": [
            {"intentId": intent_id, "sha256": hashlib.sha256(intent_id.encode()).hexdigest()}
            for intent_id in intent_ids
        ],
    }
    return {**content, "sha256": canonical_digest(content)}


def _run_target(
    *,
    target: dict[str, Any],
    expected_decision: str,
    candidate: Path,
    source: Path,
    provider: SemanticAuthorProvider,
    options: ExperimentalIntentCalibrationOptions,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="p55-t10b-") as temporary:
        workspace = _prepare_workspace(candidate, source, Path(temporary))
        manifest = yaml.safe_load((workspace / "specpm.yaml").read_text(encoding="utf-8"))
        pack = build_semantic_author_input_pack(
            workspace,
            observed_catalog(manifest),
            options=SemanticAuthorInputPackOptions(document_paths=("README.md",)),
        )
        failures = []
        for attempt in range(1, options.provider_max_attempts + 1):
            try:
                semantic_pass = run_semantic_author_pass(
                    pack,
                    provider,
                    options=SemanticAuthorPassOptions(
                        timeout_seconds=options.timeout_seconds,
                        max_output_bytes=options.max_output_bytes,
                        json_repair_max_attempts=options.json_repair_max_attempts,
                    ),
                    semantic_focus={
                        "purposeConceptGroups": target["purposeConceptGroups"],
                        "specificTerms": target["specificTerms"],
                    },
                )
                quality = evaluate_semantic_proposal_quality(pack, semantic_pass)
                if semantic_pass["providerReceipt"]["modelId"] != "gpt-5.3-codex-spark":
                    raise SemanticAuthorPassError(
                        "calibration provider receipt model does not match the frozen plan"
                    )
                return {
                    "repositoryId": target["repositoryId"],
                    "candidateId": pack["candidateId"],
                    "sourceBundleSha256": pack["sourceBundleSha256"],
                    "status": "completed",
                    "expectedDecision": expected_decision,
                    "providerAttemptCount": attempt,
                    "priorAttemptFailureCodes": failures,
                    "qualityStatus": quality["status"],
                    "qualityDiagnosticCodes": [item["code"] for item in quality["diagnostics"]],
                    "proposalSha256": semantic_pass["proposal"]["proposalSha256"],
                    "decisionPolicySha256": semantic_pass["experimentalIntentDecisionPolicy"][
                        "policySha256"
                    ],
                    "providerReceipt": semantic_pass["providerReceipt"],
                    "claims": semantic_pass["proposal"]["claims"],
                    "intentDecisions": semantic_pass["proposal"]["intentDecisions"],
                    "metrics": target_metrics(target, semantic_pass, quality, expected_decision),
                }
            except (SemanticAuthorPassError, ValueError) as exc:
                failures.append(str(exc)[:500])
    return {
        "repositoryId": target["repositoryId"],
        "candidateId": candidate.name,
        "status": "failed",
        "expectedDecision": expected_decision,
        "providerAttemptCount": options.provider_max_attempts,
        "failureCodes": failures,
    }


def _prepare_workspace(candidate: Path, source: Path, root: Path) -> Path:
    workspace = root / "workspace"
    workspace.mkdir()
    shutil.copy2(candidate / "specpm.yaml", workspace / "specpm.yaml")
    shutil.copytree(candidate / "specs", workspace / "specs")
    shutil.copy2(candidate / "harvest.json", workspace / "harvest.json")
    readme = next(
        (
            path
            for name in ("README.md", "README.markdown", "README")
            if (path := source / name).is_file()
        ),
        None,
    )
    if readme is None:
        raise ValueError(f"README evidence is unavailable: {source.name}")
    shutil.copy2(readme, workspace / "README.md")
    return workspace


def _resolve_candidate(root: Path, repository_id: str, directory: str) -> Path:
    choices = (root / repository_id / directory, root / repository_id / "candidate" / directory)
    for choice in choices:
        if (choice / "specpm.yaml").is_file() and (choice / "specs").is_dir():
            return choice
    raise ValueError(f"target candidate is unavailable: {repository_id}/{directory}")


def _validate_source_checkout(source: Path, expected_revision: str) -> None:
    if not source.is_dir() or source.is_symlink():
        raise ValueError(f"target source checkout is unavailable: {source.name}")
    if git_head(source) != expected_revision:
        raise ValueError(f"target source revision mismatch: {source.name}")
    dirty = git_dirty_status(source)
    if dirty is None:
        raise ValueError(f"target source status is unavailable: {source.name}")
    if dirty:
        raise ValueError(f"target source checkout is dirty: {source.name}")


def _source_revisions(manifest_dir: Path) -> dict[str, str]:
    expected = set(EXPECTED_REPOSITORY_IDS)
    revisions = {
        record["id"]: record["revision"]
        for record in read_repository_source_manifests(manifest_dir)
        if record.get("id") in expected and isinstance(record.get("revision"), str)
    }
    if set(revisions) != expected:
        raise ValueError("calibration sources are absent from the pinned manifest")
    return {repository_id: revisions[repository_id] for repository_id in EXPECTED_REPOSITORY_IDS}


def _load_rubric(path: Path, plan: dict[str, Any]) -> dict[str, Any]:
    try:
        rubric = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read targeted semantic rubric: {exc}") from exc
    if canonical_digest(rubric) != plan["targetRubric"]["sha256"]:
        raise ValueError("targeted semantic rubric digest is stale")
    repository_ids = [item.get("repositoryId") for item in rubric.get("targets", [])]
    if repository_ids != list(EXPECTED_REPOSITORY_IDS):
        raise ValueError("targeted semantic rubric target order is invalid")
    return rubric


def _validate_options(options: ExperimentalIntentCalibrationOptions, plan: dict[str, Any]) -> None:
    if (
        options.provider_max_attempts != plan["attemptBudget"]["providerMaxAttempts"]
        or options.json_repair_max_attempts
        != plan["attemptBudget"]["jsonRepairMaxAttemptsPerProviderAttempt"]
        or options.timeout_seconds <= 0
        or options.max_output_bytes <= 0
    ):
        raise ValueError("calibration execution options violate the frozen plan")


def _passes(value: float, rule: dict[str, Any]) -> bool:
    return {
        "greater_than_or_equal": value >= rule["threshold"],
        "less_than_or_equal": value <= rule["threshold"],
        "equal": value == rule["threshold"],
    }[rule["operator"]]


def _duplicate_count(values: list[str]) -> int:
    return sum(count - 1 for count in Counter(values).values() if count > 1)


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def digest_without(value: dict[str, Any], key: str) -> str:
    return canonical_digest({name: item for name, item in value.items() if name != key})
