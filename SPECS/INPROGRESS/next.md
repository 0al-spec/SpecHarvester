# Next Task: P52-T1 Controlled 50-100 Repository Corpus Plan

**Status:** Selected
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Depends On:** `P51-T8` Larger Curated Corpus Exit Decision

## Objective

Create the Phase 52 planning contract for a controlled 50-100 repository
corpus. The plan will define the staged rollout, Codex Spark agent boundary,
calibration gates, source-selection policy, quality metrics, and follow-up
tasks before any repository is acquired or processed.

## Source Evidence

P52-T1 takes its planning authority from the completed P51-T8 fixture:

```text
tests/fixtures/larger_curated_corpus_exit_decision/p51-t8-larger-curated-corpus-exit-decision.example.json
```

P51-T8 is author-review evidence ready, but it recorded
`furtherExpansionApproved: false` and `registryPromotionAllowed: false`.
P52-T1 may author a new controlled planning phase; it may not interpret P51-T8
as authorization to run a corpus batch.

## Boundaries

- Do not clone or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested code, adapters, Codex, or AI.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat static, AI, AI-enriched, planning, triage, handoff, or adapter
  output as registry truth.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
