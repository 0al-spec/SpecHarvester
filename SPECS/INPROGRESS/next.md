# Next Task: P13-T1 SpecNode Refinement Prompt Contract

**Status:** READY

**Updated:** 2026-05-22

## Description

The next recommended task is `P13-T1`: define a versioned SpecNode refinement
prompt contract so model-facing prompt templates become repository-owned,
reviewable artifacts instead of ad-hoc runtime wording.

This should preserve the existing SpecNode trust boundary: prompts consume only
bounded deterministic `compactModelInput`, require schema-bound output, enforce
evidence-reference rules, and calibrate confidence without granting model output
registry authority.

## Recently Archived

- `P11-T6` Captured LM Studio `openai/gpt-oss-20b` compatibility by documenting
  `response_format.type: json_schema` as the preferred structured-output mode,
  avoiding assumptions about `json_object`, and adding strict parser fallback
  for direct JSON object content and `gpt-oss` channel-wrapped JSON.
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

## Parked

- None.

## Newly Observed Smoke Gaps

- Live LM Studio probing showed `openai/gpt-oss-20b` can follow
  `json_schema`, but semantic quality is prompt-sensitive: a weak prompt can
  make the model describe SpecPM generation instead of the target package.

## Next Step

Run Flow for `P13-T1`, then follow with `P13-T2` semantic review and `P13-T3`
feedback-driven retry orchestration.
