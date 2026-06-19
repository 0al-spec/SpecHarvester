from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from spec_harvester.producer_receipt import canonical_sha256
from spec_harvester.trusted_local_adapter_runner import (
    artifact_reference,
    digest_string,
    object_value,
    path_reference,
    read_json_object,
    render_json,
)

SYNTHETIC_SANDBOX_RUN_API_VERSION = "spec-harvester.synthetic-trusted-local-adapter-sandbox-run/v0"
SYNTHETIC_SANDBOX_RUN_KIND = "SpecHarvesterSyntheticTrustedLocalAdapterSandboxRun"
SYNTHETIC_SANDBOX_RUN_SCHEMA_VERSION = 1
SYNTHETIC_SANDBOX_RUN_AUTHORITY = "producer_synthetic_trusted_local_adapter_sandbox_run_only"

SYNTHETIC_SANDBOX_RUN_VERIFIER_API_VERSION = (
    "spec-harvester.synthetic-trusted-local-adapter-sandbox-run-verifier/v0"
)
SYNTHETIC_SANDBOX_RUN_VERIFIER_KIND = (
    "SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport"
)
SYNTHETIC_SANDBOX_RUN_VERIFIER_SCHEMA_VERSION = 1
SYNTHETIC_SANDBOX_RUN_VERIFIER_AUTHORITY = (
    "producer_synthetic_trusted_local_adapter_sandbox_run_verifier_only"
)

ADAPTER_OUTPUT_CANDIDATE_AUTHORITY = "producer_adapter_output_candidate_evidence_only"

EXPECTED_LINKED_ARTIFACTS = {
    "sandboxContract": {
        "kind": "SpecHarvesterTrustedLocalAdapterSandboxContract",
        "authority": "producer_trusted_local_adapter_sandbox_contract_only",
    },
    "sandboxPreflight": {
        "kind": "SpecHarvesterTrustedLocalAdapterSandboxPreflightReport",
        "authority": "producer_trusted_local_adapter_sandbox_preflight_only",
    },
    "sandboxRunnerValidation": {
        "kind": "SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport",
        "authority": "producer_trusted_local_adapter_sandbox_runner_validation_only",
    },
}

EXPECTED_OUTPUT_ROLES = {
    "trusted_local_adapter_output": "SpecHarvesterTrustedLocalAdapterOutputCandidate",
    "trusted_local_adapter_diagnostics": "SpecHarvesterTrustedLocalAdapterDiagnostics",
    "trusted_local_adapter_audit_record": "SpecHarvesterTrustedLocalAdapterAuditRecord",
}


@dataclass(frozen=True)
class SyntheticTrustedLocalAdapterSandboxRunVerifierOptions:
    fixture: Path


def build_synthetic_trusted_local_adapter_sandbox_run_verifier_report(
    options: SyntheticTrustedLocalAdapterSandboxRunVerifierOptions,
) -> dict[str, Any]:
    return SyntheticTrustedLocalAdapterSandboxRunVerifier(options).report()


def write_synthetic_trusted_local_adapter_sandbox_run_verifier_report(
    path: Path,
    payload: dict[str, Any],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_json(payload), encoding="utf-8")


class SyntheticTrustedLocalAdapterSandboxRunVerifier:
    def __init__(self, options: SyntheticTrustedLocalAdapterSandboxRunVerifierOptions):
        self.options = options

    def report(self) -> dict[str, Any]:
        fixture = read_json_object(
            self.options.fixture,
            "synthetic trusted local adapter sandbox run fixture",
        )
        fixture_digest = digest_string(self.options.fixture)

        check_fixture_identity(fixture)
        check_fixture_contract(fixture)
        linked_artifacts = verified_linked_artifacts(fixture)
        approval = verified_operator_approval(fixture, linked_artifacts)
        output_root = verified_output_root(fixture, approval)
        output_candidates = verified_output_candidates(fixture, approval, linked_artifacts)
        audit_record = verified_audit_record(fixture, output_candidates)
        check_execution_boundary(fixture)
        check_non_authority_statements(fixture)

        fixture_ref = artifact_reference(
            path=self.options.fixture,
            digest=fixture_digest,
            api_version=SYNTHETIC_SANDBOX_RUN_API_VERSION,
            kind=SYNTHETIC_SANDBOX_RUN_KIND,
            schema_version=SYNTHETIC_SANDBOX_RUN_SCHEMA_VERSION,
            authority=SYNTHETIC_SANDBOX_RUN_AUTHORITY,
        )
        checks = accepted_checks()
        return {
            "apiVersion": SYNTHETIC_SANDBOX_RUN_VERIFIER_API_VERSION,
            "kind": SYNTHETIC_SANDBOX_RUN_VERIFIER_KIND,
            "schemaVersion": SYNTHETIC_SANDBOX_RUN_VERIFIER_SCHEMA_VERSION,
            "status": "passed",
            "verifierId": verifier_id(fixture_ref),
            "authority": SYNTHETIC_SANDBOX_RUN_VERIFIER_AUTHORITY,
            "contract": {
                "purpose": (
                    "Verify a synthetic trusted local adapter sandbox run fixture "
                    "and linked artifacts without enabling real adapter execution."
                ),
                "contractVersion": "0.1.0",
                "verifierAuthority": SYNTHETIC_SANDBOX_RUN_VERIFIER_AUTHORITY,
                "fixtureAuthority": SYNTHETIC_SANDBOX_RUN_AUTHORITY,
                "adapterOutputAuthority": ADAPTER_OUTPUT_CANDIDATE_AUTHORITY,
                "verifierIsExecutionPermission": False,
                "syntheticOutputIsRegistryTruth": False,
            },
            "fixture": {
                **fixture_ref,
                "digestVerified": True,
            },
            "linkedArtifacts": linked_artifacts,
            "operatorApproval": approval,
            "syntheticOutputRoot": output_root,
            "syntheticOutputCandidates": output_candidates,
            "auditRecord": audit_record,
            "validation": {
                "status": "passed",
                "acceptedChecks": checks,
                "errorCount": 0,
                "warningCount": 1,
            },
            "executionBoundary": {
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
                "operatorApprovalIsReusable": False,
                "syntheticRunIsRealExecutionPermission": False,
                "syntheticRunVerificationIsExecutionPermission": False,
                "appliedToDrafting": False,
                "registryAuthority": False,
                "adapterOutputAccepted": False,
            },
            "summary": {
                "linkedArtifactCount": len(linked_artifacts),
                "syntheticOutputCandidateCount": len(output_candidates),
                "acceptedCount": len(checks),
                "errorCount": 0,
                "warningCount": 1,
                "realAdapterProcessSpawned": False,
                "thirdPartyAdapterCodeLoaded": False,
                "executedAdapterCount": 0,
                "verifiedOutputByteCount": sum(item["byteSize"] for item in output_candidates),
            },
            "diagnostics": [
                {
                    "severity": "info",
                    "code": "synthetic_sandbox_run_verifier",
                    "message": (
                        "Synthetic sandbox run fixture and linked artifacts were "
                        "verified without loading adapter code or spawning a real "
                        "adapter process."
                    ),
                },
                {
                    "severity": "warning",
                    "code": "synthetic_sandbox_run_verifier_is_not_execution_permission",
                    "message": (
                        "This verifier report is producer-side review evidence only "
                        "and does not grant execution authority or registry authority."
                    ),
                },
            ],
            "nonAuthorityStatements": non_authority_statements(),
            "followUp": {
                "syntheticRunFixtureTask": "P42-T5",
                "realLocalAdapterRunTask": "deferred_until_after_review",
            },
        }


def accepted_checks() -> list[dict[str, str]]:
    return [
        {
            "code": "synthetic_fixture_identity_valid",
            "status": "passed",
            "target": "fixture",
            "message": "Synthetic sandbox run fixture identity and authority are valid.",
        },
        {
            "code": "linked_artifact_digests_verified",
            "status": "passed",
            "target": "linkedArtifacts",
            "message": "Sandbox contract, preflight, and runner validation digests match bytes.",
        },
        {
            "code": "operator_approval_binding_verified",
            "status": "passed",
            "target": "operatorApproval.approvalBinding",
            "message": (
                "Approval binding is tied to one adapter, repository, policy, and output root."
            ),
        },
        {
            "code": "synthetic_output_digests_verified",
            "status": "passed",
            "target": "syntheticOutputCandidates",
            "message": "Synthetic output byte sizes and SHA-256 digests match linked files.",
        },
        {
            "code": "audit_record_verified",
            "status": "passed",
            "target": "auditRecord",
            "message": "Audit record path, digest, runtime counters, and questions are verified.",
        },
        {
            "code": "no_real_execution_boundary_preserved",
            "status": "passed",
            "target": "executionBoundary",
            "message": (
                "Verification preserves no adapter process, no dependency, and no network use."
            ),
        },
        {
            "code": "non_authority_boundary_preserved",
            "status": "passed",
            "target": "nonAuthorityStatements",
            "message": "Verifier report is not execution permission and has no registry authority.",
        },
    ]


def check_fixture_identity(payload: dict[str, Any]) -> None:
    if payload.get("apiVersion") != SYNTHETIC_SANDBOX_RUN_API_VERSION:
        raise ValueError(
            f"Unsupported synthetic sandbox run apiVersion: {payload.get('apiVersion')!r}"
        )
    if payload.get("kind") != SYNTHETIC_SANDBOX_RUN_KIND:
        raise ValueError(f"Unsupported synthetic sandbox run kind: {payload.get('kind')!r}")
    if payload.get("schemaVersion") != SYNTHETIC_SANDBOX_RUN_SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported synthetic sandbox run schemaVersion: {payload.get('schemaVersion')!r}"
        )
    if payload.get("authority") != SYNTHETIC_SANDBOX_RUN_AUTHORITY:
        raise ValueError(
            f"Unsupported synthetic sandbox run authority: {payload.get('authority')!r}"
        )


def check_fixture_contract(payload: dict[str, Any]) -> None:
    contract = object_value(payload.get("contract"), "synthetic sandbox run contract")
    if contract.get("defaultExecution") != "synthetic_fixture_only":
        raise ValueError("Synthetic sandbox run defaultExecution must be synthetic_fixture_only")
    if contract.get("syntheticRunAuthority") != SYNTHETIC_SANDBOX_RUN_AUTHORITY:
        raise ValueError("Synthetic sandbox run authority mismatch in contract")
    if contract.get("adapterOutputAuthority") != ADAPTER_OUTPUT_CANDIDATE_AUTHORITY:
        raise ValueError("Synthetic sandbox run adapter output authority mismatch")
    if contract.get("syntheticRunIsRealExecutionPermission") is not False:
        raise ValueError("Synthetic run must not be real execution permission")
    if contract.get("syntheticOutputIsRegistryTruth") is not False:
        raise ValueError("Synthetic output must not be registry truth")


def verified_linked_artifacts(payload: dict[str, Any]) -> list[dict[str, Any]]:
    linked = object_value(payload.get("linkedArtifacts"), "linked artifacts")
    if set(linked) != set(EXPECTED_LINKED_ARTIFACTS):
        raise ValueError("Synthetic sandbox run linkedArtifacts set is invalid")
    verified = []
    for name, expected in EXPECTED_LINKED_ARTIFACTS.items():
        reference = object_value(linked.get(name), f"{name} linked artifact")
        path = resolve_safe_path(reference.get("path"), f"{name} linked artifact path")
        digest = digest_string(path)
        artifact_payload = read_json_object(path, f"{name} linked artifact")
        if reference.get("kind") != expected["kind"]:
            raise ValueError(f"{name} linked artifact kind mismatch")
        if reference.get("authority") != expected["authority"]:
            raise ValueError(f"{name} linked artifact authority mismatch")
        if reference.get("required") is not True:
            raise ValueError(f"{name} linked artifact must be required")
        if reference.get("digest") != digest:
            raise ValueError(f"{name} linked artifact digest does not match file bytes")
        if artifact_payload.get("kind") != expected["kind"]:
            raise ValueError(f"{name} linked artifact file kind mismatch")
        if artifact_payload.get("authority") != expected["authority"]:
            raise ValueError(f"{name} linked artifact file authority mismatch")
        verified.append(
            {
                "role": name,
                "path": path_reference(path),
                "digest": digest,
                "kind": expected["kind"],
                "authority": expected["authority"],
                "required": True,
                "digestVerified": True,
            }
        )
    return verified


def verified_operator_approval(
    payload: dict[str, Any],
    linked_artifacts: list[dict[str, Any]],
) -> dict[str, Any]:
    approval = object_value(payload.get("operatorApproval"), "operator approval")
    if approval.get("status") != "synthetic_approval_fixture_provided":
        raise ValueError("Operator approval status must be synthetic_approval_fixture_provided")
    if approval.get("approvalMode") != "single_adapter_single_repository_single_synthetic_run":
        raise ValueError("Operator approval mode must bind one adapter/repository/run")
    for field in (
        "approvalProvidedByFixture",
        "approvedForRealAdapterExecution",
        "approvalIsExecutionPermission",
        "approvalIsRegistryAcceptance",
        "approvalIsReusableAcrossRepositories",
    ):
        expected = field == "approvalProvidedByFixture"
        if approval.get(field) is not expected:
            raise ValueError(f"Operator approval {field} must be {expected!r}")

    binding = object_value(approval.get("approvalBinding"), "operator approval binding")
    adapter = object_value(payload.get("adapterPackageIdentity"), "adapter package identity")
    target = object_value(payload.get("targetRepository"), "target repository")
    policy = object_value(payload.get("sandboxPolicyIdentity"), "sandbox policy identity")
    linked_by_role = {item["role"]: item for item in linked_artifacts}
    if binding.get("adapterId") != adapter.get("adapterId"):
        raise ValueError("Operator approval adapterId must match adapterPackageIdentity")
    package_source = object_value(adapter.get("packageSource"), "adapter package source")
    if binding.get("adapterDigest") != package_source.get("digest"):
        raise ValueError("Operator approval adapterDigest must match adapter package digest")
    if binding.get("targetRepositoryId") != target.get("id"):
        raise ValueError("Operator approval targetRepositoryId must match target repository")
    if binding.get("targetRepositoryRevision") != target.get("revision"):
        raise ValueError("Operator approval targetRepositoryRevision must match target repository")
    if binding.get("sandboxPolicyId") != policy.get("policyId"):
        raise ValueError("Operator approval sandboxPolicyId must match policy")
    if binding.get("sandboxPolicyVersion") != policy.get("policyVersion"):
        raise ValueError("Operator approval sandboxPolicyVersion must match policy")
    if (
        binding.get("sandboxRunnerValidationDigest")
        != (linked_by_role["sandboxRunnerValidation"]["digest"])
    ):
        raise ValueError("Operator approval runner validation digest mismatch")
    output_root = object_value(payload.get("syntheticOutputRoot"), "synthetic output root")
    if binding.get("declaredOutputRoot") != output_root.get("path"):
        raise ValueError("Operator approval declaredOutputRoot must match synthetic output root")
    required = list_value(approval.get("approvalMustBind"), "operator approval approvalMustBind")
    for field in (
        "adapterId",
        "adapterDigest",
        "targetRepositoryId",
        "targetRepositoryRevision",
        "sandboxPolicyId",
        "sandboxPolicyVersion",
        "sandboxRunnerValidationDigest",
        "declaredOutputRoot",
        "syntheticOutputCandidates[].digest",
    ):
        if field not in required:
            raise ValueError(f"Operator approval approvalMustBind missing {field}")
    return {
        "status": approval["status"],
        "approvalMode": approval["approvalMode"],
        "approvalProvidedByFixture": True,
        "approvedForRealAdapterExecution": False,
        "approvalIsExecutionPermission": False,
        "approvalIsRegistryAcceptance": False,
        "approvalIsReusableAcrossRepositories": False,
        "bindingVerified": True,
        "approvalBinding": {
            "adapterId": binding["adapterId"],
            "adapterDigest": binding["adapterDigest"],
            "targetRepositoryId": binding["targetRepositoryId"],
            "targetRepositoryRevision": binding["targetRepositoryRevision"],
            "sandboxPolicyId": binding["sandboxPolicyId"],
            "sandboxPolicyVersion": binding["sandboxPolicyVersion"],
            "sandboxRunnerValidationDigest": binding["sandboxRunnerValidationDigest"],
            "declaredOutputRoot": binding["declaredOutputRoot"],
        },
    }


def verified_output_root(payload: dict[str, Any], approval: dict[str, Any]) -> dict[str, Any]:
    output_root = object_value(payload.get("syntheticOutputRoot"), "synthetic output root")
    path = resolve_safe_path(output_root.get("path"), "synthetic output root path")
    if output_root.get("path") != approval["approvalBinding"]["declaredOutputRoot"]:
        raise ValueError("Synthetic output root must match approval binding")
    expected_flags = {
        "pathFormat": "posix_relative",
        "parentSegmentsAllowed": False,
        "absolutePathsAllowed": False,
        "backslashAllowed": False,
        "networkPathsAllowed": False,
    }
    for key, expected in expected_flags.items():
        if output_root.get(key) != expected:
            raise ValueError(f"Synthetic output root {key} must be {expected!r}")
    if not path.is_dir():
        raise ValueError("Synthetic output root path must exist as a directory")
    return {
        "path": path_reference(path),
        **expected_flags,
        "safeRelativePathVerified": True,
    }


def verified_output_candidates(
    payload: dict[str, Any],
    approval: dict[str, Any],
    linked_artifacts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    candidates = list_value(
        payload.get("syntheticOutputCandidates"),
        "synthetic output candidates",
    )
    if len(candidates) != len(EXPECTED_OUTPUT_ROLES):
        raise ValueError("Synthetic output candidate count is invalid")
    outputs_by_role = {
        object_value(candidate, "synthetic output candidate").get("role"): object_value(
            candidate, "synthetic output candidate"
        )
        for candidate in candidates
    }
    if set(outputs_by_role) != set(EXPECTED_OUTPUT_ROLES):
        raise ValueError("Synthetic output candidate roles are invalid")
    linked_digests = {item["digest"] for item in linked_artifacts}
    binding = approval["approvalBinding"]
    verified = []
    for role, expected_kind in EXPECTED_OUTPUT_ROLES.items():
        output = outputs_by_role[role]
        path = resolve_safe_path(output.get("path"), f"{role} output path")
        output_bytes = path.read_bytes()
        digest = f"sha256:{hashlib.sha256(output_bytes).hexdigest()}"
        output_payload = read_json_object(path, f"{role} output artifact")
        if output.get("kind") != expected_kind:
            raise ValueError(f"{role} output candidate kind mismatch")
        if output_payload.get("kind") != expected_kind:
            raise ValueError(f"{role} output artifact file kind mismatch")
        if output.get("authority") != ADAPTER_OUTPUT_CANDIDATE_AUTHORITY:
            raise ValueError(f"{role} output candidate authority mismatch")
        if output_payload.get("authority") != ADAPTER_OUTPUT_CANDIDATE_AUTHORITY:
            raise ValueError(f"{role} output artifact file authority mismatch")
        if output.get("byteSize") != len(output_bytes):
            raise ValueError(f"{role} output byteSize does not match file bytes")
        if output.get("digest") != digest:
            raise ValueError(f"{role} output digest does not match file bytes")
        if output.get("adapterId") != binding["adapterId"]:
            raise ValueError(f"{role} output adapterId mismatch")
        if output.get("adapterDigest") != binding["adapterDigest"]:
            raise ValueError(f"{role} output adapterDigest mismatch")
        if output.get("diagnosticsStatus") != "clean":
            raise ValueError(f"{role} output diagnosticsStatus must be clean")
        if output.get("outputIsRegistryTruth") is not False:
            raise ValueError(f"{role} output must not be registry truth")
        source_digests = set(list_value(output.get("sourceInputDigests"), f"{role} source digests"))
        if not linked_digests.issubset(source_digests):
            raise ValueError(
                f"{role} output sourceInputDigests must include linked artifact digests"
            )
        check_output_runtime_boundary(output_payload, role)
        verified.append(
            {
                "role": role,
                "path": path_reference(path),
                "byteSize": len(output_bytes),
                "digest": digest,
                "kind": expected_kind,
                "authority": ADAPTER_OUTPUT_CANDIDATE_AUTHORITY,
                "producerRunId": output["producerRunId"],
                "adapterId": output["adapterId"],
                "adapterDigest": output["adapterDigest"],
                "sourceInputDigestCount": len(source_digests),
                "byteSizeVerified": True,
                "digestVerified": True,
                "outputIsRegistryTruth": False,
            }
        )
    return verified


def check_output_runtime_boundary(payload: dict[str, Any], role: str) -> None:
    if role == "trusted_local_adapter_output":
        candidate = object_value(
            payload.get("candidateEvidence"),
            "adapter output candidateEvidence",
        )
        if candidate.get("appliedToDrafting") is not False:
            raise ValueError("Adapter output candidate must not be applied to drafting")
        if candidate.get("registryAuthority") is not False:
            raise ValueError("Adapter output candidate must not have registry authority")
        return
    counters = object_value(payload.get("runtimeCounters"), f"{role} runtime counters")
    if counters.get("realAdapterProcessSpawned") is not False:
        raise ValueError(f"{role} runtimeCounters realAdapterProcessSpawned must be false")
    if counters.get("thirdPartyAdapterCodeLoaded") is not False:
        raise ValueError(f"{role} runtimeCounters thirdPartyAdapterCodeLoaded must be false")
    if counters.get("executedAdapterCount") != 0:
        raise ValueError(f"{role} runtimeCounters executedAdapterCount must be 0")
    if counters.get("dependencyInstallation") != "not_allowed":
        raise ValueError(f"{role} runtimeCounters dependencyInstallation must be not_allowed")
    if counters.get("packageManagers") != "not_invoked":
        raise ValueError(f"{role} runtimeCounters packageManagers must be not_invoked")
    if counters.get("networkAccess") != "none":
        raise ValueError(f"{role} runtimeCounters networkAccess must be none")


def verified_audit_record(
    payload: dict[str, Any],
    output_candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    audit = object_value(payload.get("auditRecord"), "audit record")
    if audit.get("required") is not True:
        raise ValueError("Audit record must be required")
    if audit.get("replayable") is not True:
        raise ValueError("Audit record must be replayable")
    path = resolve_safe_path(audit.get("path"), "audit record path")
    digest = digest_string(path)
    outputs_by_role = {item["role"]: item for item in output_candidates}
    audit_output = outputs_by_role["trusted_local_adapter_audit_record"]
    if audit.get("digest") != digest:
        raise ValueError("Audit record digest does not match file bytes")
    if audit.get("digest") != audit_output["digest"]:
        raise ValueError("Audit record digest must match audit output candidate")
    required_fields = set(list_value(audit.get("requiredFields"), "audit requiredFields"))
    expected_required = {
        "operatorApproval",
        "adapterPackageIdentity",
        "sandboxPolicyIdentity",
        "sandboxRunnerValidationDigest",
        "inputArtifactDigests",
        "syntheticOutputCandidateDigests",
        "runtimeCounters",
        "diagnostics",
        "nonAuthorityStatements",
    }
    if required_fields != expected_required:
        raise ValueError("Audit record requiredFields set is invalid")
    questions = set(
        list_value(audit.get("reviewerQuestionsAnswered"), "audit reviewerQuestionsAnswered")
    )
    expected_questions = {
        "what_was_approved",
        "what_was_read",
        "what_was_written",
        "why_output_remains_non_authoritative",
    }
    if questions != expected_questions:
        raise ValueError("Audit record reviewerQuestionsAnswered set is invalid")
    audit_payload = read_json_object(path, "audit record artifact")
    if audit_payload.get("kind") != EXPECTED_OUTPUT_ROLES["trusted_local_adapter_audit_record"]:
        raise ValueError("Audit record artifact kind mismatch")
    if audit_payload.get("authority") != ADAPTER_OUTPUT_CANDIDATE_AUTHORITY:
        raise ValueError("Audit record artifact authority mismatch")
    check_output_runtime_boundary(audit_payload, "trusted_local_adapter_audit_record")
    return {
        "required": True,
        "replayable": True,
        "path": path_reference(path),
        "digest": digest,
        "digestVerified": True,
        "requiredFieldCount": len(required_fields),
        "reviewerQuestionsAnswered": sorted(questions),
    }


def check_execution_boundary(payload: dict[str, Any]) -> None:
    boundary = object_value(payload.get("executionBoundary"), "execution boundary")
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
        "operatorApprovalIsReusable": False,
        "syntheticRunIsRealExecutionPermission": False,
        "appliedToDrafting": False,
        "registryAuthority": False,
        "adapterOutputAccepted": False,
    }
    for key, expected_value in expected.items():
        if boundary.get(key) != expected_value:
            raise ValueError(f"Execution boundary {key} must be {expected_value!r}")


def check_non_authority_statements(payload: dict[str, Any]) -> None:
    statements = set(list_value(payload.get("nonAuthorityStatements"), "nonAuthorityStatements"))
    required = {
        "synthetic_sandbox_run_is_not_real_execution_permission",
        "synthetic_adapter_output_is_not_registry_truth",
        "operator_approval_fixture_is_not_reusable",
        "does_not_load_third_party_adapter_code",
        "does_not_execute_real_adapters",
        "does_not_run_real_adapter_processes",
        "does_not_install_dependencies",
        "does_not_invoke_package_managers",
        "does_not_execute_harvested_code",
        "does_not_run_ai",
        "does_not_accept_packages",
        "does_not_accept_relations",
        "does_not_publish_registry_metadata",
        "does_not_remove_preview_only",
        "does_not_treat_sandbox_runner_validation_as_execution_permission",
    }
    missing = required.difference(statements)
    if missing:
        raise ValueError(f"Synthetic sandbox run nonAuthorityStatements missing {sorted(missing)}")


def resolve_safe_path(value: Any, label: str) -> Path:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string")
    assert_safe_relative_path(value, label)
    path = Path(value)
    if not path.exists():
        raise ValueError(f"{label} does not exist: {value}")
    return path


def assert_safe_relative_path(value: str, label: str) -> None:
    if not value:
        raise ValueError(f"{label} must not be empty")
    if "\\" in value:
        raise ValueError(f"{label} must use POSIX separators")
    if "://" in value:
        raise ValueError(f"{label} must not be a URI")
    pure = PurePosixPath(value)
    if pure.is_absolute():
        raise ValueError(f"{label} must be relative")
    if value.startswith("//"):
        raise ValueError(f"{label} must not be a network path")
    if ".." in pure.parts:
        raise ValueError(f"{label} must not contain parent segments")


def list_value(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    return value


def verifier_id(fixture_ref: dict[str, Any]) -> str:
    digest = canonical_sha256({"fixture": fixture_ref})
    return f"synthetic-trusted-local-adapter-sandbox-run-verifier-{digest[:16]}"


def non_authority_statements() -> list[str]:
    return [
        "synthetic_sandbox_run_verifier_is_not_execution_permission",
        "synthetic_sandbox_run_is_not_real_execution_permission",
        "synthetic_adapter_output_is_not_registry_truth",
        "operator_approval_fixture_is_not_reusable",
        "does_not_load_third_party_adapter_code",
        "does_not_execute_real_adapters",
        "does_not_run_real_adapter_processes",
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
        "does_not_treat_sandbox_runner_validation_as_execution_permission",
        "does_not_treat_synthetic_run_verification_as_execution_permission",
        "does_not_treat_ai_output_as_registry_truth",
    ]
