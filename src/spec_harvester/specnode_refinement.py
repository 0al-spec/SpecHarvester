from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

PRODUCER_NAME = "SpecHarvester"
DEFAULT_PRODUCER_VERSION = "0.1.0"
SPECNODE_SCHEMA_VERSION = 1
PUBLIC_INTERFACE_INDEX_FILENAME = "public-interface-index.json"

PROMPT_BUDGET = {
    "maxPromptBytes": 60_000,
    "maxPromptTokens": 8_192,
    "maxPublicSymbols": 200,
    "maxSemanticClusters": 50,
    "truncationPolicy": "deterministic_priority_order",
    "redactionPolicy": "path_digest_and_summary_only",
}
AUTHORITY_POLICY = {
    "modelFilesystemAccess": "none",
    "modelShellAccess": "none",
    "rawSourceAccess": "none",
    "secretAccess": "none",
    "candidateMutation": "proposal_only",
}
JOB_POLICY = {
    "modelFilesystemAccess": "none",
    "modelShellAccess": "none",
    "modelNetworkAccess": "provider_only",
    "allowedTools": [],
    "candidateMutation": "proposal_only",
    "temperature": 0.2,
    "tokenBudget": 8_192,
    "timeoutSeconds": 120,
}
EXCLUDED_CONTENT = {
    "rawRepositorySource": "excluded",
    "documentationBodies": "excluded",
    "dependencyDirectories": "excluded",
    "providerLogs": "excluded",
    "secrets": "excluded",
    "arbitraryPrompts": "excluded",
}
ALLOWED_PATCH_OPERATIONS = {
    "add_field",
    "replace_field",
    "remove_field",
    "append_unique",
    "replace_list_item_by_id",
    "remove_list_item_by_id",
}
FORBIDDEN_OPERATION_MARKERS = {
    "rawUnifiedDiff",
    "fullFileReplacement",
    "shellCommand",
    "gitCommand",
    "networkFetch",
    "providerCall",
    "packageManagerCommand",
    "testRunnerCommand",
    "buildToolCommand",
}
ALLOWED_REJECTION_CODES = {
    "insufficient_evidence",
    "prompt_budget_exceeded",
    "provider_unavailable",
    "model_output_invalid",
    "policy_violation",
    "unsupported_candidate_shape",
    "schema_validation_failed",
    "safety_boundary_triggered",
}
USAGE_RECEIPT_REQUIRED_FIELDS = {
    "kind",
    "jobId",
    "providerReceipt",
    "providerReceiptDigest",
    "modelId",
    "inputTokens",
    "outputTokens",
    "totalTokens",
    "finishReason",
    "attempts",
    "startedAt",
    "completedAt",
    "durationMs",
    "timeoutPolicy",
    "retryPolicy",
    "temperature",
    "maxOutputTokens",
    "promptBudget",
    "responseSha256",
    "redactionPolicy",
}
PROVIDER_RECEIPT_REQUIRED_FIELDS = {
    "kind",
    "providerKind",
    "providerName",
    "baseUrl",
    "endpoint",
    "modelId",
    "requestId",
    "startedAt",
    "completedAt",
    "durationMs",
    "status",
    "attempts",
    "timeoutPolicy",
    "retryPolicy",
    "temperature",
    "maxOutputTokens",
    "promptBudget",
    "inputTokens",
    "outputTokens",
    "totalTokens",
    "finishReason",
    "responseSha256",
    "redactionPolicy",
}
_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_MANIFEST_METADATA_KEYS = {"id", "name", "version", "summary", "license"}
GPT_OSS_MESSAGE_MARKER = "<|message|>"
GPT_OSS_CHANNEL_MARKER = "<|channel|>"


class SpecNodeProviderUnavailable(RuntimeError):
    """Raised by a smoke provider when the local SpecNode-compatible endpoint is absent."""


class SpecNodeRefinementValidationError(ValueError):
    """Raised when SpecNode output does not satisfy the smoke validation contract."""


class SpecNodeModelJSONParseError(ValueError):
    """Raised when provider message content cannot be parsed as one JSON object."""


class SpecNodeCompatibleProvider(Protocol):
    def refine(
        self,
        *,
        job: dict[str, Any],
        preview_plan: dict[str, Any],
    ) -> dict[str, Any]:
        """Return a SpecNodeRefinementResult for a typed refinement job."""


@dataclass(frozen=True)
class SpecNodeRefinementSmokeOptions:
    candidate_workspace: Path
    provider: SpecNodeCompatibleProvider | None = None
    producer_version: str = DEFAULT_PRODUCER_VERSION


def run_specnode_refinement_smoke(options: SpecNodeRefinementSmokeOptions) -> dict[str, Any]:
    bundle = build_specnode_artifact_bundle(
        options.candidate_workspace,
        producer_version=options.producer_version,
    )
    preview_plan = build_refine_preview_plan(bundle, options.candidate_workspace)
    job = build_specnode_refinement_job(
        bundle,
        preview_plan,
        producer_version=options.producer_version,
    )

    status = "ok"
    diagnostics: list[dict[str, str]] = []
    if options.provider is None:
        status = "provider_unavailable"
        result = build_provider_unavailable_result(job, preview_plan)
        diagnostics.append(
            {
                "severity": "info",
                "code": "provider_unavailable",
                "message": "No SpecNode-compatible provider configured; returned fallback.",
            }
        )
    else:
        try:
            result = options.provider.refine(job=job, preview_plan=preview_plan)
        except SpecNodeProviderUnavailable:
            status = "provider_unavailable"
            result = build_provider_unavailable_result(job, preview_plan)
            diagnostics.append(
                {
                    "severity": "info",
                    "code": "provider_unavailable",
                    "message": "SpecNode-compatible provider reported unavailable.",
                }
            )

    validate_specnode_refinement_result(
        result,
        job=job,
        preview_plan=preview_plan,
        bundle=bundle,
    )
    return {
        "schemaVersion": SPECNODE_SCHEMA_VERSION,
        "kind": "SpecNodeProviderSmokeRun",
        "status": status,
        "bundle": bundle,
        "previewPlan": preview_plan,
        "job": job,
        "refinementResult": result,
        "diagnostics": diagnostics,
    }


def build_specnode_artifact_bundle(
    candidate_workspace: Path,
    *,
    producer_version: str = DEFAULT_PRODUCER_VERSION,
) -> dict[str, Any]:
    workspace = candidate_workspace.resolve()
    if not workspace.exists() or not workspace.is_dir():
        raise ValueError(f"Candidate workspace does not exist: {candidate_workspace}")

    manifest = _required_file(workspace, "specpm.yaml")
    manifest_text = manifest.read_text(encoding="utf-8")
    manifest_metadata = _parse_manifest_metadata(manifest_text)
    spec_paths = _parse_manifest_spec_paths(manifest_text)
    if not spec_paths:
        spec_paths = sorted(
            path.relative_to(workspace).as_posix()
            for path in (workspace / "specs").glob("*.spec.yaml")
        )

    artifacts: list[dict[str, Any]] = []
    artifacts.append(_artifact_record(workspace, "harvest.json", "harvest_snapshot", required=True))
    artifacts.append(
        _artifact_record(workspace, "specpm.yaml", "spec_package_manifest", required=True)
    )
    for index, spec_path in enumerate(spec_paths, start=1):
        artifacts.append(
            _artifact_record(
                workspace,
                spec_path,
                "boundary_spec" if index == 1 else f"boundary_spec_{index}",
                required=True,
            )
        )

    public_interface = workspace / PUBLIC_INTERFACE_INDEX_FILENAME
    if public_interface.exists():
        artifacts.append(
            _artifact_record(
                workspace,
                PUBLIC_INTERFACE_INDEX_FILENAME,
                "public_interface_index",
                required=False,
            )
        )

    snapshot = _read_json(workspace / "harvest.json")
    source = snapshot.get("source") if isinstance(snapshot.get("source"), dict) else {}
    return {
        "schemaVersion": SPECNODE_SCHEMA_VERSION,
        "kind": "SpecHarvesterSpecNodeArtifactBundle",
        "candidateId": manifest_metadata.get("id", "unknown.candidate"),
        "candidateVersion": manifest_metadata.get("version", "0.1.0"),
        "workspaceRoot": ".",
        "producer": {"name": PRODUCER_NAME, "version": producer_version},
        "source": {
            "repository": source.get("repository"),
            "revision": source.get("revision"),
        },
        "artifacts": artifacts,
        "policy": dict(AUTHORITY_POLICY),
    }


def build_refine_preview_plan(
    bundle: dict[str, Any],
    candidate_workspace: Path,
) -> dict[str, Any]:
    workspace = candidate_workspace.resolve()
    snapshot = _read_json(workspace / "harvest.json")
    manifest_text = (workspace / "specpm.yaml").read_text(encoding="utf-8")
    manifest_metadata = _parse_manifest_metadata(manifest_text)
    spec_paths = _bundle_artifact_paths(bundle, prefix="boundary_spec")
    spec_texts = [
        (workspace / spec_path).read_text(encoding="utf-8")
        for spec_path in spec_paths
        if (workspace / spec_path).exists()
    ]
    public_interface = _optional_json(workspace / PUBLIC_INTERFACE_INDEX_FILENAME)

    artifact_digests = [
        {"id": item["id"], "path": item["path"], "sha256": item["sha256"]}
        for item in bundle.get("artifacts", [])
        if isinstance(item, dict)
    ]
    candidate_metadata = _candidate_metadata(
        manifest_metadata,
        manifest_text,
        spec_paths,
        spec_texts,
    )
    return {
        "schemaVersion": SPECNODE_SCHEMA_VERSION,
        "kind": "SpecHarvesterRefinePreviewPlan",
        "command": "refine-preview",
        "sourceBundle": {
            "kind": "SpecHarvesterSpecNodeArtifactBundle",
            "digest": canonical_json_sha256_digest(bundle),
        },
        "candidate": {
            "packageId": bundle.get("candidateId"),
            "packageVersion": bundle.get("candidateVersion"),
            "workspaceRoot": ".",
            "specPaths": spec_paths,
        },
        "artifactDigests": artifact_digests,
        "compactModelInput": {
            "harvestSummary": _harvest_summary(snapshot),
            "projectProfile": _compact_project_profile(snapshot),
            "publicInterfaceSummary": _public_interface_summary(public_interface),
            "semanticEvidenceIndex": _semantic_evidence_index(spec_texts),
            "validationSummaries": {},
            "draftCandidateMetadata": candidate_metadata,
        },
        "promptBudget": dict(PROMPT_BUDGET),
        "excludedContent": dict(EXCLUDED_CONTENT),
        "policy": dict(AUTHORITY_POLICY),
    }


def build_specnode_refinement_job(
    bundle: dict[str, Any],
    preview_plan: dict[str, Any],
    *,
    producer_version: str = DEFAULT_PRODUCER_VERSION,
) -> dict[str, Any]:
    plan_digest = canonical_json_sha256_digest(preview_plan)
    return {
        "schemaVersion": SPECNODE_SCHEMA_VERSION,
        "kind": "SpecNodeRefinementJob",
        "jobId": f"specnode-smoke-{plan_digest.removeprefix('sha256:')[:16]}",
        "createdAt": "2026-05-22T00:00:00Z",
        "producer": {"name": PRODUCER_NAME, "version": producer_version},
        "bundle": {
            "kind": "SpecHarvesterSpecNodeArtifactBundle",
            "digest": canonical_json_sha256_digest(bundle),
        },
        "previewPlan": {
            "kind": "SpecHarvesterRefinePreviewPlan",
            "digest": plan_digest,
        },
        "policy": dict(JOB_POLICY),
        "requestedOutputs": [
            "candidatePatchProposal",
            "reviewNotes",
            "rejectionReason",
            "usageReceipt",
        ],
    }


def build_provider_unavailable_result(
    job: dict[str, Any],
    preview_plan: dict[str, Any],
) -> dict[str, Any]:
    job_digest = canonical_json_sha256_digest(job)
    preview_digest = canonical_json_sha256_digest(preview_plan)
    provider_receipt = {
        "kind": "SpecNodeProviderUsageReceipt",
        "providerKind": "openai_compatible",
        "providerName": "unconfigured",
        "baseUrl": None,
        "endpoint": None,
        "modelId": "unavailable",
        "requestId": "provider-unavailable",
        "startedAt": "2026-05-22T00:00:00Z",
        "completedAt": "2026-05-22T00:00:00Z",
        "durationMs": 0,
        "status": "provider_unavailable",
        "attempts": 0,
        "timeoutPolicy": {},
        "retryPolicy": {},
        "temperature": 0.2,
        "maxOutputTokens": 0,
        "promptBudget": preview_plan.get("promptBudget", {}),
        "inputTokens": 0,
        "outputTokens": 0,
        "totalTokens": 0,
        "finishReason": "provider_unavailable",
        "responseSha256": canonical_json_sha256_digest({"status": "provider_unavailable"}),
        "redactionPolicy": "path_digest_and_summary_only",
    }
    provider_receipt_digest = canonical_json_sha256_digest(provider_receipt)
    usage_receipt = {
        "kind": "SpecNodeProposalUsageReceipt",
        "jobId": job.get("jobId"),
        "rejectionId": "provider-unavailable",
        "providerReceipt": provider_receipt,
        "providerReceiptDigest": provider_receipt_digest,
        "modelId": "unavailable",
        "inputTokens": 0,
        "outputTokens": 0,
        "totalTokens": 0,
        "finishReason": "provider_unavailable",
        "attempts": 0,
        "startedAt": "2026-05-22T00:00:00Z",
        "completedAt": "2026-05-22T00:00:00Z",
        "durationMs": 0,
        "timeoutPolicy": {},
        "retryPolicy": {},
        "temperature": 0.2,
        "maxOutputTokens": 0,
        "promptBudget": preview_plan.get("promptBudget", {}),
        "responseSha256": provider_receipt["responseSha256"],
        "redactionPolicy": "path_digest_and_summary_only",
    }
    rejection = {
        "kind": "SpecNodeRejectionReason",
        "rejectionId": "provider-unavailable",
        "code": "provider_unavailable",
        "message": "No SpecNode-compatible provider is configured for this smoke run.",
        "sourceJobDigest": job_digest,
        "sourcePreviewPlanDigest": preview_digest,
        "evidenceRefs": ["harvest_snapshot", "spec_package_manifest"],
        "usageReceipt": usage_receipt,
    }
    return {
        "schemaVersion": SPECNODE_SCHEMA_VERSION,
        "kind": "SpecNodeRefinementResult",
        "job": {
            "kind": "SpecNodeRefinementJob",
            "jobId": job.get("jobId"),
            "digest": job_digest,
        },
        "result": {"kind": "rejectionReason", "rejection": rejection},
        "reviewNotes": [],
        "usageReceipt": usage_receipt,
    }


def validate_specnode_refinement_result(
    result: dict[str, Any],
    *,
    job: dict[str, Any],
    preview_plan: dict[str, Any],
    bundle: dict[str, Any],
) -> None:
    errors: list[str] = []
    if result.get("kind") != "SpecNodeRefinementResult":
        errors.append("result kind must be SpecNodeRefinementResult")
    if result.get("schemaVersion") != SPECNODE_SCHEMA_VERSION:
        errors.append("result schemaVersion must be 1")

    expected_job_digest = canonical_json_sha256_digest(job)
    expected_preview_digest = canonical_json_sha256_digest(preview_plan)
    expected_bundle_digest = canonical_json_sha256_digest(bundle)
    expected_artifact_digests = _artifact_digest_records(bundle)
    result_job = result.get("job")
    if not isinstance(result_job, dict):
        errors.append("result job must be an object")
    else:
        if result_job.get("jobId") != job.get("jobId"):
            errors.append("result jobId must match source job")
        if result_job.get("digest") != expected_job_digest:
            errors.append("result job digest must match source job")

    usage_receipt = result.get("usageReceipt")
    _validate_usage_receipt(
        usage_receipt,
        errors=errors,
        expected_job_id=job.get("jobId"),
    )

    result_body = result.get("result")
    if not isinstance(result_body, dict):
        errors.append("result body must be an object")
    else:
        result_kind = result_body.get("kind")
        if result_kind == "candidatePatchProposal":
            proposal = result_body.get("proposal")
            if not isinstance(proposal, dict):
                errors.append("candidatePatchProposal result requires proposal object")
            else:
                _validate_patch_proposal(
                    proposal,
                    errors=errors,
                    bundle=bundle,
                    expected_artifact_digests=expected_artifact_digests,
                    expected_job_digest=expected_job_digest,
                    expected_bundle_digest=expected_bundle_digest,
                    expected_preview_digest=expected_preview_digest,
                    usage_receipt=usage_receipt,
                )
        elif result_kind == "rejectionReason":
            rejection = result_body.get("rejection")
            if not isinstance(rejection, dict):
                errors.append("rejectionReason result requires rejection object")
            else:
                _validate_rejection(
                    rejection,
                    errors=errors,
                    expected_job_digest=expected_job_digest,
                    expected_preview_digest=expected_preview_digest,
                    usage_receipt=usage_receipt,
                )
        else:
            errors.append("result kind must be candidatePatchProposal or rejectionReason")

    review_notes = result.get("reviewNotes")
    if review_notes is not None and not isinstance(review_notes, list):
        errors.append("reviewNotes must be a list when present")

    if errors:
        raise SpecNodeRefinementValidationError("; ".join(errors))


def canonical_json_sha256_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return f"sha256:{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"


def parse_specnode_model_json_object(content: str) -> dict[str, Any]:
    """Parse direct JSON or the observed gpt-oss channel-wrapped JSON object."""
    text = content.strip()
    if not text:
        raise SpecNodeModelJSONParseError("model content is empty")

    if GPT_OSS_MESSAGE_MARKER in text:
        payloads = _gpt_oss_message_payloads(text)
        if len(payloads) != 1:
            raise SpecNodeModelJSONParseError("expected exactly one gpt-oss JSON message payload")
        return _parse_exact_json_object(payloads[0])
    return _parse_exact_json_object(text)


def _validate_patch_proposal(
    proposal: dict[str, Any],
    *,
    errors: list[str],
    bundle: dict[str, Any],
    expected_artifact_digests: list[dict[str, Any]],
    expected_job_digest: str,
    expected_bundle_digest: str,
    expected_preview_digest: str,
    usage_receipt: Any,
) -> None:
    for field in (
        "proposalId",
        "candidateId",
        "candidateVersion",
        "baseCandidateDigest",
        "sourceJobDigest",
        "sourcePreviewPlanDigest",
        "sourceArtifactDigests",
        "operations",
        "provenance",
        "validationExpectations",
    ):
        if field not in proposal:
            errors.append(f"proposal missing required field: {field}")

    if proposal.get("kind") != "SpecNodeCandidatePatchProposal":
        errors.append("proposal kind must be SpecNodeCandidatePatchProposal")
    if proposal.get("candidateId") != bundle.get("candidateId"):
        errors.append("proposal candidateId must match bundle")
    if proposal.get("candidateVersion") != bundle.get("candidateVersion"):
        errors.append("proposal candidateVersion must match bundle")
    if proposal.get("sourceJobDigest") != expected_job_digest:
        errors.append("proposal sourceJobDigest must match job digest")
    if proposal.get("sourcePreviewPlanDigest") != expected_preview_digest:
        errors.append("proposal sourcePreviewPlanDigest must match preview plan digest")
    if not _is_digest(proposal.get("baseCandidateDigest")):
        errors.append("proposal baseCandidateDigest must be a sha256 digest")
    if proposal.get("sourceArtifactDigests") != expected_artifact_digests:
        errors.append("proposal sourceArtifactDigests must match bundle artifact digests")

    provenance = proposal.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("proposal provenance must be an object")
    else:
        if provenance.get("kind") != "SpecNodeProposalProvenance":
            errors.append("provenance kind must be SpecNodeProposalProvenance")
        if provenance.get("sourceJobDigest") != expected_job_digest:
            errors.append("provenance sourceJobDigest must match job digest")
        if provenance.get("sourceBundleDigest") != expected_bundle_digest:
            errors.append("provenance sourceBundleDigest must match bundle digest")
        if provenance.get("sourcePreviewPlanDigest") != expected_preview_digest:
            errors.append("provenance sourcePreviewPlanDigest must match preview plan digest")
        if provenance.get("sourceArtifactDigests") != expected_artifact_digests:
            errors.append("provenance sourceArtifactDigests must match bundle artifact digests")
        if provenance.get("baseCandidateDigest") != proposal.get("baseCandidateDigest"):
            errors.append("provenance baseCandidateDigest must match proposal")
        if not _is_digest(provenance.get("providerReceiptDigest")):
            errors.append("provenance providerReceiptDigest must be a sha256 digest")
        if isinstance(usage_receipt, dict) and provenance.get(
            "providerReceiptDigest"
        ) != usage_receipt.get("providerReceiptDigest"):
            errors.append("provenance providerReceiptDigest must match usageReceipt")
        if provenance.get("redactionPolicy") != "path_digest_and_summary_only":
            errors.append("provenance redactionPolicy must be path_digest_and_summary_only")

    if isinstance(usage_receipt, dict) and usage_receipt.get("proposalId") != proposal.get(
        "proposalId"
    ):
        errors.append("usageReceipt proposalId must match proposal")

    expectations = proposal.get("validationExpectations")
    if not isinstance(expectations, dict):
        errors.append("validationExpectations must be an object")
    else:
        for field in (
            "requiresSchemaValidation",
            "requiresHumanReview",
            "requiresSpecPMValidationAfterApply",
        ):
            if expectations.get(field) is not True:
                errors.append(f"validationExpectations.{field} must be true")

    operations = proposal.get("operations")
    if not isinstance(operations, list):
        errors.append("proposal operations must be a list")
    else:
        for index, operation in enumerate(operations):
            if not isinstance(operation, dict):
                errors.append(f"operation {index} must be an object")
                continue
            _validate_patch_operation(operation, errors=errors, index=index)


def _validate_patch_operation(
    operation: dict[str, Any],
    *,
    errors: list[str],
    index: int,
) -> None:
    operation_kind = operation.get("op")
    if operation_kind not in ALLOWED_PATCH_OPERATIONS:
        errors.append(f"operation {index} uses forbidden op: {operation_kind!r}")
    for marker in FORBIDDEN_OPERATION_MARKERS:
        if marker in operation or operation_kind == marker:
            errors.append(f"operation {index} contains forbidden marker: {marker}")

    target_file = operation.get("targetFile")
    if not isinstance(target_file, str) or not _is_allowed_target_file(target_file):
        errors.append(f"operation {index} targetFile is outside allowed candidate files")
    if not _is_digest(operation.get("expectedCurrentValueSha256")):
        errors.append(f"operation {index} requires expectedCurrentValueSha256 digest")
    if not isinstance(operation.get("rationale"), str) or not operation["rationale"].strip():
        errors.append(f"operation {index} requires rationale")
    evidence_refs = operation.get("evidenceRefs")
    if not isinstance(evidence_refs, list) or not all(
        isinstance(item, str) for item in evidence_refs
    ):
        errors.append(f"operation {index} requires string evidenceRefs")


def _validate_rejection(
    rejection: dict[str, Any],
    *,
    errors: list[str],
    expected_job_digest: str,
    expected_preview_digest: str,
    usage_receipt: Any,
) -> None:
    if rejection.get("kind") != "SpecNodeRejectionReason":
        errors.append("rejection kind must be SpecNodeRejectionReason")
    if rejection.get("code") not in ALLOWED_REJECTION_CODES:
        errors.append("rejection code is not allowed")
    if rejection.get("sourceJobDigest") != expected_job_digest:
        errors.append("rejection sourceJobDigest must match job digest")
    if rejection.get("sourcePreviewPlanDigest") != expected_preview_digest:
        errors.append("rejection sourcePreviewPlanDigest must match preview plan digest")
    rejection_usage_receipt = rejection.get("usageReceipt")
    _validate_usage_receipt(
        rejection_usage_receipt,
        errors=errors,
        expected_job_id=usage_receipt.get("jobId") if isinstance(usage_receipt, dict) else None,
    )
    if isinstance(usage_receipt, dict) and rejection_usage_receipt != usage_receipt:
        errors.append("rejection usageReceipt must match top-level usageReceipt")
    if isinstance(usage_receipt, dict) and usage_receipt.get("rejectionId") != rejection.get(
        "rejectionId"
    ):
        errors.append("usageReceipt rejectionId must match rejection")
    if not isinstance(rejection.get("evidenceRefs"), list):
        errors.append("rejection evidenceRefs must be a list")


def _validate_usage_receipt(
    value: Any,
    *,
    errors: list[str],
    expected_job_id: Any,
) -> None:
    if not isinstance(value, dict):
        errors.append("usageReceipt is required and must be an object")
        return
    if value.get("kind") != "SpecNodeProposalUsageReceipt":
        errors.append("usageReceipt kind must be SpecNodeProposalUsageReceipt")
    for field in sorted(USAGE_RECEIPT_REQUIRED_FIELDS):
        if field not in value:
            errors.append(f"usageReceipt missing required field: {field}")
    if value.get("jobId") != expected_job_id:
        errors.append("usageReceipt jobId must match source job")

    provider_receipt = value.get("providerReceipt")
    if not isinstance(provider_receipt, dict):
        errors.append("usageReceipt providerReceipt must be an object")
        return
    if provider_receipt.get("kind") != "SpecNodeProviderUsageReceipt":
        errors.append("providerReceipt kind must be SpecNodeProviderUsageReceipt")
    for field in sorted(PROVIDER_RECEIPT_REQUIRED_FIELDS):
        if field not in provider_receipt:
            errors.append(f"providerReceipt missing required field: {field}")

    provider_digest = value.get("providerReceiptDigest")
    if provider_digest != canonical_json_sha256_digest(provider_receipt):
        errors.append("usageReceipt providerReceiptDigest must match providerReceipt")
    if not _is_digest(value.get("responseSha256")):
        errors.append("usageReceipt responseSha256 must be a sha256 digest")
    if not _is_digest(provider_receipt.get("responseSha256")):
        errors.append("providerReceipt responseSha256 must be a sha256 digest")


def _is_allowed_target_file(value: str) -> bool:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return False
    return value == "specpm.yaml" or (
        value.startswith("specs/") and value.endswith(".spec.yaml") and len(path.parts) == 2
    )


def _gpt_oss_message_payloads(text: str) -> list[str]:
    payloads: list[str] = []
    for segment in text.split(GPT_OSS_MESSAGE_MARKER)[1:]:
        end = segment.find(GPT_OSS_CHANNEL_MARKER)
        payload = segment[:end] if end != -1 else segment
        payload = payload.strip()
        if payload:
            payloads.append(payload)
    return payloads


def _parse_exact_json_object(text: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    try:
        value, index = decoder.raw_decode(text)
    except json.JSONDecodeError as exc:
        raise SpecNodeModelJSONParseError(f"model content is not valid JSON: {exc.msg}") from exc
    if text[index:].strip():
        raise SpecNodeModelJSONParseError("model content contains trailing non-JSON text")
    if not isinstance(value, dict):
        raise SpecNodeModelJSONParseError("model content JSON payload must be an object")
    return value


def _is_digest(value: Any) -> bool:
    return isinstance(value, str) and bool(_DIGEST_RE.match(value))


def _harvest_summary(snapshot: dict[str, Any]) -> dict[str, Any]:
    files = snapshot.get("files") if isinstance(snapshot.get("files"), list) else []
    file_kind_counts: dict[str, int] = {}
    package_manifests: list[dict[str, Any]] = []
    for item in files:
        if not isinstance(item, dict):
            continue
        kind = str(item.get("kind") or "unknown")
        file_kind_counts[kind] = file_kind_counts.get(kind, 0) + 1
        if kind == "package_manifest":
            package = item.get("package") if isinstance(item.get("package"), dict) else {}
            package_manifests.append(
                {
                    "path": item.get("path"),
                    "ecosystem": package.get("ecosystem"),
                    "name": package.get("name"),
                    "version": package.get("version"),
                    "description": package.get("description"),
                    "semanticHints": item.get("semanticHints", []),
                }
            )
    return {
        "kind": snapshot.get("kind"),
        "source": snapshot.get("source", {}),
        "summary": snapshot.get("summary", {}),
        "policy": snapshot.get("policy", {}),
        "fileKindCounts": dict(sorted(file_kind_counts.items())),
        "packageManifests": sorted(package_manifests, key=lambda item: str(item.get("path"))),
    }


def _compact_project_profile(snapshot: dict[str, Any]) -> dict[str, Any]:
    profile = snapshot.get("projectProfile")
    if not isinstance(profile, dict):
        return {}
    allowed = {
        "kind",
        "languages",
        "ecosystems",
        "manifests",
        "analyzerPlan",
        "confidence",
        "evidencePaths",
        "diagnostics",
    }
    return {key: profile[key] for key in sorted(allowed) if key in profile}


def _public_interface_summary(index: dict[str, Any] | None) -> dict[str, Any]:
    if index is None:
        return {"status": "absent"}
    symbols: list[dict[str, Any]] = []
    packages = index.get("packages", [])
    if not isinstance(packages, list):
        packages = []
    for package in packages:
        if not isinstance(package, dict):
            continue
        package_symbols = package.get("symbols", [])
        if not isinstance(package_symbols, list):
            package_symbols = []
        for symbol in package_symbols:
            if not isinstance(symbol, dict):
                continue
            symbols.append(
                {
                    "name": symbol.get("name"),
                    "kind": symbol.get("kind"),
                    "signature": symbol.get("signature"),
                    "path": symbol.get("path"),
                }
            )
    return {
        "kind": index.get("kind"),
        "summary": index.get("summary", {}),
        "analyzers": index.get("analyzers", []),
        "selectedSymbols": symbols[: PROMPT_BUDGET["maxPublicSymbols"]],
    }


def _artifact_digest_records(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    artifacts = bundle.get("artifacts")
    if not isinstance(artifacts, list):
        return []
    records: list[dict[str, Any]] = []
    for item in artifacts:
        if not isinstance(item, dict):
            continue
        records.append(
            {
                "id": item.get("id"),
                "path": item.get("path"),
                "sha256": item.get("sha256"),
            }
        )
    return records


def _semantic_evidence_index(spec_texts: list[str]) -> dict[str, Any]:
    text = "\n".join(spec_texts)
    intent_ids = sorted(set(re.findall(r"intent\.[A-Za-z0-9_.-]+", text)))
    evidence_ids = sorted(set(re.findall(r"^\s*id:\s*([A-Za-z0-9_.-]+)\s*$", text, re.MULTILINE)))
    semantic_evidence_ids = [
        evidence_id for evidence_id in evidence_ids if "semantic" in evidence_id.lower()
    ]
    return {
        "intentIds": intent_ids[: PROMPT_BUDGET["maxSemanticClusters"]],
        "semanticEvidenceIds": semantic_evidence_ids,
        "documentationBodies": "excluded",
    }


def _candidate_metadata(
    manifest_metadata: dict[str, str],
    manifest_text: str,
    spec_paths: list[str],
    spec_texts: list[str],
) -> dict[str, Any]:
    combined = "\n".join([manifest_text, *spec_texts])
    capability_ids = sorted(set(re.findall(r"\b[A-Za-z0-9_.-]+\.core\.[A-Za-z0-9_.-]+", combined)))
    return {
        "packageId": manifest_metadata.get("id"),
        "packageVersion": manifest_metadata.get("version"),
        "name": manifest_metadata.get("name"),
        "summary": manifest_metadata.get("summary"),
        "license": manifest_metadata.get("license"),
        "specPaths": spec_paths,
        "capabilityIds": capability_ids,
        "intentIds": sorted(set(re.findall(r"intent\.[A-Za-z0-9_.-]+", combined))),
    }


def _artifact_record(
    workspace: Path,
    relative_path: str,
    artifact_id: str,
    *,
    required: bool,
) -> dict[str, Any]:
    if not _is_safe_relative_path(relative_path):
        raise ValueError(f"Unsafe artifact path: {relative_path}")
    path = workspace / relative_path
    if required:
        _required_file(workspace, relative_path)
    if path.is_symlink():
        raise ValueError(f"Artifact path must not be a symlink: {relative_path}")
    return {
        "id": artifact_id,
        "path": relative_path,
        "required": required,
        "sha256": _sha256_file(path),
    }


def _bundle_artifact_paths(bundle: dict[str, Any], *, prefix: str) -> list[str]:
    artifacts = bundle.get("artifacts")
    if not isinstance(artifacts, list):
        return []
    return [
        item["path"]
        for item in artifacts
        if isinstance(item, dict)
        and isinstance(item.get("id"), str)
        and item["id"].startswith(prefix)
        and isinstance(item.get("path"), str)
    ]


def _parse_manifest_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    in_metadata = False
    for line in text.splitlines():
        if line == "metadata:":
            in_metadata = True
            continue
        if not in_metadata:
            continue
        if line and not line.startswith(" "):
            break
        match = re.match(r"^  ([A-Za-z0-9_]+):\s*(.*)$", line)
        if match and match.group(1) in _MANIFEST_METADATA_KEYS:
            metadata[match.group(1)] = _strip_yaml_scalar(match.group(2))
    return metadata


def _parse_manifest_spec_paths(text: str) -> list[str]:
    spec_paths: list[str] = []
    in_specs = False
    for line in text.splitlines():
        if line == "specs:":
            in_specs = True
            continue
        if not in_specs:
            continue
        if line and not line.startswith(" "):
            break
        match = re.match(r"^  - path:\s*(.*)$", line)
        if match:
            value = _strip_yaml_scalar(match.group(1))
            if value:
                spec_paths.append(value)
    return spec_paths


def _strip_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON artifact must be an object: {path}")
    return value


def _optional_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return _read_json(path)


def _required_file(workspace: Path, relative_path: str) -> Path:
    if not _is_safe_relative_path(relative_path):
        raise ValueError(f"Unsafe required path: {relative_path}")
    path = workspace / relative_path
    if not path.exists() or not path.is_file():
        raise ValueError(f"Required artifact is missing: {relative_path}")
    if path.is_symlink():
        raise ValueError(f"Required artifact must not be a symlink: {relative_path}")
    return path


def _is_safe_relative_path(value: str) -> bool:
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts and bool(path.parts)


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
