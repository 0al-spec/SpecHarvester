from __future__ import annotations

import json
import subprocess
import tempfile
import time
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

from spec_harvester.autonomous_candidate_batch import (
    AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME,
    DEFAULT_LM_STUDIO_BASE_URL,
    AutonomousCandidateBatchOptions,
    run_autonomous_candidate_batch,
)
from spec_harvester.batch_collection import resolve_checkout
from spec_harvester.model_json_repair import DEFAULT_JSON_REPAIR_MAX_ATTEMPTS
from spec_harvester.package_set_ai_draft_proposal import (
    PackageSetAIDraftProposalOptions,
    build_package_set_ai_draft_proposal,
    model_request_record,
    write_package_set_ai_draft_proposal,
)
from spec_harvester.package_set_ai_enrichment import (
    PackageSetAIEnrichmentOptions,
    build_package_set_ai_enrichment_proposal,
    write_package_set_ai_enrichment_proposal,
)
from spec_harvester.producer_receipt import digest_record, sha256_file
from spec_harvester.source_manifest import read_repository_source_manifests

CONTROLLED_CALIBRATION_API_VERSION = "spec-harvester.controlled-calibration/v0"
CONTROLLED_CALIBRATION_KIND = "SpecHarvesterControlledCalibrationReport"
CONTROLLED_CALIBRATION_SCHEMA_VERSION = 1
CONTROLLED_CALIBRATION_REPORT_FILENAME = "controlled-calibration-report.json"
CONTROLLED_CALIBRATION_REPOSITORY_IDS = frozenset({"fastapi", "fastmcp", "flask", "gin", "xyflow"})
DEFAULT_CODEX_COMMAND = "codex"
DEFAULT_CODEX_MODEL = "gpt-5.3-codex-spark"
DEFAULT_CODEX_TIMEOUT_SECONDS = 300.0
DEFAULT_CODEX_SCHEMA_PATH = Path(
    "tests/fixtures/codex_spark_external_model_adapter_contract/"
    "package-set-ai-draft-final-message.schema.json"
)
STATIC_DIRNAME = "static-only"
LM_STUDIO_DIRNAME = "lm-studio"
CODEX_DIRNAME = "codex-spark"


@dataclass(frozen=True)
class ControlledCalibrationOptions:
    """Options for one P52-T3 five-repository calibration."""

    inputs: Path
    out: Path
    lm_studio_base_url: str = DEFAULT_LM_STUDIO_BASE_URL
    lm_studio_model: str | None = None
    codex_command: str = DEFAULT_CODEX_COMMAND
    codex_model: str = DEFAULT_CODEX_MODEL
    codex_schema: Path = DEFAULT_CODEX_SCHEMA_PATH
    codex_timeout_seconds: float = DEFAULT_CODEX_TIMEOUT_SECONDS
    json_repair_max_attempts: int = DEFAULT_JSON_REPAIR_MAX_ATTEMPTS
    run_lm_studio: bool = True
    run_codex: bool = True


@dataclass(frozen=True)
class CodexExecutionResult:
    """Bounded metadata retained from one external Codex invocation."""

    exit_code: int | None
    duration_ms: int
    failure: str | None = None


class CodexSparkExecutor:
    """Run Codex without retaining its stdout, stderr, or session state."""

    def __init__(self, command: str, timeout_seconds: float):
        self.command = command
        self.timeout_seconds = timeout_seconds

    def execute(self, command: list[str]) -> CodexExecutionResult:
        started = time.monotonic()
        try:
            completed = subprocess.run(  # noqa: S603
                command,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=self.timeout_seconds,
            )
        except FileNotFoundError:
            return CodexExecutionResult(
                exit_code=None,
                duration_ms=elapsed_milliseconds(started),
                failure="codex_command_unavailable",
            )
        except subprocess.TimeoutExpired:
            return CodexExecutionResult(
                exit_code=None,
                duration_ms=elapsed_milliseconds(started),
                failure="codex_timeout",
            )
        return CodexExecutionResult(
            exit_code=completed.returncode,
            duration_ms=elapsed_milliseconds(started),
            failure=None if completed.returncode == 0 else "codex_nonzero_exit",
        )

    def version(self) -> str | None:
        try:
            completed = subprocess.run(  # noqa: S603
                [self.command, "--version"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
        if completed.returncode != 0:
            return None
        value = completed.stdout.strip()
        return value[:120] if value else None


class CodexEvidenceStage:
    """Build a compact temporary evidence stage for a read-only Codex call."""

    def __init__(self, root: Path, request: dict[str, Any], inventory: Path):
        self.root = root
        self.request = request
        self.inventory = inventory

    def write(self) -> None:
        write_json(self.root / "package-set-ai-draft-request.json", self.request)
        (self.root / "workspace-inventory.json").write_bytes(self.inventory.read_bytes())
        for item in list_value(self.request.get("evidence")):
            path = relative_evidence_path(item.get("path")) if isinstance(item, dict) else None
            text = item.get("text") if isinstance(item, dict) else None
            if path is None or not isinstance(text, str):
                continue
            destination = self.root / "evidence" / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding="utf-8")

    def make_read_only(self) -> None:
        for path in sorted(self.root.rglob("*"), reverse=True):
            if path.is_file():
                path.chmod(0o444)
            elif path.is_dir():
                path.chmod(0o555)
        self.root.chmod(0o555)

    def make_writable(self) -> None:
        self.root.chmod(0o755)
        for path in self.root.rglob("*"):
            if path.is_file():
                path.chmod(0o644)
            elif path.is_dir():
                path.chmod(0o755)


class ControlledCalibration:
    """Run one bounded P52 calibration without accepting generated proposals."""

    def __init__(
        self,
        options: ControlledCalibrationOptions,
        *,
        batch_runner: Callable[[AutonomousCandidateBatchOptions], dict[str, Any]] = (
            run_autonomous_candidate_batch
        ),
        codex_executor: CodexSparkExecutor | None = None,
        checkout_head_reader: Callable[[Path], str | None] | None = None,
        checkout_dirty_reader: Callable[[Path], str | None] | None = None,
    ) -> None:
        self.options = options
        self.batch_runner = batch_runner
        self.codex_executor = codex_executor or CodexSparkExecutor(
            options.codex_command,
            options.codex_timeout_seconds,
        )
        self.checkout_head_reader = checkout_head_reader or git_head
        self.checkout_dirty_reader = checkout_dirty_reader or git_dirty_status
        self.static_root = options.out / STATIC_DIRNAME
        self.lm_studio_root = options.out / LM_STUDIO_DIRNAME
        self.codex_root = options.out / CODEX_DIRNAME

    def run(self) -> dict[str, Any]:
        sources = self.sources()
        self.validate_lm_studio_options()
        schema = self.schema() if self.options.run_codex else {}
        self.options.out.mkdir(parents=True, exist_ok=True)
        static = self.static_baseline()
        static_repositories = list_value(static.get("repositories"))
        static_passed = static.get("status") == "passed"
        lm_studio = self.lm_studio_control(static_repositories, static_passed)
        codex = self.codex_control(static_repositories, static_passed, schema)
        report = calibration_report(
            options=self.options,
            sources=sources,
            static=static,
            lm_studio=lm_studio,
            codex=codex,
            static_report_path=self.static_root / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME,
        )
        write_controlled_calibration_report(
            self.options.out / CONTROLLED_CALIBRATION_REPORT_FILENAME,
            report,
        )
        return report

    def sources(self) -> list[dict[str, Any]]:
        sources = read_repository_source_manifests(self.options.inputs)
        ids = {string_value(item.get("id")) for item in sources}
        if ids != CONTROLLED_CALIBRATION_REPOSITORY_IDS or len(sources) != 5:
            expected = ", ".join(sorted(CONTROLLED_CALIBRATION_REPOSITORY_IDS))
            actual = ", ".join(sorted(value for value in ids if value))
            raise ValueError(
                "P52-T3 requires exactly the five controlled repositories "
                f"({expected}); received ({actual})"
            )
        inputs_root = self.options.inputs.resolve()
        for source in sources:
            revision = string_value(source.get("revision"))
            if not revision or source.get("ref") is not None:
                raise ValueError(
                    f"P52-T3 source {source['id']!r} must use a pinned revision, not a ref"
                )
            checkout = resolve_checkout(inputs_root, source)
            head = self.checkout_head_reader(checkout)
            if head != revision:
                raise ValueError(f"P52-T3 checkout revision mismatch for {source['id']!r}")
            dirty_status = self.checkout_dirty_reader(checkout)
            if dirty_status is None:
                raise ValueError(f"P52-T3 checkout status unavailable for {source['id']!r}")
            if dirty_status:
                raise ValueError(f"P52-T3 checkout must be clean for {source['id']!r}")
        return sources

    def schema(self) -> dict[str, Any]:
        if self.options.codex_timeout_seconds <= 0:
            raise ValueError("--codex-timeout-seconds must be greater than zero")

        schema_path = self.options.codex_schema.resolve()
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError("P52-T3 Codex final-message schema is unavailable") from exc
        if not isinstance(schema, dict):
            raise ValueError("P52-T3 Codex final-message schema must be an object")
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001
            raise ValueError("P52-T3 Codex final-message schema is invalid") from exc
        return schema

    def validate_lm_studio_options(self) -> None:
        if not self.options.run_lm_studio:
            return
        if self.options.json_repair_max_attempts < 0:
            raise ValueError("--json-repair-max-attempts must be zero or greater")
        if not self.options.lm_studio_model:
            raise ValueError("LM Studio control requires --lm-studio-model")

    def static_baseline(self) -> dict[str, Any]:
        return self.batch_runner(
            AutonomousCandidateBatchOptions(
                inputs=self.options.inputs,
                out=self.static_root,
                skip_ai=True,
                repository_profile_selection="auto",
            )
        )

    def lm_studio_control(
        self,
        static_repositories: list[Any],
        static_passed: bool,
    ) -> dict[str, Any]:
        if not self.options.run_lm_studio:
            return skipped_control("disabled_by_operator")
        if not static_passed:
            return skipped_control("static_baseline_failed")

        records = []
        for static_record in static_repositories:
            if not isinstance(static_record, dict):
                continue
            records.append(self.lm_studio_repository_record(static_record))
        return {
            "status": control_status(records),
            "provider": {
                "kind": "openai_compatible",
                "name": "lm_studio",
                "model": self.options.lm_studio_model,
                "baseUrl": self.options.lm_studio_base_url,
                "responseFormat": "json_schema",
            },
            "repositories": records,
            "privacy": privacy_record(),
            "authority": "proposal_only_not_registry_acceptance",
        }

    def lm_studio_repository_record(self, static_record: dict[str, Any]) -> dict[str, Any]:
        repository_id = string_value(static_record.get("id"))
        inventory = self.inventory_path(repository_id)
        bundle_set = self.bundle_set_path(repository_id)
        checkout = Path(string_value(static_record.get("checkout")))
        output_root = self.lm_studio_root / repository_id
        draft_path = output_root / "package-set-ai-draft-proposal.json"
        enrichment_path = output_root / "package-set-ai-enrichment-proposal.json"
        try:
            draft = build_package_set_ai_draft_proposal(
                PackageSetAIDraftProposalOptions(
                    inventory=inventory,
                    source_checkout=checkout,
                    provider_base_url=self.options.lm_studio_base_url,
                    provider_name="lm_studio",
                    model=self.options.lm_studio_model,
                    json_repair_max_attempts=self.options.json_repair_max_attempts,
                )
            )
            write_package_set_ai_draft_proposal(draft_path, draft)
            enrichment = build_package_set_ai_enrichment_proposal(
                PackageSetAIEnrichmentOptions(
                    bundle_set=bundle_set,
                    source_checkout=checkout,
                    provider_base_url=self.options.lm_studio_base_url,
                    provider_name="lm_studio",
                    model=self.options.lm_studio_model,
                    json_repair_max_attempts=self.options.json_repair_max_attempts,
                )
            )
            write_package_set_ai_enrichment_proposal(enrichment_path, enrichment)
        except Exception:  # noqa: BLE001
            return {
                "id": repository_id,
                "status": "failed",
                "failure": "lm_studio_proposal_failed",
            }
        return {
            "id": repository_id,
            "status": status_from_proposals(draft, enrichment),
            "draft": proposal_record(draft_path, draft, self.options.out),
            "enrichment": proposal_record(enrichment_path, enrichment, self.options.out),
            "diagnosticCodes": sorted(diagnostic_codes(draft) | diagnostic_codes(enrichment)),
        }

    def codex_control(
        self,
        static_repositories: list[Any],
        static_passed: bool,
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.options.run_codex:
            return skipped_control("disabled_by_operator")
        if not static_passed:
            return skipped_control("static_baseline_failed")

        records = []
        version = self.codex_executor.version()
        for static_record in static_repositories:
            if not isinstance(static_record, dict):
                continue
            records.append(self.codex_repository_record(static_record, schema, version))
        return {
            "status": control_status(records),
            "provider": {
                "kind": "codex_exec_external_model_output",
                "model": self.options.codex_model,
                "codexCliVersion": version,
                "execution": "operator_opt_in_external",
                "sandbox": "read-only",
                "ephemeral": True,
                "ignoreUserConfig": True,
                "skipGitRepoCheck": True,
            },
            "repositories": records,
            "privacy": privacy_record(),
            "authority": "proposal_only_not_registry_acceptance",
        }

    def codex_repository_record(
        self,
        static_record: dict[str, Any],
        schema: dict[str, Any],
        version: str | None,
    ) -> dict[str, Any]:
        repository_id = string_value(static_record.get("id"))
        inventory = self.inventory_path(repository_id)
        checkout = Path(string_value(static_record.get("checkout")))
        request = model_request_record(
            PackageSetAIDraftProposalOptions(
                inventory=inventory,
                source_checkout=checkout,
            )
        )
        schema_path = self.options.codex_schema.resolve()
        receipt = {
            "model": self.options.codex_model,
            "codexCliVersion": version,
            "sandbox": "read-only",
            "schemaDigest": digest_record(sha256_file(schema_path)),
            "evidenceDigest": digest_record(sha256_json(request)),
            "rawPromptPersisted": False,
            "rawResponsePersisted": False,
            "chainOfThoughtPersisted": False,
        }
        with tempfile.TemporaryDirectory(prefix="specharvester-p52-codex-") as temporary_root:
            root = Path(temporary_root)
            stage = CodexEvidenceStage(root / "evidence", request, inventory)
            stage.root.mkdir()
            stage.write()
            stage.make_read_only()
            final_message = root / "final-message.json"
            command = self.codex_command(stage.root, schema_path, final_message)
            try:
                execution = self.codex_executor.execute(command)
            finally:
                stage.make_writable()
            receipt.update(
                {
                    "durationMs": execution.duration_ms,
                    "exitCode": execution.exit_code,
                }
            )
            if execution.failure is not None:
                return codex_failure_record(repository_id, execution.failure, receipt)
            if not final_message.is_file():
                return codex_failure_record(
                    repository_id,
                    "codex_final_message_missing",
                    receipt,
                )
            try:
                final_payload = json.loads(final_message.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return codex_failure_record(
                    repository_id,
                    "codex_final_message_invalid_json",
                    receipt,
                )
            if not isinstance(final_payload, dict):
                return codex_failure_record(
                    repository_id,
                    "codex_final_message_schema_invalid",
                    receipt,
                )
            receipt["finalOutputDigest"] = digest_record(sha256_json(final_payload))
            errors = schema_validation_errors(schema, final_payload)
            if errors:
                receipt["schemaValid"] = False
                return {
                    "id": repository_id,
                    "status": "failed",
                    "failure": "codex_final_message_schema_invalid",
                    "schemaValid": False,
                    "schemaErrors": errors,
                    "receipt": receipt,
                }
            receipt["schemaValid"] = True
            proposal_path = root / "validated-proposal.json"
            write_json(proposal_path, mapping_value(final_payload.get("proposal")))
            proposal = build_package_set_ai_draft_proposal(
                PackageSetAIDraftProposalOptions(
                    inventory=inventory,
                    source_checkout=checkout,
                    model_output=proposal_path,
                )
            )
            proposal["provider"] = {
                "kind": "codex_exec_external_model_output",
                "name": "codex",
                "model": self.options.codex_model,
                "baseUrl": None,
                "execution": "external_schema_validated",
            }
            proposal["providerReceipt"] = receipt
            durable_path = self.codex_root / repository_id / "package-set-ai-draft-proposal.json"
            write_package_set_ai_draft_proposal(durable_path, proposal)
        diagnostic_code_set = diagnostic_codes(proposal)
        return {
            "id": repository_id,
            "status": "completed" if proposal.get("status") != "failed" else "failed",
            "schemaValid": True,
            "repositorySpecific": repository_specific(proposal),
            "unsupportedClaimCount": unsupported_claim_count(diagnostic_code_set),
            "diagnosticCodes": sorted(diagnostic_code_set),
            "proposal": proposal_record(durable_path, proposal, self.options.out),
            "receipt": receipt,
        }

    def codex_command(self, stage: Path, schema: Path, final_message: Path) -> list[str]:
        return [
            self.options.codex_command,
            "exec",
            "--model",
            self.options.codex_model,
            "--sandbox",
            "read-only",
            "--ephemeral",
            "--ignore-user-config",
            "--skip-git-repo-check",
            "--cd",
            str(stage),
            "--output-schema",
            str(schema),
            "--output-last-message",
            str(final_message),
            (
                "Read only the deterministic package-set draft request and allowlisted "
                "evidence in this directory. Return exactly one JSON object matching "
                "the supplied output schema. Every evidencePaths entry must be copied "
                "verbatim from allowedEvidencePaths in the request; never cite "
                "package-set-ai-draft-request.json, an evidence/ path, or an absolute "
                "path. The supplied P52 inventory is non-empty: selectedMembers must "
                "include at least one package from packages, and a single-package "
                "inventory must select its only package rather than only excluding it. "
                "The proposal is review evidence only: do not claim package acceptance, "
                "relation acceptance, registry publication, or any fact unsupported by "
                "the supplied evidence paths."
            ),
        ]

    def inventory_path(self, repository_id: str) -> Path:
        return self.static_root / "collected" / repository_id / "workspace-inventory.json"

    def bundle_set_path(self, repository_id: str) -> Path:
        return self.static_root / "package-sets" / repository_id


def run_controlled_calibration(options: ControlledCalibrationOptions) -> dict[str, Any]:
    """Run one P52-T3 controlled calibration."""
    return ControlledCalibration(options).run()


def calibration_report(
    *,
    options: ControlledCalibrationOptions,
    sources: list[dict[str, Any]],
    static: dict[str, Any],
    lm_studio: dict[str, Any],
    codex: dict[str, Any],
    static_report_path: Path,
) -> dict[str, Any]:
    metrics = quality_metrics(static, codex)
    threshold_passed = all(item["passed"] for item in metrics.values())
    controls_completed = (
        static.get("status") == "passed"
        and lm_studio.get("status") == "completed"
        and codex.get("status") == "completed"
    )
    unlocked = threshold_passed and controls_completed
    return {
        "apiVersion": CONTROLLED_CALIBRATION_API_VERSION,
        "kind": CONTROLLED_CALIBRATION_KIND,
        "schemaVersion": CONTROLLED_CALIBRATION_SCHEMA_VERSION,
        "phase": "P52",
        "task": "P52-T3",
        "status": "passed" if unlocked else "failed",
        "sources": [source_record(item) for item in sources],
        "staticOnly": {
            "status": static.get("status"),
            "report": optional_artifact_record(static_report_path, options.out),
            "repositories": static_repository_records(static),
        },
        "lmStudio": lm_studio,
        "codexSpark": codex,
        "qualityMetrics": metrics,
        "decision": {
            "thresholdsMet": threshold_passed,
            "controlsCompleted": controls_completed,
            "p52T4Unlocked": unlocked,
            "selectedDecision": "unlock_p52_t4" if unlocked else "block_p52_t4",
        },
        "privacy": privacy_record(),
        "authority": "producer_calibration_evidence_only",
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
        "trustBoundary": [
            "Static, LM Studio, and Codex outputs are proposal-only calibration evidence.",
            "Codex receives only a temporary compact allowlisted evidence stage.",
            (
                "Raw prompts, raw model responses, Codex stdout/stderr, and session state "
                "are not persisted."
            ),
            "SpecPM remains the acceptance, relation, and registry authority.",
        ],
    }


def quality_metrics(static: dict[str, Any], codex: dict[str, Any]) -> dict[str, dict[str, Any]]:
    static_repositories = [
        item for item in list_value(static.get("repositories")) if isinstance(item, dict)
    ]
    codex_repositories = [
        item for item in list_value(codex.get("repositories")) if isinstance(item, dict)
    ]
    static_total = len(static_repositories)
    codex_total = len(codex_repositories)
    return {
        "staticCompletionRate": rate_metric(
            numerator=sum(item.get("status") == "passed" for item in static_repositories),
            denominator=static_total,
            minimum=0.95,
        ),
        "codexCompletionRate": rate_metric(
            numerator=sum(item.get("status") == "completed" for item in codex_repositories),
            denominator=codex_total,
            minimum=0.90,
        ),
        "schemaValidRate": rate_metric(
            numerator=sum(item.get("schemaValid") is True for item in codex_repositories),
            denominator=codex_total,
            minimum=0.98,
        ),
        "repositorySpecificRate": rate_metric(
            numerator=sum(item.get("repositorySpecific") is True for item in codex_repositories),
            denominator=codex_total,
            minimum=0.80,
        ),
        "unsupportedClaimRate": maximum_rate_metric(
            numerator=sum(
                int(item.get("unsupportedClaimCount", 0)) > 0 for item in codex_repositories
            ),
            denominator=codex_total,
            maximum=0.05,
        ),
    }


def rate_metric(*, numerator: int, denominator: int, minimum: float) -> dict[str, Any]:
    value = numerator / denominator if denominator else 0.0
    return {
        "value": value,
        "numerator": numerator,
        "denominator": denominator,
        "minimum": minimum,
        "passed": value >= minimum,
    }


def maximum_rate_metric(*, numerator: int, denominator: int, maximum: float) -> dict[str, Any]:
    value = numerator / denominator if denominator else 1.0
    return {
        "value": value,
        "numerator": numerator,
        "denominator": denominator,
        "maximum": maximum,
        "passed": value <= maximum,
    }


def static_repository_records(static: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    for item in list_value(static.get("repositories")):
        if not isinstance(item, dict):
            continue
        preflight = mapping_value(item.get("preflight"))
        records.append(
            {
                "id": string_value(item.get("id")),
                "status": item.get("status"),
                "preflightStatus": preflight.get("status"),
            }
        )
    return records


def source_record(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": string_value(source.get("id")),
        "repository": string_value(source.get("repository")),
        "revision": string_value(source.get("revision")),
        "sourceManifest": mapping_value(source.get("sourceManifest")),
    }


def proposal_record(path: Path, proposal: dict[str, Any], output_root: Path) -> dict[str, Any]:
    return {
        "path": relative_output_path(path, output_root),
        "digest": digest_record(sha256_file(path)),
        "status": proposal.get("status"),
        "summary": mapping_value(proposal.get("summary")),
    }


def optional_artifact_record(path: Path, output_root: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return {
        "path": relative_output_path(path, output_root),
        "digest": digest_record(sha256_file(path)),
    }


def relative_output_path(path: Path, output_root: Path) -> str:
    try:
        return path.relative_to(output_root).as_posix()
    except ValueError:
        return path.name


def status_from_proposals(draft: dict[str, Any], enrichment: dict[str, Any]) -> str:
    if draft.get("status") == "failed" or enrichment.get("status") == "failed":
        return "failed"
    return "completed"


def control_status(records: list[dict[str, Any]]) -> str:
    if not records:
        return "failed"
    return "completed" if all(item.get("status") == "completed" for item in records) else "failed"


def skipped_control(reason: str) -> dict[str, Any]:
    return {
        "status": "skipped",
        "reason": reason,
        "repositories": [],
        "privacy": privacy_record(),
        "authority": "proposal_only_not_registry_acceptance",
    }


def codex_failure_record(
    repository_id: str,
    failure: str,
    receipt: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": repository_id,
        "status": "failed",
        "failure": failure,
        "schemaValid": False,
        "repositorySpecific": False,
        "unsupportedClaimCount": 0,
        "receipt": receipt,
    }


def schema_validation_errors(
    schema: dict[str, Any], payload: dict[str, Any]
) -> list[dict[str, Any]]:
    validator = Draft202012Validator(schema)
    return [
        {
            "keyword": error.validator,
            "path": "/".join(str(part) for part in error.absolute_path),
        }
        for error in sorted(
            validator.iter_errors(payload), key=lambda item: list(item.absolute_path)
        )
    ]


def repository_specific(proposal: dict[str, Any]) -> bool:
    summary = mapping_value(proposal.get("summary"))
    validation_guard = mapping_value(proposal.get("validationGuard"))
    return (
        proposal.get("status") != "failed"
        and validation_guard.get("status") == "passed"
        and int(summary.get("selectedMemberCount", 0)) > 0
        and not unsupported_claim_count(diagnostic_codes(proposal))
    )


def unsupported_claim_count(codes: set[str]) -> int:
    unsupported_codes = {
        "model_evidence_path_unsupported",
        "model_package_id_mismatch",
        "package_set_id_mismatch",
        "selected_member_unknown",
        "relation_target_unknown",
    }
    return len(codes & unsupported_codes)


def diagnostic_codes(proposal: dict[str, Any]) -> set[str]:
    return {
        string_value(item.get("code"))
        for item in list_value(proposal.get("diagnostics"))
        if isinstance(item, dict) and string_value(item.get("code"))
    }


def privacy_record() -> dict[str, Any]:
    return {
        "rawPromptsPersisted": False,
        "rawModelResponsesPersisted": False,
        "chainOfThoughtPersisted": False,
        "secretsIncluded": False,
        "scope": "spec_harvester_durable_artifacts",
        "externalProviderLogging": "operator_managed_not_verified",
    }


def git_head(checkout: Path) -> str | None:
    result = subprocess.run(  # noqa: S603
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def git_dirty_status(checkout: Path) -> str | None:
    result = subprocess.run(  # noqa: S603
        ["git", "-C", str(checkout), "status", "--porcelain", "--untracked-files=all"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def relative_evidence_path(value: Any) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return None
    return path


def write_controlled_calibration_report(path: Path, report: dict[str, Any]) -> None:
    write_json(path, report)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_json(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return sha256(encoded).hexdigest()


def elapsed_milliseconds(started: float) -> int:
    return int((time.monotonic() - started) * 1000)


def mapping_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""
