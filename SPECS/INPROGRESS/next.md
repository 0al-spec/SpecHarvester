# Next Task: P11-T6 LM Studio JSON Schema Compatibility

**Status:** SELECTED

**Updated:** 2026-05-22

## Description

Capture LM Studio `openai/gpt-oss-20b` runtime compatibility by requiring
OpenAI-compatible `json_schema` response format for structured provider output
and adding a safe parser fallback for `gpt-oss` channel-wrapped JSON returned in
plain text mode.

## Recently Archived

- `P11-T5` Added executable SpecNode provider smoke coverage with deterministic
  artifact bundle assembly, compact `SpecHarvesterRefinePreviewPlan` input,
  local SpecNode-compatible provider-stub validation, structural
  `SpecNodeRefinementResult` checks, and deterministic `provider_unavailable`
  fallback.
- `P11-T4` Defined schema-validated model output for
  `SpecNodeCandidatePatchProposal`, `SpecNodeCandidatePatchOperation`,
  proposal provenance, usage receipts, review notes, and
  `SpecNodeRejectionReason` before any generated change can be applied.
- `P11-T3` Defined the OpenAI-compatible provider adapter boundary for local
  SpecNode execution, including LM Studio discovery, endpoint allowlisting,
  health checks, model listing, timeout, retry, temperature, token-budget
  policy, usage receipts, and authority limits.
- `P11-T2` Defined the deterministic `SpecHarvesterRefinePreviewPlan` contract
  with compact model input sections, artifact digests, prompt-budget controls,
  excluded raw content, and DocC/GitHub documentation contract coverage.
- `P11-T1` Defined the `SpecHarvesterSpecNodeArtifactBundle` and
  `SpecNodeRefinementJob` contract for future SpecNode-assisted candidate
  refinement without granting the model shell, filesystem, raw source, secret,
  or direct mutation authority.

## Parked

- None.

## Newly Observed Smoke Gaps

- LM Studio `openai/gpt-oss-20b` rejects `response_format.type: json_object`
  and accepts `response_format.type: json_schema`.
- In plain text mode, `openai/gpt-oss-20b` may wrap JSON as
  `<|channel|>final <|constrain|>JSON<|message|>{...}`.

## Next Step

Implement `P11-T6` through Flow and PR: document `json_schema` as the preferred
structured-output mode, add deterministic parser fallback for channel-wrapped
JSON, and cover both paths with tests.
