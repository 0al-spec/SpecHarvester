# SpecNode Provider Smoke Coverage

Status: Phase 11 smoke coverage

This document defines the executable smoke coverage for the SpecHarvester to
SpecNode refinement bridge.

The coverage verifies that deterministic candidate artifacts can be converted
into weak-model drafting inputs, passed to a local SpecNode-compatible provider
test double, and validated as untrusted proposal metadata. It does not call LM Studio,
does not execute a real model, and does not apply generated changes.

## Contract Names

- `SpecNodeProviderSmokeRun`: smoke-run envelope produced by the local harness.
- `SpecHarvesterSpecNodeArtifactBundle`: deterministic candidate artifact
  bundle built from `harvest.json`, `specpm.yaml`, `specs/*.spec.yaml`, and
  optional `public-interface-index.json`.
- `SpecHarvesterRefinePreviewPlan`: compact weak-model input plan containing
  `compactModelInput` sections and prompt budget policy.
- `SpecNodeRefinementJob`: typed job passed to a SpecNode-compatible provider
  stub.
- `SpecNodeRefinementResult`: typed provider output containing either
  `candidatePatchProposal` or `rejectionReason`.
- `SpecNodeRejectionReason`: deterministic fallback when no provider is
  configured.

## Smoke Sequence

```text
candidate workspace
  -> SpecHarvesterSpecNodeArtifactBundle
  -> SpecHarvesterRefinePreviewPlan
  -> SpecNodeRefinementJob
  -> local SpecNode-compatible provider stub
  -> SpecNodeRefinementResult
  -> structural validation before apply
```

The provider stub is an in-process test double for SpecNode behavior. It is not
an OpenAI-compatible HTTP client and not a direct LM Studio call. Production
ownership remains unchanged: SpecHarvester does not contact providers;
SpecNode owns provider discovery, model execution, provenance, and usage
receipt generation.

## Compact Input Boundary

The smoke harness builds `compactModelInput` from deterministic artifacts:

- `harvestSummary`
- `projectProfile`
- `publicInterfaceSummary`
- `semanticEvidenceIndex`
- `validationSummaries`
- `draftCandidateMetadata`

The plan must declare the same excluded-content boundary as the
`refine-preview` contract:

- `rawRepositorySource: excluded`
- `documentationBodies: excluded`
- `dependencyDirectories: excluded`
- `providerLogs: excluded`
- `secrets: excluded`
- `arbitraryPrompts: excluded`

These fields are tested so weak-model drafting inputs contain bounded summaries,
IDs, counts, paths, and digests rather than raw repository source or raw
documentation bodies.

## Provider-Unavailable Fallback

Provider availability is optional. When no local SpecNode-compatible provider is
configured, the harness returns a deterministic `SpecNodeRefinementResult` with
`result.kind: rejectionReason` and `code: provider_unavailable`.

The fallback includes a `usageReceipt` and a `SpecNodeProviderUsageReceipt`
whose status is `provider_unavailable`. It does not mutate candidate files and
does not fail deterministic harvesting, drafting, validation, or batch smoke
tests.

## Structural Validation

Successful provider output must pass structural validation before it can be
shown for human review.

The validator requires:

- `kind: SpecNodeRefinementResult`
- matching `SpecNodeRefinementJob` digest
- `SpecNodeProposalUsageReceipt`
- proposal or rejection, but not both
- `SpecNodeCandidatePatchProposal` provenance bound to job, bundle, preview
  plan, provider receipt, and artifact digests
- `requiresSchemaValidation: true`
- `requiresHumanReview: true`
- `requiresSpecPMValidationAfterApply: true`

Patch operations are allowed only for metadata edits against `specpm.yaml` and
`specs/*.spec.yaml`.

Rejected operation markers include:

- `rawUnifiedDiff`
- `fullFileReplacement`
- `shellCommand`
- `gitCommand`
- `networkFetch`
- `providerCall`
- `packageManagerCommand`
- `testRunnerCommand`
- `buildToolCommand`
- direct file writes

This keeps the smoke layer aligned with the patch proposal contract: model
output is untrusted proposal metadata, not accepted registry truth.

## Non-Goals

The smoke coverage does not:

- implement SpecNode itself;
- call LM Studio or any OpenAI-compatible endpoint;
- discover providers;
- stream prompts or provider logs;
- run shell commands;
- read secrets;
- read raw repository source outside deterministic artifacts;
- apply patches;
- publish or promote candidates.

## Review Rule

A passing `SpecNodeProviderSmokeRun` proves the bridge contracts compose under a
local provider test double and that the provider-unavailable fallback is safe.
It does not prove model quality. Human review and SpecPM validation remain
required after any future accepted edit.
