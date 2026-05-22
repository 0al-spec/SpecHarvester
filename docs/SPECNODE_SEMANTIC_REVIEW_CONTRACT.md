# SpecNode Semantic Review Contract

Status: Phase 13 contract

This document defines the clean-context semantic review pass for generated
`SpecNodeRefinementResult` proposals.

The semantic reviewer is a second model pass. It sees only deterministic
evidence, the generated candidate or patch proposal, and a fixed review rubric.
It must emit typed findings. It cannot mutate candidates, emit patch
operations, apply retry directives, or override structural validation.

## Contract Names

- `SpecNodeSemanticReviewContract`: versioned contract for clean-context review.
- `semanticReviewContractVersion`: stable semantic version for the review
  rubric and output boundary.
- `SpecNodeSemanticReviewJob`: deterministic job envelope sent to the reviewer.
- `SpecNodeSemanticReviewRubric`: fixed review rubric embedded in the job.
- `SpecNodeSemanticReviewResult`: schema-bound review output.
- `SpecNodeSemanticReviewFinding`: one typed review finding.
- `SpecNodeSemanticReviewVerdict`: bounded verdict value.

## Relationship to Existing Contracts

Semantic review runs after first-pass structural validation:

```text
SpecHarvesterSpecNodeArtifactBundle
  -> SpecHarvesterRefinePreviewPlan
  -> SpecNodeRefinementPromptContract
  -> SpecNodeRefinementJob
  -> SpecNodeRefinementResult
  -> SpecHarvester structural validation
  -> SpecNodeSemanticReviewJob
  -> SpecNodeSemanticReviewResult
  -> human review
  -> optional retry orchestration
```

`SpecNodeSemanticReviewContract` does not replace
[`SPECNODE_PATCH_PROPOSAL_CONTRACT.md`](SPECNODE_PATCH_PROPOSAL_CONTRACT.md).
The patch proposal contract proves structural safety. Semantic review checks
whether the structurally valid proposal is meaningful for the target package.

`SpecNodeSemanticReviewContract` also does not replace
[`SPECNODE_REFINEMENT_PROMPT_CONTRACT.md`](SPECNODE_REFINEMENT_PROMPT_CONTRACT.md).
The first-pass prompt produces `SpecNodeRefinementResult`. The second pass
reviews that result without seeing the first-pass prompt transcript.

## Clean Context

`SpecNodeSemanticReviewJob` may include only:

- `SpecHarvesterSpecNodeArtifactBundle` digest and artifact digests;
- `SpecHarvesterRefinePreviewPlan` digest;
- `compactModelInput` from the preview plan;
- candidate metadata from the preview plan;
- the reviewed `SpecNodeRefinementResult` digest and generated proposal or
  rejection content;
- fixed `SpecNodeSemanticReviewRubric`;
- clean-context policy and excluded-content declarations.

The job must exclude:

- `firstPassPromptTranscript: excluded`;
- `chainOfThought: excluded`;
- `firstPassProviderLogs: excluded`;
- `providerLogs: excluded`;
- `rawRepositorySource: excluded`;
- `documentationBodies: excluded`;
- `dependencyDirectories: excluded`;
- `secrets: excluded`;
- `arbitraryPrompts: excluded`;
- `retryDirectives: excluded`.

The reviewer must not receive raw source files, raw documentation bodies,
provider logs, chain-of-thought, authentication material, package manager
output, or arbitrary user prompts.

The review policy is stricter than first-pass proposal generation:
`candidateMutation: none`.

## Review Job Shape

```json
{
  "schemaVersion": 1,
  "kind": "SpecNodeSemanticReviewJob",
  "jobId": "specnode-semantic-review-0123456789abcdef",
  "contract": {
    "kind": "SpecNodeSemanticReviewContract",
    "semanticReviewContractVersion": "1.0.0",
    "outputKind": "SpecNodeSemanticReviewResult"
  },
  "sourceBundle": {
    "kind": "SpecHarvesterSpecNodeArtifactBundle",
    "digest": "sha256:64-hex-digest",
    "artifactDigests": []
  },
  "previewPlan": {
    "kind": "SpecHarvesterRefinePreviewPlan",
    "digest": "sha256:64-hex-digest",
    "compactModelInput": {},
    "candidate": {}
  },
  "reviewedRefinementResult": {
    "kind": "SpecNodeReviewedRefinementResult",
    "digest": "sha256:64-hex-digest",
    "result": {
      "kind": "candidatePatchProposal"
    }
  },
  "policy": {
    "modelFilesystemAccess": "none",
    "modelShellAccess": "none",
    "modelNetworkAccess": "provider_only",
    "allowedTools": [],
    "rawSourceAccess": "none",
    "secretAccess": "none",
    "candidateMutation": "none"
  },
  "excludedContent": {
    "firstPassPromptTranscript": "excluded",
    "chainOfThought": "excluded",
    "providerLogs": "excluded",
    "rawRepositorySource": "excluded",
    "arbitraryPrompts": "excluded"
  },
  "rubric": {
    "kind": "SpecNodeSemanticReviewRubric",
    "verdicts": ["approve", "needs_revision", "reject"],
    "findingCodes": ["wrong_package_intent"]
  },
  "requestedOutputs": ["verdict", "findings", "summary"]
}
```

## Output Contract

The reviewer must return one `SpecNodeSemanticReviewResult` using
`response_format.type: json_schema` when the provider supports strict schema
mode. `response_format.type: json_object` is only an explicit fallback and must
still be parsed as exactly one JSON object.

```json
{
  "schemaVersion": 1,
  "kind": "SpecNodeSemanticReviewResult",
  "job": {
    "kind": "SpecNodeSemanticReviewJob",
    "jobId": "specnode-semantic-review-0123456789abcdef",
    "digest": "sha256:64-hex-digest"
  },
  "reviewedRefinementResult": {
    "kind": "SpecNodeRefinementResult",
    "digest": "sha256:64-hex-digest"
  },
  "verdict": "needs_revision",
  "findings": [
    {
      "kind": "SpecNodeSemanticReviewFinding",
      "findingId": "finding-001",
      "code": "wrong_package_intent",
      "severity": "blocking",
      "message": "The proposal describes SpecPM generation instead of the target package.",
      "target": {
        "kind": "candidate_patch_operation",
        "operationId": "op-001"
      },
      "evidenceRefs": ["public_interface_index", "op-001", "reviewed_refinement_result"]
    }
  ],
  "summary": "The proposal needs revision before human review."
}
```

Allowed verdicts:

- `approve`
- `needs_revision`
- `reject`

Allowed severities:

- `info`
- `warning`
- `blocking`

`approve` cannot contain blocking findings. `needs_revision` and `reject` must
contain at least one finding. `reject` must contain at least one blocking
finding.

## Finding Taxonomy

Allowed `SpecNodeSemanticReviewFinding.code` values:

- `wrong_package_intent`: the proposal describes the generator, SpecPM, or the
  refinement task instead of target package behavior.
- `unsupported_capability_claim`: a capability, interface, or intent claim is
  not supported by deterministic evidence.
- `missing_evidence_reference`: a claim lacks a known artifact ID, evidence ID,
  operation ID, or reviewed result reference.
- `overconfident_confidence_score`: confidence exceeds deterministic evidence
  coverage.
- `unsafe_negative_claim`: the proposal claims absence or non-support from
  missing evidence alone.
- `schema_policy_mismatch`: the proposal conflicts with schema, SpecPM, or
  validation policy.
- `authority_boundary_violation`: the proposal asks for shell commands, direct
  file writes, provider calls, network fetches, package manager commands, test
  runner commands, or build tool commands.
- `prompt_contract_violation`: the proposal violates
  `SpecNodeRefinementPromptContract`, including task self-description such as
  `generate_specpm`.

## Evidence Reference Rules

Every finding must include non-empty `evidenceRefs`.

Allowed references are:

- artifact IDs from `SpecHarvesterSpecNodeArtifactBundle`, such as
  `harvest_snapshot`, `spec_package_manifest`, `boundary_spec`, and
  `public_interface_index`;
- deterministic preview-plan sections such as `compact_model_input`,
  `harvest_summary`, `project_profile`, `public_interface_summary`,
  `semantic_evidence_index`, `validation_summaries`, and
  `draft_candidate_metadata`;
- semantic evidence IDs from `semanticEvidenceIndex`;
- operation IDs, proposal IDs, or rejection IDs in the reviewed
  `SpecNodeRefinementResult`;
- `reviewed_refinement_result` or `refinement_result`.

Unknown IDs, collapsed ranges, invented evidence references, raw source line
claims, and references to provider logs must be rejected.

## Mutation Boundary

`SpecNodeSemanticReviewResult` is review-only metadata.

It must not contain:

- `candidatePatchProposal`;
- `proposal`;
- `operations`;
- `patch` or `patches`;
- `retryDirective` or `retryDirectives`;
- `rawUnifiedDiff`;
- `fullFileReplacement`;
- `shellCommand`;
- `gitCommand`;
- `networkFetch`;
- `providerCall`;
- `packageManagerCommand`;
- `testRunnerCommand`;
- `buildToolCommand`;
- direct file writes;
- any instruction to apply, publish, merge, or mutate candidate files.

Follow-up retry orchestration belongs to a later bounded controller and must
consume findings as data. The semantic reviewer itself cannot request a retry.

## Rejection Conditions

SpecHarvester must reject semantic review output when:

- output is not `SpecNodeSemanticReviewResult`;
- schema version is unsupported;
- job digest or reviewed refinement result digest does not match;
- verdict is outside the allowed set;
- findings are missing for `needs_revision` or `reject`;
- `approve` contains blocking findings;
- `reject` lacks a blocking finding;
- any finding code or severity is unknown;
- any finding lacks a non-empty message or known evidence reference;
- output contains mutation, patch, retry, shell, network, or direct file-write
  fields.

## Security Notes

Semantic review is a weak-model quality gate, not a trust oracle. Its output is
untrusted metadata. Structural validation, SpecPM validation, and human review
remain mandatory before any generated edit can be accepted.
