from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

from spec_harvester.model_json_repair import (
    DEFAULT_JSON_REPAIR_MAX_ATTEMPTS,
    ModelJsonFailure,
    ModelJsonParseError,
    complete_json_with_repair,
)
from spec_harvester.model_json_repair import (
    parse_model_json_object as parse_model_json_object_shared,
)
from spec_harvester.package_set_drafter import read_inventory
from spec_harvester.producer_receipt import digest_record, sha256_file
from spec_harvester.producer_reports import (
    AUTHOR_READY_STATUS_READY,
    AUTHOR_READY_STOP_DECISION_STOP,
    stop_policy_summary_from_diagnostics,
)

PACKAGE_SET_AI_DRAFT_API_VERSION = "spec-harvester.package-set-ai-draft/v0"
PACKAGE_SET_AI_DRAFT_KIND = "SpecHarvesterPackageSetAIDraftProposal"
PACKAGE_SET_AI_DRAFT_SCHEMA_VERSION = 1
PACKAGE_SET_AI_DRAFT_REQUESTS_KIND = "SpecHarvesterPackageSetAIDraftRequests"
DEFAULT_TIMEOUT_SECONDS = 120.0
DEFAULT_MAX_OUTPUT_TOKENS = 3000
DEFAULT_TEMPERATURE = 0.0
LOCAL_PROVIDER_HOSTS = {"localhost", "127.0.0.1", "::1"}
MAX_EVIDENCE_TEXT_CHARS = 8000

PROPOSED_MEMBER_ROLES = {
    "workspace",
    "primary_package",
    "published_package",
    "plugin_package",
    "cli_package",
    "platform_binary_package",
    "example_package",
    "fixture_package",
    "test_package",
    "private_tooling_package",
    "member_package",
}

PROPOSED_MEMBER_ROLE_ALIASES = {
    "adapter": "plugin_package",
    "adapter_package": "plugin_package",
    "binding": "published_package",
    "binary": "platform_binary_package",
    "binary_package": "platform_binary_package",
    "bridge": "plugin_package",
    "bridge_package": "plugin_package",
    "cli": "cli_package",
    "command_line": "cli_package",
    "command_line_package": "cli_package",
    "core": "primary_package",
    "core_library": "primary_package",
    "core_package": "primary_package",
    "core_runtime": "primary_package",
    "demo": "example_package",
    "demo_package": "example_package",
    "example": "example_package",
    "extension": "plugin_package",
    "extension_package": "plugin_package",
    "fixture": "fixture_package",
    "framework_adapter": "plugin_package",
    "framework_binding": "published_package",
    "internal_tool": "private_tooling_package",
    "internal_tooling": "private_tooling_package",
    "library": "published_package",
    "library_package": "published_package",
    "main": "primary_package",
    "main_package": "primary_package",
    "member": "member_package",
    "module": "member_package",
    "native_binary": "platform_binary_package",
    "npm_package": "published_package",
    "package": "member_package",
    "package_set_root": "workspace",
    "playground": "example_package",
    "primary": "primary_package",
    "public_package": "published_package",
    "published": "published_package",
    "react_binding": "published_package",
    "root": "workspace",
    "root_package": "workspace",
    "runtime": "primary_package",
    "runtime_package": "primary_package",
    "sub_package": "member_package",
    "subpackage": "member_package",
    "svelte_binding": "published_package",
    "test": "test_package",
    "testing": "test_package",
    "tool": "private_tooling_package",
    "tooling": "private_tooling_package",
    "tooling_package": "private_tooling_package",
    "workspace_member": "member_package",
    "workspace_package": "workspace",
}

TRUST_BOUNDARY_NOTES = [
    "Workspace inventory remains deterministic producer evidence.",
    "LLM output is a schema-bound package-set draft proposal only.",
    (
        "Model output cannot accept packages, accept relations, mutate generated "
        "specs, or publish registry metadata."
    ),
    "SpecPM remains the validation, acceptance, relation, and registry authority.",
    "Maintainers decide which proposed members, exclusions, and relations are accepted.",
    "Raw prompts, raw provider responses, secrets, and model chain-of-thought are not persisted.",
]


@dataclass(frozen=True)
class PackageSetAIDraftProposalOptions:
    inventory: Path
    source_checkout: Path | None = None
    provider_base_url: str | None = None
    provider_name: str = "lm_studio"
    model: str | None = None
    model_output: Path | None = None
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    json_repair_max_attempts: int = DEFAULT_JSON_REPAIR_MAX_ATTEMPTS


class PackageSetAIDraftProposalError(RuntimeError):
    """Raised when package-set AI draft proposal generation fails."""


class OpenAICompatibleDraftProvider:
    def __init__(
        self,
        *,
        base_url: str,
        provider_name: str,
        model: str,
        timeout_seconds: float,
        max_output_tokens: int,
        temperature: float,
        json_repair_max_attempts: int,
    ) -> None:
        self.base_url = normalize_local_provider_base_url(base_url)
        self.provider_name = provider_name
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.json_repair_max_attempts = json_repair_max_attempts

    def complete_json(self, request: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        started = time.monotonic()
        system_prompt = (
            "Return exactly one valid JSON object and no prose. "
            "Use only supplied evidence paths. Do not claim registry acceptance."
        )
        result = complete_json_with_repair(
            request=request,
            system_prompt=system_prompt,
            send_messages=self.send_messages,
            max_repair_attempts=self.json_repair_max_attempts,
        )
        raw_content = result.raw_content
        response_payload = result.response_payload
        receipt = {
            "providerKind": "openai_compatible",
            "providerName": self.provider_name,
            "baseUrl": self.base_url,
            "endpoint": "/v1/chat/completions",
            "modelId": str(response_payload.get("model") or self.model),
            "requestId": f"package-set-ai-draft-{request['packageSet']['id']}",
            "startedAt": utc_now(),
            "durationMs": int((time.monotonic() - started) * 1000),
            "temperature": self.temperature,
            "maxOutputTokens": self.max_output_tokens,
            "usage": result.usage,
            "jsonRepairNeeded": result.repair_needed,
            "jsonRepairAttemptCount": result.repair_attempt_count,
            "jsonRepairStatus": result.repair_status,
            "rawPromptPersisted": False,
            "rawResponsePersisted": False,
            "chainOfThoughtPersisted": False,
        }
        if isinstance(result, ModelJsonFailure):
            return {}, receipt
        receipt["responseDigest"] = sha256_text(raw_content)
        return result.payload, receipt

    def send_messages(self, messages: list[dict[str, str]]) -> tuple[str, dict[str, Any]]:
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_output_tokens,
            "messages": messages,
        }
        http_request = urllib.request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            raise PackageSetAIDraftProposalError(f"Provider request failed: {exc}") from exc

        try:
            choice = response_payload["choices"][0]
            raw_content = choice["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise PackageSetAIDraftProposalError("Provider response has unexpected shape") from exc
        if not isinstance(raw_content, str):
            raise PackageSetAIDraftProposalError("Provider response content must be a string")
        return raw_content, response_payload


def build_package_set_ai_draft_proposal(
    options: PackageSetAIDraftProposalOptions,
) -> dict[str, Any]:
    if options.json_repair_max_attempts < 0:
        raise ValueError("json_repair_max_attempts must be zero or greater")
    if options.model_output is not None and (options.provider_base_url or options.model):
        raise ValueError("--model-output cannot be combined with provider execution options")
    request = model_request_record(options)
    model_output: dict[str, Any]
    provider_receipt: dict[str, Any]
    provider_record: dict[str, Any]
    if options.model_output is not None:
        model_output = model_output_from_file(options.model_output)
        provider_receipt = {"source": str(options.model_output), "execution": "external"}
        provider_record = {
            "kind": "external_model_output",
            "name": "external",
            "model": None,
            "baseUrl": None,
            "execution": "not_run_by_spec_harvester",
        }
    else:
        if not options.provider_base_url or not options.model:
            raise ValueError("provider execution requires --provider-base-url and --model")
        provider = OpenAICompatibleDraftProvider(
            base_url=options.provider_base_url,
            provider_name=options.provider_name,
            model=options.model,
            timeout_seconds=options.timeout_seconds,
            max_output_tokens=options.max_output_tokens,
            temperature=options.temperature,
            json_repair_max_attempts=options.json_repair_max_attempts,
        )
        model_output, provider_receipt = provider.complete_json(request)
        provider_record = {
            "kind": "openai_compatible",
            "name": options.provider_name,
            "model": options.model,
            "baseUrl": provider.base_url,
            "execution": "operator_opt_in_local",
        }
    return proposal_from_model_output(
        request=request,
        model_output=model_output,
        provider=provider_record,
        provider_receipt=provider_receipt,
    )


def model_request_record(options: PackageSetAIDraftProposalOptions) -> dict[str, Any]:
    inventory_path = options.inventory.resolve()
    inventory = read_inventory(inventory_path)
    packages = package_records(inventory)
    if not packages:
        packages = source_package_fallback_records(inventory)
    workspace_id = workspace_package_id(packages)
    evidence = evidence_records(inventory_path, inventory, options.source_checkout)
    evidence_paths = [item["path"] for item in evidence]
    return {
        "task": (
            "Propose a reviewable SpecPM package-set draft from deterministic workspace inventory."
        ),
        "apiVersion": PACKAGE_SET_AI_DRAFT_API_VERSION,
        "kind": "SpecHarvesterPackageSetAIDraftRequest",
        "schemaVersion": PACKAGE_SET_AI_DRAFT_SCHEMA_VERSION,
        "packageSet": {
            "id": workspace_id,
            "source": mapping_value(inventory.get("source")),
            "packageInventoryCount": len(packages),
        },
        "requiredJsonShape": {
            "packageSet": {
                "packageId": workspace_id,
                "summary": "one sentence repository/package-set summary",
                "evidencePaths": ["workspace-inventory.json"],
                "confidence": "high|medium|low",
            },
            "selectedMembers": [
                {
                    "packageId": "stable package id from inventory",
                    "role": (
                        "primary_package|published_package|plugin_package|cli_package|"
                        "platform_binary_package|example_package|fixture_package|"
                        "test_package|private_tooling_package"
                    ),
                    "sourceTargetPath": "path from inventory",
                    "reason": "why this member belongs in the package set",
                    "evidencePaths": ["workspace-inventory.json", "packages/name/package.json"],
                    "confidence": "high|medium|low",
                }
            ],
            "excludedPackages": [
                {
                    "packageId": "stable package id from inventory",
                    "category": (
                        "fixture|test|example|private_tooling|platform_artifact|out_of_scope"
                    ),
                    "reason": "why this inventory package should not become a primary member",
                    "evidencePaths": ["workspace-inventory.json"],
                    "confidence": "high|medium|low",
                }
            ],
            "relations": [
                {
                    "id": "stable relation id",
                    "type": "contains",
                    "sourcePackageId": workspace_id,
                    "targetPackageId": "selected member package id",
                    "evidencePaths": ["workspace-inventory.json"],
                    "confidence": "high|medium|low",
                }
            ],
            "evidenceGaps": ["missing deterministic evidence"],
            "overallConfidence": "high|medium|low",
        },
        "constraints": [
            "Return proposal evidence only; do not claim registry acceptance.",
            "Use only packageIds and sourceTargetPath values present in inventory.",
            "Use only supplied evidence paths.",
            (
                "Prefer primary published packages over tests, fixtures, examples, "
                "playgrounds, or platform-only binary packages."
            ),
            "Explain every selected member and every important exclusion.",
            "Relations may only connect the aggregate package set to selected members.",
        ],
        "allowedEvidencePaths": evidence_paths,
        "evidence": evidence,
        "packages": compact_package_records(packages),
        "privacy": {
            "rawPromptsPersisted": False,
            "rawModelResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "secretsIncluded": False,
        },
    }


def proposal_from_model_output(
    *,
    request: dict[str, Any],
    model_output: dict[str, Any],
    provider: dict[str, Any],
    provider_receipt: dict[str, Any],
) -> dict[str, Any]:
    diagnostics: list[dict[str, Any]] = []
    diagnostics.extend(json_repair_diagnostics(provider_receipt, "packageSet"))
    allowed_paths = set(string_list(request.get("allowedEvidencePaths")))
    inventory_by_id = {
        item["packageId"]: item
        for item in list_value(request.get("packages"))
        if isinstance(item, dict) and isinstance(item.get("packageId"), str)
    }
    validation_guard = model_output_validation_guard(model_output, request, inventory_by_id)
    diagnostics.extend(validation_guard["diagnostics"])
    package_set = package_set_proposal(model_output, request, allowed_paths, diagnostics)
    selected_members = selected_member_proposals(
        model_output, inventory_by_id, allowed_paths, diagnostics
    )
    selected_ids = {member["packageId"] for member in selected_members}
    excluded_packages = excluded_package_proposals(
        model_output,
        inventory_by_id,
        selected_ids,
        allowed_paths,
        diagnostics,
        report_unknown_exclusions=False,
    )
    relations = relation_proposals(
        model_output,
        package_set,
        selected_ids,
        allowed_paths,
        diagnostics,
    )
    error_count = sum(1 for item in diagnostics if item["severity"] == "error")
    warning_count = sum(1 for item in diagnostics if item["severity"] == "warning")
    status = "failed" if error_count else ("warning" if warning_count else "completed")
    return {
        "apiVersion": PACKAGE_SET_AI_DRAFT_API_VERSION,
        "kind": PACKAGE_SET_AI_DRAFT_KIND,
        "schemaVersion": PACKAGE_SET_AI_DRAFT_SCHEMA_VERSION,
        "status": status,
        "authority": "proposal_only_not_registry_acceptance",
        "packageSet": package_set,
        "selectedMembers": selected_members,
        "excludedPackages": excluded_packages,
        "relations": relations,
        "provider": provider,
        "providerReceipt": provider_receipt,
        "validationGuard": validation_guard,
        "inputs": input_records(request),
        "diagnostics": diagnostics,
        "summary": {
            "selectedMemberCount": len(selected_members),
            "excludedPackageCount": len(excluded_packages),
            "relationCount": len(relations),
            "errorCount": error_count,
            "warningCount": warning_count,
        },
        "stopPolicySummary": package_set_ai_draft_stop_policy_summary(
            source_status=status,
            error_count=error_count,
            warning_count=warning_count,
            subject_count=len(selected_members),
            inventory_by_id=inventory_by_id,
            package_set=package_set,
            validation_guard=validation_guard,
        ),
        "evidenceGaps": string_list(model_output.get("evidenceGaps")),
        "overallConfidence": confidence_value(model_output.get("overallConfidence")),
        "privacy": {
            "rawPromptsPersisted": False,
            "rawModelResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "secretsIncluded": False,
        },
        "trustBoundary": TRUST_BOUNDARY_NOTES,
        "nonGoals": [
            "deterministic_spec_generation",
            "specpm_acceptance",
            "package_acceptance",
            "relation_acceptance",
            "registry_publication",
            "package_execution",
            "package_manager_execution",
            "model_authored_file_mutation",
        ],
    }


def model_output_validation_guard(
    model_output: dict[str, Any],
    request: dict[str, Any],
    inventory_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    diagnostics: list[dict[str, Any]] = []
    output_package_set = mapping_value(model_output.get("packageSet"))
    request_package_set = mapping_value(request.get("packageSet"))
    request_package_id = string_value(request_package_set.get("id"))
    output_package_id = string_value(output_package_set.get("packageId"))

    if not request_package_id and not output_package_id:
        diagnostics.append(
            diagnostic(
                "error",
                "package_set_subject_identity_missing",
                (
                    "Model output and deterministic request context both omit "
                    "the package-set subject identity."
                ),
                "packageSet",
                {
                    "modelField": "packageSet.packageId",
                    "requestField": "packageSet.id",
                },
            )
        )

    if len(inventory_by_id) > 1:
        for index, item in enumerate(list_value(model_output.get("excludedPackages"))):
            if not isinstance(item, dict):
                continue
            package_id = string_value(item.get("packageId"))
            if not package_id or package_id not in inventory_by_id:
                diagnostics.append(
                    diagnostic(
                        "warning",
                        "excluded_package_unknown",
                        ("Excluded package packageId is not present in workspace inventory."),
                        package_id,
                        {"index": index},
                    )
                )

    error_count = sum(1 for item in diagnostics if item["severity"] == "error")
    warning_count = sum(1 for item in diagnostics if item["severity"] == "warning")
    status = "failed" if error_count else ("warning" if warning_count else "passed")
    return {
        "authority": "producer_deterministic_pre_normalization_validation",
        "status": status,
        "diagnosticCount": len(diagnostics),
        "errorCount": error_count,
        "warningCount": warning_count,
        "diagnostics": diagnostics,
    }


def package_set_proposal(
    model_output: dict[str, Any],
    request: dict[str, Any],
    allowed_paths: set[str],
    diagnostics: list[dict[str, Any]],
) -> dict[str, Any]:
    output_value = model_output.get("packageSet")
    output = mapping_value(output_value)
    fallback = mapping_value(request.get("packageSet"))
    request_package_id = string_value(fallback.get("id"))
    output_package_id = string_value(output.get("packageId"))
    package_id = request_package_id or output_package_id
    if not isinstance(output_value, dict):
        diagnostics.append(
            diagnostic(
                "warning",
                "package_set_subject_metadata_missing",
                "Model output omits the top-level packageSet metadata object.",
                package_id,
                {
                    "modelField": "packageSet",
                    "requestField": "packageSet.id",
                },
            )
        )
    evidence_paths = supported_paths(
        string_list(output.get("evidencePaths")),
        allowed_paths,
        diagnostics,
        "packageSet",
        package_id,
    )
    if not evidence_paths and "workspace-inventory.json" in allowed_paths:
        evidence_paths = ["workspace-inventory.json"]
    if output_package_id and request_package_id and output_package_id != request_package_id:
        diagnostics.append(
            diagnostic(
                "error",
                "package_set_id_mismatch",
                "Model output packageSet.packageId disagrees with the request package-set id.",
                request_package_id,
                {"modelPackageId": output_package_id},
            )
        )
    return {
        "packageId": package_id,
        "summary": string_value(output.get("summary")),
        "evidencePaths": evidence_paths,
        "confidence": confidence_value(output.get("confidence")),
    }


def selected_member_proposals(
    model_output: dict[str, Any],
    inventory_by_id: dict[str, dict[str, Any]],
    allowed_paths: set[str],
    diagnostics: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    records = []
    seen: set[str] = set()
    for index, item in enumerate(list_value(model_output.get("selectedMembers"))):
        if not isinstance(item, dict):
            diagnostics.append(
                diagnostic(
                    "warning",
                    "selected_member_invalid",
                    "selectedMembers item is not an object.",
                    "",
                    {"index": index},
                )
            )
            continue
        package_id = string_value(item.get("packageId"))
        if not package_id or package_id not in inventory_by_id:
            diagnostics.append(
                diagnostic(
                    "error",
                    "selected_member_unknown",
                    "Selected member packageId is not present in workspace inventory.",
                    package_id,
                    {"index": index},
                )
            )
            continue
        if package_id in seen:
            diagnostics.append(
                diagnostic(
                    "warning",
                    "selected_member_duplicate",
                    "Selected member is duplicated.",
                    package_id,
                )
            )
            continue
        seen.add(package_id)
        inventory_record = inventory_by_id[package_id]
        model_role = string_value(item.get("role"))
        role, role_normalized = normalize_selected_member_role(model_role)
        if not role_normalized:
            diagnostics.append(
                diagnostic(
                    "warning",
                    "selected_member_role_unknown",
                    "Selected member role is outside the documented taxonomy.",
                    package_id,
                    {
                        "modelRole": model_role,
                        "normalizedFallbackRole": role,
                    },
                )
            )
        records.append(
            {
                "packageId": package_id,
                "role": role,
                "inventoryRole": string_value(inventory_record.get("inventoryRole")),
                "sourceTargetPath": string_value(inventory_record.get("sourceTargetPath")),
                "manifestPath": string_value(inventory_record.get("manifestPath")),
                "reason": string_value(item.get("reason")),
                "evidencePaths": supported_paths(
                    string_list(item.get("evidencePaths")),
                    allowed_paths,
                    diagnostics,
                    "selectedMembers",
                    package_id,
                ),
                "confidence": confidence_value(item.get("confidence")),
            }
        )
    return sorted(records, key=lambda item: item["packageId"])


def normalize_selected_member_role(model_role: str) -> tuple[str, bool]:
    if not model_role:
        return "member_package", True
    normalized = re.sub(r"[^a-z0-9]+", "_", model_role.strip().lower()).strip("_")
    if normalized in PROPOSED_MEMBER_ROLES:
        return normalized, True
    alias = PROPOSED_MEMBER_ROLE_ALIASES.get(normalized)
    if alias is not None:
        return alias, True
    return "member_package", False


def package_set_ai_draft_stop_policy_summary(
    *,
    source_status: str,
    error_count: int,
    warning_count: int,
    subject_count: int,
    inventory_by_id: dict[str, dict[str, Any]],
    package_set: dict[str, Any],
    validation_guard: dict[str, Any],
) -> dict[str, Any]:
    summary = stop_policy_summary_from_diagnostics(
        source_status=source_status,
        error_count=error_count,
        warning_count=warning_count,
        subject_count=subject_count,
    )
    zero_subject_policy = zero_subject_policy_record(
        source_status=source_status,
        error_count=error_count,
        warning_count=warning_count,
        subject_count=subject_count,
        inventory_by_id=inventory_by_id,
        package_set=package_set,
        validation_guard=validation_guard,
    )
    if zero_subject_policy["status"] == "accepted_non_blocking":
        summary["status"] = AUTHOR_READY_STATUS_READY
        summary["decision"] = AUTHOR_READY_STOP_DECISION_STOP
        summary["reason"] = "single_package_no_proposal_subjects_non_blocking"
        summary["summary"] = (
            "Diagnostic-clean single-package inventory already supplies the proposal "
            "subject; no additional package-set members are required."
        )
    summary["zeroSubjectPolicy"] = zero_subject_policy
    return summary


def zero_subject_policy_record(
    *,
    source_status: str,
    error_count: int,
    warning_count: int,
    subject_count: int,
    inventory_by_id: dict[str, dict[str, Any]],
    package_set: dict[str, Any],
    validation_guard: dict[str, Any],
) -> dict[str, Any]:
    inventory_package_ids = sorted(inventory_by_id)
    record = {
        "status": "not_applicable",
        "reason": "proposal_subjects_present",
        "inventoryPackageCount": len(inventory_package_ids),
        "inventoryPackageIds": inventory_package_ids,
        "packageSetId": string_value(package_set.get("packageId")),
    }
    if subject_count > 0:
        return record
    record["status"] = "requires_regeneration"
    if len(inventory_by_id) != 1:
        record["reason"] = "package_set_requires_selected_members"
        return record
    if source_status != "completed" or error_count or warning_count:
        record["reason"] = "single_package_proposal_has_diagnostics"
        return record
    if validation_guard.get("status") != "passed":
        record["reason"] = "single_package_validation_guard_not_passed"
        return record
    if not record["packageSetId"]:
        record["reason"] = "single_package_package_set_identity_missing"
        return record
    record["status"] = "accepted_non_blocking"
    record["reason"] = "single_package_inventory_subject_stable"
    return record


def excluded_package_proposals(
    model_output: dict[str, Any],
    inventory_by_id: dict[str, dict[str, Any]],
    selected_ids: set[str],
    allowed_paths: set[str],
    diagnostics: list[dict[str, Any]],
    *,
    report_unknown_exclusions: bool = True,
) -> list[dict[str, Any]]:
    records = []
    seen: set[str] = set()
    single_package_inventory = len(inventory_by_id) == 1
    for index, item in enumerate(list_value(model_output.get("excludedPackages"))):
        if not isinstance(item, dict):
            diagnostics.append(
                diagnostic(
                    "warning",
                    "excluded_package_invalid",
                    "excludedPackages item is not an object.",
                    "",
                    {"index": index},
                )
            )
            continue
        package_id = string_value(item.get("packageId"))
        if not package_id or package_id not in inventory_by_id:
            if single_package_inventory:
                continue
            if not report_unknown_exclusions:
                continue
            diagnostics.append(
                diagnostic(
                    "warning",
                    "excluded_package_unknown",
                    "Excluded package packageId is not present in workspace inventory.",
                    package_id,
                    {"index": index},
                )
            )
            continue
        if package_id in selected_ids:
            diagnostics.append(
                diagnostic(
                    "warning",
                    "excluded_package_also_selected",
                    "Excluded package was also selected as a member.",
                    package_id,
                )
            )
        if package_id in seen:
            continue
        seen.add(package_id)
        inventory_record = inventory_by_id[package_id]
        records.append(
            {
                "packageId": package_id,
                "category": string_value(item.get("category")),
                "inventoryRole": string_value(inventory_record.get("inventoryRole")),
                "sourceTargetPath": string_value(inventory_record.get("sourceTargetPath")),
                "manifestPath": string_value(inventory_record.get("manifestPath")),
                "reason": string_value(item.get("reason")),
                "evidencePaths": supported_paths(
                    string_list(item.get("evidencePaths")),
                    allowed_paths,
                    diagnostics,
                    "excludedPackages",
                    package_id,
                ),
                "confidence": confidence_value(item.get("confidence")),
            }
        )
    return sorted(records, key=lambda item: item["packageId"])


def relation_proposals(
    model_output: dict[str, Any],
    package_set: dict[str, Any],
    selected_ids: set[str],
    allowed_paths: set[str],
    diagnostics: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    records = []
    seen: set[str] = set()
    package_set_id = package_set["packageId"]
    for index, item in enumerate(list_value(model_output.get("relations"))):
        if not isinstance(item, dict):
            diagnostics.append(
                diagnostic(
                    "warning",
                    "relation_invalid",
                    "relations item is not an object.",
                    "",
                    {"index": index},
                )
            )
            continue
        source = (
            first_string_value(
                item, ("sourcePackageId", "source", "sourcePackage", "fromPackageId")
            )
            or package_set_id
        )
        target = first_string_value(
            item,
            ("targetPackageId", "target", "targetPackage", "toPackageId", "packageId"),
        )
        relation_type = string_value(item.get("type")) or "contains"
        if relation_type != "contains":
            diagnostics.append(
                diagnostic(
                    "error",
                    "relation_type_unsupported",
                    "Package-set AI draft relations must use type 'contains'.",
                    relation_type,
                    {"index": index},
                )
            )
            continue
        if source != package_set_id:
            diagnostics.append(
                diagnostic(
                    "error",
                    "relation_source_not_package_set",
                    "Relation source must be the proposed aggregate package-set id.",
                    source,
                    {"index": index},
                )
            )
            continue
        if target not in selected_ids:
            diagnostics.append(
                diagnostic(
                    "error",
                    "relation_target_not_selected",
                    "Relation target must be one of the selected member package ids.",
                    target,
                    {"index": index},
                )
            )
            continue
        relation_id = string_value(item.get("id")) or f"{source}.contains.{target}"
        if relation_id in seen:
            continue
        seen.add(relation_id)
        records.append(
            {
                "id": relation_id,
                "type": relation_type,
                "sourcePackageId": source,
                "targetPackageId": target,
                "evidencePaths": supported_paths(
                    string_list(item.get("evidencePaths")),
                    allowed_paths,
                    diagnostics,
                    "relations",
                    relation_id,
                ),
                "confidence": confidence_value(item.get("confidence")),
            }
        )
    return sorted(records, key=lambda item: item["id"])


def supported_paths(
    paths: list[str],
    allowed_paths: set[str],
    diagnostics: list[dict[str, Any]],
    field: str,
    subject: str,
) -> list[str]:
    supported = []
    unsupported = []
    for path in paths:
        clean = path.strip()
        if not clean:
            continue
        if clean in allowed_paths:
            supported.append(clean)
        else:
            unsupported.append(clean)
    if unsupported:
        diagnostics.append(
            diagnostic(
                "warning",
                "model_evidence_path_unsupported",
                f"{field} for {subject} cites unsupported evidence paths.",
                subject,
                {"paths": sorted(set(unsupported))},
            )
        )
    return sorted(set(supported))


def input_records(request: dict[str, Any]) -> list[dict[str, Any]]:
    evidence = [item for item in list_value(request.get("evidence")) if isinstance(item, dict)]
    records = []
    inventory_record = next(
        (item for item in evidence if item.get("role") == "workspace_inventory"),
        None,
    )
    if inventory_record:
        records.append(
            {
                "role": "workspace_inventory",
                "path": inventory_record["path"],
                "pathScope": "request_relative",
                "digest": inventory_record.get("digest"),
            }
        )
    records.append(
        {
            "role": "compact_model_input",
            "packageCount": len(list_value(request.get("packages"))),
            "evidencePathCount": len(string_list(request.get("allowedEvidencePaths"))),
            "evidencePaths": string_list(request.get("allowedEvidencePaths")),
        }
    )
    return records


def evidence_records(
    inventory_path: Path,
    inventory: dict[str, Any],
    source_checkout: Path | None,
) -> list[dict[str, Any]]:
    records = [
        {
            "role": "workspace_inventory",
            "path": "workspace-inventory.json",
            "digest": digest_record(sha256_file(inventory_path)),
            "textIncluded": False,
        }
    ]
    for manifest_path in workspace_manifest_paths(inventory):
        records.append(
            {
                "role": "workspace_manifest",
                "path": manifest_path,
                "textIncluded": False,
            }
        )
    for package in package_records(inventory):
        manifest_path = string_value(package.get("manifestPath"))
        if manifest_path:
            records.append(
                {
                    "role": "package_manifest",
                    "path": manifest_path,
                    "textIncluded": False,
                }
            )
    if source_checkout is not None:
        records.extend(source_checkout_evidence(source_checkout))
    return dedupe_evidence(records)


def source_checkout_evidence(source_checkout: Path) -> list[dict[str, Any]]:
    root = source_checkout.resolve()
    records = []
    for relative, role in (
        ("package.json", "root_package_manifest"),
        ("README.md", "root_readme"),
        ("readme.md", "root_readme"),
    ):
        record = text_evidence_record(root, relative, role)
        if record is not None:
            records.append(record)
    return records


def text_evidence_record(root: Path, relative: str, role: str) -> dict[str, Any] | None:
    artifact = (root / relative).resolve()
    if not artifact.is_file() or not artifact.is_relative_to(root):
        return None
    try:
        text = artifact.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    return {
        "role": role,
        "path": relative,
        "digest": digest_record(sha256_file(artifact)),
        "text": text[:MAX_EVIDENCE_TEXT_CHARS],
        "truncated": len(text) > MAX_EVIDENCE_TEXT_CHARS,
        "textIncluded": True,
    }


def compact_package_records(packages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for package in packages:
        records.append(
            {
                "packageId": string_value(package.get("proposedSpecpmPackageId")),
                "inventoryRole": string_value(package.get("role")),
                "ecosystem": string_value(package.get("ecosystem")),
                "name": string_value(package.get("name")),
                "version": string_value(package.get("version")),
                "sourceTargetPath": string_value(package.get("sourceTargetPath")),
                "manifestPath": string_value(package.get("manifestPath")),
                "packageManager": string_value(package.get("packageManager")),
            }
        )
    return sorted(records, key=lambda item: item["packageId"])


def workspace_package_id(packages: list[dict[str, Any]]) -> str:
    for package in packages:
        if package.get("role") == "workspace" and isinstance(
            package.get("proposedSpecpmPackageId"), str
        ):
            return package["proposedSpecpmPackageId"]
    for package in packages:
        package_id = package.get("proposedSpecpmPackageId")
        if isinstance(package_id, str) and package_id:
            namespace = package_id.split(".")[0]
            return f"{namespace}.workspace"
    return "package-set"


def package_records(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    packages = inventory.get("packages")
    if not isinstance(packages, list):
        return []
    return [item for item in packages if isinstance(item, dict)]


def source_package_fallback_records(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    source = mapping_value(inventory.get("source"))
    package_id = string_value(source.get("packageId"))
    if not package_id:
        return []
    target = mapping_value(source.get("target"))
    return [
        {
            "proposedSpecpmPackageId": package_id,
            "role": "member_package",
            "ecosystem": "",
            "name": package_id,
            "version": "",
            "sourceTargetPath": string_value(target.get("path")) or ".",
            "manifestPath": "",
            "packageManager": "",
        }
    ]


def workspace_manifest_paths(inventory: dict[str, Any]) -> list[str]:
    records = []
    for item in list_value(inventory.get("workspaceManifests")):
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            records.append(item["path"])
    return sorted(set(records))


def model_output_from_file(path: Path) -> dict[str, Any]:
    payload = read_json_object(path)
    if isinstance(payload.get("proposal"), dict):
        return payload["proposal"]
    return payload


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Cannot read JSON artifact {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON artifact {path}: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"JSON artifact must be an object: {path}")
    return payload


def write_model_request_record(path: Path, request: dict[str, Any]) -> None:
    payload = {
        "apiVersion": PACKAGE_SET_AI_DRAFT_API_VERSION,
        "kind": PACKAGE_SET_AI_DRAFT_REQUESTS_KIND,
        "schemaVersion": PACKAGE_SET_AI_DRAFT_SCHEMA_VERSION,
        "requests": [request],
        "privacy": {
            "rawPromptsPersisted": False,
            "rawModelResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "secretsIncluded": False,
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_package_set_ai_draft_proposal(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_model_json_object(raw_content: str) -> dict[str, Any]:
    try:
        return parse_model_json_object_shared(raw_content)
    except ModelJsonParseError as exc:
        raise PackageSetAIDraftProposalError(str(exc)) from exc


def json_repair_diagnostics(
    provider_receipt: dict[str, Any],
    subject: str,
) -> list[dict[str, Any]]:
    if not provider_receipt.get("jsonRepairNeeded"):
        return []
    attempt_count = provider_receipt.get("jsonRepairAttemptCount")
    repair_status = string_value(provider_receipt.get("jsonRepairStatus"))
    diagnostics = [
        diagnostic(
            "warning",
            "ai_json_repair_needed",
            "Initial local model output was not a valid JSON object; bounded repair was attempted.",
            subject,
            {
                "repairAttemptCount": attempt_count if isinstance(attempt_count, int) else 0,
                "jsonRepairStatus": repair_status,
            },
        )
    ]
    if repair_status == "exhausted":
        diagnostics.append(
            diagnostic(
                "error",
                "ai_json_repair_exhausted",
                "Local model output remained invalid JSON after bounded repair attempts.",
                subject,
                {
                    "repairAttemptCount": attempt_count if isinstance(attempt_count, int) else 0,
                },
            )
        )
    return diagnostics


def normalize_local_provider_base_url(value: str) -> str:
    parsed = urllib.parse.urlparse(value.strip().rstrip("/"))
    if parsed.scheme != "http" or parsed.hostname not in LOCAL_PROVIDER_HOSTS:
        raise ValueError("Provider base URL must be an explicit local http URL")
    if parsed.username or parsed.password:
        raise ValueError("Provider base URL must not include credentials")
    if (
        parsed.params
        or parsed.query
        or parsed.fragment
        or ";" in parsed.netloc
        or ";" in parsed.path
    ):
        raise ValueError("Provider base URL must not include params, query, or fragment")
    path = parsed.path.rstrip("/")
    if path == "/v1":
        path = ""
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))


def dedupe_evidence(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    for record in records:
        path = record.get("path")
        if isinstance(path, str) and path not in deduped:
            deduped[path] = record
    return [deduped[path] for path in sorted(deduped)]


def mapping_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def first_string_value(payload: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = string_value(payload.get(key))
        if value:
            return value
    return ""


def string_list(value: Any) -> list[str]:
    return [item for item in list_value(value) if isinstance(item, str)]


def confidence_value(value: Any) -> str:
    return value if value in {"high", "medium", "low"} else "low"


def diagnostic(
    severity: str,
    code: str,
    message: str,
    subject: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "severity": severity,
        "code": code,
        "message": message,
        "subject": subject,
    }
    if extra:
        payload.update(extra)
    return payload


def sha256_text(value: str) -> str:
    return "sha256:" + sha256(value.encode("utf-8")).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
