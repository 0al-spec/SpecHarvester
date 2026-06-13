from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.bundle_set_preflight import (
    BundleSetPreflightOptions,
    run_bundle_set_preflight,
)
from spec_harvester.collector import DEFAULT_MAX_FILE_BYTES
from spec_harvester.package_set_ai_draft_proposal import (
    DEFAULT_MAX_OUTPUT_TOKENS as DEFAULT_AI_DRAFT_MAX_OUTPUT_TOKENS,
)
from spec_harvester.package_set_ai_draft_proposal import (
    DEFAULT_TEMPERATURE as DEFAULT_AI_DRAFT_TEMPERATURE,
)
from spec_harvester.package_set_ai_draft_proposal import (
    DEFAULT_TIMEOUT_SECONDS as DEFAULT_AI_DRAFT_TIMEOUT_SECONDS,
)
from spec_harvester.package_set_ai_draft_proposal import (
    PackageSetAIDraftProposalOptions,
    build_package_set_ai_draft_proposal,
    normalize_local_provider_base_url,
    write_package_set_ai_draft_proposal,
)
from spec_harvester.package_set_ai_draft_proposal import (
    model_request_record as package_set_ai_draft_request,
)
from spec_harvester.package_set_ai_draft_proposal import (
    write_model_request_record as write_package_set_ai_draft_request,
)
from spec_harvester.package_set_ai_enrichment import (
    DEFAULT_MAX_OUTPUT_TOKENS as DEFAULT_AI_ENRICHMENT_MAX_OUTPUT_TOKENS,
)
from spec_harvester.package_set_ai_enrichment import (
    DEFAULT_TEMPERATURE as DEFAULT_AI_ENRICHMENT_TEMPERATURE,
)
from spec_harvester.package_set_ai_enrichment import (
    DEFAULT_TIMEOUT_SECONDS as DEFAULT_AI_ENRICHMENT_TIMEOUT_SECONDS,
)
from spec_harvester.package_set_ai_enrichment import (
    PackageSetAIEnrichmentOptions,
    build_package_set_ai_enrichment_proposal,
    write_package_set_ai_enrichment_proposal,
)
from spec_harvester.package_set_ai_enrichment import (
    model_request_records as package_set_ai_enrichment_requests,
)
from spec_harvester.package_set_ai_enrichment import (
    write_model_request_records as write_package_set_ai_enrichment_requests,
)
from spec_harvester.package_set_drafter import (
    AUTONOMOUS_POPULAR_MVP_ROLE_SELECTION_PROFILE,
    PackageSetDraftOptions,
    draft_package_set,
)

AUTONOMOUS_CANDIDATE_BATCH_API_VERSION = "spec-harvester.autonomous-candidate-batch/v0"
AUTONOMOUS_CANDIDATE_BATCH_KIND = "SpecHarvesterAutonomousCandidateBatchReport"
AUTONOMOUS_CANDIDATE_BATCH_SCHEMA_VERSION = 1
AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME = "autonomous-candidate-batch-report.json"
DEFAULT_LM_STUDIO_BASE_URL = "http://127.0.0.1:1234"
DEFAULT_PROVIDER_NAME = "lm_studio"
DEFAULT_AUTONOMOUS_ROLE_PROFILE = AUTONOMOUS_POPULAR_MVP_ROLE_SELECTION_PROFILE
COLLECTED_DIRNAME = "collected"
PACKAGE_SETS_DIRNAME = "package-sets"
REPORTS_DIRNAME = "reports"
AI_DIRNAME = "ai"
BUNDLE_SET_PREFLIGHT_FILENAME = "bundle-set-preflight.json"
AI_DRAFT_REQUEST_FILENAME = "package-set-ai-draft-request.json"
AI_DRAFT_PROPOSAL_FILENAME = "package-set-ai-draft-proposal.json"
AI_ENRICHMENT_REQUEST_FILENAME = "package-set-ai-enrichment-requests.json"
AI_ENRICHMENT_PROPOSAL_FILENAME = "package-set-ai-enrichment-proposal.json"

TRUST_BOUNDARY_NOTES = [
    "Autonomous candidate batch output is producer evidence only.",
    "Generated package files remain preview candidates until explicit SpecPM review.",
    (
        "SpecHarvester does not clone repositories, install dependencies, "
        "run builds, or execute package scripts."
    ),
    "Live model execution is limited to the operator-provided local OpenAI-compatible endpoint.",
    "Raw prompts, raw provider responses, secrets, and chain-of-thought are not persisted.",
    "SpecPM remains the validation, acceptance, relation, and registry authority.",
]


@dataclass(frozen=True)
class AutonomousCandidateBatchOptions:
    inputs: Path
    out: Path
    selected_ids: tuple[str, ...] = ()
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    strict_public: bool = True
    analyzer_cache_dir: Path | None = None
    role_profile: str = DEFAULT_AUTONOMOUS_ROLE_PROFILE
    roles: tuple[str, ...] = ()
    skip_ai: bool = False
    lm_studio_base_url: str = DEFAULT_LM_STUDIO_BASE_URL
    lm_studio_model: str | None = None
    provider_name: str = DEFAULT_PROVIDER_NAME
    ai_draft_timeout_seconds: float = DEFAULT_AI_DRAFT_TIMEOUT_SECONDS
    ai_draft_max_output_tokens: int = DEFAULT_AI_DRAFT_MAX_OUTPUT_TOKENS
    ai_draft_temperature: float = DEFAULT_AI_DRAFT_TEMPERATURE
    ai_enrichment_timeout_seconds: float = DEFAULT_AI_ENRICHMENT_TIMEOUT_SECONDS
    ai_enrichment_max_output_tokens: int = DEFAULT_AI_ENRICHMENT_MAX_OUTPUT_TOKENS
    ai_enrichment_temperature: float = DEFAULT_AI_ENRICHMENT_TEMPERATURE


class AutonomousCandidateBatch:
    def __init__(self, options: AutonomousCandidateBatchOptions):
        self.options = options
        self.out = options.out
        self.collected_root = self.out / COLLECTED_DIRNAME
        self.package_sets_root = self.out / PACKAGE_SETS_DIRNAME
        self.reports_root = self.out / REPORTS_DIRNAME

    def run(self) -> dict[str, Any]:
        self.validate_options()
        self.out.mkdir(parents=True, exist_ok=True)
        collection = self.collect()
        repositories = [self.repository_record(record) for record in collection["collected"]]
        status = batch_status(collection, repositories)
        report = {
            "apiVersion": AUTONOMOUS_CANDIDATE_BATCH_API_VERSION,
            "kind": AUTONOMOUS_CANDIDATE_BATCH_KIND,
            "schemaVersion": AUTONOMOUS_CANDIDATE_BATCH_SCHEMA_VERSION,
            "status": status,
            "input": str(self.options.inputs),
            "outputRoot": str(self.out),
            "selectedIds": list(self.options.selected_ids),
            "collection": collection_record(collection, self.validation_report_path()),
            "ai": self.ai_mode_record(),
            "summary": {
                "collectedCount": collection["collectedCount"],
                "skippedCount": collection["skippedCount"],
                "processedCount": len(repositories),
                "passedPreflightCount": count_status(repositories, "preflight", "passed"),
                "failedRepositoryCount": sum(
                    1 for item in repositories if item["status"] == "failed"
                ),
                "aiDraftProposalCount": count_present(repositories, "aiDraft"),
                "aiEnrichmentProposalCount": count_present(repositories, "aiEnrichment"),
            },
            "repositories": repositories,
            "skipped": collection["skipped"],
            "authority": "producer_preview_evidence_only",
            "nonGoals": [
                "repository_clone",
                "network_scraping",
                "package_execution",
                "dependency_installation",
                "specpm_acceptance",
                "registry_publication",
            ],
            "trustBoundary": TRUST_BOUNDARY_NOTES,
        }
        write_autonomous_candidate_batch_report(self.report_path(), report)
        return report

    def validate_options(self) -> None:
        if not self.options.skip_ai and not self.options.lm_studio_model:
            raise ValueError(
                "autonomous candidate batch live AI mode requires --lm-studio-model; "
                "pass --skip-ai for deterministic offline runs"
            )
        if not self.options.skip_ai:
            normalize_local_provider_base_url(self.options.lm_studio_base_url)

    def collect(self) -> dict[str, Any]:
        return collect_batch_snapshots(
            BatchCollectOptions(
                inputs=self.options.inputs,
                out=self.collected_root,
                selected_ids=self.options.selected_ids,
                max_file_bytes=self.options.max_file_bytes,
                report=self.validation_report_path(),
                strict_public=self.options.strict_public,
                emit_interface_indexes=True,
                analyzer_cache_dir=self.options.analyzer_cache_dir or self.out / "analyzer-cache",
                emit_workspace_inventory=True,
            )
        )

    def repository_record(self, collected: dict[str, Any]) -> dict[str, Any]:
        repository_id = str(collected["id"])
        bundle_set = self.package_sets_root / repository_id
        ai_root = bundle_set / AI_DIRNAME
        record: dict[str, Any] = {
            "id": repository_id,
            "repository": collected["repository"],
            "revision": collected["revision"],
            "ref": collected["ref"],
            "checkout": collected["checkout"],
            "packageId": collected["packageId"],
            "harvest": artifact_record(collected["output"]),
            "workspaceInventory": artifact_record(
                str(collected.get("workspaceInventory", {}).get("output") or "")
            ),
            "interfaceIndex": optional_record(collected.get("interfaceIndex")),
            "status": "pending",
        }
        try:
            inventory = inventory_path(collected)
            draft_result = draft_package_set(
                PackageSetDraftOptions(
                    inventory=inventory,
                    out=bundle_set,
                    role_profile=self.options.role_profile,
                    roles=self.options.roles,
                )
            )
            record["packageSetDraft"] = package_set_draft_record(bundle_set, draft_result)
            preflight = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=bundle_set))
            preflight_path = bundle_set / BUNDLE_SET_PREFLIGHT_FILENAME
            write_json(preflight_path, preflight)
            record["preflight"] = preflight_record(preflight_path, preflight)
            if self.options.skip_ai:
                record["aiDraft"] = skipped_ai_record("ai_disabled_by_operator")
                record["aiEnrichment"] = skipped_ai_record("ai_disabled_by_operator")
            else:
                record["aiDraft"] = self.ai_draft_record(
                    inventory=inventory,
                    source_checkout=Path(collected["checkout"]),
                    ai_root=ai_root,
                )
                record["aiEnrichment"] = self.ai_enrichment_record(
                    bundle_set=bundle_set,
                    source_checkout=Path(collected["checkout"]),
                    ai_root=ai_root,
                )
            record["authorReadyDraftSummary"] = author_ready_summary(bundle_set)
            record["status"] = repository_status(record)
        except Exception as exc:  # noqa: BLE001
            record["status"] = "failed"
            record.setdefault("diagnostics", []).append(
                {
                    "severity": "error",
                    "code": "autonomous_candidate_batch_repository_failed",
                    "message": str(exc),
                }
            )
        return record

    def ai_draft_record(
        self, *, inventory: Path, source_checkout: Path, ai_root: Path
    ) -> dict[str, Any]:
        options = PackageSetAIDraftProposalOptions(
            inventory=inventory,
            source_checkout=source_checkout,
            provider_base_url=self.options.lm_studio_base_url,
            provider_name=self.options.provider_name,
            model=self.options.lm_studio_model,
            timeout_seconds=self.options.ai_draft_timeout_seconds,
            max_output_tokens=self.options.ai_draft_max_output_tokens,
            temperature=self.options.ai_draft_temperature,
        )
        request_path = ai_root / AI_DRAFT_REQUEST_FILENAME
        output_path = ai_root / AI_DRAFT_PROPOSAL_FILENAME
        write_package_set_ai_draft_request(request_path, package_set_ai_draft_request(options))
        proposal = build_package_set_ai_draft_proposal(options)
        write_package_set_ai_draft_proposal(output_path, proposal)
        return ai_proposal_record(request_path, output_path, proposal)

    def ai_enrichment_record(
        self,
        *,
        bundle_set: Path,
        source_checkout: Path,
        ai_root: Path,
    ) -> dict[str, Any]:
        options = PackageSetAIEnrichmentOptions(
            bundle_set=bundle_set,
            source_checkout=source_checkout,
            provider_base_url=self.options.lm_studio_base_url,
            provider_name=self.options.provider_name,
            model=self.options.lm_studio_model,
            timeout_seconds=self.options.ai_enrichment_timeout_seconds,
            max_output_tokens=self.options.ai_enrichment_max_output_tokens,
            temperature=self.options.ai_enrichment_temperature,
        )
        request_path = ai_root / AI_ENRICHMENT_REQUEST_FILENAME
        output_path = ai_root / AI_ENRICHMENT_PROPOSAL_FILENAME
        write_package_set_ai_enrichment_requests(
            request_path,
            package_set_ai_enrichment_requests(options),
        )
        proposal = build_package_set_ai_enrichment_proposal(options)
        write_package_set_ai_enrichment_proposal(output_path, proposal)
        return ai_proposal_record(request_path, output_path, proposal)

    def ai_mode_record(self) -> dict[str, Any]:
        if self.options.skip_ai:
            return {
                "mode": "disabled",
                "provider": None,
                "model": None,
                "reason": "operator_disabled",
            }
        return {
            "mode": "local_lm_studio",
            "provider": self.options.provider_name,
            "baseUrl": normalize_local_provider_base_url(self.options.lm_studio_base_url),
            "model": self.options.lm_studio_model,
            "execution": "operator_opt_in_local",
            "rawPromptPersisted": False,
            "rawResponsePersisted": False,
            "chainOfThoughtPersisted": False,
        }

    def validation_report_path(self) -> Path:
        return self.reports_root / "batch-validation-report.json"

    def report_path(self) -> Path:
        return self.out / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME


def run_autonomous_candidate_batch(options: AutonomousCandidateBatchOptions) -> dict[str, Any]:
    return AutonomousCandidateBatch(options).run()


def write_autonomous_candidate_batch_report(path: Path, report: dict[str, Any]) -> None:
    write_json(path, report)


def inventory_path(collected: dict[str, Any]) -> Path:
    record = collected.get("workspaceInventory")
    if not isinstance(record, dict):
        raise ValueError("workspace inventory output is missing from collect-batch result")
    output = record.get("output")
    if not isinstance(output, str) or not output:
        raise ValueError("workspace inventory output path is missing from collect-batch result")
    return Path(output)


def package_set_draft_record(bundle_set: Path, draft_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": draft_result["status"],
        "bundleSet": str(bundle_set),
        "summary": draft_result["summary"],
        "relationProposals": draft_result["relationProposals"],
        "candidateCount": draft_result["candidateCount"],
        "skippedCount": draft_result["skippedCount"],
        "relationCount": draft_result["relationCount"],
    }


def preflight_record(path: Path, preflight: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": preflight["status"],
        "path": str(path),
        "candidateCount": preflight["summary"]["candidateCount"],
        "candidatePreflightPassedCount": preflight["summary"]["candidatePreflightPassedCount"],
        "relationCount": preflight["summary"]["relationCount"],
        "errorCount": preflight["summary"]["errorCount"],
        "warningCount": preflight["summary"]["warningCount"],
    }


def ai_proposal_record(
    request_path: Path,
    output_path: Path,
    proposal: dict[str, Any],
) -> dict[str, Any]:
    return {
        "status": proposal["status"],
        "request": str(request_path),
        "output": str(output_path),
        "authority": proposal.get("authority"),
        "summary": proposal.get("summary", {}),
        "stopPolicySummary": proposal.get("stopPolicySummary"),
        "privacy": proposal.get("privacy", {}),
    }


def skipped_ai_record(reason: str) -> dict[str, Any]:
    return {"status": "skipped", "reason": reason}


def author_ready_summary(bundle_set: Path) -> dict[str, Any] | None:
    payload = read_json(bundle_set / "package-set-draft.json")
    summary = payload.get("authorReadyDraftSummary")
    return summary if isinstance(summary, dict) else None


def repository_status(record: dict[str, Any]) -> str:
    preflight = record.get("preflight", {})
    if not isinstance(preflight, dict) or preflight.get("status") != "passed":
        return "failed"
    ai_records = [record.get("aiDraft"), record.get("aiEnrichment")]
    for item in ai_records:
        if isinstance(item, dict) and item.get("status") not in {
            "completed",
            "warning",
            "skipped",
        }:
            return "failed"
    return "passed"


def batch_status(collection: dict[str, Any], repositories: list[dict[str, Any]]) -> str:
    if collection.get("status") == "error":
        return "failed"
    if any(repository.get("status") == "failed" for repository in repositories):
        return "failed"
    return "passed"


def collection_record(collection: dict[str, Any], validation_report: Path) -> dict[str, Any]:
    return {
        "status": collection["status"],
        "outputRoot": collection["outputRoot"],
        "validationReport": str(validation_report),
        "collectedCount": collection["collectedCount"],
        "skippedCount": collection["skippedCount"],
    }


def artifact_record(path: str) -> dict[str, str]:
    return {"path": path}


def optional_record(value: Any) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None


def count_status(repositories: list[dict[str, Any]], key: str, status: str) -> int:
    return sum(
        1
        for repository in repositories
        if isinstance(repository.get(key), dict) and repository[key].get("status") == status
    )


def count_present(repositories: list[dict[str, Any]], key: str) -> int:
    return sum(
        1
        for repository in repositories
        if isinstance(repository.get(key), dict)
        and repository[key].get("status") in {"completed", "warning"}
    )


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON artifact must be an object: {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
