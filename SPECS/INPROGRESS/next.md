# Next Task: P51-T5 Larger Curated Corpus AI-Enabled Proposal-Only Gate

**Status:** Selected
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T5`
**Last Archived:** `P51-T4` Larger Curated Corpus Static-Only Gate
**Depends On:** `P51-T4` Larger Curated Corpus Static-Only Gate

## Goal

Run the larger curated corpus AI-enabled proposal-only gate after the P51-T4
static-only gate passed for all 12 selected sources.

## Context

P51-T4 processed all 12 selected sources from the P51 manifest in static-only
mode:

```text
inputs/p51-larger-curated-corpus/repositories.yml
```

The static-only gate fixture is:

```text
tests/fixtures/larger_curated_corpus_static_only_gate/p51-t4-larger-curated-corpus-static-only-gate.example.json
```

P51-T4 passed with 12 processed repositories, 0 failed repositories, 15 preview
candidates, 3 relation proposals, 0 AI proposals, and 0 adapter sidecars.

## Scope

- Run the AI-enabled larger curated corpus gate over the same 12 selected
  sources.
- Preserve proposal-only AI draft and enrichment outputs.
- Record local provider metadata, model identity, processed/failed counts,
  warnings, diagnostics, and per-source AI proposal state.
- Preserve raw prompt, raw provider response, secret, and chain-of-thought
  non-persistence.
- Carry `xyflow.operator_checkout_origin_fork_mismatch` and
  `docc2context.source_checkout_had_untracked_doccarchive` forward as review
  evidence.
- Decide whether P51-T6 output triage can proceed.

## Boundaries

- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat static output, readiness output, AI output, rerun output,
  planning output, or adapter output as registry truth.
- Do not persist raw prompts.
- Do not persist raw provider responses.
- Do not persist secrets.
- Do not persist chain-of-thought.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
