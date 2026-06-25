# P51-T5 Larger Curated Corpus AI-Enabled Proposal-Only Gate

**Status:** Planned
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T5`
**Created:** 2026-06-25T14:50:36+03:00
**Depends On:** `P51-T4` Larger Curated Corpus Static-Only Gate
**Reasoning Effort:** medium

## Goal

Run the larger curated corpus AI-enabled proposal-only gate over the same 12
selected P51 sources after the P51-T4 static-only gate passed, and record
durable evidence that decides whether P51-T6 output triage can proceed.

## Context

P51-T4 processed all 12 repositories from the P51 source manifest in
static-only mode:

```text
inputs/p51-larger-curated-corpus/repositories.yml
```

The static-only gate passed with 12 processed repositories, 0 failed
repositories, 15 preview candidates, 3 relation proposals, 0 AI proposals, and
0 adapter sidecars.

P51-T5 is the first AI-enabled gate for the larger curated corpus. It may use
the operator's local LM Studio/OpenAI-compatible endpoint, but all model output
must remain proposal-only review evidence.

## Deliverables

- Real AI-enabled `autonomous-candidate-batch` output under a timestamped
  `/tmp` run root.
- Machine-readable P51-T5 AI-enabled gate fixture under
  `tests/fixtures/larger_curated_corpus_ai_enabled_gate/`.
- GitHub and DocC documentation explaining run inputs, provider metadata,
  model identity, processed/failed counts, warnings, diagnostics, proposal
  counts, caveats, non-persistence boundaries, and next gate.
- Contract tests proving fixture identity, P51-T4 static gate linkage, source
  manifest linkage, batch report digest, provider metadata, proposal-only
  authority, raw prompt/response/secret/chain-of-thought non-persistence,
  per-source AI proposal state, caveat carry-forward, and current next-task
  pointer.
- A validation report recording exact commands and results.

## Acceptance Criteria

- The run consumes `inputs/p51-larger-curated-corpus/repositories.yml`.
- The run uses AI-enabled `autonomous-candidate-batch` with
  `--repository-profile-selection auto`, local LM Studio provider metadata, the
  selected model id, `--json-repair-max-attempts 1`, and explicit
  `--apply-ai-enrichment`.
- The fixture records processed, failed, preflight, candidate, relation,
  warning, repository-profile, AI draft, AI enrichment, AI-enriched preview,
  token, and quality-gate counts for all 12 selected repositories.
- AI draft and enrichment output remains proposal-only review evidence and does
  not become registry truth.
- Raw prompts, raw provider responses, secrets, and chain-of-thought are not
  persisted.
- Trusted local adapter execution remains disabled and adapter sidecars do not
  become authority.
- `xyflow.partial_public_interface_index`,
  `xyflow.operator_checkout_origin_fork_mismatch`, and
  `docc2context.source_checkout_had_untracked_doccarchive` are carried forward
  as review evidence.
- If the AI-enabled batch passes with no failed repositories, the fixture marks
  P51-T6 output triage as allowed.
- `SPECS/INPROGRESS/next.md` selects `P51-T6` after archival.

## Non-Goals

- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat static output, readiness output, AI output, rerun output,
  planning output, enriched preview output, or adapter output as registry truth.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
- Do not substitute a smaller targeted run for the 12-source larger curated
  corpus gate.

## Validation Plan

- Parse the larger curated corpus source manifest through
  `spec_harvester source-manifests`.
- Verify the local LM Studio/OpenAI-compatible endpoint is reachable before the
  batch run.
- Run AI-enabled `autonomous-candidate-batch` with local provider settings,
  `--json-repair-max-attempts 1`, `--apply-ai-enrichment`, and
  `--repository-profile-selection auto`.
- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for P51-T5 and linked P51 artifacts.
- Run project quality gates from `.flow/params.yaml`.
