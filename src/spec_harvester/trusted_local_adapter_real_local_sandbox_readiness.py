from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.producer_receipt import canonical_sha256
from spec_harvester.trusted_local_adapter_runner import (
    artifact_reference,
    digest_string,
    object_value,
    path_reference_root,
    read_json_object,
    render_json,
)
from spec_harvester.trusted_local_adapter_synthetic_sandbox_run_verifier import (
    SYNTHETIC_SANDBOX_RUN_VERIFIER_API_VERSION,
    SYNTHETIC_SANDBOX_RUN_VERIFIER_AUTHORITY,
    SYNTHETIC_SANDBOX_RUN_VERIFIER_KIND,
    SYNTHETIC_SANDBOX_RUN_VERIFIER_SCHEMA_VERSION,
)

REAL_LOCAL_SANDBOX_READINESS_API_VERSION = (
    "spec-harvester.real-local-trusted-adapter-sandbox-run-readiness/v0"
)
REAL_LOCAL_SANDBOX_READINESS_KIND = "SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport"
REAL_LOCAL_SANDBOX_READINESS_SCHEMA_VERSION = 1
REAL_LOCAL_SANDBOX_READINESS_AUTHORITY = (
    "producer_real_local_trusted_adapter_sandbox_run_readiness_only"
)


@dataclass(frozen=True)
class RealLocalTrustedAdapterSandboxRunReadinessOptions:
    verifier_report: Path


def build_real_local_trusted_adapter_sandbox_run_readiness_report(
    options: RealLocalTrustedAdapterSandboxRunReadinessOptions,
) -> dict[str, Any]:
    return RealLocalTrustedAdapterSandboxRunReadiness(options).report()


def write_real_local_trusted_adapter_sandbox_run_readiness_report(
    path: Path,
    payload: dict[str, Any],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_json(payload), encoding="utf-8")


class RealLocalTrustedAdapterSandboxRunReadiness:
    def __init__(self, options: RealLocalTrustedAdapterSandboxRunReadinessOptions):
        self.options = options

    def report(self) -> dict[str, Any]:
        verifier = read_json_object(
            self.options.verifier_report,
            "synthetic sandbox run verifier report",
        )
        verifier_digest = digest_string(self.options.verifier_report)
        artifact_root = path_reference_root(self.options.verifier_report)

        check_verifier_identity(verifier)
        check_verifier_contract(verifier)
        check_verifier_artifact_summaries(verifier)
        operator_binding = check_operator_approval(verifier)
        check_verifier_execution_boundary(verifier)
        check_verifier_non_authority_statements(verifier)

        verifier_ref = artifact_reference(
            path=self.options.verifier_report,
            reference_root=artifact_root,
            digest=verifier_digest,
            api_version=SYNTHETIC_SANDBOX_RUN_VERIFIER_API_VERSION,
            kind=SYNTHETIC_SANDBOX_RUN_VERIFIER_KIND,
            schema_version=SYNTHETIC_SANDBOX_RUN_VERIFIER_SCHEMA_VERSION,
            authority=SYNTHETIC_SANDBOX_RUN_VERIFIER_AUTHORITY,
        )
        checks = accepted_checks()
        return {
            "apiVersion": REAL_LOCAL_SANDBOX_READINESS_API_VERSION,
            "kind": REAL_LOCAL_SANDBOX_READINESS_KIND,
            "schemaVersion": REAL_LOCAL_SANDBOX_READINESS_SCHEMA_VERSION,
            "status": "ready_for_explicit_real_run_review",
            "readinessId": readiness_id(verifier_ref),
            "authority": REAL_LOCAL_SANDBOX_READINESS_AUTHORITY,
            "contract": {
                "purpose": (
                    "Validate prerequisites for reviewing a future real local "
                    "trusted adapter sandbox run without enabling execution."
                ),
                "contractVersion": "0.1.0",
                "readinessAuthority": REAL_LOCAL_SANDBOX_READINESS_AUTHORITY,
                "verifierAuthority": SYNTHETIC_SANDBOX_RUN_VERIFIER_AUTHORITY,
                "readinessIsExecutionPermission": False,
                "readinessIsRegistryAuthority": False,
            },
            "verifierReport": {
                **verifier_ref,
                "status": "passed",
                "digestVerified": True,
                "verifierIsExecutionPermission": False,
            },
            "readinessDecision": {
                "status": "ready_for_explicit_real_run_review",
                "decision": "ready_for_review_not_execution",
                "readyForExplicitReview": True,
                "readyForExecution": False,
                "readinessIsExecutionPermission": False,
                "readinessIsRegistryAuthority": False,
            },
            "realRunPrerequisites": {
                "operatorApproval": operator_approval_prerequisites(operator_binding),
                "sandboxRuntime": sandbox_runtime_prerequisites(),
                "filesystemAndOutputPolicy": filesystem_output_policy_prerequisites(),
                "auditPolicy": audit_policy_prerequisites(),
                "rollbackAndReview": rollback_review_prerequisites(),
            },
            "readinessGate": {
                "mode": "review_only_no_execution_readiness_gate",
                "runtimeInvoked": False,
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
                "runtimeInvoked": False,
                "realRunImplementationPresent": False,
                "readinessGateIsExecutionPermission": False,
                "syntheticRunVerificationIsExecutionPermission": False,
                "appliedToDrafting": False,
                "registryAuthority": False,
                "adapterOutputAccepted": False,
            },
            "summary": {
                "acceptedCount": len(checks),
                "errorCount": 0,
                "warningCount": 1,
                "linkedArtifactCount": verifier["summary"]["linkedArtifactCount"],
                "syntheticOutputCandidateCount": verifier["summary"][
                    "syntheticOutputCandidateCount"
                ],
                "readyForExplicitReview": True,
                "readyForExecution": False,
                "executedAdapterCount": 0,
                "runtimeInvoked": False,
            },
            "diagnostics": [
                {
                    "severity": "info",
                    "code": "real_local_sandbox_run_readiness_gate",
                    "message": (
                        "Verifier report and real-run review prerequisites were "
                        "checked without loading adapter code or spawning processes."
                    ),
                },
                {
                    "severity": "warning",
                    "code": "readiness_gate_is_not_execution_permission",
                    "message": (
                        "This report is readiness evidence for explicit review only; "
                        "it does not grant execution permission or registry authority."
                    ),
                },
            ],
            "nonAuthorityStatements": non_authority_statements(),
            "followUp": {
                "syntheticRunVerifierTask": "P42-T6",
                "realLocalAdapterRunTask": "deferred_until_after_explicit_review",
            },
        }


def accepted_checks() -> list[dict[str, str]]:
    return [
        {
            "code": "verifier_report_identity_valid",
            "status": "passed",
            "target": "verifierReport",
            "message": "Verifier report identity, status, and authority are valid.",
        },
        {
            "code": "verifier_report_no_execution_boundary_preserved",
            "status": "passed",
            "target": "verifierReport.executionBoundary",
            "message": "Verifier report remains non-execution evidence.",
        },
        {
            "code": "operator_approval_prerequisites_declared",
            "status": "passed",
            "target": "realRunPrerequisites.operatorApproval",
            "message": "Real-run approval must be explicit, scoped, and non-reusable.",
        },
        {
            "code": "sandbox_runtime_prerequisites_declared",
            "status": "passed",
            "target": "realRunPrerequisites.sandboxRuntime",
            "message": "Sandbox runtime requirements are declared without invoking runtime.",
        },
        {
            "code": "filesystem_output_audit_policy_declared",
            "status": "passed",
            "target": "realRunPrerequisites",
            "message": "Filesystem, output digest, and audit requirements are declared.",
        },
        {
            "code": "readiness_gate_no_execution",
            "status": "passed",
            "target": "readinessGate",
            "message": "Readiness gate did not load code, spawn processes, or use network.",
        },
        {
            "code": "non_authority_boundary_preserved",
            "status": "passed",
            "target": "nonAuthorityStatements",
            "message": "Readiness gate is not execution permission or registry authority.",
        },
    ]


def check_verifier_identity(payload: dict[str, Any]) -> None:
    if payload.get("apiVersion") != SYNTHETIC_SANDBOX_RUN_VERIFIER_API_VERSION:
        raise ValueError(f"Unsupported verifier apiVersion: {payload.get('apiVersion')!r}")
    if payload.get("kind") != SYNTHETIC_SANDBOX_RUN_VERIFIER_KIND:
        raise ValueError(f"Unsupported verifier kind: {payload.get('kind')!r}")
    if payload.get("schemaVersion") != SYNTHETIC_SANDBOX_RUN_VERIFIER_SCHEMA_VERSION:
        raise ValueError(f"Unsupported verifier schemaVersion: {payload.get('schemaVersion')!r}")
    if payload.get("authority") != SYNTHETIC_SANDBOX_RUN_VERIFIER_AUTHORITY:
        raise ValueError(f"Unsupported verifier authority: {payload.get('authority')!r}")
    if payload.get("status") != "passed":
        raise ValueError("Verifier status must be passed")


def check_verifier_contract(payload: dict[str, Any]) -> None:
    contract = object_value(payload.get("contract"), "verifier contract")
    if contract.get("verifierIsExecutionPermission") is not False:
        raise ValueError("Verifier contract must not grant execution permission")
    if contract.get("syntheticOutputIsRegistryTruth") is not False:
        raise ValueError("Verifier contract must not treat synthetic output as registry truth")


def check_verifier_artifact_summaries(payload: dict[str, Any]) -> None:
    fixture = object_value(payload.get("fixture"), "verifier fixture reference")
    if fixture.get("digestVerified") is not True:
        raise ValueError("Verifier fixture digest must be verified")
    linked = list_value(payload.get("linkedArtifacts"), "verifier linkedArtifacts")
    if len(linked) != 3:
        raise ValueError("Verifier must have three linked artifacts")
    if {object_value(item, "linked artifact").get("role") for item in linked} != {
        "sandboxContract",
        "sandboxPreflight",
        "sandboxRunnerValidation",
    }:
        raise ValueError("Verifier linked artifact roles are invalid")
    for item in linked:
        artifact = object_value(item, "linked artifact")
        if artifact.get("digestVerified") is not True:
            raise ValueError("Verifier linked artifact digest must be verified")
    outputs = list_value(payload.get("syntheticOutputCandidates"), "verifier output candidates")
    if len(outputs) != 3:
        raise ValueError("Verifier must have three output candidates")
    for item in outputs:
        output = object_value(item, "verifier output candidate")
        if output.get("byteSizeVerified") is not True:
            raise ValueError("Verifier output byte size must be verified")
        if output.get("digestVerified") is not True:
            raise ValueError("Verifier output digest must be verified")
        if output.get("outputIsRegistryTruth") is not False:
            raise ValueError("Verifier output must not be registry truth")
    audit = object_value(payload.get("auditRecord"), "verifier audit record")
    if audit.get("required") is not True:
        raise ValueError("Verifier audit record must be required")
    if audit.get("replayable") is not True:
        raise ValueError("Verifier audit record must be replayable")
    if audit.get("digestVerified") is not True:
        raise ValueError("Verifier audit record digest must be verified")
    validation = object_value(payload.get("validation"), "verifier validation")
    if validation.get("status") != "passed":
        raise ValueError("Verifier validation status must be passed")
    if validation.get("errorCount") != 0:
        raise ValueError("Verifier validation errorCount must be 0")
    summary = object_value(payload.get("summary"), "verifier summary")
    if summary.get("linkedArtifactCount") != 3:
        raise ValueError("Verifier summary linkedArtifactCount must be 3")
    if summary.get("syntheticOutputCandidateCount") != 3:
        raise ValueError("Verifier summary syntheticOutputCandidateCount must be 3")
    if summary.get("executedAdapterCount") != 0:
        raise ValueError("Verifier summary executedAdapterCount must be 0")


def check_operator_approval(payload: dict[str, Any]) -> dict[str, Any]:
    approval = object_value(payload.get("operatorApproval"), "verifier operatorApproval")
    if approval.get("bindingVerified") is not True:
        raise ValueError("Verifier operator approval binding must be verified")
    if approval.get("approvedForRealAdapterExecution") is not False:
        raise ValueError("Verifier approval must not approve real adapter execution")
    if approval.get("approvalIsExecutionPermission") is not False:
        raise ValueError("Verifier approval must not be execution permission")
    if approval.get("approvalIsRegistryAcceptance") is not False:
        raise ValueError("Verifier approval must not be registry acceptance")
    if approval.get("approvalIsReusableAcrossRepositories") is not False:
        raise ValueError("Verifier approval must not be reusable")
    binding = object_value(approval.get("approvalBinding"), "verifier approvalBinding")
    required = {
        "adapterId",
        "adapterDigest",
        "targetRepositoryId",
        "targetRepositoryRevision",
        "sandboxPolicyId",
        "sandboxPolicyVersion",
    }
    missing = required.difference(binding)
    if missing:
        raise ValueError(f"Verifier approvalBinding missing {sorted(missing)}")
    return binding


def check_verifier_execution_boundary(payload: dict[str, Any]) -> None:
    boundary = object_value(payload.get("executionBoundary"), "verifier executionBoundary")
    expected = {
        "adapterExecution": "synthetic_fixture_only",
        "realAdapterProcessSpawned": False,
        "thirdPartyAdapterCodeLoaded": False,
        "adapterCodeImportAttempted": False,
        "executedAdapterCount": 0,
        "dependencyInstallation": "not_allowed",
        "packageManagers": "not_invoked",
        "harvestedCodeExecution": "not_allowed",
        "aiExecution": "not_run",
        "networkAccess": "none",
        "syntheticRunVerificationIsExecutionPermission": False,
        "registryAuthority": False,
        "adapterOutputAccepted": False,
    }
    for key, expected_value in expected.items():
        if boundary.get(key) != expected_value:
            raise ValueError(f"Verifier executionBoundary {key} must be {expected_value!r}")


def check_verifier_non_authority_statements(payload: dict[str, Any]) -> None:
    statements = set(
        list_value(payload.get("nonAuthorityStatements"), "verifier nonAuthorityStatements")
    )
    required = {
        "synthetic_sandbox_run_verifier_is_not_execution_permission",
        "does_not_execute_real_adapters",
        "does_not_run_real_adapter_processes",
        "does_not_install_dependencies",
        "does_not_invoke_package_managers",
        "does_not_treat_synthetic_run_verification_as_execution_permission",
        "does_not_accept_packages",
        "does_not_publish_registry_metadata",
    }
    missing = required.difference(statements)
    if missing:
        raise ValueError(f"Verifier nonAuthorityStatements missing {sorted(missing)}")


def operator_approval_prerequisites(binding: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "explicit_real_run_approval_required",
        "approvalProvidedByReadinessGate": False,
        "approvalIsExecutionPermission": False,
        "approvalIsRegistryAcceptance": False,
        "approvalMayBeReusedAcrossRepositories": False,
        "mustBind": [
            "adapterId",
            "adapterDigest",
            "targetRepositoryId",
            "targetRepositoryRevision",
            "sandboxPolicyId",
            "sandboxPolicyVersion",
            "outputRoot",
            "auditRecordPath",
        ],
        "syntheticBindingCarriedForward": {
            "adapterId": binding["adapterId"],
            "adapterDigest": binding["adapterDigest"],
            "targetRepositoryId": binding["targetRepositoryId"],
            "targetRepositoryRevision": binding["targetRepositoryRevision"],
            "sandboxPolicyId": binding["sandboxPolicyId"],
            "sandboxPolicyVersion": binding["sandboxPolicyVersion"],
        },
    }


def sandbox_runtime_prerequisites() -> dict[str, Any]:
    return {
        "status": "requirements_declared_not_invoked",
        "runtimeInvocationAllowedByReadinessGate": False,
        "runtimeImplementationRequiredBeforeExecution": True,
        "processIsolationRequired": True,
        "sealedEnvironmentRequired": True,
        "dependencyIsolationRequired": True,
        "networkDefault": "deny",
        "packageManagersDefault": "not_invoked",
        "runtimeAvailabilityCheckedByExecution": False,
    }


def filesystem_output_policy_prerequisites() -> dict[str, Any]:
    return {
        "status": "requirements_declared",
        "inputAllowlistRequired": True,
        "outputRootMustBeEmptyOrDedicated": True,
        "parentSegmentsAllowed": False,
        "absolutePathsAllowed": False,
        "backslashAllowed": False,
        "networkPathsAllowed": False,
        "outputDigestVerificationRequired": True,
        "outputIsRegistryTruth": False,
    }


def audit_policy_prerequisites() -> dict[str, Any]:
    return {
        "status": "required",
        "replayableAuditRecordRequired": True,
        "runtimeCountersRequired": True,
        "inputArtifactDigestsRequired": True,
        "outputArtifactDigestsRequired": True,
        "diagnosticsRequired": True,
        "nonAuthorityStatementsRequired": True,
    }


def rollback_review_prerequisites() -> dict[str, Any]:
    return {
        "status": "required_before_execution",
        "maintainerReviewRequired": True,
        "previewOnlyRemovalAllowed": False,
        "registryAcceptanceAllowed": False,
        "adapterOutputAcceptanceAllowed": False,
    }


def list_value(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    return value


def readiness_id(verifier_ref: dict[str, Any]) -> str:
    digest = canonical_sha256({"verifierReport": verifier_ref})
    return f"real-local-trusted-adapter-sandbox-run-readiness-{digest[:16]}"


def non_authority_statements() -> list[str]:
    return [
        "real_local_sandbox_readiness_is_not_execution_permission",
        "synthetic_run_verifier_is_not_execution_permission",
        "does_not_load_third_party_adapter_code",
        "does_not_execute_real_adapters",
        "does_not_run_real_adapter_processes",
        "does_not_install_dependencies",
        "does_not_invoke_package_managers",
        "does_not_execute_harvested_code",
        "does_not_run_ai",
        "does_not_use_network",
        "does_not_accept_packages",
        "does_not_accept_relations",
        "does_not_seed_baselines",
        "does_not_publish_registry_metadata",
        "does_not_remove_preview_only",
        "does_not_treat_synthetic_adapter_output_as_registry_truth",
        "does_not_treat_readiness_as_execution_permission",
        "does_not_grant_registry_authority",
    ]
