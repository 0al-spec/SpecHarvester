from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.ai_enrichment_candidate_patch import (
    AI_ENRICHMENT_CANDIDATE_PATCH_FILENAME,
    AIEnrichmentCandidatePatchOptions,
    build_ai_enrichment_candidate_patch,
)
from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.bundle_set_preflight import (
    BundleSetPreflightOptions,
    run_bundle_set_preflight,
)
from spec_harvester.collector import DEFAULT_MAX_FILE_BYTES
from spec_harvester.model_json_repair import DEFAULT_JSON_REPAIR_MAX_ATTEMPTS
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
from spec_harvester.producer_receipt import digest_record, sha256_file
from spec_harvester.repository_plugin_applicability import evaluate_repository_plugin_applicability
from spec_harvester.repository_profile_detection import (
    RepositoryIdentity,
    RepositoryProfileDetectionOptions,
    build_repository_profile_detection,
    write_repository_profile_detection,
)
from spec_harvester.trusted_local_adapter_runner import (
    TRUSTED_LOCAL_ADAPTER_RUN_REPORT_API_VERSION,
    TRUSTED_LOCAL_ADAPTER_RUN_REPORT_AUTHORITY,
    TRUSTED_LOCAL_ADAPTER_RUN_REPORT_KIND,
    TRUSTED_LOCAL_ADAPTER_RUN_REPORT_SCHEMA_VERSION,
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
ENRICHED_DIRNAME = "enriched"
BUNDLE_SET_PREFLIGHT_FILENAME = "bundle-set-preflight.json"
AI_DRAFT_REQUEST_FILENAME = "package-set-ai-draft-request.json"
AI_DRAFT_PROPOSAL_FILENAME = "package-set-ai-draft-proposal.json"
AI_ENRICHMENT_REQUEST_FILENAME = "package-set-ai-enrichment-requests.json"
AI_ENRICHMENT_PROPOSAL_FILENAME = "package-set-ai-enrichment-proposal.json"
REPOSITORY_PROFILE_DETECTION_FILENAME = "repository-profile-detection.json"
REPOSITORY_PLUGIN_APPLICABILITY_DIRNAME = "repository-plugin-applicability"
REPOSITORY_PLUGIN_APPLICABILITY_FILENAME = "repository-plugin-applicability-report.json"
REPOSITORY_PLUGIN_APPLICABILITY_API_VERSION = "spec-harvester.repository-plugin-applicability/v0"
REPOSITORY_PLUGIN_APPLICABILITY_KIND = "SpecHarvesterRepositoryPluginApplicabilityReport"
REPOSITORY_PLUGIN_APPLICABILITY_AUTHORITY = "producer_plugin_applicability_only"
REPOSITORY_PLUGIN_ADAPTER_EVIDENCE_DIRNAME = "repository-plugin-adapter-evidence"
REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FILENAME = "adapter-manifest.json"
REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_FILENAME = "adapter-preflight-report.json"
REPOSITORY_PLUGIN_ADAPTER_MANIFEST_API_VERSION = "spec-harvester.repository-plugin-adapter/v0"
REPOSITORY_PLUGIN_ADAPTER_MANIFEST_KIND = "SpecHarvesterRepositoryPluginAdapterManifest"
REPOSITORY_PLUGIN_ADAPTER_MANIFEST_AUTHORITY = "producer_plugin_adapter_manifest_only"
REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_API_VERSION = (
    "spec-harvester.repository-plugin-adapter-preflight/v0"
)
REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_KIND = "SpecHarvesterRepositoryPluginAdapterPreflightReport"
REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_AUTHORITY = "producer_plugin_adapter_preflight_only"
TRUSTED_LOCAL_ADAPTER_RUN_EVIDENCE_DIRNAME = "trusted-local-adapter-run-evidence"
TRUSTED_LOCAL_ADAPTER_RUN_REPORT_FILENAME = "trusted-local-adapter-run-report.json"
REQUIRED_TRUSTED_LOCAL_ADAPTER_RUN_NON_AUTHORITY_STATEMENTS = (
    "runner_report_is_not_execution_permission",
    "preflight_pass_is_not_execution_permission",
    "does_not_load_third_party_adapter_code",
    "does_not_execute_adapters",
    "does_not_run_adapter_processes",
    "does_not_clone_or_fetch_repositories",
    "does_not_install_dependencies",
    "does_not_invoke_package_managers",
    "does_not_execute_harvested_code",
    "does_not_run_ai",
    "does_not_change_static_plugin_applicability_evaluation",
    "does_not_change_autonomous_batch_behavior",
    "does_not_accept_packages",
    "does_not_accept_relations",
    "does_not_seed_baselines",
    "does_not_publish_registry_metadata",
    "does_not_remove_preview_only",
    "does_not_treat_adapter_output_as_registry_truth",
    "does_not_treat_adapter_preflight_as_registry_truth",
    "does_not_treat_ai_output_as_registry_truth",
)

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
    parser_profile_id: str | None = None
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
    json_repair_max_attempts: int = DEFAULT_JSON_REPAIR_MAX_ATTEMPTS
    apply_ai_enrichment: bool = False
    repository_profile_selection: str = "none"
    repository_plugin_applicability: Path | None = None
    repository_plugin_registry: Path | None = None
    repository_plugin_static_evidence_envelope: Path | None = None
    repository_plugin_adapter_manifest: Path | None = None
    repository_plugin_adapter_preflight: Path | None = None
    trusted_local_adapter_run_report: Path | None = None


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
        repository_plugin_applicability = self.repository_plugin_applicability_record()
        repository_plugin_adapter_evidence = self.repository_plugin_adapter_evidence_record()
        trusted_local_adapter_run_evidence = self.trusted_local_adapter_run_evidence_record()
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
            "repositoryProfileSelection": self.repository_profile_selection_record(),
            "repositoryPluginApplicability": repository_plugin_applicability,
            "repositoryPluginAdapterEvidence": repository_plugin_adapter_evidence,
            "trustedLocalAdapterRunEvidence": trusted_local_adapter_run_evidence,
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
                "aiEnrichedPreviewAppliedCount": sum_nested_summary(
                    repositories, "aiEnrichedPreview", "appliedCount"
                ),
                "aiEnrichedPreviewSkippedCount": sum_nested_summary(
                    repositories, "aiEnrichedPreview", "skippedCount"
                ),
                "aiEnrichedPreviewFailedCount": sum_nested_summary(
                    repositories, "aiEnrichedPreview", "failedCount"
                ),
                "repositoryProfileDetectionCount": count_present(
                    repositories, "repositoryProfileDetection"
                ),
                "repositoryProfileSelectedCount": count_profile_decision(repositories, "selected"),
                "repositoryProfileFallbackCount": count_profile_decision(repositories, "fallback"),
                "repositoryProfileDisabledCount": count_profile_decision(repositories, "disabled"),
                "repositoryPluginApplicabilitySidecarCount": (
                    1 if repository_plugin_applicability.get("status") == "recorded" else 0
                ),
                "repositoryPluginAdapterEvidenceSidecarCount": (
                    1 if repository_plugin_adapter_evidence.get("status") == "recorded" else 0
                ),
                "trustedLocalAdapterRunEvidenceSidecarCount": (
                    1 if trusted_local_adapter_run_evidence.get("status") == "recorded" else 0
                ),
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
        if self.options.json_repair_max_attempts < 0:
            raise ValueError("--json-repair-max-attempts must be zero or greater")
        if not self.repository_profile_selection():
            raise ValueError("--repository-profile-selection must be non-empty")
        if self.options.repository_plugin_applicability is None:
            has_registry = self.options.repository_plugin_registry is not None
            has_static_evidence = (
                self.options.repository_plugin_static_evidence_envelope is not None
            )
            if has_registry != has_static_evidence:
                raise ValueError(
                    "--repository-plugin-registry and "
                    "--repository-plugin-static-evidence-envelope must be provided together"
                )
        has_adapter_manifest = self.options.repository_plugin_adapter_manifest is not None
        has_adapter_preflight = self.options.repository_plugin_adapter_preflight is not None
        if has_adapter_manifest != has_adapter_preflight:
            raise ValueError(
                "--repository-plugin-adapter-manifest and "
                "--repository-plugin-adapter-preflight must be provided together"
            )

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
                parser_profile_id=self.options.parser_profile_id,
            )
        )

    def repository_record(self, collected: dict[str, Any]) -> dict[str, Any]:
        repository_id = str(collected["id"])
        bundle_set = self.package_sets_root / repository_id
        ai_root = bundle_set / AI_DIRNAME
        repository_profile_detection_path = (
            self.reports_root
            / "repository-profile-detections"
            / repository_id
            / REPOSITORY_PROFILE_DETECTION_FILENAME
        )
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
            record["repositoryProfileDetection"] = self.repository_profile_detection_record(
                collected=collected,
                inventory=inventory,
                output_path=repository_profile_detection_path,
            )
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
                record["aiEnrichedPreview"] = skipped_ai_record("ai_disabled_by_operator")
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
                record["aiEnrichedPreview"] = self.ai_enriched_preview_record(
                    bundle_set=bundle_set,
                    draft_result=draft_result,
                    ai_enrichment=record["aiEnrichment"],
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

    def repository_profile_detection_record(
        self,
        *,
        collected: dict[str, Any],
        inventory: Path,
        output_path: Path,
    ) -> dict[str, Any]:
        payload = build_repository_profile_detection(
            RepositoryProfileDetectionOptions(
                repository=repository_identity_from_collected(collected),
                selection=self.repository_profile_selection(),
                evidence_paths=repository_profile_evidence_paths(
                    inventory,
                    harvest=Path(collected["output"]),
                    source_target=string_or_none(collected.get("target")),
                ),
            )
        )
        write_repository_profile_detection(output_path, payload)
        selection = payload["selection"]
        return {
            "status": "completed",
            "path": str(output_path),
            "authority": payload["authority"],
            "mode": selection["mode"],
            "overrideSource": selection["overrideSource"],
            "selectedProfileId": selection["selectedProfileId"],
            "fallbackProfileId": selection["fallbackProfileId"],
            "confidence": selection["confidence"],
            "decision": selection["decision"],
            "reasonCodes": selection["reasonCodes"],
            "candidateProfileCount": len(payload.get("candidateProfiles", [])),
            "rejectedProfileCount": len(payload.get("rejectedProfiles", [])),
            "advisoryHintCount": len(payload.get("advisoryDownstreamHints", [])),
            "diagnosticCodes": diagnostic_codes(payload),
        }

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
            json_repair_max_attempts=self.options.json_repair_max_attempts,
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
            json_repair_max_attempts=self.options.json_repair_max_attempts,
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

    def ai_enriched_preview_record(
        self,
        *,
        bundle_set: Path,
        draft_result: dict[str, Any],
        ai_enrichment: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.options.apply_ai_enrichment:
            return skipped_ai_record("operator_disabled")
        proposal_path = ai_enrichment.get("output")
        if ai_enrichment.get("status") != "completed" or not isinstance(proposal_path, str):
            skipped = [
                {
                    "packageId": candidate.get("packageId"),
                    "reason": "ai_enrichment_not_clean",
                }
                for candidate in candidate_records(draft_result)
            ]
            return {
                "status": "skipped",
                "reason": "ai_enrichment_not_clean",
                "summary": {"appliedCount": 0, "skippedCount": len(skipped), "failedCount": 0},
                "applied": [],
                "skipped": skipped,
                "failed": [],
            }

        enriched_root = bundle_set / ENRICHED_DIRNAME
        applied: list[dict[str, Any]] = []
        skipped: list[dict[str, Any]] = []
        failed: list[dict[str, Any]] = []
        for candidate in candidate_records(draft_result):
            package_id = str(candidate.get("packageId") or "")
            candidate_path = safe_bundle_path(bundle_set, candidate.get("candidatePath"))
            if not package_id or not candidate_path.is_dir():
                skipped.append(
                    {
                        "packageId": package_id,
                        "reason": "candidate_path_missing",
                    }
                )
                continue
            output = enriched_root / safe_enriched_candidate_dir(package_id)
            try:
                patch = build_ai_enrichment_candidate_patch(
                    AIEnrichmentCandidatePatchOptions(
                        proposal=Path(proposal_path),
                        candidate=candidate_path,
                        output=output,
                        package_id=package_id,
                    )
                )
            except ValueError as exc:
                skipped.append(
                    {
                        "packageId": package_id,
                        "reason": "ai_enrichment_patch_skipped",
                        "message": str(exc),
                    }
                )
                continue
            except Exception as exc:  # noqa: BLE001
                failed.append(
                    {
                        "packageId": package_id,
                        "reason": "ai_enrichment_patch_failed",
                        "message": str(exc),
                    }
                )
                continue
            applied.append(
                {
                    "packageId": package_id,
                    "candidate": str(output),
                    "patchReport": str(output / AI_ENRICHMENT_CANDIDATE_PATCH_FILENAME),
                    "appliedChangeCount": len(patch.get("appliedChanges", [])),
                    "skippedChangeCount": len(patch.get("skippedChanges", [])),
                    "previewOnly": bool(mapping_value(patch.get("subject")).get("previewOnly")),
                    "sourceMutated": bool(mapping_value(patch.get("subject")).get("sourceMutated")),
                }
            )
        status = "failed" if failed else ("prepared" if applied else "skipped")
        return {
            "status": status,
            "root": str(enriched_root),
            "authority": "producer_preview_evidence_only",
            "summary": {
                "appliedCount": len(applied),
                "skippedCount": len(skipped),
                "failedCount": len(failed),
            },
            "applied": applied,
            "skipped": skipped,
            "failed": failed,
            "nonGoals": [
                "specpm_acceptance",
                "relation_acceptance",
                "preview_only_removal",
                "source_candidate_mutation",
                "registry_publication",
            ],
        }

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
            "jsonRepairMaxAttempts": self.options.json_repair_max_attempts,
            "rawPromptPersisted": False,
            "rawResponsePersisted": False,
            "chainOfThoughtPersisted": False,
        }

    def repository_profile_selection_record(self) -> dict[str, Any]:
        return {
            "mode": self.repository_profile_selection(),
            "defaultMode": "none",
            "artifact": REPOSITORY_PROFILE_DETECTION_FILENAME,
            "authority": "producer_profile_selection_only",
            "execution": "static_collected_evidence_only",
            "advisoryHintsAppliedToDrafting": False,
            "registryAuthority": False,
        }

    def repository_profile_selection(self) -> str:
        return self.options.repository_profile_selection.strip()

    def repository_plugin_applicability_record(self) -> dict[str, Any]:
        source = self.options.repository_plugin_applicability
        registry_source = self.options.repository_plugin_registry
        static_evidence_source = self.options.repository_plugin_static_evidence_envelope
        output_path = (
            self.reports_root
            / REPOSITORY_PLUGIN_APPLICABILITY_DIRNAME
            / REPOSITORY_PLUGIN_APPLICABILITY_FILENAME
        )
        if source is not None:
            payload = read_json(source)
            validate_repository_plugin_applicability(payload, source)
            write_json(output_path, payload)
            return repository_plugin_applicability_record_from_payload(
                payload=payload,
                source=str(source),
                source_mode="explicit_sidecar",
                output_path=output_path,
            )
        if registry_source is None and static_evidence_source is None:
            return {
                "status": "not_provided",
                "reason": "operator_not_provided",
                "appliedToDrafting": False,
                "registryAuthority": False,
            }

        if registry_source is None or static_evidence_source is None:
            raise ValueError(
                "--repository-plugin-registry and "
                "--repository-plugin-static-evidence-envelope must be provided together"
            )
        registry = read_json(registry_source)
        static_evidence = read_json(static_evidence_source)
        payload = evaluate_repository_plugin_applicability(registry, static_evidence)
        validate_repository_plugin_applicability(payload, output_path)
        write_json(output_path, payload)
        return repository_plugin_applicability_record_from_payload(
            payload=payload,
            source="auto_static_evaluator",
            source_mode="auto_static_evaluator",
            output_path=output_path,
            inputs={
                "registry": str(registry_source),
                "staticEvidenceEnvelope": str(static_evidence_source),
            },
        )

    def repository_plugin_adapter_evidence_record(self) -> dict[str, Any]:
        manifest_source = self.options.repository_plugin_adapter_manifest
        preflight_source = self.options.repository_plugin_adapter_preflight
        if manifest_source is None and preflight_source is None:
            return {
                "status": "not_provided",
                "reason": "operator_not_provided",
                "appliedToDrafting": False,
                "registryAuthority": False,
                "adapterExecution": "not_run",
            }
        if manifest_source is None or preflight_source is None:
            raise ValueError(
                "--repository-plugin-adapter-manifest and "
                "--repository-plugin-adapter-preflight must be provided together"
            )

        manifest = read_json(manifest_source)
        preflight = read_json(preflight_source)
        validate_repository_plugin_adapter_manifest(manifest, manifest_source)
        validate_repository_plugin_adapter_preflight(
            preflight,
            preflight_source,
            expected_manifest_digest=sha256_file(manifest_source),
        )
        output_root = self.reports_root / REPOSITORY_PLUGIN_ADAPTER_EVIDENCE_DIRNAME
        manifest_output = output_root / REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FILENAME
        preflight_output = output_root / REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_FILENAME
        write_json(manifest_output, manifest)
        write_json(preflight_output, preflight)
        return repository_plugin_adapter_evidence_record_from_payload(
            manifest=manifest,
            preflight=preflight,
            manifest_source=manifest_source,
            preflight_source=preflight_source,
            manifest_output=manifest_output,
            preflight_output=preflight_output,
        )

    def trusted_local_adapter_run_evidence_record(self) -> dict[str, Any]:
        source = self.options.trusted_local_adapter_run_report
        if source is None:
            return {
                "status": "not_provided",
                "reason": "operator_not_provided",
                "appliedToDrafting": False,
                "registryAuthority": False,
                "adapterExecution": "not_run",
            }

        payload = read_json(source)
        validate_trusted_local_adapter_run_report(payload, source)
        output_path = (
            self.reports_root
            / TRUSTED_LOCAL_ADAPTER_RUN_EVIDENCE_DIRNAME
            / TRUSTED_LOCAL_ADAPTER_RUN_REPORT_FILENAME
        )
        write_json(output_path, payload)
        return trusted_local_adapter_run_evidence_record_from_payload(
            payload=payload,
            source=source,
            output_path=output_path,
        )

    def validation_report_path(self) -> Path:
        return self.reports_root / "batch-validation-report.json"

    def report_path(self) -> Path:
        return self.out / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME


def run_autonomous_candidate_batch(options: AutonomousCandidateBatchOptions) -> dict[str, Any]:
    return AutonomousCandidateBatch(options).run()


def write_autonomous_candidate_batch_report(path: Path, report: dict[str, Any]) -> None:
    write_json(path, report)


def repository_plugin_applicability_record_from_payload(
    *,
    payload: dict[str, Any],
    source: str,
    source_mode: str,
    output_path: Path,
    inputs: dict[str, str] | None = None,
) -> dict[str, Any]:
    summary = mapping_value(payload.get("summary"))
    record: dict[str, Any] = {
        "status": "recorded",
        "source": source,
        "sourceMode": source_mode,
        "path": str(output_path),
        "digest": digest_record(sha256_file(output_path)),
        "apiVersion": payload["apiVersion"],
        "kind": payload["kind"],
        "schemaVersion": payload["schemaVersion"],
        "authority": payload["authority"],
        "mode": payload.get("mode"),
        "repository": mapping_value(payload.get("repository")),
        "registry": mapping_value(payload.get("registry")),
        "summary": {
            "selectedCount": int_value(summary.get("selectedCount")),
            "rejectedCount": int_value(summary.get("rejectedCount")),
            "fallbackCount": int_value(summary.get("fallbackCount")),
            "blockedCount": int_value(summary.get("blockedCount")),
            "diagnosticCount": int_value(summary.get("diagnosticCount")),
        },
        "diagnosticCodes": diagnostic_codes(payload),
        "appliedToDrafting": False,
        "registryAuthority": False,
        "nonGoals": [
            "plugin_execution",
            "third_party_plugin_loading",
            "parser_profile_behavior_change",
            "repository_profile_scoring_change",
            "specpm_acceptance",
            "relation_acceptance",
            "preview_only_removal",
            "registry_publication",
        ],
    }
    if inputs is not None:
        record["inputs"] = inputs
    return record


def repository_plugin_adapter_evidence_record_from_payload(
    *,
    manifest: dict[str, Any],
    preflight: dict[str, Any],
    manifest_source: Path,
    preflight_source: Path,
    manifest_output: Path,
    preflight_output: Path,
) -> dict[str, Any]:
    manifest_summary = mapping_value(manifest.get("summary"))
    preflight_summary = mapping_value(preflight.get("summary"))
    return {
        "status": "recorded",
        "sourceMode": "explicit_sidecar",
        "authority": REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_AUTHORITY,
        "manifest": {
            "source": str(manifest_source),
            "sourceDigest": digest_record(sha256_file(manifest_source)),
            "path": str(manifest_output),
            "digest": digest_record(sha256_file(manifest_output)),
            "apiVersion": manifest["apiVersion"],
            "kind": manifest["kind"],
            "schemaVersion": manifest["schemaVersion"],
            "authority": manifest["authority"],
            "adapterCount": int_value(manifest_summary.get("adapterCount")),
        },
        "preflight": {
            "source": str(preflight_source),
            "sourceDigest": digest_record(sha256_file(preflight_source)),
            "path": str(preflight_output),
            "digest": digest_record(sha256_file(preflight_output)),
            "apiVersion": preflight["apiVersion"],
            "kind": preflight["kind"],
            "schemaVersion": preflight["schemaVersion"],
            "authority": preflight["authority"],
            "allowedCount": int_value(preflight_summary.get("allowedCount")),
            "rejectedCount": int_value(preflight_summary.get("rejectedCount")),
            "fallbackCount": int_value(preflight_summary.get("fallbackCount")),
            "blockedCount": int_value(preflight_summary.get("blockedCount")),
            "diagnosticCount": int_value(preflight_summary.get("diagnosticCount")),
            "executedAdapterCount": int_value(preflight_summary.get("executedAdapterCount")),
        },
        "summary": {
            "adapterCount": int_value(manifest_summary.get("adapterCount")),
            "allowedCount": int_value(preflight_summary.get("allowedCount")),
            "rejectedCount": int_value(preflight_summary.get("rejectedCount")),
            "fallbackCount": int_value(preflight_summary.get("fallbackCount")),
            "blockedCount": int_value(preflight_summary.get("blockedCount")),
            "diagnosticCount": int_value(preflight_summary.get("diagnosticCount")),
            "executedAdapterCount": int_value(preflight_summary.get("executedAdapterCount")),
        },
        "diagnosticCodes": diagnostic_codes(preflight),
        "appliedToDrafting": False,
        "registryAuthority": False,
        "adapterExecution": "not_run",
        "adapterOutputAccepted": False,
        "nonGoals": [
            "adapter_loading",
            "adapter_execution",
            "third_party_adapter_code_loading",
            "repository_clone",
            "network_discovery",
            "dependency_installation",
            "package_manager_invocation",
            "harvested_code_execution",
            "ai_execution",
            "static_plugin_applicability_behavior_change",
            "specpm_acceptance",
            "relation_acceptance",
            "baseline_seeding",
            "preview_only_removal",
            "registry_publication",
        ],
    }


def trusted_local_adapter_run_evidence_record_from_payload(
    *,
    payload: dict[str, Any],
    source: Path,
    output_path: Path,
) -> dict[str, Any]:
    runner = mapping_value(payload.get("runner"))
    boundary = mapping_value(payload.get("executionBoundary"))
    summary = mapping_value(payload.get("summary"))
    validation = mapping_value(payload.get("validation"))
    return {
        "status": "recorded",
        "source": str(source),
        "sourceMode": "explicit_sidecar",
        "sourceDigest": digest_record(sha256_file(source)),
        "path": str(output_path),
        "digest": digest_record(sha256_file(output_path)),
        "apiVersion": payload["apiVersion"],
        "kind": payload["kind"],
        "schemaVersion": payload["schemaVersion"],
        "authority": payload["authority"],
        "runId": payload.get("runId"),
        "runStatus": payload.get("status"),
        "runner": {
            "mode": runner.get("mode"),
            "enabled": runner.get("enabled"),
            "runtimeImplemented": runner.get("runtimeImplemented"),
            "adapterExecution": runner.get("adapterExecution"),
            "adapterCodeLoaded": runner.get("adapterCodeLoaded"),
            "adapterProcessSpawned": runner.get("adapterProcessSpawned"),
            "executedAdapterCount": int_value(runner.get("executedAdapterCount")),
            "dependencyInstallation": runner.get("dependencyInstallation"),
            "packageManagers": runner.get("packageManagers"),
            "harvestedCodeExecution": runner.get("harvestedCodeExecution"),
            "aiExecution": runner.get("aiExecution"),
            "networkAccess": runner.get("networkAccess"),
        },
        "executionBoundary": {
            "adapterExecution": boundary.get("adapterExecution"),
            "adapterCodeLoaded": boundary.get("adapterCodeLoaded"),
            "executedAdapterCount": int_value(boundary.get("executedAdapterCount")),
            "runtimeImplemented": boundary.get("runtimeImplemented"),
            "requestIsExecutionPermission": boundary.get("requestIsExecutionPermission"),
            "preflightPassIsExecutionPermission": (
                boundary.get("preflightPassIsExecutionPermission")
            ),
            "runnerReportIsExecutionPermission": (
                boundary.get("runnerReportIsExecutionPermission")
            ),
            "appliedToDrafting": boundary.get("appliedToDrafting"),
            "registryAuthority": boundary.get("registryAuthority"),
            "adapterOutputAccepted": boundary.get("adapterOutputAccepted"),
        },
        "summary": {
            "acceptedCount": int_value(summary.get("acceptedCount")),
            "errorCount": int_value(summary.get("errorCount")),
            "warningCount": int_value(summary.get("warningCount")),
            "executedAdapterCount": int_value(summary.get("executedAdapterCount")),
            "runtimeImplementedAdapterCount": int_value(
                summary.get("runtimeImplementedAdapterCount")
            ),
        },
        "validation": {
            "status": validation.get("status"),
            "errorCount": int_value(validation.get("errorCount")),
            "warningCount": int_value(validation.get("warningCount")),
        },
        "diagnosticCodes": diagnostic_codes(payload),
        "nonAuthorityStatements": sorted(
            item
            for item in list_value(payload.get("nonAuthorityStatements"))
            if isinstance(item, str)
        ),
        "appliedToDrafting": False,
        "registryAuthority": False,
        "adapterExecution": "not_run",
        "adapterCodeLoaded": False,
        "adapterProcessSpawned": False,
        "executedAdapterCount": 0,
        "adapterOutputAccepted": False,
        "nonGoals": [
            "adapter_loading",
            "adapter_execution",
            "third_party_adapter_code_loading",
            "repository_clone",
            "network_discovery",
            "dependency_installation",
            "package_manager_invocation",
            "harvested_code_execution",
            "ai_execution",
            "static_plugin_applicability_behavior_change",
            "autonomous_batch_behavior_change",
            "specpm_acceptance",
            "relation_acceptance",
            "baseline_seeding",
            "preview_only_removal",
            "registry_publication",
        ],
    }


def inventory_path(collected: dict[str, Any]) -> Path:
    record = collected.get("workspaceInventory")
    if not isinstance(record, dict):
        raise ValueError("workspace inventory output is missing from collect-batch result")
    output = record.get("output")
    if not isinstance(output, str) or not output:
        raise ValueError("workspace inventory output path is missing from collect-batch result")
    return Path(output)


def repository_identity_from_collected(collected: dict[str, Any]) -> RepositoryIdentity:
    source_manifest = mapping_value(collected.get("sourceManifest"))
    return RepositoryIdentity(
        repository_id=str(collected["id"]),
        repository_url=str(collected["repository"]),
        ref=string_or_none(collected.get("ref")),
        revision=string_or_none(collected.get("revision")),
        source_manifest_path=string_or_none(source_manifest.get("path")),
        source_manifest_entry_id=str(collected["id"]),
        declared_repository_profile=None,
    )


def repository_profile_evidence_paths(
    inventory: Path,
    *,
    harvest: Path | None = None,
    source_target: str | None = None,
) -> tuple[str, ...]:
    payload = read_json(inventory)
    paths: list[str] = []
    for item in payload.get("workspaceManifests", []):
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            paths.append(item["path"])
    for item in payload.get("packages", []):
        if isinstance(item, dict) and isinstance(item.get("manifestPath"), str):
            paths.append(item["manifestPath"])
    if not paths and harvest is not None:
        paths.extend(
            target_local_harvested_path(path, source_target)
            for path in harvested_manifest_evidence_paths(harvest)
        )
    return tuple(unique_sorted(paths))


def harvested_manifest_evidence_paths(harvest: Path) -> tuple[str, ...]:
    payload = read_json(harvest)
    paths: list[str] = []
    for item in payload.get("files", []):
        if not isinstance(item, dict):
            continue
        if item.get("kind") not in {"package_manifest", "workspace_manifest"}:
            continue
        path = item.get("path")
        if isinstance(path, str):
            paths.append(path)
    return tuple(unique_sorted(paths))


def target_local_harvested_path(path: str, source_target: str | None) -> str:
    target = (source_target or "").strip()
    if not target or target == ".":
        return path
    target_parts = Path(target).parts
    path_parts = Path(path).parts
    if tuple(path_parts[: len(target_parts)]) != tuple(target_parts):
        return path
    remaining = path_parts[len(target_parts) :]
    if remaining:
        return Path(*remaining).as_posix()
    return Path(path).name


def unique_sorted(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


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
        "diagnosticCodes": diagnostic_codes(proposal),
        "jsonRepair": json_repair_record(proposal),
        "stopPolicySummary": proposal.get("stopPolicySummary"),
        "privacy": proposal.get("privacy", {}),
    }


def skipped_ai_record(reason: str) -> dict[str, Any]:
    return {"status": "skipped", "reason": reason}


def diagnostic_codes(proposal: dict[str, Any]) -> list[str]:
    return sorted(
        {
            item["code"]
            for item in proposal.get("diagnostics", [])
            if isinstance(item, dict) and isinstance(item.get("code"), str)
        }
    )


def json_repair_record(proposal: dict[str, Any]) -> dict[str, Any]:
    provider_receipt = proposal.get("providerReceipt")
    if isinstance(provider_receipt, dict):
        return {
            "needed": bool(provider_receipt.get("jsonRepairNeeded")),
            "attemptCount": int_value(provider_receipt.get("jsonRepairAttemptCount")),
            "status": provider_receipt.get("jsonRepairStatus") or "not_needed",
        }
    member_receipts = [
        item.get("providerReceipt")
        for item in proposal.get("proposals", [])
        if isinstance(item, dict) and isinstance(item.get("providerReceipt"), dict)
    ]
    needed = [receipt for receipt in member_receipts if receipt.get("jsonRepairNeeded")]
    exhausted = [
        receipt for receipt in member_receipts if receipt.get("jsonRepairStatus") == "exhausted"
    ]
    return {
        "needed": bool(needed),
        "attemptCount": sum(
            int_value(receipt.get("jsonRepairAttemptCount")) for receipt in member_receipts
        ),
        "repairedCount": sum(
            1 for receipt in member_receipts if receipt.get("jsonRepairStatus") == "repaired"
        ),
        "exhaustedCount": len(exhausted),
        "status": "exhausted" if exhausted else ("repaired" if needed else "not_needed"),
    }


def int_value(value: Any) -> int:
    return value if isinstance(value, int) else 0


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
    enriched_preview = record.get("aiEnrichedPreview")
    if isinstance(enriched_preview, dict) and enriched_preview.get("status") not in {
        "prepared",
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


def validate_repository_plugin_applicability(payload: dict[str, Any], path: Path) -> None:
    expected = {
        "apiVersion": REPOSITORY_PLUGIN_APPLICABILITY_API_VERSION,
        "kind": REPOSITORY_PLUGIN_APPLICABILITY_KIND,
        "schemaVersion": 1,
        "authority": REPOSITORY_PLUGIN_APPLICABILITY_AUTHORITY,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise ValueError(
                f"repository plugin applicability report {path} has unsupported {key}: "
                f"{payload.get(key)!r}"
            )
    summary = mapping_value(payload.get("summary"))
    for key in (
        "selectedCount",
        "rejectedCount",
        "fallbackCount",
        "blockedCount",
        "diagnosticCount",
    ):
        if type(summary.get(key)) is not int:
            raise ValueError(
                f"repository plugin applicability report {path} must include integer summary.{key}"
            )
    if not isinstance(payload.get("nonAuthorityStatements"), list):
        raise ValueError(
            f"repository plugin applicability report {path} must include nonAuthorityStatements"
        )


def validate_repository_plugin_adapter_manifest(payload: dict[str, Any], path: Path) -> None:
    expected = {
        "apiVersion": REPOSITORY_PLUGIN_ADAPTER_MANIFEST_API_VERSION,
        "kind": REPOSITORY_PLUGIN_ADAPTER_MANIFEST_KIND,
        "schemaVersion": 1,
        "authority": REPOSITORY_PLUGIN_ADAPTER_MANIFEST_AUTHORITY,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise ValueError(
                f"repository plugin adapter manifest {path} has unsupported {key}: "
                f"{payload.get(key)!r}"
            )
    adapters = payload.get("adapters")
    if not isinstance(adapters, list):
        raise ValueError(f"repository plugin adapter manifest {path} must include adapters")
    summary = mapping_value(payload.get("summary"))
    if type(summary.get("adapterCount")) is not int:
        raise ValueError(
            f"repository plugin adapter manifest {path} must include integer summary.adapterCount"
        )
    if summary["adapterCount"] != len(adapters):
        raise ValueError(
            f"repository plugin adapter manifest {path} summary.adapterCount must match adapters"
        )
    boundary = mapping_value(payload.get("sidecarBoundary"))
    if boundary.get("appliedToDrafting") is not False:
        raise ValueError(
            f"repository plugin adapter manifest {path} must record appliedToDrafting false"
        )
    if boundary.get("registryAuthority") is not False:
        raise ValueError(
            f"repository plugin adapter manifest {path} must record registryAuthority false"
        )
    if boundary.get("adapterExecution") != "not_run":
        raise ValueError(
            f"repository plugin adapter manifest {path} must record adapterExecution not_run"
        )
    if not isinstance(payload.get("nonAuthorityStatements"), list):
        raise ValueError(
            f"repository plugin adapter manifest {path} must include nonAuthorityStatements"
        )


def validate_repository_plugin_adapter_preflight(
    payload: dict[str, Any],
    path: Path,
    *,
    expected_manifest_digest: str,
) -> None:
    expected = {
        "apiVersion": REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_API_VERSION,
        "kind": REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_KIND,
        "schemaVersion": 1,
        "authority": REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_AUTHORITY,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise ValueError(
                f"repository plugin adapter preflight {path} has unsupported {key}: "
                f"{payload.get(key)!r}"
            )
    manifest = mapping_value(payload.get("manifest"))
    if manifest.get("kind") != REPOSITORY_PLUGIN_ADAPTER_MANIFEST_KIND:
        raise ValueError(
            f"repository plugin adapter preflight {path} has unsupported manifest.kind"
        )
    if manifest.get("authority") != REPOSITORY_PLUGIN_ADAPTER_MANIFEST_AUTHORITY:
        raise ValueError(
            f"repository plugin adapter preflight {path} has unsupported manifest.authority"
        )
    if manifest.get("digest") != f"sha256:{expected_manifest_digest}":
        raise ValueError(
            f"repository plugin adapter preflight {path} manifest.digest does not match manifest"
        )

    summary = mapping_value(payload.get("summary"))
    for key in (
        "allowedCount",
        "rejectedCount",
        "fallbackCount",
        "blockedCount",
        "diagnosticCount",
        "executedAdapterCount",
    ):
        if type(summary.get(key)) is not int:
            raise ValueError(
                f"repository plugin adapter preflight {path} must include integer summary.{key}"
            )
    expected_counts = {
        "allowedCount": len(list_value(payload.get("allowedAdapters"))),
        "rejectedCount": len(list_value(payload.get("rejectedAdapters"))),
        "fallbackCount": len(list_value(payload.get("fallbackAdapters"))),
        "blockedCount": len(list_value(payload.get("blockedAdapters"))),
        "diagnosticCount": len(list_value(payload.get("diagnostics"))),
    }
    for key, value in expected_counts.items():
        if summary[key] != value:
            raise ValueError(f"repository plugin adapter preflight {path} summary.{key} mismatch")
    if summary["executedAdapterCount"] != 0:
        raise ValueError(
            f"repository plugin adapter preflight {path} must not record executed adapters"
        )

    execution = mapping_value(payload.get("adapterExecution"))
    boundary = mapping_value(payload.get("sidecarBoundary"))
    if execution.get("adapterCodeLoaded") is not False:
        raise ValueError(
            f"repository plugin adapter preflight {path} must record adapterCodeLoaded false"
        )
    if execution.get("adapterExecution") != "not_run":
        raise ValueError(
            f"repository plugin adapter preflight {path} must record adapterExecution not_run"
        )
    if execution.get("executedAdapterCount") != 0:
        raise ValueError(
            f"repository plugin adapter preflight {path} must record executedAdapterCount 0"
        )
    if boundary.get("appliedToDrafting") is not False:
        raise ValueError(
            f"repository plugin adapter preflight {path} must record appliedToDrafting false"
        )
    if boundary.get("registryAuthority") is not False:
        raise ValueError(
            f"repository plugin adapter preflight {path} must record registryAuthority false"
        )
    if boundary.get("adapterExecution") != "not_run":
        raise ValueError(
            f"repository plugin adapter preflight {path} "
            "must record sidecar adapterExecution not_run"
        )
    if boundary.get("adapterOutputAccepted") is not False:
        raise ValueError(
            f"repository plugin adapter preflight {path} must record adapterOutputAccepted false"
        )
    if not isinstance(payload.get("nonAuthorityStatements"), list):
        raise ValueError(
            f"repository plugin adapter preflight {path} must include nonAuthorityStatements"
        )


def validate_trusted_local_adapter_run_report(payload: dict[str, Any], path: Path) -> None:
    expected = {
        "apiVersion": TRUSTED_LOCAL_ADAPTER_RUN_REPORT_API_VERSION,
        "kind": TRUSTED_LOCAL_ADAPTER_RUN_REPORT_KIND,
        "schemaVersion": TRUSTED_LOCAL_ADAPTER_RUN_REPORT_SCHEMA_VERSION,
        "authority": TRUSTED_LOCAL_ADAPTER_RUN_REPORT_AUTHORITY,
        "status": "no_execution_report_emitted",
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise ValueError(
                f"trusted local adapter run report {path} has unsupported {key}: "
                f"{payload.get(key)!r}"
            )

    runner = mapping_value(payload.get("runner"))
    expected_runner = {
        "enabled": False,
        "runtimeImplemented": False,
        "adapterExecution": "not_run",
        "adapterCodeLoaded": False,
        "adapterCodeImportAttempted": False,
        "adapterProcessSpawned": False,
        "executedAdapterCount": 0,
        "dependencyInstallation": "not_allowed",
        "packageManagers": "not_invoked",
        "harvestedCodeExecution": "not_allowed",
        "aiExecution": "not_run",
        "networkAccess": "none",
    }
    for key, value in expected_runner.items():
        require_trusted_run_exact_value(runner, path, f"runner.{key}", value)
    if runner.get("mode") != "disabled_no_execution_skeleton":
        raise ValueError(
            f"trusted local adapter run report {path} must record disabled runner mode"
        )

    validation = mapping_value(payload.get("validation"))
    if validation.get("status") != "passed":
        raise ValueError(
            f"trusted local adapter run report {path} must record validation.status passed"
        )
    if validation.get("errorCount") != 0:
        raise ValueError(
            f"trusted local adapter run report {path} must record validation.errorCount 0"
        )

    boundary = mapping_value(payload.get("executionBoundary"))
    expected_boundary = {
        "adapterExecution": "not_run",
        "adapterCodeLoaded": False,
        "executedAdapterCount": 0,
        "runtimeImplemented": False,
        "requestIsExecutionPermission": False,
        "preflightPassIsExecutionPermission": False,
        "runnerReportIsExecutionPermission": False,
        "appliedToDrafting": False,
        "registryAuthority": False,
        "adapterOutputAccepted": False,
    }
    for key, value in expected_boundary.items():
        require_trusted_run_exact_value(boundary, path, f"executionBoundary.{key}", value)

    summary = mapping_value(payload.get("summary"))
    for key in (
        "acceptedCount",
        "errorCount",
        "warningCount",
        "executedAdapterCount",
        "runtimeImplementedAdapterCount",
    ):
        if type(summary.get(key)) is not int:
            raise ValueError(
                f"trusted local adapter run report {path} must include integer summary.{key}"
            )
    if summary["errorCount"] != 0:
        raise ValueError(f"trusted local adapter run report {path} must record errorCount 0")
    if summary["executedAdapterCount"] != 0:
        raise ValueError(
            f"trusted local adapter run report {path} must record executedAdapterCount 0"
        )
    if int_value(summary.get("runtimeImplementedAdapterCount")) != 0:
        raise ValueError(
            f"trusted local adapter run report {path} must record runtimeImplementedAdapterCount 0"
        )

    statements = payload.get("nonAuthorityStatements")
    if not isinstance(statements, list):
        raise ValueError(
            f"trusted local adapter run report {path} must include nonAuthorityStatements"
        )
    missing = [
        statement
        for statement in REQUIRED_TRUSTED_LOCAL_ADAPTER_RUN_NON_AUTHORITY_STATEMENTS
        if statement not in statements
    ]
    if missing:
        raise ValueError(
            f"trusted local adapter run report {path} is missing nonAuthorityStatements: "
            f"{', '.join(missing)}"
        )


def require_trusted_run_exact_value(
    payload: dict[str, Any],
    path: Path,
    field: str,
    expected: str | int | bool,
) -> None:
    value = payload.get(field.rsplit(".", maxsplit=1)[-1])
    if type(expected) is int and type(value) is not int:
        raise ValueError(f"trusted local adapter run report {path} must include integer {field}")
    if value != expected:
        raise ValueError(
            f"trusted local adapter run report {path} must record {field} {expected!r}"
        )


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


def count_profile_decision(repositories: list[dict[str, Any]], decision: str) -> int:
    return sum(
        1
        for repository in repositories
        if isinstance(repository.get("repositoryProfileDetection"), dict)
        and repository["repositoryProfileDetection"].get("decision") == decision
    )


def sum_nested_summary(repositories: list[dict[str, Any]], key: str, summary_key: str) -> int:
    total = 0
    for repository in repositories:
        record = repository.get(key)
        if not isinstance(record, dict):
            continue
        summary = record.get("summary")
        if not isinstance(summary, dict):
            continue
        value = summary.get(summary_key)
        if isinstance(value, int):
            total += value
    return total


def candidate_records(draft_result: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in draft_result.get("candidates", []) if isinstance(item, dict)]


def safe_bundle_path(root: Path, relative: Any) -> Path:
    value = str(relative or "")
    path = Path(value)
    if not value or path.is_absolute():
        return root / "__invalid__"
    resolved_root = root.resolve()
    resolved = (resolved_root / path).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        return root / "__invalid__"
    return resolved


def safe_enriched_candidate_dir(package_id: str) -> str:
    candidate = "".join(ch if ch.isalnum() or ch in "._-" else "-" for ch in package_id)
    return candidate.strip(".-") or "package"


def mapping_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON artifact must be an object: {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
