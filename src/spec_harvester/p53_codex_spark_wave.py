from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester import controlled_calibration as calibration
from spec_harvester.autonomous_candidate_batch import (
    AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME,
    AutonomousCandidateBatchOptions,
    run_autonomous_candidate_batch,
)
from spec_harvester.mass_campaign_orchestration import (
    CampaignRepositoryInput,
    apply_repository_result,
    build_campaign_checkpoint,
    read_campaign_checkpoint,
    recover_interrupted_reservations,
    reserve_dispatch,
    stop_campaign,
    write_campaign_checkpoint,
)
from spec_harvester.mass_corpus_source_manifest import read_mass_corpus_selection_metadata
from spec_harvester.source_manifest import read_repository_source_manifests

P53_CHECKPOINT_FILENAME = "p53-campaign-checkpoint.json"
P53_OUTCOMES_FILENAME = "p53-codex-spark-wave-outcomes.json"
WAVE_ONE = "wave-1"
WAVE_TWO = "wave-2"
WAVE_THREE = "wave-3"
WAVE_FOUR = "wave-4"
MAX_CONCURRENCY = 2
WAVE_CONFIGURATION = {
    WAVE_ONE: {
        "task": "P53-T6",
        "positions": range(1, 26),
        "reportFilename": "p53-t6-codex-spark-wave-1-report.json",
    },
    WAVE_TWO: {
        "task": "P53-T8",
        "positions": range(26, 51),
        "reportFilename": "p53-t8-codex-spark-wave-2-report.json",
    },
    WAVE_THREE: {
        "task": "P53-T10",
        "positions": range(51, 76),
        "reportFilename": "p53-t10-codex-spark-wave-3-report.json",
    },
    WAVE_FOUR: {
        "task": "P53-T12",
        "positions": range(76, 101),
        "reportFilename": "p53-t12-codex-spark-wave-4-report.json",
    },
}


@dataclass(frozen=True)
class P53CodexSparkWaveOptions:
    inputs: Path
    metadata: Path
    campaign_plan: Path
    out: Path
    codex_command: str = calibration.DEFAULT_CODEX_COMMAND
    codex_model: str = calibration.DEFAULT_CODEX_MODEL
    codex_schema: Path = calibration.DEFAULT_CODEX_SCHEMA_PATH
    codex_timeout_seconds: float = calibration.DEFAULT_CODEX_TIMEOUT_SECONDS
    wave: str = WAVE_ONE
    scale_out_decision: Path | None = None


class P53CodexSparkWave:
    def __init__(self, options: P53CodexSparkWaveOptions) -> None:
        self.options = options
        if options.wave not in WAVE_CONFIGURATION:
            raise ValueError(f"P53 supports only configured waves: {', '.join(WAVE_CONFIGURATION)}")
        self.static_root = options.out / "static-only"
        self.checkpoint_path = options.out / P53_CHECKPOINT_FILENAME
        self.outcomes_path = options.out / P53_OUTCOMES_FILENAME
        self.calibration = calibration.ControlledCalibration(
            calibration.ControlledCalibrationOptions(
                inputs=options.inputs,
                out=options.out,
                codex_command=options.codex_command,
                codex_model=options.codex_model,
                codex_schema=options.codex_schema,
                codex_timeout_seconds=options.codex_timeout_seconds,
                run_lm_studio=False,
                run_codex=True,
            )
        )

    def run(self) -> dict[str, Any]:
        plan = read_json(self.options.campaign_plan)
        scale_out_decision = self.validate_scale_out_decision(plan)
        sources = wave_sources(self.options.inputs, self.options.metadata, self.options.wave)
        expected_checkpoint = build_campaign_checkpoint(
            plan,
            tuple(
                CampaignRepositoryInput(
                    repository_id=source["id"],
                    input_digest=input_digest(source),
                    wave_id=self.options.wave,
                )
                for source in sources
            ),
        )
        self.options.out.mkdir(parents=True, exist_ok=True)
        checkpoint = self.resume_or_create_checkpoint(expected_checkpoint)
        if scale_out_decision is not None:
            checkpoint["unlockedWave"] = self.options.wave
            write_campaign_checkpoint(self.checkpoint_path, checkpoint)
        static = run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=self.options.inputs,
                out=self.static_root,
                selected_ids=tuple(source["id"] for source in sources),
                skip_ai=True,
                repository_profile_selection="auto",
                verify_checkout_revisions=True,
            )
        )
        if static.get("status") != "passed":
            return self.write_report(
                sources, static, checkpoint, [], "failed", {}, scale_out_decision
            )
        records = {record["id"]: record for record in static["repositories"]}
        schema = self.calibration.schema()
        version = self.calibration.codex_executor.version()
        outcomes = self.load_outcomes({source["id"] for source in sources})
        while True:
            checkpoint, identifiers = reserve_dispatch(checkpoint)
            write_campaign_checkpoint(self.checkpoint_path, checkpoint)
            if not identifiers:
                break
            with ThreadPoolExecutor(max_workers=MAX_CONCURRENCY) as pool:
                futures = {
                    pool.submit(
                        self.calibration.codex_repository_record, records[item], schema, version
                    ): item
                    for item in identifiers
                }
                for future in as_completed(futures):
                    repository_id = futures[future]
                    record = future.result()
                    outcomes[repository_id] = record
                    self.write_outcomes(outcomes)
                    checkpoint = apply_repository_result(
                        checkpoint,
                        repository_id,
                        outcome=outcome_kind(record),
                        token_used=reserved_token_charge(checkpoint, repository_id),
                        wall_time_seconds=duration_seconds(record),
                    )
                    write_campaign_checkpoint(self.checkpoint_path, checkpoint)
        outcome_records = list(outcomes.values())
        quality = quality_metrics(plan, static, outcome_records)
        completed = all(item["state"] == "completed" for item in checkpoint["repositories"])
        if completed and not quality["passed"]:
            checkpoint = stop_campaign(checkpoint, "quality_threshold_failure")
            write_campaign_checkpoint(self.checkpoint_path, checkpoint)
        stop = checkpoint["stop"]
        natural_wave_budget_exhaustion = (
            completed and isinstance(stop, dict) and stop.get("trigger") == "wave_budget_limit"
        )
        status = (
            "passed"
            if completed and quality["passed"] and (stop is None or natural_wave_budget_exhaustion)
            else "failed"
        )
        return self.write_report(
            sources, static, checkpoint, outcome_records, status, quality, scale_out_decision
        )

    def validate_scale_out_decision(self, plan: dict[str, Any]) -> dict[str, Any] | None:
        if self.options.wave == WAVE_ONE:
            if self.options.scale_out_decision is not None:
                raise ValueError("P53 wave-1 does not accept a scale-out decision artifact")
            return None
        if self.options.scale_out_decision is None:
            task = "P53-T7" if self.options.wave == WAVE_TWO else "P53-T9"
            raise ValueError(
                f"P53 {self.options.wave} requires a validated {task} scale-out decision artifact"
            )
        payload = read_json_object(self.options.scale_out_decision)
        expected = {
            WAVE_TWO: (
                "P53-T7",
                WAVE_ONE,
                WAVE_TWO,
                "unlock_wave-2_only",
                "P53-T6",
                "wave1Minimum",
            ),
            WAVE_THREE: (
                "P53-T9",
                WAVE_TWO,
                WAVE_THREE,
                "unlock_wave-3_only",
                "P53-T8",
                "waves2To4Minimum",
            ),
            WAVE_FOUR: (
                "P53-T11",
                WAVE_THREE,
                WAVE_FOUR,
                "unlock_wave-4_only",
                "P53-T10",
                "waves2To4Minimum",
            ),
        }[self.options.wave]
        required = {
            "apiVersion": "spec-harvester.p53-scale-out-decision/v0",
            "kind": "SpecHarvesterP53ScaleOutDecision",
            "phase": "P53",
            "task": expected[0],
            "status": "passed",
            "fromWave": expected[1],
            "toWave": expected[2],
            "decision": expected[3],
        }
        if any(payload.get(key) != value for key, value in required.items()):
            raise ValueError(f"P53 {self.options.wave} scale-out decision is not authorized")
        source_report = calibration.mapping_value(payload.get("sourceWaveReport"))
        source_digest = source_report.get("sha256")
        source_path = source_report.get("path")
        if (
            source_report.get("task") != expected[4]
            or not isinstance(source_digest, str)
            or len(source_digest) != 64
            or any(character not in "0123456789abcdef" for character in source_digest)
        ):
            raise ValueError(
                f"P53 {self.options.wave} scale-out decision has no valid source digest"
            )
        if not isinstance(source_path, str) or not Path(source_path).is_file():
            raise ValueError(
                f"P53 {self.options.wave} scale-out decision lacks durable source evidence"
            )
        if calibration.sha256(Path(source_path).read_bytes()).hexdigest() != source_digest:
            raise ValueError(f"P53 {self.options.wave} source evidence digest mismatch")
        source_payload = read_json_object(Path(source_path))
        if source_payload.get("task") != expected[4] or source_payload.get("status") != "passed":
            raise ValueError(f"P53 {self.options.wave} source evidence is not a passed prior wave")
        metrics = calibration.mapping_value(payload.get("qualityMetrics"))
        thresholds = calibration.mapping_value(plan.get("qualityMetrics"))
        if (
            not metric_at_least(
                metrics, "codexCompletionRate", thresholds, "codexCompletionRateMinimum"
            )
            or not metric_at_least(metrics, "schemaValidRate", thresholds, "schemaValidRateMinimum")
            or not metric_at_least(
                metrics, "repositorySpecificRate", thresholds, "repositorySpecificRateMinimum"
            )
            or not metric_at_most(
                metrics, "unsupportedClaimRate", thresholds, "unsupportedClaimRateMaximum"
            )
            or metrics.get("terminalFailureCount") != 0
        ):
            raise ValueError("P53 wave-2 scale-out decision does not meet P53 quality thresholds")
        review = calibration.mapping_value(payload.get("humanReview"))
        reviewed_ids = review.get("reviewedRepositoryIds")
        required_reviews = calibration.mapping_value(thresholds.get("humanReview")).get(expected[5])
        if (
            not isinstance(required_reviews, int)
            or review.get("minimumRequired") != required_reviews
            or not isinstance(reviewed_ids, list)
            or len(reviewed_ids) < required_reviews
            or len(set(reviewed_ids)) != len(reviewed_ids)
            or not all(
                isinstance(repository_id, str) and repository_id for repository_id in reviewed_ids
            )
        ):
            raise ValueError(
                f"P53 {self.options.wave} scale-out decision has insufficient review evidence"
            )
        completed_ids = {
            item.get("id")
            for item in calibration.mapping_value(source_payload.get("codexSpark")).get(
                "repositories", []
            )
            if isinstance(item, dict) and item.get("status") == "completed"
        }
        if not set(reviewed_ids).issubset(completed_ids):
            raise ValueError(
                f"P53 {self.options.wave} reviews are not backed by completed outcomes"
            )
        correction = calibration.mapping_value(payload.get("correctionDisposition"))
        if self.options.wave == WAVE_THREE:
            artifacts = calibration.mapping_value(correction.get("artifacts"))
            if any(
                not valid_sha256(calibration.mapping_value(artifacts.get(name)).get("sha256"))
                for name in ("followUpReport", "correctedProposal", "targetedStaticReport")
            ):
                raise ValueError("P53 wave-3 scale-out decision lacks corrective evidence digests")
        return {
            "path": str(self.options.scale_out_decision),
            "sha256": calibration.sha256(self.options.scale_out_decision.read_bytes()).hexdigest(),
            "task": payload["task"],
            "sourceWaveReport": source_report,
            "correctionDisposition": correction if self.options.wave == WAVE_THREE else None,
        }

    def resume_or_create_checkpoint(self, expected: dict[str, Any]) -> dict[str, Any]:
        if not self.checkpoint_path.is_file():
            write_campaign_checkpoint(self.checkpoint_path, expected)
            return expected
        checkpoint = read_campaign_checkpoint(self.checkpoint_path)
        if checkpoint["runId"] != expected["runId"]:
            raise ValueError("P53-T6 checkpoint run identity does not match pinned inputs")
        checkpoint = recover_interrupted_reservations(checkpoint)
        write_campaign_checkpoint(self.checkpoint_path, checkpoint)
        return checkpoint

    def load_outcomes(self, source_ids: set[str]) -> dict[str, dict[str, Any]]:
        if not self.outcomes_path.is_file():
            return {}
        payload = read_json_object(self.outcomes_path)
        records = payload.get("repositories")
        if not isinstance(records, list):
            raise ValueError("P53-T6 outcomes must contain repositories")
        outcomes = {
            item["id"]: item
            for item in records
            if (
                isinstance(item, dict)
                and isinstance(item.get("id"), str)
                and item["id"] in source_ids
            )
        }
        if len(outcomes) != len(records):
            raise ValueError("P53-T6 outcomes contain an unknown or duplicate repository")
        return outcomes

    def write_outcomes(self, outcomes: dict[str, dict[str, Any]]) -> None:
        calibration.write_json(
            self.outcomes_path,
            {
                "apiVersion": "spec-harvester.p53-codex-spark-outcomes/v0",
                "kind": "SpecHarvesterP53CodexSparkOutcomes",
                "schemaVersion": 1,
                "repositories": sorted(outcomes.values(), key=lambda item: item["id"]),
            },
        )

    def write_report(
        self,
        sources: list[dict[str, Any]],
        static: dict[str, Any],
        checkpoint: dict[str, Any],
        outcomes: list[dict[str, Any]],
        status: str,
        quality: dict[str, Any],
        scale_out_decision: dict[str, Any] | None,
    ) -> dict[str, Any]:
        report = {
            "apiVersion": "spec-harvester.p53-codex-spark-wave/v0",
            "kind": "SpecHarvesterP53CodexSparkWaveReport",
            "schemaVersion": 1,
            "phase": "P53",
            "task": WAVE_CONFIGURATION[self.options.wave]["task"],
            "status": status,
            "wave": self.options.wave,
            "sourceIds": [source["id"] for source in sources],
            "static": {
                "status": static.get("status"),
                "report": str(self.static_root / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME),
            },
            "codexSpark": {
                "provider": "codex_exec_external_model_output",
                "model": self.options.codex_model,
                "maxConcurrency": MAX_CONCURRENCY,
                "repositories": sorted(outcomes, key=lambda item: item["id"]),
                "authority": "proposal_only_not_registry_acceptance",
            },
            "checkpoint": str(self.checkpoint_path),
            "outcomes": str(self.outcomes_path),
            "checkpointSummary": {
                "completed": sum(
                    item["state"] == "completed" for item in checkpoint["repositories"]
                ),
                "terminalFailed": sum(
                    item["state"] == "terminal_failed" for item in checkpoint["repositories"]
                ),
                "stop": checkpoint["stop"],
            },
            "quality": quality,
            "scaleOutDecision": scale_out_decision,
            "privacy": calibration.privacy_record(),
            "authority": "producer_wave_evidence_only",
        }
        calibration.write_json(
            self.options.out / WAVE_CONFIGURATION[self.options.wave]["reportFilename"], report
        )
        return report


def wave_one_sources(inputs: Path, metadata_path: Path) -> list[dict[str, Any]]:
    return wave_sources(inputs, metadata_path, WAVE_ONE)


def wave_sources(inputs: Path, metadata_path: Path, wave: str) -> list[dict[str, Any]]:
    if wave not in WAVE_CONFIGURATION:
        raise ValueError(f"P53 supports only configured waves: {', '.join(WAVE_CONFIGURATION)}")
    metadata = read_mass_corpus_selection_metadata(metadata_path)
    positions = {item["id"]: item["position"] for item in metadata["repositories"]}
    waves = {item["id"]: item["wave"] for item in metadata["repositories"]}
    selected = [
        item for item in read_repository_source_manifests(inputs) if waves[item["id"]] == wave
    ]
    selected.sort(key=lambda item: positions[item["id"]])
    expected_positions = list(WAVE_CONFIGURATION[wave]["positions"])
    if (
        len(selected) != len(expected_positions)
        or [positions[item["id"]] for item in selected] != expected_positions
    ):
        raise ValueError(
            f"P53 {wave} requires exactly positions "
            f"{expected_positions[0]} through {expected_positions[-1]}"
        )
    return selected


def input_digest(source: dict[str, Any]) -> str:
    encoded = json.dumps(source, sort_keys=True, separators=(",", ":")).encode()
    return calibration.sha256(encoded).hexdigest()


def outcome_kind(record: dict[str, Any]) -> str:
    if record.get("status") == "completed":
        return "completed"
    if record.get("failure") in {
        "codex_timeout",
        "codex_nonzero_exit",
        "codex_final_message_missing",
    }:
        return "timeout"
    if record.get("failure") in {
        "codex_final_message_invalid_json",
        "codex_final_message_schema_invalid",
    }:
        return "schema_repairable_failure"
    return "terminal_failure"


def duration_seconds(record: dict[str, Any]) -> int:
    receipt = calibration.mapping_value(record.get("receipt"))
    return max(0, int(receipt.get("durationMs", 0)) // 1000)


def reserved_token_charge(checkpoint: dict[str, Any], repository_id: str) -> int:
    record = next(item for item in checkpoint["repositories"] if item["id"] == repository_id)
    return int(record["reservedTokens"])


def quality_metrics(
    plan: dict[str, Any], static: dict[str, Any], outcomes: list[dict[str, Any]]
) -> dict[str, Any]:
    thresholds = plan["qualityMetrics"]
    static_records = static.get("repositories", [])
    if not isinstance(static_records, list):
        static_records = []
    values = {
        "staticCompletionRate": rate(
            sum(item.get("status") == "passed" for item in static_records),
            len(static_records),
        ),
        "codexCompletionRate": rate(
            sum(item.get("status") == "completed" for item in outcomes), len(outcomes)
        ),
        "schemaValidRate": rate(
            sum(item.get("schemaValid") is True for item in outcomes), len(outcomes)
        ),
        "repositorySpecificRate": rate(
            sum(item.get("repositorySpecific") is True for item in outcomes), len(outcomes)
        ),
        "unsupportedClaimRate": rate(
            sum(int(item.get("unsupportedClaimCount", 0)) > 0 for item in outcomes), len(outcomes)
        ),
    }
    passed = (
        values["staticCompletionRate"] >= thresholds["staticCompletionRateMinimum"]
        and values["codexCompletionRate"] >= thresholds["codexCompletionRateMinimum"]
        and values["schemaValidRate"] >= thresholds["schemaValidRateMinimum"]
        and values["repositorySpecificRate"] >= thresholds["repositorySpecificRateMinimum"]
        and values["unsupportedClaimRate"] <= thresholds["unsupportedClaimRateMaximum"]
    )
    return {"passed": passed, "metrics": values}


def rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def metric_at_least(
    metrics: dict[str, Any], metric: str, thresholds: dict[str, Any], threshold: str
) -> bool:
    value = metrics.get(metric)
    minimum = thresholds.get(threshold)
    return (
        isinstance(value, (int, float)) and isinstance(minimum, (int, float)) and value >= minimum
    )


def metric_at_most(
    metrics: dict[str, Any], metric: str, thresholds: dict[str, Any], threshold: str
) -> bool:
    value = metrics.get(metric)
    maximum = thresholds.get(threshold)
    return (
        isinstance(value, (int, float)) and isinstance(maximum, (int, float)) and value <= maximum
    )


def valid_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def read_json(path: Path) -> dict[str, Any]:
    value = read_json_object(path)
    if not isinstance(value, dict):
        raise ValueError("P53 campaign plan must be a JSON object")
    return value


def read_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("P53 JSON artifact must be an object")
    return value


def run_p53_codex_spark_wave(options: P53CodexSparkWaveOptions) -> dict[str, Any]:
    return P53CodexSparkWave(options).run()
