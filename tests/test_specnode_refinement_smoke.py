from __future__ import annotations

import json
import textwrap
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.drafter import DraftOptions, draft_spec_package
from spec_harvester.specnode_refinement import (
    SpecNodeModelJSONParseError,
    SpecNodeProviderUnavailable,
    SpecNodeRefinementSmokeOptions,
    SpecNodeRefinementValidationError,
    SpecNodeSemanticReviewValidationError,
    build_provider_unavailable_result,
    build_refine_preview_plan,
    build_specnode_artifact_bundle,
    build_specnode_refinement_job,
    build_specnode_semantic_review_job,
    canonical_json_sha256_digest,
    parse_specnode_model_json_object,
    run_specnode_refinement_smoke,
    validate_specnode_refinement_result,
    validate_specnode_semantic_review_result,
)


def test_specnode_refinement_smoke_uses_local_provider_with_compact_inputs(
    tmp_path: Path,
) -> None:
    candidate = build_candidate_workspace(tmp_path)
    before_files = candidate_file_snapshot(candidate)
    provider = ScriptedSpecNodeProvider()

    result = run_specnode_refinement_smoke(
        SpecNodeRefinementSmokeOptions(candidate_workspace=candidate, provider=provider)
    )

    assert result["kind"] == "SpecNodeProviderSmokeRun"
    assert result["status"] == "ok"
    assert result["refinementResult"]["result"]["kind"] == "candidatePatchProposal"
    assert result["refinementResult"]["usageReceipt"]["kind"] == "SpecNodeProposalUsageReceipt"
    assert provider.received_job is not None
    assert provider.received_preview_plan is not None
    assert provider.received_preview_plan["compactModelInput"]["harvestSummary"]["kind"] == (
        "SpecHarvesterEvidenceSnapshot"
    )
    assert provider.received_preview_plan["compactModelInput"]["projectProfile"]["languages"]
    assert (
        provider.received_preview_plan["compactModelInput"]["publicInterfaceSummary"]["summary"][
            "symbolCount"
        ]
        > 0
    )
    assert provider.received_preview_plan["excludedContent"] == {
        "rawRepositorySource": "excluded",
        "documentationBodies": "excluded",
        "dependencyDirectories": "excluded",
        "providerLogs": "excluded",
        "secrets": "excluded",
        "arbitraryPrompts": "excluded",
    }

    serialized_plan = json.dumps(provider.received_preview_plan, sort_keys=True)
    assert "class DemoApp" not in serialized_plan
    assert "def route" not in serialized_plan
    assert "SpecNode Smoke Fixture is a web framework" not in serialized_plan
    assert "MIT License" not in serialized_plan
    assert candidate_file_snapshot(candidate) == before_files


def test_specnode_refinement_smoke_returns_deterministic_fallback_without_provider(
    tmp_path: Path,
) -> None:
    candidate = build_candidate_workspace(tmp_path)
    before_files = candidate_file_snapshot(candidate)

    first = run_specnode_refinement_smoke(
        SpecNodeRefinementSmokeOptions(candidate_workspace=candidate)
    )
    second = run_specnode_refinement_smoke(
        SpecNodeRefinementSmokeOptions(candidate_workspace=candidate)
    )

    assert first["status"] == "provider_unavailable"
    assert first["refinementResult"] == second["refinementResult"]
    rejection = first["refinementResult"]["result"]["rejection"]
    assert rejection["kind"] == "SpecNodeRejectionReason"
    assert rejection["code"] == "provider_unavailable"
    assert rejection["usageReceipt"]["providerReceipt"]["status"] == "provider_unavailable"
    assert first["diagnostics"][0]["code"] == "provider_unavailable"
    assert candidate_file_snapshot(candidate) == before_files


def test_specnode_refinement_smoke_converts_provider_unavailable_to_fallback(
    tmp_path: Path,
) -> None:
    candidate = build_candidate_workspace(tmp_path)

    result = run_specnode_refinement_smoke(
        SpecNodeRefinementSmokeOptions(
            candidate_workspace=candidate,
            provider=UnavailableSpecNodeProvider(),
        )
    )

    assert result["status"] == "provider_unavailable"
    assert result["refinementResult"]["result"]["rejection"]["code"] == "provider_unavailable"


def test_specnode_refinement_smoke_supports_absent_public_interface_index(
    tmp_path: Path,
) -> None:
    candidate = build_candidate_workspace(tmp_path)
    (candidate / "public-interface-index.json").unlink()

    result = run_specnode_refinement_smoke(
        SpecNodeRefinementSmokeOptions(candidate_workspace=candidate)
    )

    assert result["status"] == "provider_unavailable"
    compact_input = result["previewPlan"]["compactModelInput"]
    assert compact_input["publicInterfaceSummary"] == {"status": "absent"}


def test_specnode_model_json_parser_accepts_direct_and_gpt_oss_wrapped_objects() -> None:
    direct = parse_specnode_model_json_object(
        '{"kind":"SpecNodeProviderProbe","status":"ok","candidateId":"demo.core"}'
    )
    direct_with_marker_literal = parse_specnode_model_json_object(
        '{"kind":"SpecNodeProviderProbe","note":"literal <|message|> marker"}'
    )
    wrapped = parse_specnode_model_json_object(
        "<|channel|>final <|constrain|>JSON<|message|>"
        '{"kind":"SpecNodeProviderProbe","status":"ok","candidateId":"demo.core"}'
    )

    assert direct == {
        "kind": "SpecNodeProviderProbe",
        "status": "ok",
        "candidateId": "demo.core",
    }
    assert direct_with_marker_literal == {
        "kind": "SpecNodeProviderProbe",
        "note": "literal <|message|> marker",
    }
    assert wrapped == direct


@pytest.mark.parametrize(
    "content",
    [
        "",
        "[]",
        '"scalar"',
        "{} {}",
        "<|channel|>final <|constrain|>JSON<|message|>not-json",
        '<|channel|>final<|message|>{"a":1}<|channel|>analysis<|message|>{"b":2}',
        '<|channel|>final<|message|>[{"a":1}]',
    ],
)
def test_specnode_model_json_parser_rejects_unsafe_or_ambiguous_content(
    content: str,
) -> None:
    with pytest.raises(SpecNodeModelJSONParseError):
        parse_specnode_model_json_object(content)


def test_specnode_refinement_smoke_rejects_unsafe_provider_output(
    tmp_path: Path,
) -> None:
    candidate = build_candidate_workspace(tmp_path)
    before_files = candidate_file_snapshot(candidate)

    with pytest.raises(SpecNodeRefinementValidationError, match="forbidden marker"):
        run_specnode_refinement_smoke(
            SpecNodeRefinementSmokeOptions(
                candidate_workspace=candidate,
                provider=ScriptedSpecNodeProvider(unsafe=True),
            )
        )

    assert candidate_file_snapshot(candidate) == before_files


def test_specnode_refinement_smoke_rejects_missing_candidate_workspace(
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError, match="Candidate workspace does not exist"):
        run_specnode_refinement_smoke(
            SpecNodeRefinementSmokeOptions(candidate_workspace=tmp_path / "missing")
        )


def test_specnode_refinement_validation_rejects_malformed_results(
    tmp_path: Path,
) -> None:
    candidate = build_candidate_workspace(tmp_path)
    bundle = build_specnode_artifact_bundle(candidate)
    preview_plan = build_refine_preview_plan(bundle, candidate)
    job = build_specnode_refinement_job(bundle, preview_plan)
    valid_result = successful_refinement_result(job, preview_plan)
    fallback_result = build_provider_unavailable_result(job, preview_plan)

    cases = [
        malformed_result_case(valid_result, lambda result: result.update({"kind": "WrongKind"})),
        malformed_result_case(
            valid_result,
            lambda result: result.update({"schemaVersion": 2}),
        ),
        malformed_result_case(valid_result, lambda result: result.update({"job": "bad"})),
        malformed_result_case(
            valid_result,
            lambda result: result.update({"usageReceipt": {"kind": "bad"}}),
        ),
        malformed_result_case(valid_result, mutate_usage_receipt_to_remove_required_fields),
        malformed_result_case(valid_result, mutate_usage_receipt_to_break_digest_binding),
        malformed_result_case(valid_result, lambda result: result.update({"result": "bad"})),
        malformed_result_case(
            valid_result,
            lambda result: result.update({"result": {"kind": "unsupported"}}),
        ),
        malformed_result_case(
            valid_result,
            lambda result: result.update({"result": {"kind": "candidatePatchProposal"}}),
        ),
        malformed_result_case(
            fallback_result,
            lambda result: result.update({"result": {"kind": "rejectionReason"}}),
        ),
        malformed_result_case(
            valid_result,
            lambda result: result.update({"reviewNotes": "bad"}),
        ),
    ]

    for malformed in cases:
        with pytest.raises(SpecNodeRefinementValidationError):
            validate_specnode_refinement_result(
                malformed,
                job=job,
                preview_plan=preview_plan,
                bundle=bundle,
            )


def test_specnode_refinement_validation_rejects_malformed_proposals(
    tmp_path: Path,
) -> None:
    candidate = build_candidate_workspace(tmp_path)
    bundle = build_specnode_artifact_bundle(candidate)
    preview_plan = build_refine_preview_plan(bundle, candidate)
    job = build_specnode_refinement_job(bundle, preview_plan)
    valid_result = successful_refinement_result(job, preview_plan)

    def proposal_case(mutator) -> dict[str, Any]:
        result = deepcopy(valid_result)
        mutator(result["result"]["proposal"])
        return result

    cases = [
        proposal_case(lambda proposal: proposal.pop("proposalId")),
        proposal_case(lambda proposal: proposal.update({"kind": "WrongProposal"})),
        proposal_case(lambda proposal: proposal.update({"candidateId": "other.core"})),
        proposal_case(lambda proposal: proposal.update({"candidateVersion": "9.9.9"})),
        proposal_case(lambda proposal: proposal.update({"sourceJobDigest": "sha256:" + "0" * 64})),
        proposal_case(
            lambda proposal: proposal.update({"sourcePreviewPlanDigest": "sha256:" + "0" * 64})
        ),
        proposal_case(lambda proposal: proposal.update({"baseCandidateDigest": "bad"})),
        proposal_case(lambda proposal: proposal.update({"sourceArtifactDigests": []})),
        proposal_case(lambda proposal: proposal.update({"provenance": "bad"})),
        proposal_case(lambda proposal: proposal.update({"validationExpectations": "bad"})),
        proposal_case(lambda proposal: proposal.update({"operations": "bad"})),
        proposal_case(lambda proposal: proposal.update({"operations": ["bad"]})),
        proposal_case(mutate_provenance_to_break_digest_binding),
        proposal_case(mutate_expectations_to_false),
        proposal_case(mutate_operation_to_break_shape),
    ]

    for malformed in cases:
        with pytest.raises(SpecNodeRefinementValidationError):
            validate_specnode_refinement_result(
                malformed,
                job=job,
                preview_plan=preview_plan,
                bundle=bundle,
            )


def test_specnode_refinement_validation_rejects_malformed_rejections(
    tmp_path: Path,
) -> None:
    candidate = build_candidate_workspace(tmp_path)
    bundle = build_specnode_artifact_bundle(candidate)
    preview_plan = build_refine_preview_plan(bundle, candidate)
    job = build_specnode_refinement_job(bundle, preview_plan)
    valid_result = build_provider_unavailable_result(job, preview_plan)

    def rejection_case(mutator) -> dict[str, Any]:
        result = deepcopy(valid_result)
        mutator(result["result"]["rejection"])
        return result

    cases = [
        rejection_case(lambda rejection: rejection.update({"kind": "WrongRejection"})),
        rejection_case(lambda rejection: rejection.update({"code": "run_shell"})),
        rejection_case(
            lambda rejection: rejection.update({"sourceJobDigest": "sha256:" + "0" * 64})
        ),
        rejection_case(
            lambda rejection: rejection.update({"sourcePreviewPlanDigest": "sha256:" + "0" * 64})
        ),
        rejection_case(lambda rejection: rejection.update({"usageReceipt": {"kind": "bad"}})),
        rejection_case(mutate_rejection_usage_receipt_to_break_identity),
        rejection_case(lambda rejection: rejection.update({"evidenceRefs": "bad"})),
    ]

    for malformed in cases:
        with pytest.raises(SpecNodeRefinementValidationError):
            validate_specnode_refinement_result(
                malformed,
                job=job,
                preview_plan=preview_plan,
                bundle=bundle,
            )


def test_specnode_semantic_review_job_uses_clean_context_and_review_only_policy(
    tmp_path: Path,
) -> None:
    candidate = build_candidate_workspace(tmp_path)
    bundle = build_specnode_artifact_bundle(candidate)
    preview_plan = build_refine_preview_plan(bundle, candidate)
    job = build_specnode_refinement_job(bundle, preview_plan)
    refinement_result = successful_refinement_result(job, preview_plan)
    review_job = build_specnode_semantic_review_job(bundle, preview_plan, refinement_result)

    assert review_job["kind"] == "SpecNodeSemanticReviewJob"
    assert review_job["contract"]["kind"] == "SpecNodeSemanticReviewContract"
    assert review_job["contract"]["outputKind"] == "SpecNodeSemanticReviewResult"
    assert review_job["policy"]["candidateMutation"] == "none"
    assert review_job["excludedContent"]["firstPassPromptTranscript"] == "excluded"
    assert review_job["excludedContent"]["chainOfThought"] == "excluded"
    assert review_job["reviewedRefinementResult"]["digest"] == canonical_json_sha256_digest(
        refinement_result
    )
    assert "wrong_package_intent" in review_job["rubric"]["findingCodes"]
    assert "authority_boundary_violation" in review_job["rubric"]["findingCodes"]

    serialized_job = json.dumps(review_job, sort_keys=True)
    assert "class DemoApp" not in serialized_job
    assert "def route" not in serialized_job
    assert "firstPassProviderLogs" in serialized_job


def test_specnode_semantic_review_validation_accepts_typed_findings(
    tmp_path: Path,
) -> None:
    candidate = build_candidate_workspace(tmp_path)
    bundle = build_specnode_artifact_bundle(candidate)
    preview_plan = build_refine_preview_plan(bundle, candidate)
    job = build_specnode_refinement_job(bundle, preview_plan)
    refinement_result = successful_refinement_result(job, preview_plan)
    review_job = build_specnode_semantic_review_job(bundle, preview_plan, refinement_result)

    validate_specnode_semantic_review_result(
        semantic_review_result(review_job, refinement_result, verdict="approve", findings=[]),
        review_job=review_job,
        preview_plan=preview_plan,
        refinement_result=refinement_result,
        bundle=bundle,
    )
    validate_specnode_semantic_review_result(
        semantic_review_result(
            review_job,
            refinement_result,
            verdict="needs_revision",
            findings=[
                semantic_review_finding(
                    code="wrong_package_intent",
                    severity="blocking",
                    evidence_refs=[
                        "public_interface_index",
                        "op-001",
                        "reviewed_refinement_result",
                    ],
                )
            ],
        ),
        review_job=review_job,
        preview_plan=preview_plan,
        refinement_result=refinement_result,
        bundle=bundle,
    )


def test_specnode_semantic_review_validation_rejects_mutating_or_unknown_findings(
    tmp_path: Path,
) -> None:
    candidate = build_candidate_workspace(tmp_path)
    bundle = build_specnode_artifact_bundle(candidate)
    preview_plan = build_refine_preview_plan(bundle, candidate)
    job = build_specnode_refinement_job(bundle, preview_plan)
    refinement_result = successful_refinement_result(job, preview_plan)
    review_job = build_specnode_semantic_review_job(bundle, preview_plan, refinement_result)
    valid_result = semantic_review_result(
        review_job,
        refinement_result,
        verdict="needs_revision",
        findings=[semantic_review_finding()],
    )

    cases = [
        malformed_result_case(valid_result, lambda result: result.update({"operations": []})),
        malformed_result_case(valid_result, lambda result: result.update({"retryDirective": {}})),
        malformed_result_case(
            valid_result,
            lambda result: result["findings"][0].update({"code": "invented_code"}),
        ),
        malformed_result_case(
            valid_result,
            lambda result: result["findings"][0].update({"evidenceRefs": ["unknown"]}),
        ),
        semantic_review_result(
            review_job,
            refinement_result,
            verdict="approve",
            findings=[semantic_review_finding(severity="blocking")],
        ),
        semantic_review_result(
            review_job,
            refinement_result,
            verdict="reject",
            findings=[semantic_review_finding(severity="warning")],
        ),
    ]

    for malformed in cases:
        with pytest.raises(SpecNodeSemanticReviewValidationError):
            validate_specnode_semantic_review_result(
                malformed,
                review_job=review_job,
                preview_plan=preview_plan,
                refinement_result=refinement_result,
                bundle=bundle,
            )


class ScriptedSpecNodeProvider:
    def __init__(self, *, unsafe: bool = False) -> None:
        self.unsafe = unsafe
        self.received_job: dict[str, Any] | None = None
        self.received_preview_plan: dict[str, Any] | None = None

    def refine(
        self,
        *,
        job: dict[str, Any],
        preview_plan: dict[str, Any],
    ) -> dict[str, Any]:
        self.received_job = job
        self.received_preview_plan = preview_plan
        result = successful_refinement_result(job, preview_plan)
        if self.unsafe:
            operation = result["result"]["proposal"]["operations"][0]
            operation["op"] = "shellCommand"
            operation["shellCommand"] = "cat ~/.ssh/id_rsa"
        return result


class UnavailableSpecNodeProvider:
    def refine(
        self,
        *,
        job: dict[str, Any],
        preview_plan: dict[str, Any],
    ) -> dict[str, Any]:
        raise SpecNodeProviderUnavailable("not running")


def malformed_result_case(source: dict[str, Any], mutator) -> dict[str, Any]:
    result = deepcopy(source)
    mutator(result)
    return result


def mutate_usage_receipt_to_remove_required_fields(result: dict[str, Any]) -> None:
    usage_receipt = result["usageReceipt"]
    usage_receipt.pop("jobId")
    usage_receipt.pop("providerReceiptDigest")
    usage_receipt["providerReceipt"].pop("modelId")


def mutate_usage_receipt_to_break_digest_binding(result: dict[str, Any]) -> None:
    usage_receipt = result["usageReceipt"]
    usage_receipt["providerReceiptDigest"] = "sha256:" + "0" * 64
    usage_receipt["responseSha256"] = "bad"
    usage_receipt["providerReceipt"]["responseSha256"] = "bad"
    usage_receipt["proposalId"] = "other-proposal"


def mutate_provenance_to_break_digest_binding(proposal: dict[str, Any]) -> None:
    provenance = proposal["provenance"]
    provenance["kind"] = "WrongProvenance"
    provenance["sourceJobDigest"] = "sha256:" + "0" * 64
    provenance["sourceBundleDigest"] = "sha256:" + "0" * 64
    provenance["sourcePreviewPlanDigest"] = "sha256:" + "0" * 64
    provenance["sourceArtifactDigests"] = []
    provenance["baseCandidateDigest"] = "sha256:" + "0" * 64
    provenance["providerReceiptDigest"] = "bad"
    provenance["redactionPolicy"] = "raw"


def mutate_expectations_to_false(proposal: dict[str, Any]) -> None:
    proposal["validationExpectations"] = {
        "requiresSchemaValidation": False,
        "requiresHumanReview": False,
        "requiresSpecPMValidationAfterApply": False,
    }


def mutate_operation_to_break_shape(proposal: dict[str, Any]) -> None:
    operation = proposal["operations"][0]
    operation["targetFile"] = "../outside.yaml"
    operation["expectedCurrentValueSha256"] = "bad"
    operation["rationale"] = ""
    operation["evidenceRefs"] = ["harvest_snapshot", 1]


def mutate_rejection_usage_receipt_to_break_identity(rejection: dict[str, Any]) -> None:
    rejection["usageReceipt"]["rejectionId"] = "other-rejection"


def successful_refinement_result(
    job: dict[str, Any],
    preview_plan: dict[str, Any],
) -> dict[str, Any]:
    job_digest = canonical_json_sha256_digest(job)
    preview_digest = canonical_json_sha256_digest(preview_plan)
    bundle_digest = preview_plan["sourceBundle"]["digest"]
    response_digest = canonical_json_sha256_digest({"result": "ok"})
    provider_receipt = {
        "kind": "SpecNodeProviderUsageReceipt",
        "providerKind": "openai_compatible",
        "providerName": "scripted_specnode_smoke_provider",
        "baseUrl": "in-process://specnode-smoke",
        "endpoint": "refine",
        "modelId": "weak-local-smoke-model",
        "requestId": "scripted-request",
        "startedAt": "2026-05-22T00:00:00Z",
        "completedAt": "2026-05-22T00:00:00Z",
        "durationMs": 1,
        "status": "ok",
        "attempts": 1,
        "timeoutPolicy": {"totalTimeoutSeconds": 120},
        "retryPolicy": {"maxAttempts": 1},
        "temperature": 0.2,
        "maxOutputTokens": 512,
        "promptBudget": preview_plan["promptBudget"],
        "inputTokens": 128,
        "outputTokens": 64,
        "totalTokens": 192,
        "finishReason": "stop",
        "responseSha256": response_digest,
        "redactionPolicy": "path_digest_and_summary_only",
    }
    provider_receipt_digest = canonical_json_sha256_digest(provider_receipt)
    usage_receipt = {
        "kind": "SpecNodeProposalUsageReceipt",
        "jobId": job["jobId"],
        "proposalId": "proposal-scripted-001",
        "providerReceipt": provider_receipt,
        "providerReceiptDigest": provider_receipt_digest,
        "modelId": "weak-local-smoke-model",
        "inputTokens": 128,
        "outputTokens": 64,
        "totalTokens": 192,
        "finishReason": "stop",
        "attempts": 1,
        "startedAt": "2026-05-22T00:00:00Z",
        "completedAt": "2026-05-22T00:00:00Z",
        "durationMs": 1,
        "timeoutPolicy": {"totalTimeoutSeconds": 120},
        "retryPolicy": {"maxAttempts": 1},
        "temperature": 0.2,
        "maxOutputTokens": 512,
        "promptBudget": preview_plan["promptBudget"],
        "responseSha256": response_digest,
        "redactionPolicy": "path_digest_and_summary_only",
    }
    source_artifacts = preview_plan["artifactDigests"]
    candidate = preview_plan["candidate"]
    base_digest = canonical_json_sha256_digest(candidate)
    return {
        "schemaVersion": 1,
        "kind": "SpecNodeRefinementResult",
        "job": {
            "kind": "SpecNodeRefinementJob",
            "jobId": job["jobId"],
            "digest": job_digest,
        },
        "result": {
            "kind": "candidatePatchProposal",
            "proposal": {
                "kind": "SpecNodeCandidatePatchProposal",
                "proposalId": "proposal-scripted-001",
                "candidateId": candidate["packageId"],
                "candidateVersion": candidate["packageVersion"],
                "baseCandidateDigest": base_digest,
                "sourceJobDigest": job_digest,
                "sourcePreviewPlanDigest": preview_digest,
                "sourceArtifactDigests": source_artifacts,
                "operations": [
                    {
                        "operationId": "op-001",
                        "op": "replace_field",
                        "targetFile": candidate["specPaths"][0],
                        "targetPointer": "/intent/summary",
                        "expectedCurrentValueSha256": canonical_json_sha256_digest(
                            {"current": "summary"}
                        ),
                        "value": "Clarified candidate summary from compact evidence.",
                        "rationale": "Improves review wording using deterministic summaries.",
                        "evidenceRefs": ["harvest_snapshot", "public_interface_index"],
                        "confidence": 0.72,
                    }
                ],
                "provenance": {
                    "kind": "SpecNodeProposalProvenance",
                    "sourceJobDigest": job_digest,
                    "sourceBundleDigest": bundle_digest,
                    "sourcePreviewPlanDigest": preview_digest,
                    "sourceArtifactDigests": source_artifacts,
                    "baseCandidateDigest": base_digest,
                    "providerReceiptDigest": provider_receipt_digest,
                    "modelId": "weak-local-smoke-model",
                    "createdAt": "2026-05-22T00:00:00Z",
                    "policyDigest": canonical_json_sha256_digest(job["policy"]),
                    "promptBudget": preview_plan["promptBudget"],
                    "redactionPolicy": "path_digest_and_summary_only",
                    "schemaVersion": 1,
                },
                "validationExpectations": {
                    "requiresSchemaValidation": True,
                    "requiresHumanReview": True,
                    "requiresSpecPMValidationAfterApply": True,
                },
            },
        },
        "reviewNotes": [
            {
                "noteId": "note-001",
                "severity": "info",
                "message": "Scripted smoke provider returned review-only metadata.",
                "evidenceRefs": ["harvest_snapshot"],
                "operationIds": ["op-001"],
                "confidence": 0.8,
            }
        ],
        "usageReceipt": usage_receipt,
    }


def semantic_review_result(
    review_job: dict[str, Any],
    refinement_result: dict[str, Any],
    *,
    verdict: str,
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "SpecNodeSemanticReviewResult",
        "job": {
            "kind": "SpecNodeSemanticReviewJob",
            "jobId": review_job["jobId"],
            "digest": canonical_json_sha256_digest(review_job),
        },
        "reviewedRefinementResult": {
            "kind": "SpecNodeRefinementResult",
            "digest": canonical_json_sha256_digest(refinement_result),
        },
        "verdict": verdict,
        "findings": findings,
        "summary": "Semantic review completed against clean deterministic context.",
    }


def semantic_review_finding(
    *,
    code: str = "unsupported_capability_claim",
    severity: str = "warning",
    evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "kind": "SpecNodeSemanticReviewFinding",
        "findingId": "finding-001",
        "code": code,
        "severity": severity,
        "message": "The proposal claim needs deterministic evidence before acceptance.",
        "target": {
            "kind": "candidate_patch_operation",
            "operationId": "op-001",
        },
        "evidenceRefs": evidence_refs or ["harvest_snapshot", "op-001"],
    }


def build_candidate_workspace(tmp_path: Path) -> Path:
    inputs = tmp_path / "inputs"
    checkout = tmp_path / "checkout"
    candidate_root = tmp_path / "candidate"
    inputs.mkdir()
    write_fixture(checkout)
    (inputs / "repositories.yml").write_text(
        textwrap.dedent(
            f"""
            repositories:
              - id: specnode-smoke
                repository: https://github.com/example/specnode-smoke
                revision: {"1" * 40}
                checkout: {json.dumps(str(checkout))}
                packageId: specnode_smoke.core
                labels: [synthetic, specnode-smoke]
            """
        ).lstrip(),
        encoding="utf-8",
    )

    collect_batch_snapshots(
        BatchCollectOptions(
            inputs=inputs,
            out=candidate_root,
            emit_interface_indexes=True,
            analyzer_cache_dir=tmp_path / "analyzer-cache",
        )
    )
    candidate = candidate_root / "specnode-smoke"
    draft_spec_package(
        DraftOptions(
            snapshot=candidate,
            out=candidate,
            package_id="specnode_smoke.core",
            name="SpecNode Smoke Fixture",
        )
    )
    return candidate


def write_fixture(root: Path) -> None:
    files = {
        "README.md": textwrap.dedent(
            """
            # SpecNode Smoke Fixture

            SpecNode Smoke Fixture is a web framework with routing, middleware,
            handlers, request context, response objects, JSON, and API contract
            examples for deterministic semantic evidence.
            """
        ),
        "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
        "pyproject.toml": (
            "[project]\n"
            "name = 'specnode-smoke'\n"
            "version = '1.0.0'\n"
            "description = 'Synthetic SpecNode smoke package.'\n"
        ),
        "src/specnode_smoke/__init__.py": ("from .app import DemoApp\n\n__all__ = ['DemoApp']\n"),
        "src/specnode_smoke/app.py": textwrap.dedent(
            """
            class DemoApp:
                def route(self, rule):
                    return rule

                def before_request(self, callback):
                    return callback
            """
        ),
    }
    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.lstrip(), encoding="utf-8")


def candidate_file_snapshot(candidate: Path) -> dict[str, str]:
    return {
        path.relative_to(candidate).as_posix(): path.read_text(encoding="utf-8")
        for path in sorted(candidate.rglob("*"))
        if path.is_file()
    }
