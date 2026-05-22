# SpecNode Refinement Retry Orchestration

This page mirrors the GitHub contract for bounded feedback-driven
SpecNode-assisted refinement retry orchestration.

The controller consumes structurally validated `SpecNodeRefinementResult` data
and clean-context `SpecNodeSemanticReviewResult` findings. It may schedule a
new refinement attempt by converting findings into deterministic
`SpecNodeRetryDirective` data. It cannot mutate candidates, apply patches, call
tools, or let review text become arbitrary prompt text.

## Contract Names

- `SpecNodeRefinementRetryOrchestrationContract`
- `retryOrchestrationContractVersion`
- `SpecNodeRefinementRetryRun`
- `SpecNodeRefinementRetryPolicy`
- `SpecNodeRefinementRetryAttempt`
- `SpecNodeRetryDirectiveSet`
- `SpecNodeRetryDirective`
- `SpecNodeRetryContext`

## Relationship to Existing Contracts

```text
SpecHarvesterSpecNodeArtifactBundle
  -> SpecHarvesterRefinePreviewPlan
  -> SpecNodeRefinementJob
  -> SpecNodeRefinementResult
  -> SpecNodeSemanticReviewJob
  -> SpecNodeSemanticReviewResult
  -> SpecNodeRetryDirectiveSet
  -> optional SpecNodeRetryContext
  -> next SpecNodeRefinementJob
```

`SpecNodeRefinementRetryOrchestrationContract` starts only after
`SpecNodeRefinementResult` structural validation and
`SpecNodeSemanticReviewResult` validation pass. The semantic reviewer emits
findings only; the deterministic controller decides whether to stop, retry, or
stop at the retry cap.

## Retry Policy

`SpecNodeRefinementRetryPolicy` fields include `maxAttempts`, `attemptCount`,
`artifactReuse: same_bundle_and_preview_plan`, and
`retryDirectiveSource: SpecNodeSemanticReviewFinding`.

The implementation default is `maxAttempts: 2`. The hard safety limit is `5`.

Every attempt must reuse the same `sourceBundleDigest`,
`sourcePreviewPlanDigest`, `SpecHarvesterSpecNodeArtifactBundle`,
`SpecHarvesterRefinePreviewPlan`, and `compactModelInput`.

If source artifacts change, the caller must start a new
`SpecNodeRefinementRetryRun` instead of continuing the old run.

## Retry Run Shape

```json
{
  "schemaVersion": 1,
  "kind": "SpecNodeRefinementRetryRun",
  "contract": {
    "kind": "SpecNodeRefinementRetryOrchestrationContract",
    "retryOrchestrationContractVersion": "1.0.0"
  },
  "status": "retry_limit_reached",
  "retryPolicy": {
    "kind": "SpecNodeRefinementRetryPolicy",
    "maxAttempts": 2,
    "attemptCount": 2,
    "artifactReuse": "same_bundle_and_preview_plan",
    "retryDirectiveSource": "SpecNodeSemanticReviewFinding"
  },
  "sourceBundle": {
    "kind": "SpecHarvesterSpecNodeArtifactBundle",
    "digest": "sha256:64-hex-digest"
  },
  "previewPlan": {
    "kind": "SpecHarvesterRefinePreviewPlan",
    "digest": "sha256:64-hex-digest"
  },
  "attempts": [],
  "finalRefinementResultDigest": "sha256:64-hex-digest",
  "finalSemanticReviewResultDigest": "sha256:64-hex-digest"
}
```

Allowed run statuses are `approved`, `retry_scheduled`, and
`retry_limit_reached`.

## Attempt Audit Trail

Each `SpecNodeRefinementRetryAttempt` records `attemptIndex`, `status`,
`sourceBundleDigest`, `sourcePreviewPlanDigest`, refinement job digest and job
ID, refinement result digest, semantic review job digest and job ID, semantic
review result digest and verdict, and `SpecNodeRetryDirectiveSet` digest and
content.

The audit trail is deterministic metadata. It does not contain raw source,
provider logs, first-pass prompt transcripts, chain-of-thought, arbitrary
prompts, or candidate file contents.

## Directive Mapping

The controller maps semantic review finding codes to bounded retry directive
codes:

- `wrong_package_intent` -> `refocus_target_package_intent`
- `unsupported_capability_claim` -> `remove_or_evidence_capability_claim`
- `missing_evidence_reference` -> `add_evidence_reference_or_drop_claim`
- `overconfident_confidence_score` -> `lower_confidence_or_add_evidence`
- `unsafe_negative_claim` -> `remove_unsupported_negative_claim`
- `schema_policy_mismatch` -> `align_with_schema_policy`
- `authority_boundary_violation` -> `remove_authority_request`
- `prompt_contract_violation` -> `restore_prompt_contract_boundary`

`SpecNodeRetryDirective` fields include `directiveId`, `code`,
`sourceFindingId`, `sourceFindingCode`, `sourceFindingSeverity`, `target`,
`evidenceRefs`, and `boundedInstruction`.

`SpecNodeRetryDirectiveSet` also records
`sourceSemanticReviewResultDigest` so every retry directive set is bound to the
exact semantic review result that produced it.

`boundedInstruction` is repository-owned static text. It must not copy the
semantic review finding message into the retry prompt.

## Directive Policy

`SpecNodeRetryDirectiveSet.policy` must include
`rawTextPropagation: forbidden`, `candidateOutputAuthority: proposal_only`, and
`maxDirectives`.

Retry directives must not contain raw repository source, raw documentation
bodies, provider logs, first-pass prompt transcripts, chain-of-thought,
arbitrary prompts, `candidatePatchProposal`, `operations`, `patch`, `patches`,
nested `retryDirective`, `rawUnifiedDiff`, `fullFileReplacement`,
`shellCommand`, `gitCommand`, `networkFetch`, `providerCall`,
`packageManagerCommand`, `testRunnerCommand`, `buildToolCommand`, or direct
file writes.

## Retry Context

When a retry is scheduled, the next `SpecNodeRefinementJob` may include
`SpecNodeRetryContext`:

```json
{
  "kind": "SpecNodeRetryContext",
  "attemptIndex": 1,
  "sourceBundleDigest": "sha256:64-hex-digest",
  "sourcePreviewPlanDigest": "sha256:64-hex-digest",
  "retryDirectiveSetDigest": "sha256:64-hex-digest",
  "retryDirectiveSet": {
    "kind": "SpecNodeRetryDirectiveSet"
  }
}
```

This context is bounded data. It does not expand model authority. The retry job
keeps `candidateMutation: proposal_only`, `modelFilesystemAccess: none`, and
`modelShellAccess: none`.

## Stop Rules

The controller stops when semantic review verdict is `approve`, `maxAttempts`
has been reached, provider output fails structural validation, semantic review
output fails validation, or retry directive validation fails.

`needs_revision` and `reject` verdicts may schedule a retry only when the next
attempt would remain within `maxAttempts`.

## Rejection Conditions

Reject a retry run when run kind or schema version is invalid, contract version
is unsupported, `maxAttempts` is below `1` or above `5`, `attemptCount` exceeds
`maxAttempts`, attempt indexes are missing or non-sequential, any attempt has a
different `sourceBundleDigest` or `sourcePreviewPlanDigest`, final digests do
not match the last attempt, retry directive codes are outside the allowlist,
retry directives lack `sourceFindingId`, known finding code, non-empty evidence
refs, or static `boundedInstruction`, or retry directives contain raw text
propagation, shell/network/tool authority, direct file writes, raw diffs, or
nested retry directives.

## Security Notes

Retry orchestration is deterministic control logic. It is not a trust oracle and
does not make model output authoritative. Structural validation, semantic
review, SpecPM validation, and human review remain required before generated
changes can be accepted.
