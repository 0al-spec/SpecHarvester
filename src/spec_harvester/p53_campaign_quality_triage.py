from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from spec_harvester.controlled_calibration import mapping_value, write_json

EXPECTED_WAVES = {
    "wave-1": ("P53-T6", range(1, 26)),
    "wave-2": ("P53-T8", range(26, 51)),
    "wave-3": ("P53-T10", range(51, 76)),
    "wave-4": ("P53-T12", range(76, 101)),
}
RETRYABLE_FAILURES = {
    "codex_timeout",
    "codex_nonzero_exit",
    "codex_final_message_missing",
    "codex_final_message_invalid_json",
    "codex_final_message_schema_invalid",
}
CORRECTED_OUTCOME = "schema_valid_repository_specific_zero_unsupported_claims"


@dataclass(frozen=True)
class P53CampaignQualityTriageOptions:
    metadata: Path
    campaign_plan: Path
    wave_reports: tuple[Path, ...]
    corrections: tuple[Path, ...]
    output: Path


def build_p53_campaign_quality_triage(
    options: P53CampaignQualityTriageOptions,
) -> dict[str, Any]:
    metadata = read_json_object(options.metadata)
    plan = read_json_object(options.campaign_plan)
    validate_campaign_inputs(metadata, plan)
    repositories = metadata.get("repositories")
    if not isinstance(repositories, list) or len(repositories) != 100:
        raise ValueError("P53-T13 requires exactly 100 frozen metadata repositories")
    ordered_sources = sorted(
        (mapping_value(item) for item in repositories),
        key=lambda item: int(item.get("position", 0)),
    )
    if [item.get("position") for item in ordered_sources] != list(range(1, 101)):
        raise ValueError("P53-T13 metadata must contain frozen positions 1 through 100")
    source_ids = [item.get("id") for item in ordered_sources]
    if not all(isinstance(item, str) and item for item in source_ids):
        raise ValueError("P53-T13 metadata contains an invalid source identity")
    if len(set(source_ids)) != 100:
        raise ValueError("P53-T13 metadata contains duplicate source identities")

    reports = load_wave_reports(options.wave_reports)
    corrections = load_corrections(options.corrections)
    effective_records: list[dict[str, Any]] = []
    source_artifacts: list[dict[str, Any]] = []
    stop_events: list[dict[str, Any]] = []
    corrected_count = 0
    duration_ms = 0

    for wave, (task, positions) in EXPECTED_WAVES.items():
        report_path, report = reports[wave]
        expected_ids = [source_ids[position - 1] for position in positions]
        validate_wave_report(report, wave=wave, task=task, expected_ids=expected_ids)
        source_artifacts.append(artifact_record(report_path, task))
        stop = mapping_value(report.get("checkpointSummary")).get("stop")
        if isinstance(stop, dict):
            stop_events.append({"wave": wave, **stop})
        records = mapping_value(report.get("codexSpark")).get("repositories")
        assert isinstance(records, list)
        records_by_id = {mapping_value(item).get("id"): mapping_value(item) for item in records}
        for repository_id in expected_ids:
            original = records_by_id[repository_id]
            correction = corrections.get(repository_id)
            effective = effective_outcome(original, correction)
            duration_ms += receipt_duration_ms(original)
            if correction is not None:
                corrected_count += 1
                duration_ms += receipt_duration_ms(effective)
            effective_records.append(
                repository_triage_record(
                    repository_id,
                    wave,
                    original,
                    effective,
                    correction,
                )
            )

    if set(corrections) - set(source_ids):
        raise ValueError("P53-T13 correction references a source outside the frozen corpus")
    dispositions = {
        "selectedForAuthorReview": sum(
            item["disposition"] == "selected_for_author_review" for item in effective_records
        ),
        "deferred": sum(item["disposition"] == "deferred" for item in effective_records),
        "doNotPromote": sum(item["disposition"] == "do_not_promote" for item in effective_records),
    }
    metrics = aggregate_metrics(effective_records)
    thresholds = mapping_value(plan.get("qualityMetrics"))
    quality_passed = quality_meets_thresholds(metrics, thresholds)
    budget = mapping_value(plan.get("budgetPolicy"))
    result = {
        "apiVersion": "spec-harvester.p53-campaign-quality-triage/v0",
        "kind": "SpecHarvesterP53CampaignQualityTriage",
        "schemaVersion": 1,
        "phase": "P53",
        "task": "P53-T13",
        "status": (
            "passed"
            if quality_passed
            and dispositions["deferred"] == 0
            and dispositions["doNotPromote"] == 0
            else "review_required"
        ),
        "sourceArtifacts": {
            "metadata": artifact_record(options.metadata, "P53-T3"),
            "campaignPlan": artifact_record(options.campaign_plan, "P53-T1"),
            "waveReports": source_artifacts,
            "corrections": [
                artifact_record(path, read_json_object(path).get("task", "unknown"))
                for path in options.corrections
            ],
        },
        "summary": {
            "repositoryCount": 100,
            "waveCount": 4,
            "correctedRepositoryCount": corrected_count,
            "dispositionCounts": dispositions,
        },
        "quality": {
            "passed": quality_passed,
            "metrics": metrics,
            "thresholds": thresholds,
        },
        "usage": {
            "aggregateDurationMs": duration_ms,
            "actualTokenUsage": {
                "status": "not_reported_by_worker_receipts",
                "tokens": None,
            },
            "budgetCeilings": {
                "campaignMaxTokens": budget.get("campaignMaxTokens"),
                "perRepositoryMaxTokens": budget.get("perRepositoryMaxTokens"),
            },
            "retryAccounting": {
                "correctiveRerunCount": corrected_count,
                "classifiedRetryCount": None,
                "status": "not_persisted_in_wave_reports",
            },
        },
        "stopPolicyEvents": stop_events,
        "repositories": effective_records,
        "privacy": {
            "rawPromptsPersisted": False,
            "rawProviderResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "secretsPersisted": False,
        },
        "authority": "producer_triage_evidence_only",
        "nonGoals": [
            "registry_acceptance",
            "package_acceptance",
            "relation_acceptance",
            "automatic_maintainer_disposition",
        ],
    }
    options.output.parent.mkdir(parents=True, exist_ok=True)
    write_json(options.output, result)
    return result


def load_wave_reports(paths: tuple[Path, ...]) -> dict[str, tuple[Path, dict[str, Any]]]:
    if len(paths) != 4:
        raise ValueError("P53-T13 requires exactly four wave reports")
    reports: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in paths:
        report = read_json_object(path)
        wave = report.get("wave")
        if not isinstance(wave, str) or wave not in EXPECTED_WAVES or wave in reports:
            raise ValueError("P53-T13 wave reports contain an unknown or duplicate wave")
        reports[wave] = (path, report)
    if set(reports) != set(EXPECTED_WAVES):
        raise ValueError("P53-T13 wave report set is incomplete")
    return reports


def validate_wave_report(
    report: dict[str, Any], *, wave: str, task: str, expected_ids: list[str]
) -> None:
    required = {
        "apiVersion": "spec-harvester.p53-codex-spark-wave/v0",
        "kind": "SpecHarvesterP53CodexSparkWaveReport",
        "phase": "P53",
        "task": task,
        "wave": wave,
        "authority": "producer_wave_evidence_only",
    }
    if any(report.get(key) != value for key, value in required.items()):
        raise ValueError(f"P53-T13 {wave} report is not authorized wave evidence")
    if report.get("status") not in {"passed", "failed"}:
        raise ValueError(f"P53-T13 {wave} report has no terminal status")
    if report.get("sourceIds") != expected_ids:
        raise ValueError(f"P53-T13 {wave} does not match frozen source positions")
    if mapping_value(report.get("static")).get("status") != "passed":
        raise ValueError(f"P53-T13 {wave} static evidence did not pass")
    codex = mapping_value(report.get("codexSpark"))
    if (
        codex.get("model") != "gpt-5.3-codex-spark"
        or codex.get("authority") != "proposal_only_not_registry_acceptance"
    ):
        raise ValueError(f"P53-T13 {wave} violates the Codex Spark authority boundary")
    records = codex.get("repositories")
    if not isinstance(records, list) or len(records) != 25:
        raise ValueError(f"P53-T13 {wave} must contain exactly 25 outcomes")
    record_ids = [mapping_value(item).get("id") for item in records]
    if len(set(record_ids)) != 25 or set(record_ids) != set(expected_ids):
        raise ValueError(f"P53-T13 {wave} outcomes do not match frozen source identities")
    privacy = mapping_value(report.get("privacy"))
    required_false = (
        "rawPromptsPersisted",
        "rawModelResponsesPersisted",
        "chainOfThoughtPersisted",
        "secretsIncluded",
    )
    if any(privacy.get(key) is not False for key in required_false):
        raise ValueError(f"P53-T13 {wave} violates the privacy boundary")
    for record in records:
        receipt = mapping_value(mapping_value(record).get("receipt"))
        if any(
            receipt.get(key) is not False
            for key in ("rawPromptPersisted", "rawResponsePersisted", "chainOfThoughtPersisted")
        ):
            raise ValueError(f"P53-T13 {wave} outcome receipt violates the privacy boundary")


def load_corrections(paths: tuple[Path, ...]) -> dict[str, dict[str, Any]]:
    corrections: dict[str, dict[str, Any]] = {}
    for path in paths:
        payload = read_json_object(path)
        correction = mapping_value(payload.get("correctionDisposition"))
        repository_id = correction.get("repositoryId")
        artifacts = mapping_value(correction.get("artifacts"))
        if (
            payload.get("apiVersion") != "spec-harvester.p53-targeted-correction/v0"
            or payload.get("kind") != "SpecHarvesterP53TargetedCorrection"
            or payload.get("phase") != "P53"
            or payload.get("task") != "P53-T13"
            or payload.get("status") != "passed"
            or payload.get("authority") != "producer_targeted_correction_evidence_only"
            or not isinstance(repository_id, str)
            or not repository_id
            or repository_id in corrections
            or correction.get("replacementEvidence") != "revision_verified_targeted_rerun"
            or correction.get("effectiveOutcome") != CORRECTED_OUTCOME
            or not isinstance(payload.get("effectiveRecord"), dict)
        ):
            raise ValueError("P53-T13 correction evidence is invalid")
        for name in ("followUpReport", "correctedProposal", "targetedStaticReport"):
            validate_correction_artifact(path, mapping_value(artifacts.get(name)))
        corrections[repository_id] = {
            "task": payload.get("task"),
            "path": str(path),
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "disposition": correction,
            "effectiveRecord": payload.get("effectiveRecord"),
        }
    return corrections


def effective_outcome(
    original: dict[str, Any], correction: dict[str, Any] | None
) -> dict[str, Any]:
    if correction is None:
        return original
    replacement = correction.get("effectiveRecord")
    if not isinstance(replacement, dict):
        raise ValueError("P53-T13 correction effective record is required")
    replacement_digest = mapping_value(
        mapping_value(replacement.get("proposal")).get("digest")
    ).get("value")
    expected_digest = mapping_value(
        mapping_value(correction["disposition"].get("artifacts")).get("correctedProposal")
    ).get("sha256")
    receipt = mapping_value(replacement.get("receipt"))
    if (
        replacement.get("id") != original.get("id")
        or replacement.get("status") != "completed"
        or replacement.get("schemaValid") is not True
        or replacement.get("repositorySpecific") is not True
        or replacement.get("unsupportedClaimCount") != 0
        or replacement_digest != expected_digest
        or any(
            receipt.get(key) is not False
            for key in ("rawPromptPersisted", "rawResponsePersisted", "chainOfThoughtPersisted")
        )
    ):
        raise ValueError("P53-T13 correction effective record is invalid")
    return replacement


def repository_triage_record(
    repository_id: str,
    wave: str,
    original: dict[str, Any],
    effective: dict[str, Any],
    correction: dict[str, Any] | None,
) -> dict[str, Any]:
    disposition, reasons = classify_outcome(effective)
    record = {
        "id": repository_id,
        "wave": wave,
        "disposition": disposition,
        "reasons": reasons,
        "status": effective.get("status"),
        "schemaValid": effective.get("schemaValid") is True,
        "repositorySpecific": effective.get("repositorySpecific") is True,
        "unsupportedClaimCount": int(effective.get("unsupportedClaimCount", 0)),
        "diagnosticCodes": effective.get("diagnosticCodes", []),
        "proposal": effective.get("proposal"),
        "receipt": effective.get("receipt"),
    }
    if correction is not None:
        record["correction"] = correction
        record["originalOutcome"] = {
            "repositorySpecific": original.get("repositorySpecific"),
            "unsupportedClaimCount": original.get("unsupportedClaimCount"),
            "diagnosticCodes": original.get("diagnosticCodes", []),
            "proposal": original.get("proposal"),
            "receipt": original.get("receipt"),
        }
    return record


def classify_outcome(outcome: dict[str, Any]) -> tuple[str, list[str]]:
    status = outcome.get("status")
    failure = outcome.get("failure")
    if status != "completed":
        if failure in RETRYABLE_FAILURES:
            return "deferred", [str(failure)]
        return "do_not_promote", [str(failure or "incomplete_outcome")]
    if outcome.get("schemaValid") is not True:
        return "do_not_promote", ["schema_invalid"]
    if int(outcome.get("unsupportedClaimCount", 0)) > 0:
        return "do_not_promote", ["unsupported_claim"]
    if outcome.get("repositorySpecific") is not True:
        return "deferred", ["repository_specificity_not_established"]
    proposal_status = mapping_value(outcome.get("proposal")).get("status")
    if proposal_status not in {"completed", "warning"}:
        return "deferred", ["proposal_artifact_incomplete"]
    proposal = mapping_value(outcome.get("proposal"))
    digest = mapping_value(proposal.get("digest"))
    if (
        not isinstance(proposal.get("path"), str)
        or not proposal["path"]
        or digest.get("algorithm") != "sha256"
        or not valid_sha256(digest.get("value"))
    ):
        return "deferred", ["proposal_artifact_invalid"]
    return "selected_for_author_review", []


def validate_correction_artifact(correction_path: Path, artifact: dict[str, Any]) -> None:
    relative_path = artifact.get("path")
    expected_digest = artifact.get("sha256")
    if (
        not isinstance(relative_path, str)
        or not relative_path
        or Path(relative_path).is_absolute()
        or not valid_sha256(expected_digest)
    ):
        raise ValueError("P53-T13 correction evidence is invalid")
    artifact_path = correction_path.parent / relative_path
    if (
        not artifact_path.is_file()
        or sha256(artifact_path.read_bytes()).hexdigest() != expected_digest
    ):
        raise ValueError("P53-T13 correction artifact digest mismatch")


def receipt_duration_ms(record: dict[str, Any]) -> int:
    duration = mapping_value(record.get("receipt")).get("durationMs", 0)
    return int(duration) if isinstance(duration, int) and duration >= 0 else 0


def aggregate_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    count = len(records)
    return {
        "staticCompletionRate": 1.0,
        "codexCompletionRate": rate(sum(item["status"] == "completed" for item in records), count),
        "schemaValidRate": rate(sum(item["schemaValid"] is True for item in records), count),
        "repositorySpecificRate": rate(
            sum(item["repositorySpecific"] is True for item in records), count
        ),
        "unsupportedClaimRate": rate(
            sum(item["unsupportedClaimCount"] > 0 for item in records), count
        ),
    }


def quality_meets_thresholds(metrics: dict[str, float], thresholds: dict[str, Any]) -> bool:
    return (
        metrics["staticCompletionRate"] >= thresholds.get("staticCompletionRateMinimum", 1.0)
        and metrics["codexCompletionRate"] >= thresholds.get("codexCompletionRateMinimum", 1.0)
        and metrics["schemaValidRate"] >= thresholds.get("schemaValidRateMinimum", 1.0)
        and metrics["repositorySpecificRate"]
        >= thresholds.get("repositorySpecificRateMinimum", 1.0)
        and metrics["unsupportedClaimRate"] <= thresholds.get("unsupportedClaimRateMaximum", 0.0)
    )


def artifact_record(path: Path, task: Any) -> dict[str, Any]:
    return {
        "task": task,
        "path": str(path),
        "sha256": sha256(path.read_bytes()).hexdigest(),
    }


def validate_campaign_inputs(metadata: dict[str, Any], plan: dict[str, Any]) -> None:
    metadata_required = {
        "apiVersion": "spec-harvester.mass-corpus-selection-metadata/v0",
        "kind": "SpecHarvesterMassCorpusSelectionMetadata",
        "phase": "P53",
        "task": "P53-T3",
    }
    plan_required = {
        "apiVersion": "spec-harvester.mass-repository-campaign-plan/v0",
        "kind": "SpecHarvesterMassRepositoryCampaignPlan",
        "phase": "P53",
        "task": "P53-T1",
        "authority": "producer_planning_evidence_only",
    }
    if any(metadata.get(key) != value for key, value in metadata_required.items()):
        raise ValueError("P53-T13 metadata is not authorized P53-T3 evidence")
    if any(plan.get(key) != value for key, value in plan_required.items()):
        raise ValueError("P53-T13 campaign plan is not authorized P53-T1 evidence")
    worker = mapping_value(plan.get("worker"))
    if (
        worker.get("model") != "gpt-5.3-codex-spark"
        or worker.get("invocationSurface") != "codex_exec"
        or worker.get("proposalOnly") is not True
    ):
        raise ValueError("P53-T13 campaign plan does not authorize the required worker")


def valid_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def read_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("P53-T13 JSON evidence must be an object")
    return value
