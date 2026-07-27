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
    reserve_dispatch,
    write_campaign_checkpoint,
)
from spec_harvester.mass_corpus_source_manifest import read_mass_corpus_selection_metadata
from spec_harvester.source_manifest import read_repository_source_manifests

P53_WAVE_REPORT_FILENAME = "p53-t6-codex-spark-wave-1-report.json"
P53_CHECKPOINT_FILENAME = "p53-campaign-checkpoint.json"
WAVE_ONE = "wave-1"
MAX_CONCURRENCY = 2


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


class P53CodexSparkWave:
    def __init__(self, options: P53CodexSparkWaveOptions) -> None:
        self.options = options
        self.static_root = options.out / "static-only"
        self.checkpoint_path = options.out / P53_CHECKPOINT_FILENAME
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
        sources = wave_one_sources(self.options.inputs, self.options.metadata)
        plan = read_json(self.options.campaign_plan)
        checkpoint = build_campaign_checkpoint(
            plan,
            tuple(
                CampaignRepositoryInput(
                    repository_id=source["id"],
                    input_digest=input_digest(source),
                    wave_id=WAVE_ONE,
                )
                for source in sources
            ),
        )
        self.options.out.mkdir(parents=True, exist_ok=True)
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
            return self.write_report(sources, static, checkpoint, [], "failed")
        records = {record["id"]: record for record in static["repositories"]}
        schema = self.calibration.schema()
        version = self.calibration.codex_executor.version()
        outcomes: list[dict[str, Any]] = []
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
                    outcomes.append(record)
                    checkpoint = apply_repository_result(
                        checkpoint,
                        repository_id,
                        outcome=outcome_kind(record),
                        token_used=0,
                        wall_time_seconds=duration_seconds(record),
                    )
                    write_campaign_checkpoint(self.checkpoint_path, checkpoint)
        status = (
            "passed" if all(item.get("status") == "completed" for item in outcomes) else "failed"
        )
        return self.write_report(sources, static, checkpoint, outcomes, status)

    def write_report(
        self,
        sources: list[dict[str, Any]],
        static: dict[str, Any],
        checkpoint: dict[str, Any],
        outcomes: list[dict[str, Any]],
        status: str,
    ) -> dict[str, Any]:
        report = {
            "apiVersion": "spec-harvester.p53-codex-spark-wave/v0",
            "kind": "SpecHarvesterP53CodexSparkWaveReport",
            "schemaVersion": 1,
            "phase": "P53",
            "task": "P53-T6",
            "status": status,
            "wave": WAVE_ONE,
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
            "checkpointSummary": {
                "completed": sum(
                    item["state"] == "completed" for item in checkpoint["repositories"]
                ),
                "terminalFailed": sum(
                    item["state"] == "terminal_failed" for item in checkpoint["repositories"]
                ),
                "stop": checkpoint["stop"],
            },
            "privacy": calibration.privacy_record(),
            "authority": "producer_wave_evidence_only",
        }
        calibration.write_json(self.options.out / P53_WAVE_REPORT_FILENAME, report)
        return report


def wave_one_sources(inputs: Path, metadata_path: Path) -> list[dict[str, Any]]:
    metadata = read_mass_corpus_selection_metadata(metadata_path)
    positions = {item["id"]: item["position"] for item in metadata["repositories"]}
    selected = [
        item for item in read_repository_source_manifests(inputs) if positions[item["id"]] <= 25
    ]
    if len(selected) != 25 or [positions[item["id"]] for item in selected] != list(range(1, 26)):
        raise ValueError("P53-T6 requires exactly positions 1 through 25")
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


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("P53 campaign plan must be a JSON object")
    return value


def run_p53_codex_spark_wave(options: P53CodexSparkWaveOptions) -> dict[str, Any]:
    return P53CodexSparkWave(options).run()
