# SpecNode Provider Smoke Coverage

This page mirrors the GitHub smoke coverage contract for the SpecHarvester to
SpecNode refinement bridge.

The coverage verifies that deterministic candidate artifacts can become
weak-model drafting inputs, pass through a local SpecNode-compatible provider
test double, and return validated untrusted proposal metadata. It does not call LM Studio,
execute a real model, or apply generated changes.

## Contract Names

- `SpecNodeProviderSmokeRun`
- `SpecHarvesterSpecNodeArtifactBundle`
- `SpecHarvesterRefinePreviewPlan`
- `SpecNodeRefinementJob`
- `SpecNodeRefinementResult`
- `SpecNodeRejectionReason`

## Sequence

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
an OpenAI-compatible HTTP client and not a direct LM Studio call. SpecHarvester does not contact providers;
SpecNode owns provider discovery, model execution, provenance, and usage receipt
generation.

## Compact Input Boundary

`compactModelInput` contains:

- `harvestSummary`
- `projectProfile`
- `publicInterfaceSummary`
- `semanticEvidenceIndex`
- `validationSummaries`
- `draftCandidateMetadata`

Excluded content is explicit:

- `rawRepositorySource: excluded`
- `documentationBodies: excluded`
- `dependencyDirectories: excluded`
- `providerLogs: excluded`
- `secrets: excluded`
- `arbitraryPrompts: excluded`

Weak-model drafting inputs contain bounded summaries, IDs, counts, paths, and
digests rather than raw repository source or raw documentation bodies.

## Provider-Unavailable Fallback

When no local SpecNode-compatible provider is configured, the harness returns a
deterministic `SpecNodeRefinementResult` with `result.kind: rejectionReason` and
`code: provider_unavailable`.

The fallback includes `usageReceipt` and `SpecNodeProviderUsageReceipt` with
status `provider_unavailable`. It does not mutate candidate files and does not
fail deterministic harvesting, drafting, validation, or batch smoke tests.

## Structural Validation

Successful provider output must include:

- `kind: SpecNodeRefinementResult`
- matching `SpecNodeRefinementJob` digest
- `SpecNodeProposalUsageReceipt`
- `SpecNodeCandidatePatchProposal` or `SpecNodeRejectionReason`
- provenance bound to job, bundle, preview plan, provider receipt, and artifact
  digests
- `requiresSchemaValidation: true`
- `requiresHumanReview: true`
- `requiresSpecPMValidationAfterApply: true`

Patch operations are allowed only against `specpm.yaml` and
`specs/*.spec.yaml`.

Rejected operation markers include `rawUnifiedDiff`, `fullFileReplacement`,
`shellCommand`, `gitCommand`, `networkFetch`, `providerCall`,
`packageManagerCommand`, `testRunnerCommand`, `buildToolCommand`, and direct file writes.

## Non-Goals

The smoke coverage does not implement SpecNode, call LM Studio, discover
providers, stream provider logs, run shell commands, read secrets, read raw
repository source outside deterministic artifacts, apply patches, publish, or
promote candidates.

## See Also

- <doc:SpecNodeIntegrationContract>
- <doc:SpecNodeRefinePreviewContract>
- <doc:SpecNodeProviderAdapterContract>
- <doc:SpecNodePatchProposalContract>
