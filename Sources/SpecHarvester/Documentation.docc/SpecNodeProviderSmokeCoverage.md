# SpecNode Provider Smoke Coverage

This page mirrors the GitHub smoke coverage contract for the SpecHarvester to
SpecNode refinement bridge.

The coverage verifies that deterministic candidate artifacts can become
weak-model drafting inputs, pass through a local SpecNode-compatible provider
test double, and return validated untrusted proposal metadata. Ordinary CI
coverage does not call LM Studio, execute a real model, or apply generated
changes.

## Contract Names

- `SpecNodeProviderSmokeRun`
- `SpecHarvesterSpecNodeArtifactBundle`
- `SpecHarvesterRefinePreviewPlan`
- `SpecNodeRefinementPromptContract`
- `SpecNodeRefinementJob`
- `SpecNodeRefinementResult`
- `SpecNodeSemanticReviewJob`
- `SpecNodeSemanticReviewResult`
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
  -> optional SpecNodeSemanticReviewJob
  -> optional SpecNodeSemanticReviewResult
```

The provider stub is an in-process test double for SpecNode behavior. It is not
an OpenAI-compatible HTTP client and not a direct LM Studio call. Production
ownership remains unchanged: SpecNode owns provider discovery, model execution,
provenance, and usage receipt generation. The separate manual live smoke is a
local opt-in harness for testing provider transport only.

Prompt rendering policy is defined by <doc:SpecNodeRefinementPromptContract>.
That contract covers target-package intent inference, evidence references,
negative claims, and confidence calibration.
Clean-context semantic review is defined by
<doc:SpecNodeSemanticReviewContract>. It consumes validated
`SpecNodeRefinementResult` data and emits typed review-only findings.

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

## LM Studio JSON Compatibility

Local probing with LM Studio showed `openai/gpt-oss-20b` is available through
`/v1/models` and `/v1/chat/completions`, but structured output compatibility
requires `response_format.type: json_schema`. The smoke contract must not
assume `response_format.type: json_object`.

The smoke helper `parse_specnode_model_json_object` accepts direct JSON object
content and the observed text-mode `gpt-oss` channel wrapper:

```text
<|channel|>final <|constrain|>JSON<|message|>{"kind":"SpecNodeProviderProbe"}
```

The parser rejects empty content, arrays, scalar JSON, multiple object payloads,
malformed wrappers, and trailing non-JSON text. Parsed content is still only
provider output; structural `SpecNodeRefinementResult` validation and human
review remain required.

## Manual LM Studio Live Retry Smoke

`scripts/specnode_live_retry_smoke.py` provides an opt-in live smoke for a local
OpenAI-compatible provider such as LM Studio. It is intentionally not part of
ordinary CI because CI must not depend on developer-local model infrastructure.

Required environment for manual runs:

```bash
SPECHARVESTER_LM_STUDIO_BASE_URL=http://127.0.0.1:1234
SPECHARVESTER_SPECNODE_MODEL=openai/gpt-oss-20b
```

Run the standalone script:

```bash
PYTHONPATH=src \
SPECHARVESTER_LM_STUDIO_BASE_URL=http://127.0.0.1:1234 \
SPECHARVESTER_SPECNODE_MODEL=openai/gpt-oss-20b \
python scripts/specnode_live_retry_smoke.py
```

Run the env-gated pytest path:

```bash
PYTHONPATH=src \
SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE=1 \
SPECHARVESTER_LM_STUDIO_BASE_URL=http://127.0.0.1:1234 \
SPECHARVESTER_SPECNODE_MODEL=openai/gpt-oss-20b \
python -m pytest tests/test_specnode_live_retry_smoke.py -q
```

The live smoke uses the existing
`run_specnode_refinement_retry_orchestration(...)` controller. The first
semantic review pass intentionally emits `needs_revision`, the controller turns
that finding into a bounded `SpecNodeRetryDirectiveSet`, and the second
refinement call receives `SpecNodeRetryContext`.

A successful run prints a compact JSON summary with model ID, provider base URL,
attempt count, attempt statuses, review verdict sequence, retry context
presence, token usage totals, and final result digests.

The adapter calls LM Studio for compact JSON signals, then deterministically
wraps those signals into existing SpecNode protocol objects. This keeps the
smoke focused on provider transport, `gpt-oss` JSON parsing,
`SpecNodeRetryContext` plumbing, and audit validation.

The live smoke still does not send raw repository source, secrets, provider
logs, arbitrary prompts, shell commands, package managers, build tools, test
runners, generated candidate artifacts, or accepted registry truth.

## Non-Goals

The ordinary CI smoke coverage does not implement SpecNode, call LM Studio,
discover providers, stream provider logs, run shell commands, read secrets, read
raw repository source outside deterministic artifacts, apply patches, publish,
or promote candidates.

## See Also

- <doc:SpecNodeIntegrationContract>
- <doc:SpecNodeRefinePreviewContract>
- <doc:SpecNodeProviderAdapterContract>
- <doc:SpecNodePatchProposalContract>
