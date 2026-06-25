# Next Task: P51-T4 Larger Curated Corpus Static-Only Gate

**Status:** Selected
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T4`
**Last Archived:** `P51-T3` Larger Curated Corpus Checkout Readiness Gate
**Depends On:** `P51-T3` Larger Curated Corpus Checkout Readiness Gate

## Goal

Run the larger curated corpus static-only gate after checkout readiness has
passed for all 12 selected sources.

## Context

P51-T3 verified that all 12 selected sources are present and revision-matched
against the P51-T2 manifest:

```text
inputs/p51-larger-curated-corpus/repositories.yml
```

The readiness fixture is:

```text
tests/fixtures/larger_curated_corpus_checkout_readiness/p51-t3-larger-curated-corpus-checkout-readiness.example.json
```

P51-T3 allowed the P51-T4 static-only gate.
P51-T5 AI-enabled proposal-only gate remains blocked until P51-T4 records
passing static-only evidence.

## Scope

- Run the static-only larger curated corpus gate over the 12 selected sources.
- Preserve deterministic evidence, preflight counts, diagnostics, and per-source
  static output.
- Carry `xyflow.operator_checkout_origin_fork_mismatch` and
  `docc2context.source_checkout_had_untracked_doccarchive` forward as review
  evidence.
- Record whether the static-only gate passed before P51-T5 can run AI.
- Keep all static output proposal/review evidence only.

## Boundaries

- Do not run AI in P51-T4.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat static output, readiness output, AI output, rerun output,
  planning output, or adapter output as registry truth.
