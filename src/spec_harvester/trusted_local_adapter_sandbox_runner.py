from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.producer_receipt import canonical_sha256
from spec_harvester.trusted_local_adapter_runner import (
    artifact_reference,
    digest_string,
    object_value,
    path_reference_candidates,
    path_reference_root,
    read_json_object,
    render_json,
)

TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_API_VERSION = (
    "spec-harvester.trusted-local-adapter-sandbox-contract/v0"
)
TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_KIND = "SpecHarvesterTrustedLocalAdapterSandboxContract"
TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_SCHEMA_VERSION = 1
TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_AUTHORITY = (
    "producer_trusted_local_adapter_sandbox_contract_only"
)

TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_API_VERSION = (
    "spec-harvester.trusted-local-adapter-sandbox-preflight/v0"
)
TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_KIND = (
    "SpecHarvesterTrustedLocalAdapterSandboxPreflightReport"
)
TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_SCHEMA_VERSION = 1
TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_AUTHORITY = (
    "producer_trusted_local_adapter_sandbox_preflight_only"
)

TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_API_VERSION = (
    "spec-harvester.trusted-local-adapter-sandbox-runner-validation/v0"
)
TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_KIND = (
    "SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport"
)
TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_SCHEMA_VERSION = 1
TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_AUTHORITY = (
    "producer_trusted_local_adapter_sandbox_runner_validation_only"
)


@dataclass(frozen=True)
class TrustedLocalAdapterSandboxRunnerValidationOptions:
    contract: Path
    preflight: Path


def build_trusted_local_adapter_sandbox_runner_validation_report(
    options: TrustedLocalAdapterSandboxRunnerValidationOptions,
) -> dict[str, Any]:
    return TrustedLocalAdapterSandboxRunnerValidation(options).report()


def write_trusted_local_adapter_sandbox_runner_validation_report(
    path: Path, payload: dict[str, Any]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_json(payload), encoding="utf-8")


class TrustedLocalAdapterSandboxRunnerValidation:
    def __init__(self, options: TrustedLocalAdapterSandboxRunnerValidationOptions):
        self.options = options

    def report(self) -> dict[str, Any]:
        contract = read_json_object(
            self.options.contract,
            "trusted local adapter sandbox contract",
        )
        preflight = read_json_object(
            self.options.preflight,
            "trusted local adapter sandbox preflight report",
        )
        contract_digest = digest_string(self.options.contract)
        preflight_digest = digest_string(self.options.preflight)
        artifact_root = path_reference_root(self.options.contract, self.options.preflight)

        check_contract_identity(contract)
        check_contract_boundary(contract)
        check_preflight_identity(preflight)
        check_preflight_result(preflight)
        check_preflight_contract_reference(
            preflight,
            contract_path=self.options.contract,
            contract_digest=contract_digest,
            reference_root=artifact_root,
        )

        contract_ref = artifact_reference(
            path=self.options.contract,
            reference_root=artifact_root,
            digest=contract_digest,
            api_version=TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_API_VERSION,
            kind=TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_KIND,
            schema_version=TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_SCHEMA_VERSION,
            authority=TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_AUTHORITY,
        )
        preflight_ref = artifact_reference(
            path=self.options.preflight,
            reference_root=artifact_root,
            digest=preflight_digest,
            api_version=TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_API_VERSION,
            kind=TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_KIND,
            schema_version=TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_SCHEMA_VERSION,
            authority=TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_AUTHORITY,
        )
        checks = accepted_checks()
        return {
            "apiVersion": TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_API_VERSION,
            "kind": TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_KIND,
            "schemaVersion": TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_SCHEMA_VERSION,
            "status": "no_execution_validation_report_emitted",
            "validationId": validation_id(contract_ref, preflight_ref),
            "authority": TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_AUTHORITY,
            "contract": {
                "purpose": (
                    "Validate trusted local adapter sandbox contract and preflight "
                    "artifacts through a disabled no-execution runner validation."
                ),
                "contractVersion": "0.1.0",
                "defaultExecution": "disabled",
                "runnerAuthority": TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_AUTHORITY,
                "sandboxContractAuthority": TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_AUTHORITY,
                "sandboxPreflightAuthority": TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_AUTHORITY,
                "runnerValidationIsExecutionPermission": False,
            },
            "sandboxContract": contract_ref,
            "sandboxPreflight": {
                **preflight_ref,
                "status": "passed",
                "contractDigestVerified": True,
                "preflightPassIsExecutionPermission": False,
            },
            "runner": {
                "mode": "disabled_no_execution_sandbox_runner_validation",
                "enabled": False,
                "runtimeImplemented": False,
                "sandboxRunnerImplemented": False,
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
                "registryAuthority": False,
            },
            "validation": {
                "status": "passed",
                "acceptedChecks": checks,
                "errorCount": 0,
                "warningCount": 1,
            },
            "executionBoundary": {
                "adapterExecution": "not_run",
                "adapterCodeLoaded": False,
                "adapterProcessSpawned": False,
                "executedAdapterCount": 0,
                "runtimeImplemented": False,
                "sandboxRunnerImplemented": False,
                "sandboxContractIsExecutionPermission": False,
                "sandboxPreflightIsExecutionPermission": False,
                "runnerValidationIsExecutionPermission": False,
                "operatorApprovalProvided": False,
                "appliedToDrafting": False,
                "registryAuthority": False,
                "adapterOutputAccepted": False,
            },
            "summary": {
                "acceptedCount": len(checks),
                "errorCount": 0,
                "warningCount": 1,
                "executedAdapterCount": 0,
                "runtimeImplementedAdapterCount": 0,
            },
            "diagnostics": [
                {
                    "severity": "info",
                    "code": "trusted_local_adapter_sandbox_runner_validation",
                    "message": (
                        "Disabled sandbox runner validation linked contract and preflight "
                        "artifacts without loading adapter code or running adapter processes."
                    ),
                },
                {
                    "severity": "warning",
                    "code": "sandbox_runner_validation_is_not_execution_permission",
                    "message": (
                        "This report is producer-side review evidence only and does not "
                        "grant execution authority or registry authority."
                    ),
                },
            ],
            "nonAuthorityStatements": non_authority_statements(),
            "followUp": {
                "sandboxPlanTask": "P42-T1",
                "sandboxContractTask": "P42-T2",
                "sandboxPreflightReportTask": "P42-T3",
                "syntheticApprovedAdapterRunTask": "P42-T5",
                "realLocalAdapterRunTask": "deferred_until_after_review",
            },
        }


def accepted_checks() -> list[dict[str, str]]:
    return [
        {
            "code": "sandbox_contract_identity_valid",
            "status": "passed",
            "target": "sandboxContract",
            "message": "Sandbox contract identity matches the P42-T2 contract.",
        },
        {
            "code": "sandbox_contract_boundary_no_execution",
            "status": "passed",
            "target": "sandboxContract.executionBoundary",
            "message": (
                "Sandbox contract records no execution permission and no registry authority."
            ),
        },
        {
            "code": "sandbox_preflight_identity_valid",
            "status": "passed",
            "target": "sandboxPreflight",
            "message": "Sandbox preflight identity matches the P42-T3 contract.",
        },
        {
            "code": "sandbox_preflight_status_passed_review_only",
            "status": "passed",
            "target": "sandboxPreflight.result",
            "message": "Sandbox preflight passed but explicitly remains review evidence only.",
        },
        {
            "code": "sandbox_preflight_contract_digest_matches",
            "status": "passed",
            "target": "sandboxPreflight.sandboxContract",
            "message": "Sandbox preflight contract digest matches the supplied contract bytes.",
        },
        {
            "code": "sandbox_runner_validation_disabled_no_execution",
            "status": "passed",
            "target": "runner",
            "message": "Runner validation did not load adapter code or spawn adapter processes.",
        },
        {
            "code": "non_authority_boundary_preserved",
            "status": "passed",
            "target": "executionBoundary",
            "message": (
                "Runner validation is not execution permission and has no registry authority."
            ),
        },
    ]


def check_contract_identity(payload: dict[str, Any]) -> None:
    if payload.get("apiVersion") != TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_API_VERSION:
        raise ValueError(f"Unsupported sandbox contract apiVersion: {payload.get('apiVersion')!r}")
    if payload.get("kind") != TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_KIND:
        raise ValueError(f"Unsupported sandbox contract kind: {payload.get('kind')!r}")
    if payload.get("schemaVersion") != TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported sandbox contract schemaVersion: {payload.get('schemaVersion')!r}"
        )
    if payload.get("authority") != TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_AUTHORITY:
        raise ValueError(f"Unsupported sandbox contract authority: {payload.get('authority')!r}")


def check_contract_boundary(payload: dict[str, Any]) -> None:
    boundary = object_value(payload.get("executionBoundary"), "sandbox contract executionBoundary")
    if boundary.get("adapterExecution") != "not_run":
        raise ValueError("Sandbox contract executionBoundary adapterExecution must be not_run")
    if boundary.get("adapterCodeLoaded") is not False:
        raise ValueError("Sandbox contract executionBoundary adapterCodeLoaded must be false")
    if boundary.get("adapterProcessSpawned") is not False:
        raise ValueError("Sandbox contract executionBoundary adapterProcessSpawned must be false")
    if type(boundary.get("executedAdapterCount")) is not int:
        raise ValueError("Sandbox contract executionBoundary executedAdapterCount must be integer")
    if boundary.get("executedAdapterCount") != 0:
        raise ValueError("Sandbox contract executionBoundary executedAdapterCount must be 0")
    if boundary.get("registryAuthority") is not False:
        raise ValueError("Sandbox contract executionBoundary registryAuthority must be false")
    if boundary.get("sandboxContractIsExecutionPermission") is not False:
        raise ValueError(
            "Sandbox contract executionBoundary sandboxContractIsExecutionPermission must be false"
        )


def check_preflight_identity(payload: dict[str, Any]) -> None:
    if payload.get("apiVersion") != TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_API_VERSION:
        raise ValueError(f"Unsupported sandbox preflight apiVersion: {payload.get('apiVersion')!r}")
    if payload.get("kind") != TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_KIND:
        raise ValueError(f"Unsupported sandbox preflight kind: {payload.get('kind')!r}")
    if payload.get("schemaVersion") != TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported sandbox preflight schemaVersion: {payload.get('schemaVersion')!r}"
        )
    if payload.get("authority") != TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_AUTHORITY:
        raise ValueError(f"Unsupported sandbox preflight authority: {payload.get('authority')!r}")


def check_preflight_result(payload: dict[str, Any]) -> None:
    result = object_value(payload.get("result"), "sandbox preflight result")
    if result.get("status") != "passed":
        raise ValueError("Sandbox preflight result status must be passed")
    if result.get("decision") != "sandbox_preflight_passed_review_only":
        raise ValueError("Sandbox preflight decision must be sandbox_preflight_passed_review_only")
    if result.get("preflightPassIsExecutionPermission") is not False:
        raise ValueError(
            "Sandbox preflight result must record preflightPassIsExecutionPermission false"
        )
    if result.get("adapterExecution") != "not_run":
        raise ValueError("Sandbox preflight result adapterExecution must be not_run")
    if result.get("adapterCodeLoaded") is not False:
        raise ValueError("Sandbox preflight result adapterCodeLoaded must be false")
    if result.get("adapterProcessSpawned") is not False:
        raise ValueError("Sandbox preflight result adapterProcessSpawned must be false")
    if result.get("registryAuthority") is not False:
        raise ValueError("Sandbox preflight result registryAuthority must be false")

    boundary = object_value(payload.get("executionBoundary"), "sandbox preflight executionBoundary")
    if boundary.get("adapterExecution") != "not_run":
        raise ValueError("Sandbox preflight executionBoundary adapterExecution must be not_run")
    if boundary.get("adapterCodeLoaded") is not False:
        raise ValueError("Sandbox preflight executionBoundary adapterCodeLoaded must be false")
    if boundary.get("adapterProcessSpawned") is not False:
        raise ValueError("Sandbox preflight executionBoundary adapterProcessSpawned must be false")
    if boundary.get("registryAuthority") is not False:
        raise ValueError("Sandbox preflight executionBoundary registryAuthority must be false")
    if boundary.get("sandboxPreflightIsExecutionPermission") is not False:
        raise ValueError(
            "Sandbox preflight executionBoundary "
            "sandboxPreflightIsExecutionPermission must be false"
        )


def check_preflight_contract_reference(
    payload: dict[str, Any],
    *,
    contract_path: Path,
    contract_digest: str,
    reference_root: Path,
) -> None:
    reference = object_value(payload.get("sandboxContract"), "sandbox preflight contract reference")
    if reference.get("kind") != TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_KIND:
        raise ValueError(f"Sandbox preflight contract kind mismatch: {reference.get('kind')!r}")
    if reference.get("authority") != TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_AUTHORITY:
        raise ValueError(
            f"Sandbox preflight contract authority mismatch: {reference.get('authority')!r}"
        )
    if reference.get("digest") != contract_digest:
        raise ValueError("Sandbox preflight contract digest does not match contract artifact bytes")
    if str(reference.get("path") or "") not in path_reference_candidates(
        contract_path,
        reference_root=reference_root,
    ):
        raise ValueError("Sandbox preflight contract path does not reference supplied contract")


def validation_id(contract_ref: dict[str, Any], preflight_ref: dict[str, Any]) -> str:
    digest = canonical_sha256({"sandboxContract": contract_ref, "sandboxPreflight": preflight_ref})
    return f"trusted-local-adapter-sandbox-runner-validation-{digest[:16]}"


def non_authority_statements() -> list[str]:
    return [
        "sandbox_runner_validation_is_not_execution_permission",
        "sandbox_contract_is_not_execution_permission",
        "sandbox_preflight_is_not_execution_permission",
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
        "does_not_treat_sandbox_contract_as_registry_truth",
        "does_not_treat_sandbox_preflight_as_registry_truth",
        "does_not_treat_ai_output_as_registry_truth",
    ]
