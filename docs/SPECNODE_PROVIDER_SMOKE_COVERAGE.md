# SpecNode Provider Smoke Coverage

Status: Phase 11 smoke coverage

This document defines the executable smoke coverage for the SpecHarvester to
SpecNode refinement bridge.

The coverage verifies that deterministic candidate artifacts can be converted
into weak-model drafting inputs, passed to a local SpecNode-compatible provider
test double, and validated as untrusted proposal metadata. Ordinary CI coverage
does not call LM Studio, does not execute a real model, and does not apply
generated changes.

## Contract Names

- `SpecNodeProviderSmokeRun`: smoke-run envelope produced by the local harness.
- `SpecHarvesterSpecNodeArtifactBundle`: deterministic candidate artifact
  bundle built from `harvest.json`, `specpm.yaml`, `specs/*.spec.yaml`, and
  optional `public-interface-index.json`.
- `SpecHarvesterRefinePreviewPlan`: compact weak-model input plan containing
  `compactModelInput` sections and prompt budget policy.
- `SpecNodeRefinementPromptContract`: versioned prompt rendering policy for
  target-package intent inference, evidence references, negative claims, and
  confidence calibration.
- `SpecNodeRefinementJob`: typed job passed to a SpecNode-compatible provider
  stub.
- `SpecNodeRefinementResult`: typed provider output containing either
  `candidatePatchProposal` or `rejectionReason`.
- `SpecNodeSemanticReviewJob`: clean-context review job that may be built after
  structural `SpecNodeRefinementResult` validation.
- `SpecNodeSemanticReviewResult`: typed semantic verdict and findings emitted
  by the review-only pass.
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
  -> optional SpecNodeSemanticReviewJob
  -> optional SpecNodeSemanticReviewResult
```

The provider stub is an in-process test double for SpecNode behavior. It is not
an OpenAI-compatible HTTP client and not a direct LM Studio call. Production
ownership remains unchanged: SpecNode owns provider discovery, model execution,
provenance, and usage receipt generation. The separate manual live smoke is a
local opt-in harness for testing provider transport only.
Clean-context semantic review is defined by
[`SPECNODE_SEMANTIC_REVIEW_CONTRACT.md`](SPECNODE_SEMANTIC_REVIEW_CONTRACT.md).
It consumes validated `SpecNodeRefinementResult` data and emits typed
review-only findings.

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

## LM Studio JSON Compatibility

Local probing with LM Studio showed `openai/gpt-oss-20b` is available through
`/v1/models` and `/v1/chat/completions`, but structured output compatibility
requires `response_format.type: json_schema`. The smoke contract must not assume
`response_format.type: json_object`.

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

The base URL must target a local provider host: `localhost`, `127.0.0.1`, or
`::1`.

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
refinement call receives `SpecNodeRetryContext`. A successful run prints a
compact JSON summary with:

- model ID and provider base URL;
- attempt count and attempt statuses;
- review verdict sequence;
- whether each provider call saw retry context;
- token usage totals;
- final refinement and semantic review result digests.

The adapter calls LM Studio for compact JSON signals, then deterministically
wraps those signals into the existing SpecNode protocol objects. This keeps the
smoke focused on provider transport, `gpt-oss` JSON parsing, retry-context
plumbing, and audit validation. It does not ask the model to author the full
audit schema directly.

The live smoke still does not:

- send raw repository source, secrets, provider logs, or arbitrary prompts;
- execute shell commands, package managers, build tools, tests, or network
  probes beyond the configured local provider endpoint;
- apply generated patch proposals;
- commit generated candidate artifacts;
- treat model output as accepted registry truth.

## Non-Goals

The smoke coverage does not:

- implement SpecNode itself;
- call LM Studio or any OpenAI-compatible endpoint during ordinary CI;
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
