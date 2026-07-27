# P53-T1 Mass Corpus Operating Plan

**Status:** Planned  
**Phase:** Phase 53. Mass Popular Repository Parsing and Candidate Production  
**Task:** `P53-T1`  
**Depends On:** `P52-T9` Phase 52 exit decision

## Objective

Define the immutable, machine-readable operating contract for processing 100
new operator-curated popular repositories as four sequential waves of 25. The
only AI worker named by the campaign is `gpt-5.3-codex-spark`, invoked through
the existing read-only `codex exec` external-model-output boundary. This task
defines planning evidence only; it does not acquire sources or invoke the
worker.

## Acceptance Criteria

- A durable `SpecHarvesterMassRepositoryCampaignPlan` fixture links to the
  digest-bound P52-T9 decision and records a 100-source, four-wave scope.
- The fixture makes `gpt-5.3-codex-spark` the sole worker, with `codex_exec`
  invocation, schema-validated proposal-only output, and no LM Studio path.
- It fixes concurrency at two workers initially, requires one classified retry
  at most, and defines per-repository, per-wave, and campaign token/time caps.
- It records immutable input identity, atomic checkpoint, idempotent-resume,
  receipt, privacy, stop-policy, human-review, and non-authority contracts.
- GitHub and DocC operator documents explain the campaign without implying an
  approved checkout, static run, AI call, package acceptance, or registry
  promotion.
- Documentation-contract tests validate fixture identity, source linkage,
  worker selection, sequencing, thresholds, persistence, and boundaries.

## Test-First Plan

1. Add a failing documentation-contract test for the fixture and public docs,
   including `gpt-5.3-codex-spark`, four exact wave ranges, and the three
   sequential scale-out decisions.
2. Add the minimal JSON fixture and public documentation required by that test.
3. Run focused contract tests, then the configured Python, lint, formatting,
   coverage, Swift, workplan-summary, and whitespace gates.

## Implementation Plan

1. Create the durable fixture and link it to the P52-T9 digest and selected
   decision without treating that decision as corpus execution approval.
2. Document the worker policy, bounded receipts, budgets, stop conditions,
   resume semantics, and proposal-only authority boundary in GitHub and DocC
   documentation.
3. Update documentation indexes and roadmap, then advance the next-task
   pointer to `P53-T2` after the plan is validated and archived.

## Constraints And Non-Goals

- Do not create, restore, clone, fetch, or modify any repository checkout.
- Do not invoke Codex, LM Studio, adapters, package managers, or harvested
  code; do not persist raw prompts, raw model responses, session state,
  secrets, stdout/stderr, or chain-of-thought.
- Do not accept packages or relations, publish registry metadata, seed
  baselines, remove `preview_only`, or treat planning/static/AI output as
  registry truth.
- P53-T2 implements orchestration. P53-T3 selects sources. P53-T4 through
  P53-T15 execute and evaluate the campaign; none are performed here.

## Notes

The campaign may progress only as `P53-T5 -> P53-T6 -> P53-T7 -> P53-T8 ->
P53-T9 -> P53-T10 -> P53-T11 -> P53-T12 -> P53-T13 -> P53-T14 -> P53-T15`.
Each human-review decision unlocks only the immediately following wave.
