from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from spec_harvester import controlled_calibration as calibration
from spec_harvester.autonomous_candidate_batch import AutonomousCandidateBatchOptions
from spec_harvester.batch_collection import resolve_checkout
from spec_harvester.model_json_repair import DEFAULT_JSON_REPAIR_MAX_ATTEMPTS
from spec_harvester.source_manifest import read_repository_source_manifests

TWENTY_REPOSITORY_CONTROLLED_PILOT_API_VERSION = (
    "spec-harvester.twenty-repository-controlled-pilot/v0"
)
TWENTY_REPOSITORY_CONTROLLED_PILOT_KIND = "SpecHarvesterTwentyRepositoryControlledPilotReport"
TWENTY_REPOSITORY_CONTROLLED_PILOT_REPORT_FILENAME = (
    "twenty-repository-controlled-pilot-report.json"
)
PILOT_REPOSITORY_COUNT = 20


@dataclass(frozen=True)
class TwentyRepositoryControlledPilotOptions:
    """Options for one P52-T4 twenty-repository controlled pilot."""

    inputs: Path
    out: Path
    lm_studio_base_url: str = calibration.DEFAULT_LM_STUDIO_BASE_URL
    lm_studio_model: str | None = None
    codex_command: str = calibration.DEFAULT_CODEX_COMMAND
    codex_model: str = calibration.DEFAULT_CODEX_MODEL
    codex_schema: Path = calibration.DEFAULT_CODEX_SCHEMA_PATH
    codex_timeout_seconds: float = calibration.DEFAULT_CODEX_TIMEOUT_SECONDS
    json_repair_max_attempts: int = DEFAULT_JSON_REPAIR_MAX_ATTEMPTS
    max_concurrency: int = 1
    provider_logs_disabled: bool = False
    run_lm_studio: bool = True
    run_codex: bool = True


class TwentyRepositoryControlledPilot(calibration.ControlledCalibration):
    """Run P52-T4 with deterministic single-worker controls and a stop policy."""

    def __init__(
        self,
        options: TwentyRepositoryControlledPilotOptions,
        *,
        batch_runner: Callable[[AutonomousCandidateBatchOptions], dict[str, Any]] = (
            calibration.run_autonomous_candidate_batch
        ),
        codex_executor: calibration.CodexSparkExecutor | None = None,
        checkout_head_reader: Callable[[Path], str | None] | None = None,
        checkout_dirty_reader: Callable[[Path], str | None] | None = None,
    ) -> None:
        super().__init__(
            options,  # type: ignore[arg-type]
            batch_runner=batch_runner,
            codex_executor=codex_executor,
            checkout_head_reader=checkout_head_reader,
            checkout_dirty_reader=checkout_dirty_reader,
        )

    @property
    def pilot_options(self) -> TwentyRepositoryControlledPilotOptions:
        return self.options  # type: ignore[return-value]

    def run(self) -> dict[str, Any]:
        sources = self.sources()
        self.validate_pilot_options()
        self.validate_lm_studio_options()
        schema = self.schema() if self.pilot_options.run_codex else {}
        self.options.out.mkdir(parents=True, exist_ok=True)
        static = self.static_baseline()
        static_repositories = calibration.list_value(static.get("repositories"))
        static_passed = static.get("status") == "passed"
        lm_studio = self.lm_studio_control(static_repositories, static_passed)
        codex = self.codex_control(static_repositories, static_passed, schema)
        report = controlled_pilot_report(
            options=self.pilot_options,
            sources=sources,
            static=static,
            lm_studio=lm_studio,
            codex=codex,
            static_report_path=(
                self.static_root / calibration.AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME
            ),
        )
        calibration.write_json(
            self.options.out / TWENTY_REPOSITORY_CONTROLLED_PILOT_REPORT_FILENAME,
            report,
        )
        return report

    def validate_pilot_options(self) -> None:
        if self.pilot_options.max_concurrency != 1:
            raise ValueError("P52-T4 currently requires --max-concurrency 1")

    def sources(self) -> list[dict[str, Any]]:
        sources = read_repository_source_manifests(self.options.inputs)
        identifiers = [calibration.string_value(item.get("id")) for item in sources]
        if (
            len(sources) != PILOT_REPOSITORY_COUNT
            or len(set(identifiers)) != PILOT_REPOSITORY_COUNT
        ):
            raise ValueError("P52-T4 requires exactly twenty uniquely identified repositories")

        inputs_root = self.options.inputs.resolve()
        for source in sources:
            repository_id = calibration.string_value(source.get("id"))
            repository = calibration.string_value(source.get("repository"))
            revision = calibration.string_value(source.get("revision"))
            if not repository.startswith("https://github.com/"):
                raise ValueError(f"P52-T4 source {repository_id!r} must use a public GitHub URL")
            if not revision or source.get("ref") is not None:
                raise ValueError(
                    f"P52-T4 source {repository_id!r} must use a pinned revision, not a ref"
                )
            checkout = resolve_checkout(inputs_root, source)
            if self.checkout_head_reader(checkout) != revision:
                raise ValueError(f"P52-T4 checkout revision mismatch for {repository_id!r}")
            dirty_status = self.checkout_dirty_reader(checkout)
            if dirty_status is None:
                raise ValueError(f"P52-T4 checkout status unavailable for {repository_id!r}")
            if dirty_status:
                raise ValueError(f"P52-T4 checkout must be clean for {repository_id!r}")
        return sources

    def lm_studio_control(
        self,
        static_repositories: list[Any],
        static_passed: bool,
    ) -> dict[str, Any]:
        if not self.pilot_options.provider_logs_disabled:
            return calibration.skipped_control("provider_logging_not_confirmed_disabled")
        return super().lm_studio_control(static_repositories, static_passed)

    def codex_control(
        self,
        static_repositories: list[Any],
        static_passed: bool,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.pilot_options.provider_logs_disabled:
            return calibration.skipped_control("provider_logging_not_confirmed_disabled")
        return super().codex_control(static_repositories, static_passed, schema)


def run_twenty_repository_controlled_pilot(
    options: TwentyRepositoryControlledPilotOptions,
) -> dict[str, Any]:
    """Run one P52-T4 controlled pilot."""
    return TwentyRepositoryControlledPilot(options).run()


def controlled_pilot_report(
    *,
    options: TwentyRepositoryControlledPilotOptions,
    sources: list[dict[str, Any]],
    static: dict[str, Any],
    lm_studio: dict[str, Any],
    codex: dict[str, Any],
    static_report_path: Path,
) -> dict[str, Any]:
    metrics = calibration.quality_metrics(static, codex)
    thresholds_met = all(item["passed"] for item in metrics.values())
    controls_completed = (
        static.get("status") == "passed"
        and lm_studio.get("status") == "completed"
        and codex.get("status") == "completed"
    )
    decision = pilot_decision(
        provider_logs_disabled=options.provider_logs_disabled,
        static=static,
        thresholds_met=thresholds_met,
        controls_completed=controls_completed,
    )
    return {
        "apiVersion": TWENTY_REPOSITORY_CONTROLLED_PILOT_API_VERSION,
        "kind": TWENTY_REPOSITORY_CONTROLLED_PILOT_KIND,
        "schemaVersion": 1,
        "phase": "P52",
        "task": "P52-T4",
        "status": decision["status"],
        "sources": [calibration.source_record(item) for item in sources],
        "concurrency": {
            "configured": options.max_concurrency,
            "observedMaximum": 1,
            "execution": "sequential_deterministic",
            "reason": "bounded_local_provider_and_external_agent_control",
        },
        "staticOnly": {
            "status": static.get("status"),
            "report": calibration.optional_artifact_record(static_report_path, options.out),
            "repositories": calibration.static_repository_records(static),
        },
        "lmStudio": lm_studio,
        "codexSpark": codex,
        "qualityMetrics": metrics,
        "humanReview": {
            "minimumRepositorySample": 10,
            "minimumCandidateSample": 10,
            "status": "pending_after_model_controls",
        },
        "decision": decision,
        "privacy": calibration.privacy_record(),
        "authority": "producer_controlled_pilot_evidence_only",
        "nonGoals": [
            "checkout_creation_or_restore",
            "repository_clone_or_fetch",
            "dependency_installation",
            "package_manager_execution",
            "harvested_code_execution",
            "adapter_execution",
            "package_acceptance",
            "relation_acceptance",
            "registry_publication",
            "baseline_seeding",
            "preview_only_removal",
        ],
    }


def pilot_decision(
    *,
    provider_logs_disabled: bool,
    static: dict[str, Any],
    thresholds_met: bool,
    controls_completed: bool,
) -> dict[str, Any]:
    if static.get("status") != "passed":
        return {
            "status": "failed",
            "selectedDecision": "stop_static_baseline_failure",
            "p52T5Unlocked": False,
        }
    if not provider_logs_disabled:
        return {
            "status": "blocked",
            "selectedDecision": "blocked_provider_logging_precondition",
            "p52T5Unlocked": False,
        }
    if not controls_completed or not thresholds_met:
        return {
            "status": "failed",
            "selectedDecision": "stop_quality_threshold_failure",
            "p52T5Unlocked": False,
        }
    return {
        "status": "review_pending",
        "selectedDecision": "require_human_review_sample",
        "p52T5Unlocked": False,
    }
