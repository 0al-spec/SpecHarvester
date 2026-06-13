from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from spec_harvester.source_unit_intent import SourceUnitIntentBoundary

PRODUCER_NAME = "SpecHarvester"
DEFAULT_PRODUCER_VERSION = "0.1.0"
SPECNODE_SCHEMA_VERSION = 1
PUBLIC_INTERFACE_INDEX_FILENAME = "public-interface-index.json"
SEMANTIC_REVIEW_CONTRACT_VERSION = "1.0.0"
RETRY_ORCHESTRATION_CONTRACT_VERSION = "1.0.0"
DEFAULT_RETRY_MAX_ATTEMPTS = 2
MAX_RETRY_ATTEMPTS_LIMIT = 5

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
SEMANTIC_REVIEW_POLICY = {
    "modelFilesystemAccess": "none",
    "modelShellAccess": "none",
    "modelNetworkAccess": "provider_only",
    "allowedTools": [],
    "rawSourceAccess": "none",
    "secretAccess": "none",
    "candidateMutation": "none",
    "temperature": 0.0,
    "tokenBudget": 4_096,
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
SEMANTIC_REVIEW_EXCLUDED_CONTENT = {
    **EXCLUDED_CONTENT,
    "firstPassPromptTranscript": "excluded",
    "chainOfThought": "excluded",
    "firstPassProviderLogs": "excluded",
    "retryDirectives": "excluded",
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
ALLOWED_SEMANTIC_REVIEW_VERDICTS = {
    "approve",
    "needs_revision",
    "reject",
}
ALLOWED_SEMANTIC_REVIEW_SEVERITIES = {
    "info",
    "warning",
    "blocking",
}
ALLOWED_SEMANTIC_REVIEW_CODES = {
    "wrong_package_intent",
    "unsupported_capability_claim",
    "missing_evidence_reference",
    "overconfident_confidence_score",
    "unsafe_negative_claim",
    "schema_policy_mismatch",
    "authority_boundary_violation",
    "prompt_contract_violation",
}
SEMANTIC_REVIEW_FORBIDDEN_KEYS = {
    *FORBIDDEN_OPERATION_MARKERS,
    "candidatePatchProposal",
    "candidatePatch",
    "candidateMutation",
    "operations",
    "patch",
    "patches",
    "proposal",
    "retryDirective",
    "retryDirectives",
    "apply",
    "applyPatch",
    "directFileWrites",
}
RETRY_DIRECTIVE_BY_FINDING_CODE = {
    "wrong_package_intent": "refocus_target_package_intent",
    "unsupported_capability_claim": "remove_or_evidence_capability_claim",
    "missing_evidence_reference": "add_evidence_reference_or_drop_claim",
    "overconfident_confidence_score": "lower_confidence_or_add_evidence",
    "unsafe_negative_claim": "remove_unsupported_negative_claim",
    "schema_policy_mismatch": "align_with_schema_policy",
    "authority_boundary_violation": "remove_authority_request",
    "prompt_contract_violation": "restore_prompt_contract_boundary",
}
RETRY_DIRECTIVE_INSTRUCTIONS = {
    "refocus_target_package_intent": (
        "Revise only target-package behavior claims using deterministic evidence."
    ),
    "remove_or_evidence_capability_claim": (
        "Remove unsupported capability claims or attach known evidence references."
    ),
    "add_evidence_reference_or_drop_claim": (
        "Attach known evidence references to the claim or drop the claim."
    ),
    "lower_confidence_or_add_evidence": (
        "Lower confidence or add deterministic evidence before retaining the claim."
    ),
    "remove_unsupported_negative_claim": (
        "Remove negative claims unless explicit absence evidence exists."
    ),
    "align_with_schema_policy": (
        "Align proposed metadata with schema, SpecPM, and validation policy."
    ),
    "remove_authority_request": (
        "Remove any request for shell, network, provider, tool, or file-write authority."
    ),
    "restore_prompt_contract_boundary": (
        "Return to target-package intent inference and schema-bound proposal output."
    ),
}
ALLOWED_RETRY_DIRECTIVE_CODES = set(RETRY_DIRECTIVE_INSTRUCTIONS)
ALLOWED_RETRY_RUN_STATUSES = {"approved", "retry_scheduled", "retry_limit_reached"}
ALLOWED_RETRY_ATTEMPT_STATUSES = {"approved", "retry_scheduled", "retry_limit_reached"}
RETRY_FORBIDDEN_KEYS = {
    *SEMANTIC_REVIEW_FORBIDDEN_KEYS,
    "rawRepositorySource",
    "documentationBodies",
    "providerLogs",
    "firstPassPromptTranscript",
    "chainOfThought",
    "arbitraryPrompt",
    "arbitraryPrompts",
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


class SpecNodeSemanticReviewValidationError(SpecNodeRefinementValidationError):
    """Raised when semantic review output violates the clean-context contract."""


class SpecNodeRetryOrchestrationValidationError(SpecNodeRefinementValidationError):
    """Raised when retry orchestration output violates bounded retry policy."""


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


class SpecNodeSemanticReviewer(Protocol):
    def review(
        self,
        *,
        review_job: dict[str, Any],
        preview_plan: dict[str, Any],
        refinement_result: dict[str, Any],
    ) -> dict[str, Any]:
        """Return a SpecNodeSemanticReviewResult for a clean-context review job."""


@dataclass(frozen=True)
class SpecNodeRefinementSmokeOptions:
    candidate_workspace: Path
    provider: SpecNodeCompatibleProvider | None = None
    producer_version: str = DEFAULT_PRODUCER_VERSION


@dataclass(frozen=True)
class SpecNodeRefinementRetryOptions:
    candidate_workspace: Path
    provider: SpecNodeCompatibleProvider
    reviewer: SpecNodeSemanticReviewer
    max_attempts: int = DEFAULT_RETRY_MAX_ATTEMPTS
    producer_version: str = DEFAULT_PRODUCER_VERSION


@dataclass(frozen=True)
class SpecNodeRefinementRetrySequence:
    options: SpecNodeRefinementRetryOptions

    def run(self) -> dict[str, Any]:
        _validate_retry_max_attempts(self.options.max_attempts)
        bundle = self.bundle()
        preview_plan = self.preview_plan(bundle)
        bundle_digest = canonical_json_sha256_digest(bundle)
        preview_digest = canonical_json_sha256_digest(preview_plan)

        attempts: list[dict[str, Any]] = []
        retry_directive_set: dict[str, Any] | None = None
        status = "retry_limit_reached"

        for attempt_index in range(self.options.max_attempts):
            attempt = self.attempt(
                attempt_index=attempt_index,
                bundle=bundle,
                preview_plan=preview_plan,
                bundle_digest=bundle_digest,
                preview_digest=preview_digest,
                retry_directive_set=retry_directive_set,
            )
            retry_directive_set = attempt["retryDirectiveSet"]
            status = attempt["status"]
            attempts.append(attempt)
            if status in {"approved", "retry_limit_reached"}:
                break

        run = self.run_payload(
            status=status,
            attempts=attempts,
            bundle_digest=bundle_digest,
            preview_digest=preview_digest,
            final_refinement_digest=self.last_attempt_digest(attempts, "refinementResult"),
            final_semantic_review_digest=self.last_attempt_digest(
                attempts,
                "semanticReviewResult",
            ),
        )
        validate_specnode_refinement_retry_run(
            run,
            bundle=bundle,
            preview_plan=preview_plan,
        )
        return run

    def bundle(self) -> dict[str, Any]:
        return build_specnode_artifact_bundle(
            self.options.candidate_workspace,
            producer_version=self.options.producer_version,
        )

    def preview_plan(self, bundle: dict[str, Any]) -> dict[str, Any]:
        return build_refine_preview_plan(bundle, self.options.candidate_workspace)

    def attempt(
        self,
        *,
        attempt_index: int,
        bundle: dict[str, Any],
        preview_plan: dict[str, Any],
        bundle_digest: str,
        preview_digest: str,
        retry_directive_set: dict[str, Any] | None,
    ) -> dict[str, Any]:
        refinement_job = self.refinement_job(
            attempt_index=attempt_index,
            bundle=bundle,
            preview_plan=preview_plan,
            retry_directive_set=retry_directive_set,
        )
        refinement_result = self.refinement_result(refinement_job, preview_plan, bundle)
        review_job = build_specnode_semantic_review_job(
            bundle,
            preview_plan,
            refinement_result,
            producer_version=self.options.producer_version,
        )
        semantic_review_result = self.semantic_review_result(
            review_job,
            preview_plan,
            refinement_result,
            bundle,
        )
        next_directive_set = build_specnode_retry_directives(semantic_review_result)
        status = self.attempt_status(
            semantic_review_result,
            attempt_index=attempt_index,
        )
        return _retry_attempt_record(
            attempt_index=attempt_index,
            source_bundle_digest=bundle_digest,
            source_preview_plan_digest=preview_digest,
            refinement_job=refinement_job,
            refinement_result=refinement_result,
            review_job=review_job,
            semantic_review_result=semantic_review_result,
            retry_directive_set=next_directive_set,
            status=status,
        )

    def refinement_job(
        self,
        *,
        attempt_index: int,
        bundle: dict[str, Any],
        preview_plan: dict[str, Any],
        retry_directive_set: dict[str, Any] | None,
    ) -> dict[str, Any]:
        if attempt_index == 0:
            return build_specnode_refinement_job(
                bundle,
                preview_plan,
                producer_version=self.options.producer_version,
            )
        if retry_directive_set is None:
            raise SpecNodeRetryOrchestrationValidationError(
                "retry attempt requires retry directive set"
            )
        return build_specnode_retry_refinement_job(
            bundle,
            preview_plan,
            retry_directive_set,
            attempt_index=attempt_index,
            producer_version=self.options.producer_version,
        )

    def refinement_result(
        self,
        refinement_job: dict[str, Any],
        preview_plan: dict[str, Any],
        bundle: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            result = self.options.provider.refine(
                job=refinement_job,
                preview_plan=preview_plan,
            )
        except SpecNodeProviderUnavailable:
            result = build_provider_unavailable_result(refinement_job, preview_plan)
        validate_specnode_refinement_result(
            result,
            job=refinement_job,
            preview_plan=preview_plan,
            bundle=bundle,
        )
        return result

    def semantic_review_result(
        self,
        review_job: dict[str, Any],
        preview_plan: dict[str, Any],
        refinement_result: dict[str, Any],
        bundle: dict[str, Any],
    ) -> dict[str, Any]:
        result = self.options.reviewer.review(
            review_job=review_job,
            preview_plan=preview_plan,
            refinement_result=refinement_result,
        )
        validate_specnode_semantic_review_result(
            result,
            review_job=review_job,
            preview_plan=preview_plan,
            refinement_result=refinement_result,
            bundle=bundle,
        )
        return result

    def attempt_status(
        self,
        semantic_review_result: dict[str, Any],
        *,
        attempt_index: int,
    ) -> str:
        verdict = semantic_review_result.get("verdict")
        if verdict == "approve":
            return "approved"
        if attempt_index + 1 >= self.options.max_attempts:
            return "retry_limit_reached"
        return "retry_scheduled"

    def run_payload(
        self,
        *,
        status: str,
        attempts: list[dict[str, Any]],
        bundle_digest: str,
        preview_digest: str,
        final_refinement_digest: str | None,
        final_semantic_review_digest: str | None,
    ) -> dict[str, Any]:
        return {
            "schemaVersion": SPECNODE_SCHEMA_VERSION,
            "kind": "SpecNodeRefinementRetryRun",
            "contract": {
                "kind": "SpecNodeRefinementRetryOrchestrationContract",
                "retryOrchestrationContractVersion": RETRY_ORCHESTRATION_CONTRACT_VERSION,
            },
            "status": status,
            "retryPolicy": {
                "kind": "SpecNodeRefinementRetryPolicy",
                "maxAttempts": self.options.max_attempts,
                "attemptCount": len(attempts),
                "artifactReuse": "same_bundle_and_preview_plan",
                "retryDirectiveSource": "SpecNodeSemanticReviewFinding",
            },
            "sourceBundle": {
                "kind": "SpecHarvesterSpecNodeArtifactBundle",
                "digest": bundle_digest,
            },
            "previewPlan": {
                "kind": "SpecHarvesterRefinePreviewPlan",
                "digest": preview_digest,
            },
            "attempts": attempts,
            "finalRefinementResultDigest": final_refinement_digest,
            "finalSemanticReviewResultDigest": final_semantic_review_digest,
        }

    def last_attempt_digest(self, attempts: list[dict[str, Any]], key: str) -> str | None:
        if not attempts:
            return None
        digest = _nested_digest(attempts[-1], key)
        return digest if isinstance(digest, str) else None


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


def run_specnode_refinement_retry_orchestration(
    options: SpecNodeRefinementRetryOptions,
) -> dict[str, Any]:
    return SpecNodeRefinementRetrySequence(options).run()


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
    source_unit_boundary = SourceUnitIntentBoundary.from_snapshot(snapshot).metadata()
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
            "sourceUnitIntentBoundary": source_unit_boundary,
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


def build_specnode_semantic_review_job(
    bundle: dict[str, Any],
    preview_plan: dict[str, Any],
    refinement_result: dict[str, Any],
    *,
    producer_version: str = DEFAULT_PRODUCER_VERSION,
) -> dict[str, Any]:
    bundle_digest = canonical_json_sha256_digest(bundle)
    preview_digest = canonical_json_sha256_digest(preview_plan)
    refinement_digest = canonical_json_sha256_digest(refinement_result)
    usage_receipt = refinement_result.get("usageReceipt")
    usage_receipt_digest = (
        canonical_json_sha256_digest(usage_receipt) if isinstance(usage_receipt, dict) else None
    )
    return {
        "schemaVersion": SPECNODE_SCHEMA_VERSION,
        "kind": "SpecNodeSemanticReviewJob",
        "jobId": f"specnode-semantic-review-{refinement_digest.removeprefix('sha256:')[:16]}",
        "createdAt": "2026-05-22T00:00:00Z",
        "producer": {"name": PRODUCER_NAME, "version": producer_version},
        "contract": {
            "kind": "SpecNodeSemanticReviewContract",
            "semanticReviewContractVersion": SEMANTIC_REVIEW_CONTRACT_VERSION,
            "outputKind": "SpecNodeSemanticReviewResult",
        },
        "sourceBundle": {
            "kind": "SpecHarvesterSpecNodeArtifactBundle",
            "digest": bundle_digest,
            "artifactDigests": _artifact_digest_records(bundle),
        },
        "previewPlan": {
            "kind": "SpecHarvesterRefinePreviewPlan",
            "digest": preview_digest,
            "candidate": preview_plan.get("candidate", {}),
            "compactModelInput": preview_plan.get("compactModelInput", {}),
            "artifactDigests": preview_plan.get("artifactDigests", []),
        },
        "reviewedRefinementResult": {
            "kind": "SpecNodeReviewedRefinementResult",
            "digest": refinement_digest,
            "job": refinement_result.get("job", {}),
            "result": refinement_result.get("result", {}),
            "usageReceiptDigest": usage_receipt_digest,
        },
        "policy": dict(SEMANTIC_REVIEW_POLICY),
        "excludedContent": dict(SEMANTIC_REVIEW_EXCLUDED_CONTENT),
        "rubric": {
            "kind": "SpecNodeSemanticReviewRubric",
            "verdicts": sorted(ALLOWED_SEMANTIC_REVIEW_VERDICTS),
            "findingSeverities": sorted(ALLOWED_SEMANTIC_REVIEW_SEVERITIES),
            "findingCodes": sorted(ALLOWED_SEMANTIC_REVIEW_CODES),
            "reviewChecks": [
                "target package intent matches deterministic evidence",
                "capability claims are supported by known evidence references",
                "negative claims are not inferred from absence alone",
                "confidence values are calibrated to evidence coverage",
                "output obeys SpecNodePatchProposalContract authority boundaries",
                "review emits findings only and cannot mutate candidates",
            ],
        },
        "requestedOutputs": [
            "verdict",
            "findings",
            "summary",
        ],
    }


def build_specnode_retry_directives(
    semantic_review_result: dict[str, Any],
    *,
    max_directives: int = 10,
) -> dict[str, Any]:
    verdict = semantic_review_result.get("verdict")
    findings = semantic_review_result.get("findings")
    if not isinstance(findings, list):
        findings = []
    directives: list[dict[str, Any]] = []
    if verdict in {"needs_revision", "reject"}:
        for index, finding in enumerate(findings[:max_directives], start=1):
            if not isinstance(finding, dict):
                continue
            source_code = finding.get("code")
            directive_code = RETRY_DIRECTIVE_BY_FINDING_CODE.get(str(source_code))
            if directive_code is None:
                raise SpecNodeRetryOrchestrationValidationError(
                    f"unsupported semantic review finding code for retry: {source_code!r}"
                )
            directive = {
                "kind": "SpecNodeRetryDirective",
                "directiveId": f"retry-directive-{index:03d}",
                "code": directive_code,
                "sourceFindingId": finding.get("findingId"),
                "sourceFindingCode": source_code,
                "sourceFindingSeverity": finding.get("severity"),
                "target": finding.get("target", {}),
                "evidenceRefs": finding.get("evidenceRefs", []),
                "boundedInstruction": RETRY_DIRECTIVE_INSTRUCTIONS[directive_code],
            }
            _reject_forbidden_retry_content(directive)
            directives.append(directive)

    directive_set = {
        "schemaVersion": SPECNODE_SCHEMA_VERSION,
        "kind": "SpecNodeRetryDirectiveSet",
        "sourceSemanticReviewResultDigest": canonical_json_sha256_digest(semantic_review_result),
        "sourceVerdict": verdict,
        "policy": {
            "kind": "SpecNodeRetryDirectivePolicy",
            "maxDirectives": max_directives,
            "rawTextPropagation": "forbidden",
            "candidateOutputAuthority": "proposal_only",
        },
        "directives": directives,
    }
    errors: list[str] = []
    _validate_retry_directive_set(directive_set, errors=errors)
    if errors:
        raise SpecNodeRetryOrchestrationValidationError("; ".join(errors))
    return directive_set


def build_specnode_retry_refinement_job(
    bundle: dict[str, Any],
    preview_plan: dict[str, Any],
    retry_directive_set: dict[str, Any],
    *,
    attempt_index: int,
    producer_version: str = DEFAULT_PRODUCER_VERSION,
) -> dict[str, Any]:
    if attempt_index <= 0:
        raise ValueError("retry attempt_index must be greater than zero")
    errors: list[str] = []
    _validate_retry_directive_set(retry_directive_set, errors=errors)
    if errors:
        raise SpecNodeRetryOrchestrationValidationError("; ".join(errors))

    plan_digest = canonical_json_sha256_digest(preview_plan)
    directive_digest = canonical_json_sha256_digest(retry_directive_set)
    job = build_specnode_refinement_job(
        bundle,
        preview_plan,
        producer_version=producer_version,
    )
    job.update(
        {
            "jobId": (
                f"specnode-retry-{plan_digest.removeprefix('sha256:')[:16]}-{attempt_index:02d}"
            ),
            "retryContext": {
                "kind": "SpecNodeRetryContext",
                "attemptIndex": attempt_index,
                "sourceBundleDigest": canonical_json_sha256_digest(bundle),
                "sourcePreviewPlanDigest": plan_digest,
                "retryDirectiveSetDigest": directive_digest,
                "retryDirectiveSet": retry_directive_set,
            },
        }
    )
    return job


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


def validate_specnode_semantic_review_result(
    result: dict[str, Any],
    *,
    review_job: dict[str, Any],
    preview_plan: dict[str, Any],
    refinement_result: dict[str, Any],
    bundle: dict[str, Any],
) -> None:
    errors: list[str] = []
    _validate_semantic_review_job(
        review_job,
        errors=errors,
        preview_plan=preview_plan,
        refinement_result=refinement_result,
        bundle=bundle,
    )
    for path, key in _forbidden_semantic_review_keys(result):
        errors.append(f"semantic review result contains forbidden mutation key: {path}.{key}")

    if result.get("kind") != "SpecNodeSemanticReviewResult":
        errors.append("semantic review kind must be SpecNodeSemanticReviewResult")
    if result.get("schemaVersion") != SPECNODE_SCHEMA_VERSION:
        errors.append("semantic review schemaVersion must be 1")

    expected_job_digest = canonical_json_sha256_digest(review_job)
    result_job = result.get("job")
    if not isinstance(result_job, dict):
        errors.append("semantic review job must be an object")
    else:
        if result_job.get("kind") != "SpecNodeSemanticReviewJob":
            errors.append("semantic review job kind must be SpecNodeSemanticReviewJob")
        if result_job.get("jobId") != review_job.get("jobId"):
            errors.append("semantic review jobId must match source review job")
        if result_job.get("digest") != expected_job_digest:
            errors.append("semantic review job digest must match source review job")

    reviewed = result.get("reviewedRefinementResult")
    expected_refinement_digest = canonical_json_sha256_digest(refinement_result)
    if not isinstance(reviewed, dict):
        errors.append("reviewedRefinementResult must be an object")
    else:
        if reviewed.get("kind") != "SpecNodeRefinementResult":
            errors.append("reviewedRefinementResult kind must be SpecNodeRefinementResult")
        if reviewed.get("digest") != expected_refinement_digest:
            errors.append("reviewedRefinementResult digest must match source result")

    verdict = result.get("verdict")
    if verdict not in ALLOWED_SEMANTIC_REVIEW_VERDICTS:
        errors.append("semantic review verdict is not allowed")

    findings = result.get("findings")
    blocking_count = 0
    if not isinstance(findings, list):
        errors.append("semantic review findings must be a list")
        findings = []
    else:
        allowed_refs = _allowed_semantic_review_evidence_refs(
            bundle, preview_plan, refinement_result
        )
        for index, finding in enumerate(findings):
            if not isinstance(finding, dict):
                errors.append(f"semantic review finding {index} must be an object")
                continue
            if finding.get("kind") != "SpecNodeSemanticReviewFinding":
                errors.append(f"semantic review finding {index} kind is invalid")
            if not isinstance(finding.get("findingId"), str) or not finding["findingId"].strip():
                errors.append(f"semantic review finding {index} requires findingId")
            if finding.get("code") not in ALLOWED_SEMANTIC_REVIEW_CODES:
                errors.append(f"semantic review finding {index} code is not allowed")
            severity = finding.get("severity")
            if severity not in ALLOWED_SEMANTIC_REVIEW_SEVERITIES:
                errors.append(f"semantic review finding {index} severity is not allowed")
            if severity == "blocking":
                blocking_count += 1
            if not isinstance(finding.get("message"), str) or not finding["message"].strip():
                errors.append(f"semantic review finding {index} requires message")
            _validate_semantic_review_finding_refs(
                finding.get("evidenceRefs"),
                errors=errors,
                index=index,
                allowed_refs=allowed_refs,
            )
            target = finding.get("target")
            if target is not None and not isinstance(target, dict):
                errors.append(f"semantic review finding {index} target must be an object")

    if verdict == "approve" and blocking_count:
        errors.append("approve verdict cannot contain blocking findings")
    if verdict in {"needs_revision", "reject"} and not findings:
        errors.append(f"{verdict} verdict requires at least one finding")
    if verdict == "reject" and not blocking_count:
        errors.append("reject verdict requires at least one blocking finding")

    summary = result.get("summary")
    if summary is not None and (not isinstance(summary, str) or not summary.strip()):
        errors.append("semantic review summary must be a non-empty string when present")

    if errors:
        raise SpecNodeSemanticReviewValidationError("; ".join(errors))


def validate_specnode_refinement_retry_run(
    run: dict[str, Any],
    *,
    bundle: dict[str, Any],
    preview_plan: dict[str, Any],
) -> None:
    errors: list[str] = []
    if run.get("kind") != "SpecNodeRefinementRetryRun":
        errors.append("retry run kind must be SpecNodeRefinementRetryRun")
    if run.get("schemaVersion") != SPECNODE_SCHEMA_VERSION:
        errors.append("retry run schemaVersion must be 1")
    run_status = run.get("status")
    if run_status not in ALLOWED_RETRY_RUN_STATUSES:
        errors.append("retry run status is invalid")
    contract = run.get("contract")
    if not isinstance(contract, dict):
        errors.append("retry run contract must be an object")
    else:
        if contract.get("kind") != "SpecNodeRefinementRetryOrchestrationContract":
            errors.append("retry run contract kind is invalid")
        if contract.get("retryOrchestrationContractVersion") != (
            RETRY_ORCHESTRATION_CONTRACT_VERSION
        ):
            errors.append("retry run contract version is invalid")

    source_bundle_digest = canonical_json_sha256_digest(bundle)
    preview_plan_digest = canonical_json_sha256_digest(preview_plan)
    source_bundle = run.get("sourceBundle")
    if not isinstance(source_bundle, dict) or source_bundle.get("digest") != source_bundle_digest:
        errors.append("retry run sourceBundle digest must match bundle")
    source_preview = run.get("previewPlan")
    if not isinstance(source_preview, dict) or source_preview.get("digest") != preview_plan_digest:
        errors.append("retry run previewPlan digest must match preview plan")

    retry_policy = run.get("retryPolicy")
    max_attempts = None
    if not isinstance(retry_policy, dict):
        errors.append("retry run retryPolicy must be an object")
    else:
        max_attempts = retry_policy.get("maxAttempts")
        if not isinstance(max_attempts, int) or not (1 <= max_attempts <= MAX_RETRY_ATTEMPTS_LIMIT):
            errors.append("retry run retryPolicy.maxAttempts is invalid")
        if not isinstance(retry_policy.get("attemptCount"), int):
            errors.append("retry run retryPolicy.attemptCount is invalid")
        if retry_policy.get("artifactReuse") != "same_bundle_and_preview_plan":
            errors.append("retry run retryPolicy.artifactReuse must require immutable artifacts")

    attempts = run.get("attempts")
    if not isinstance(attempts, list) or not attempts:
        errors.append("retry run attempts must be a non-empty list")
        attempts = []
    elif isinstance(max_attempts, int) and len(attempts) > max_attempts:
        errors.append("retry run attempts exceed maxAttempts")
    if isinstance(retry_policy, dict) and retry_policy.get("attemptCount") != len(attempts):
        errors.append("retry run retryPolicy.attemptCount must match attempts length")

    final_refinement_digest = None
    final_review_digest = None
    for expected_index, attempt in enumerate(attempts):
        if not isinstance(attempt, dict):
            errors.append(f"retry attempt {expected_index} must be an object")
            continue
        if attempt.get("kind") != "SpecNodeRefinementRetryAttempt":
            errors.append(f"retry attempt {expected_index} kind is invalid")
        if attempt.get("attemptIndex") != expected_index:
            errors.append(f"retry attempt {expected_index} index is not sequential")
        if attempt.get("status") not in ALLOWED_RETRY_ATTEMPT_STATUSES:
            errors.append(f"retry attempt {expected_index} status is invalid")
        if attempt.get("sourceBundleDigest") != source_bundle_digest:
            errors.append(f"retry attempt {expected_index} source bundle digest drifted")
        if attempt.get("sourcePreviewPlanDigest") != preview_plan_digest:
            errors.append(f"retry attempt {expected_index} preview plan digest drifted")
        _validate_retry_attempt_digest_refs(attempt, errors=errors, index=expected_index)
        directive_set = attempt.get("retryDirectiveSet")
        if not isinstance(directive_set, dict):
            errors.append(f"retry attempt {expected_index} retryDirectiveSet must be an object")
        else:
            _validate_retry_directive_set(directive_set, errors=errors)
            semantic_review_result = attempt.get("semanticReviewResult")
            if isinstance(semantic_review_result, dict):
                if directive_set.get("sourceSemanticReviewResultDigest") != (
                    semantic_review_result.get("digest")
                ):
                    errors.append(f"retry attempt {expected_index} directive digest mismatch")
                if directive_set.get("sourceVerdict") != semantic_review_result.get("verdict"):
                    errors.append(f"retry attempt {expected_index} directive verdict mismatch")
        final_refinement_digest = _nested_digest(attempt, "refinementResult")
        final_review_digest = _nested_digest(attempt, "semanticReviewResult")

    if attempts:
        if run.get("finalRefinementResultDigest") != final_refinement_digest:
            errors.append("retry run finalRefinementResultDigest must match last attempt")
        if run.get("finalSemanticReviewResultDigest") != final_review_digest:
            errors.append("retry run finalSemanticReviewResultDigest must match last attempt")
        final_status = attempts[-1].get("status") if isinstance(attempts[-1], dict) else None
        if run.get("status") == "approved" and final_status != "approved":
            errors.append("approved retry run requires final approved attempt")
        if run.get("status") == "retry_scheduled" and final_status != "retry_scheduled":
            errors.append("retry_scheduled run requires final retry_scheduled attempt")
        if (
            run.get("status") == "retry_scheduled"
            and isinstance(max_attempts, int)
            and len(attempts) >= max_attempts
        ):
            errors.append("retry_scheduled run requires remaining retry capacity")
        if run.get("status") == "retry_limit_reached" and final_status != "retry_limit_reached":
            errors.append("retry_limit_reached run requires final retry_limit_reached attempt")

    if errors:
        raise SpecNodeRetryOrchestrationValidationError("; ".join(errors))


def canonical_json_sha256_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return f"sha256:{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"


def parse_specnode_model_json_object(content: str) -> dict[str, Any]:
    """Parse direct JSON or the observed gpt-oss channel-wrapped JSON object."""
    text = content.strip()
    if not text:
        raise SpecNodeModelJSONParseError("model content is empty")

    try:
        return _parse_exact_json_object(text)
    except SpecNodeModelJSONParseError as direct_error:
        if not _looks_like_gpt_oss_wrapped_message(text):
            raise

        payloads = _gpt_oss_message_payloads(text)
        if len(payloads) != 1:
            raise SpecNodeModelJSONParseError(
                "expected exactly one gpt-oss JSON message payload"
            ) from direct_error
        return _parse_exact_json_object(payloads[0])


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


def _validate_semantic_review_job(
    review_job: dict[str, Any],
    *,
    errors: list[str],
    preview_plan: dict[str, Any],
    refinement_result: dict[str, Any],
    bundle: dict[str, Any],
) -> None:
    _validate_exact_keys(
        review_job,
        {
            "schemaVersion",
            "kind",
            "jobId",
            "createdAt",
            "producer",
            "contract",
            "sourceBundle",
            "previewPlan",
            "reviewedRefinementResult",
            "policy",
            "excludedContent",
            "rubric",
            "requestedOutputs",
        },
        errors=errors,
        label="semantic review source job",
    )
    if review_job.get("kind") != "SpecNodeSemanticReviewJob":
        errors.append("semantic review source job kind must be SpecNodeSemanticReviewJob")
    if review_job.get("schemaVersion") != SPECNODE_SCHEMA_VERSION:
        errors.append("semantic review source job schemaVersion must be 1")
    if review_job.get("policy") != SEMANTIC_REVIEW_POLICY:
        errors.append("semantic review source job policy must match clean-context policy")
    if review_job.get("excludedContent") != SEMANTIC_REVIEW_EXCLUDED_CONTENT:
        errors.append("semantic review source job excludedContent must match clean-context policy")

    contract = review_job.get("contract")
    if not isinstance(contract, dict):
        errors.append("semantic review source job contract must be an object")
    else:
        _validate_exact_keys(
            contract,
            {"kind", "semanticReviewContractVersion", "outputKind"},
            errors=errors,
            label="semantic review source job contract",
        )
        if contract.get("kind") != "SpecNodeSemanticReviewContract":
            errors.append("semantic review source job contract kind is invalid")
        if contract.get("semanticReviewContractVersion") != SEMANTIC_REVIEW_CONTRACT_VERSION:
            errors.append("semantic review source job contract version is invalid")
        if contract.get("outputKind") != "SpecNodeSemanticReviewResult":
            errors.append("semantic review source job outputKind is invalid")

    source_bundle = review_job.get("sourceBundle")
    expected_bundle_digest = canonical_json_sha256_digest(bundle)
    if not isinstance(source_bundle, dict):
        errors.append("semantic review sourceBundle must be an object")
    else:
        _validate_exact_keys(
            source_bundle,
            {"kind", "digest", "artifactDigests"},
            errors=errors,
            label="semantic review sourceBundle",
        )
        if source_bundle.get("kind") != "SpecHarvesterSpecNodeArtifactBundle":
            errors.append("semantic review sourceBundle kind is invalid")
        if source_bundle.get("digest") != expected_bundle_digest:
            errors.append("semantic review sourceBundle digest must match bundle")
        if source_bundle.get("artifactDigests") != _artifact_digest_records(bundle):
            errors.append("semantic review sourceBundle artifactDigests must match bundle")

    source_preview = review_job.get("previewPlan")
    expected_preview_digest = canonical_json_sha256_digest(preview_plan)
    if not isinstance(source_preview, dict):
        errors.append("semantic review previewPlan must be an object")
    else:
        _validate_exact_keys(
            source_preview,
            {"kind", "digest", "candidate", "compactModelInput", "artifactDigests"},
            errors=errors,
            label="semantic review previewPlan",
        )
        if source_preview.get("kind") != "SpecHarvesterRefinePreviewPlan":
            errors.append("semantic review previewPlan kind is invalid")
        if source_preview.get("digest") != expected_preview_digest:
            errors.append("semantic review previewPlan digest must match preview plan")
        if source_preview.get("candidate") != preview_plan.get("candidate", {}):
            errors.append("semantic review previewPlan candidate must match preview plan")
        if source_preview.get("compactModelInput") != preview_plan.get("compactModelInput", {}):
            errors.append("semantic review previewPlan compactModelInput must match preview plan")
        if source_preview.get("artifactDigests") != preview_plan.get("artifactDigests", []):
            errors.append("semantic review previewPlan artifactDigests must match preview plan")

    reviewed = review_job.get("reviewedRefinementResult")
    expected_refinement_digest = canonical_json_sha256_digest(refinement_result)
    expected_usage_receipt = refinement_result.get("usageReceipt")
    expected_usage_receipt_digest = (
        canonical_json_sha256_digest(expected_usage_receipt)
        if isinstance(expected_usage_receipt, dict)
        else None
    )
    if not isinstance(reviewed, dict):
        errors.append("semantic review reviewedRefinementResult must be an object")
    else:
        _validate_exact_keys(
            reviewed,
            {"kind", "digest", "job", "result", "usageReceiptDigest"},
            errors=errors,
            label="semantic review reviewedRefinementResult",
        )
        if reviewed.get("kind") != "SpecNodeReviewedRefinementResult":
            errors.append("semantic review reviewedRefinementResult kind is invalid")
        if reviewed.get("digest") != expected_refinement_digest:
            errors.append("semantic review reviewedRefinementResult digest must match result")
        if reviewed.get("job") != refinement_result.get("job", {}):
            errors.append("semantic review reviewedRefinementResult job must match result")
        if reviewed.get("result") != refinement_result.get("result", {}):
            errors.append("semantic review reviewedRefinementResult result must match result")
        if reviewed.get("usageReceiptDigest") != expected_usage_receipt_digest:
            errors.append(
                "semantic review reviewedRefinementResult usageReceiptDigest must match result"
            )


def _validate_exact_keys(
    value: dict[str, Any],
    allowed_keys: set[str],
    *,
    errors: list[str],
    label: str,
) -> None:
    actual_keys = set(value)
    missing_keys = allowed_keys - actual_keys
    extra_keys = actual_keys - allowed_keys
    for key in sorted(missing_keys):
        errors.append(f"{label} missing allowed-shape field: {key}")
    for key in sorted(extra_keys):
        errors.append(f"{label} contains unexpected clean-context field: {key}")


def _retry_attempt_record(
    *,
    attempt_index: int,
    source_bundle_digest: str,
    source_preview_plan_digest: str,
    refinement_job: dict[str, Any],
    refinement_result: dict[str, Any],
    review_job: dict[str, Any],
    semantic_review_result: dict[str, Any],
    retry_directive_set: dict[str, Any],
    status: str,
) -> dict[str, Any]:
    return {
        "kind": "SpecNodeRefinementRetryAttempt",
        "attemptIndex": attempt_index,
        "status": status,
        "sourceBundleDigest": source_bundle_digest,
        "sourcePreviewPlanDigest": source_preview_plan_digest,
        "refinementJob": {
            "kind": refinement_job.get("kind"),
            "jobId": refinement_job.get("jobId"),
            "digest": canonical_json_sha256_digest(refinement_job),
        },
        "refinementResult": {
            "kind": refinement_result.get("kind"),
            "digest": canonical_json_sha256_digest(refinement_result),
        },
        "semanticReviewJob": {
            "kind": review_job.get("kind"),
            "jobId": review_job.get("jobId"),
            "digest": canonical_json_sha256_digest(review_job),
        },
        "semanticReviewResult": {
            "kind": semantic_review_result.get("kind"),
            "digest": canonical_json_sha256_digest(semantic_review_result),
            "verdict": semantic_review_result.get("verdict"),
        },
        "retryDirectiveSet": retry_directive_set,
        "retryDirectiveSetDigest": canonical_json_sha256_digest(retry_directive_set),
    }


def _validate_retry_max_attempts(max_attempts: int) -> None:
    if not isinstance(max_attempts, int) or not (1 <= max_attempts <= MAX_RETRY_ATTEMPTS_LIMIT):
        raise ValueError(
            f"max_attempts must be between 1 and {MAX_RETRY_ATTEMPTS_LIMIT}, got {max_attempts!r}"
        )


def _reject_forbidden_retry_content(value: Any) -> None:
    findings = _forbidden_retry_keys(value)
    if findings:
        path, key = findings[0]
        raise SpecNodeRetryOrchestrationValidationError(
            f"retry directive contains forbidden key: {path}.{key}"
        )


def _forbidden_retry_keys(value: Any, *, path: str = "$") -> list[tuple[str, str]]:
    if isinstance(value, dict):
        findings: list[tuple[str, str]] = []
        for key, child in value.items():
            if key in RETRY_FORBIDDEN_KEYS:
                findings.append((path, key))
            findings.extend(_forbidden_retry_keys(child, path=f"{path}.{key}"))
        return findings
    if isinstance(value, list):
        findings = []
        for index, child in enumerate(value):
            findings.extend(_forbidden_retry_keys(child, path=f"{path}[{index}]"))
        return findings
    return []


def _validate_retry_directive_set(
    directive_set: Any,
    *,
    errors: list[str],
) -> None:
    if not isinstance(directive_set, dict):
        errors.append("retry directive set must be an object")
        return
    for path, key in _forbidden_retry_keys(directive_set):
        errors.append(f"retry directive set contains forbidden key: {path}.{key}")
    if directive_set.get("kind") != "SpecNodeRetryDirectiveSet":
        errors.append("retry directive set kind is invalid")
    if directive_set.get("schemaVersion") != SPECNODE_SCHEMA_VERSION:
        errors.append("retry directive set schemaVersion must be 1")
    if not _is_digest(directive_set.get("sourceSemanticReviewResultDigest")):
        errors.append("retry directive set sourceSemanticReviewResultDigest must be a digest")
    if directive_set.get("sourceVerdict") not in ALLOWED_SEMANTIC_REVIEW_VERDICTS:
        errors.append("retry directive set sourceVerdict is invalid")

    policy = directive_set.get("policy")
    if not isinstance(policy, dict):
        errors.append("retry directive set policy must be an object")
        max_directives = None
    else:
        max_directives = policy.get("maxDirectives")
        if not isinstance(max_directives, int) or max_directives < 1:
            errors.append("retry directive set policy.maxDirectives is invalid")
        if policy.get("rawTextPropagation") != "forbidden":
            errors.append("retry directive set policy must forbid raw text propagation")
        if policy.get("candidateOutputAuthority") != "proposal_only":
            errors.append(
                "retry directive set policy candidateOutputAuthority must be proposal_only"
            )

    directives = directive_set.get("directives")
    if not isinstance(directives, list):
        errors.append("retry directive set directives must be a list")
        return
    if directive_set.get("sourceVerdict") == "approve" and directives:
        errors.append("approve retry directive set must not contain directives")
    if directive_set.get("sourceVerdict") in {"needs_revision", "reject"} and not directives:
        errors.append("non-approve retry directive set requires directives")
    if isinstance(max_directives, int) and len(directives) > max_directives:
        errors.append("retry directive set directives exceed policy.maxDirectives")

    for index, directive in enumerate(directives):
        if not isinstance(directive, dict):
            errors.append(f"retry directive {index} must be an object")
            continue
        if directive.get("kind") != "SpecNodeRetryDirective":
            errors.append(f"retry directive {index} kind is invalid")
        if directive.get("code") not in ALLOWED_RETRY_DIRECTIVE_CODES:
            errors.append(f"retry directive {index} code is not allowed")
        if directive.get("boundedInstruction") != RETRY_DIRECTIVE_INSTRUCTIONS.get(
            directive.get("code")
        ):
            errors.append(f"retry directive {index} boundedInstruction is invalid")
        if not isinstance(directive.get("sourceFindingId"), str):
            errors.append(f"retry directive {index} sourceFindingId must be a string")
        if directive.get("sourceFindingCode") not in ALLOWED_SEMANTIC_REVIEW_CODES:
            errors.append(f"retry directive {index} sourceFindingCode is invalid")
        evidence_refs = directive.get("evidenceRefs")
        if (
            not isinstance(evidence_refs, list)
            or not evidence_refs
            or not all(isinstance(item, str) for item in evidence_refs)
        ):
            errors.append(f"retry directive {index} evidenceRefs must be non-empty strings")


def _validate_retry_attempt_digest_refs(
    attempt: dict[str, Any],
    *,
    errors: list[str],
    index: int,
) -> None:
    for field, expected_kind in (
        ("refinementJob", "SpecNodeRefinementJob"),
        ("refinementResult", "SpecNodeRefinementResult"),
        ("semanticReviewJob", "SpecNodeSemanticReviewJob"),
        ("semanticReviewResult", "SpecNodeSemanticReviewResult"),
    ):
        value = attempt.get(field)
        if not isinstance(value, dict):
            errors.append(f"retry attempt {index} {field} must be an object")
            continue
        if value.get("kind") != expected_kind:
            errors.append(f"retry attempt {index} {field} kind is invalid")
        if not _is_digest(value.get("digest")):
            errors.append(f"retry attempt {index} {field} digest must be a digest")
    directive_set = attempt.get("retryDirectiveSet")
    directive_digest = attempt.get("retryDirectiveSetDigest")
    if not _is_digest(directive_digest):
        errors.append(f"retry attempt {index} retryDirectiveSetDigest must be a digest")
    if isinstance(directive_set, dict) and directive_digest != canonical_json_sha256_digest(
        directive_set
    ):
        errors.append(f"retry attempt {index} retryDirectiveSetDigest must match directive set")


def _nested_digest(value: dict[str, Any], key: str) -> Any:
    nested = value.get(key)
    if not isinstance(nested, dict):
        return None
    return nested.get("digest")


def _validate_semantic_review_finding_refs(
    value: Any,
    *,
    errors: list[str],
    index: int,
    allowed_refs: set[str],
) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"semantic review finding {index} requires non-empty evidenceRefs")
        return
    for item in value:
        if not isinstance(item, str):
            errors.append(f"semantic review finding {index} evidenceRefs must be strings")
        elif item not in allowed_refs:
            errors.append(f"semantic review finding {index} uses unknown evidenceRef: {item}")


def _allowed_semantic_review_evidence_refs(
    bundle: dict[str, Any],
    preview_plan: dict[str, Any],
    refinement_result: dict[str, Any],
) -> set[str]:
    refs = {
        "source_bundle",
        "preview_plan",
        "compact_model_input",
        "harvest_summary",
        "project_profile",
        "public_interface_summary",
        "semantic_evidence_index",
        "validation_summaries",
        "draft_candidate_metadata",
        "reviewed_refinement_result",
        "refinement_result",
    }
    artifacts = bundle.get("artifacts")
    if isinstance(artifacts, list):
        refs.update(
            item["id"]
            for item in artifacts
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        )

    compact_input = preview_plan.get("compactModelInput")
    if isinstance(compact_input, dict):
        semantic_index = compact_input.get("semanticEvidenceIndex")
        if isinstance(semantic_index, dict):
            semantic_ids = semantic_index.get("semanticEvidenceIds")
            if isinstance(semantic_ids, list):
                refs.update(item for item in semantic_ids if isinstance(item, str))

    result_body = refinement_result.get("result")
    if isinstance(result_body, dict):
        proposal = result_body.get("proposal")
        if isinstance(proposal, dict):
            proposal_id = proposal.get("proposalId")
            if isinstance(proposal_id, str):
                refs.add(proposal_id)
            operations = proposal.get("operations")
            if isinstance(operations, list):
                refs.update(
                    operation["operationId"]
                    for operation in operations
                    if isinstance(operation, dict) and isinstance(operation.get("operationId"), str)
                )
        rejection = result_body.get("rejection")
        if isinstance(rejection, dict) and isinstance(rejection.get("rejectionId"), str):
            refs.add(rejection["rejectionId"])

    return refs


def _forbidden_semantic_review_keys(value: Any, *, path: str = "$") -> list[tuple[str, str]]:
    if isinstance(value, dict):
        findings: list[tuple[str, str]] = []
        for key, child in value.items():
            if key in SEMANTIC_REVIEW_FORBIDDEN_KEYS:
                findings.append((path, key))
            findings.extend(_forbidden_semantic_review_keys(child, path=f"{path}.{key}"))
        return findings
    if isinstance(value, list):
        findings = []
        for index, child in enumerate(value):
            findings.extend(_forbidden_semantic_review_keys(child, path=f"{path}[{index}]"))
        return findings
    return []


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


def _looks_like_gpt_oss_wrapped_message(text: str) -> bool:
    channel_index = text.find(GPT_OSS_CHANNEL_MARKER)
    message_index = text.find(GPT_OSS_MESSAGE_MARKER)
    return channel_index == 0 and message_index > channel_index


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
