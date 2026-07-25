from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from spec_harvester import controlled_calibration as calibration
from spec_harvester.controlled_calibration import (
    DEFAULT_CODEX_COMMAND,
    DEFAULT_CODEX_MODEL,
    DEFAULT_CODEX_SCHEMA_PATH,
    DEFAULT_CODEX_TIMEOUT_SECONDS,
    ControlledCalibrationOptions,
    quality_metrics,
    static_repository_records,
)
from spec_harvester.final_corpus_checkout_readiness import (
    MAXIMUM_REPOSITORY_COUNT,
    MINIMUM_REPOSITORY_COUNT,
)
from spec_harvester.final_corpus_static_only_gate import read_json_object, static_execution_boundary
from spec_harvester.model_json_repair import DEFAULT_JSON_REPAIR_MAX_ATTEMPTS
from spec_harvester.producer_receipt import digest_record, sha256_file
from spec_harvester.source_manifest import read_repository_source_manifests

FINAL_CORPUS_CODEX_SPARK_GATE_API_VERSION = "spec-harvester.final-corpus-codex-spark-gate/v0"
FINAL_CORPUS_CODEX_SPARK_GATE_KIND = "SpecHarvesterFinalCorpusCodexSparkGateReport"
FINAL_CORPUS_CODEX_SPARK_GATE_REPORT_FILENAME = "final-corpus-codex-spark-gate-report.json"
CODEX_DIRNAME = "codex-spark"


@dataclass(frozen=True)
class FinalCorpusCodexSparkGateOptions:
    inputs: Path
    readiness: Path
    readiness_sha256: str
    out: Path
    codex_command: str = DEFAULT_CODEX_COMMAND
    codex_model: str = DEFAULT_CODEX_MODEL
    codex_schema: Path = DEFAULT_CODEX_SCHEMA_PATH
    codex_timeout_seconds: float = DEFAULT_CODEX_TIMEOUT_SECONDS
    run_codex: bool = True
    json_repair_max_attempts: int = DEFAULT_JSON_REPAIR_MAX_ATTEMPTS


class FinalCorpusCodexSparkGate:
    def __init__(
        self,
        options: FinalCorpusCodexSparkGateOptions,
        *,
        batch_runner: Callable = calibration.run_autonomous_candidate_batch,
        codex_runner: Callable[[list[Any], bool, dict[str, Any]], dict[str, Any]] | None = None,
        codex_executor: calibration.CodexSparkExecutor | None = None,
        checkout_head_reader: Callable[[Path], str | None] | None = None,
        checkout_dirty_reader: Callable[[Path], str | None] | None = None,
    ) -> None:
        self.options = options
        self.batch_runner = batch_runner
        self._codex_runner = codex_runner
        self._calibration = calibration.ControlledCalibration(
            ControlledCalibrationOptions(
                inputs=options.inputs,
                out=options.out,
                codex_command=options.codex_command,
                codex_model=options.codex_model,
                codex_schema=options.codex_schema,
                codex_timeout_seconds=options.codex_timeout_seconds,
                run_codex=options.run_codex,
                run_lm_studio=False,
                json_repair_max_attempts=options.json_repair_max_attempts,
            ),
            batch_runner=self._batch_wrapper,
            codex_executor=codex_executor,
            checkout_head_reader=checkout_head_reader,
            checkout_dirty_reader=checkout_dirty_reader,
        )

    def _batch_wrapper(
        self, options: calibration.AutonomousCandidateBatchOptions
    ) -> dict[str, Any]:
        return self.batch_runner(options)

    @property
    def static_root(self) -> Path:
        return self.options.out / "static-only"

    def run(self) -> dict[str, Any]:
        sources = read_repository_source_manifests(self.options.inputs)
        source_by_id = {
            calibration.string_value(item.get("id")): item
            for item in sources
            if item.get("id") is not None
        }
        readiness = read_json_object(self.options.readiness, "P52-T6 readiness report")
        readiness_digest = sha256_file(self.options.readiness)
        self._validate_readiness(readiness, readiness_digest, source_by_id)
        validation = self._validate_sources(sources)
        schema = self._calibration.schema() if self.options.run_codex else {}
        self.options.out.mkdir(parents=True, exist_ok=True)
        static = self._run_static()
        static_repositories = calibration.list_value(static.get("repositories"))
        static_passed = static.get("status") == "passed"
        if self._codex_runner is not None:
            codex = self._codex_runner(static_repositories, static_passed, schema)
        else:
            codex = self._calibration.codex_control(static_repositories, static_passed, schema)
        metrics = quality_metrics(static, codex)
        threshold_met = all(item["passed"] for item in metrics.values())
        controls_completed = static_passed and codex.get("status") == "completed"
        unlocked = threshold_met and controls_completed and validation
        report = {
            "apiVersion": FINAL_CORPUS_CODEX_SPARK_GATE_API_VERSION,
            "kind": FINAL_CORPUS_CODEX_SPARK_GATE_KIND,
            "schemaVersion": 1,
            "phase": "P52",
            "task": "P52-T7",
            "status": "passed" if unlocked else "failed",
            "readiness": {
                "path": str(self.options.readiness),
                "digest": digest_record(readiness_digest),
                "status": "passed",
            },
            "staticOnly": {
                "status": static.get("status"),
                "report": static_report_record(
                    self.options.out,
                    self.static_root / calibration.AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME,
                ),
                "repositories": static_repository_records(static),
            },
            "codexSpark": codex,
            "sourceCoverage": {
                "manifestCount": len(sources),
                "resultCount": len(static_repositories),
                "resultIds": sorted(
                    calibration.string_value(item.get("id"))
                    for item in static_repositories
                    if isinstance(item, dict)
                ),
            },
            "qualityMetrics": metrics,
            "decision": {
                "p52T8Unlocked": unlocked,
                "selectedDecision": "unlock_p52_t8" if unlocked else "block_p52_t8",
            },
            "executionBoundary": {
                "static": static_execution_boundary(static, self.options.out),
                "codex": {
                    "status": codex.get("status"),
                    "provider": coding_control_value(codex.get("provider")),
                    "repositoryRecordCount": len(calibration.list_value(codex.get("repositories"))),
                },
            },
            "authority": "producer_static_and_codex_gate_evidence_only",
            "nonAuthority": {
                "acceptsPackages": False,
                "acceptsRelations": False,
                "publishesRegistryMetadata": False,
                "seedsBaselines": False,
                "removesPreviewOnly": False,
                "changesRegistryTruth": False,
            },
            "controlPolicy": {
                "prohibited": [
                    "repository_clone_or_fetch",
                    "package_execution",
                    "dependency_installation",
                    "adapter_execution",
                ]
            },
        }
        report_path = self.options.out / FINAL_CORPUS_CODEX_SPARK_GATE_REPORT_FILENAME
        report_path.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return report

    def _run_static(self) -> dict[str, Any]:
        return self.batch_runner(
            calibration.AutonomousCandidateBatchOptions(
                inputs=self.options.inputs,
                out=self.static_root,
                skip_ai=True,
                repository_profile_selection="auto",
            )
        )

    def _validate_sources(self, sources: list[dict[str, Any]]) -> bool:
        if not MINIMUM_REPOSITORY_COUNT <= len(sources) <= MAXIMUM_REPOSITORY_COUNT:
            raise ValueError("P52-T7 requires between 50 and 100 repositories")
        ids = [calibration.string_value(item.get("id")) for item in sources]
        if any(not identifier for identifier in ids) or len(ids) != len(set(ids)):
            raise ValueError("P52-T7 requires unique non-empty repository ids")
        for source in sources:
            revision = calibration.string_value(source.get("revision"))
            if not revision or source.get("ref") is not None or len(revision) != 40:
                raise ValueError(
                    f"P52-T7 source {calibration.string_value(source.get('id'))!r} must use "
                    "a pinned 40-char revision"
                )
        return True

    def _validate_readiness(
        self,
        readiness: dict[str, Any],
        observed_digest: str,
        source_by_id: dict[str, dict[str, Any]],
    ) -> None:
        if readiness.get("task") != "P52-T6" or readiness.get("status") != "passed":
            raise ValueError("P52-T6 readiness report is not passed")
        decision = calibration.mapping_value(readiness.get("decision"))
        if decision.get("p52T7Unlocked") is not True:
            raise ValueError("P52-T6 readiness does not unlock P52-T7")
        if observed_digest != self.options.readiness_sha256:
            raise ValueError("P52-T6 readiness digest mismatch")
        readiness_records = [
            record
            for record in calibration.list_value(readiness.get("repositories"))
            if isinstance(record, dict)
        ]
        readiness_ids = [calibration.string_value(record.get("id")) for record in readiness_records]
        if set(readiness_ids) != set(source_by_id):
            raise ValueError("P52-T6 readiness source ids do not match the final corpus")
        for record in readiness_records:
            if record.get("status") != "ready":
                raise ValueError("P52-T6 readiness contains blocked repositories")
            source_id = calibration.string_value(record.get("id"))
            source = source_by_id[source_id]
            if source.get("repository") != record.get("repository"):
                raise ValueError("P52-T6 readiness contains drifted repository")
            if source.get("revision") != record.get("revision"):
                raise ValueError("P52-T6 readiness contains drifted revision")


def run_final_corpus_codex_spark_gate(
    options: FinalCorpusCodexSparkGateOptions,
) -> dict[str, Any]:
    return FinalCorpusCodexSparkGate(options).run()


def static_report_record(output_root: Path, report_path: Path) -> dict[str, str] | None:
    if not report_path.is_file():
        return None
    return {
        "path": str(report_path.relative_to(output_root)),
        "digest": digest_record(sha256_file(report_path)),
    }


def coding_control_value(value: Any) -> dict[str, Any]:
    payload = calibration.mapping_value(value)
    return {
        "kind": payload.get("kind"),
        "model": payload.get("model"),
        "sandbox": payload.get("sandbox"),
        "execution": payload.get("execution"),
    }
