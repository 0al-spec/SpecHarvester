# Next Task: P51-T3 Larger Curated Corpus Checkout Readiness Gate

**Status:** Selected
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T3`
**Last Archived:** `P51-T2` Larger Curated Corpus Source Plan and Manifest Criteria
**Depends On:** `P51-T2` Larger Curated Corpus Source Plan and Manifest Criteria

## Goal

Run the larger curated corpus checkout readiness gate for the 12 selected
P51-T2 sources before any static-only or AI-enabled corpus run.

## Context

P51-T2 authored the source plan and manifest criteria for the larger curated
corpus. The selected manifest is:

```text
inputs/p51-larger-curated-corpus/repositories.yml
```

The source-plan fixture is:

```text
tests/fixtures/larger_curated_corpus_source_plan/p51-t2-larger-curated-corpus-source-plan.example.json
```

P51-T2 did not verify checkout readiness and did not approve execution.
P51-T3 must verify every selected source has an operator-provided pinned local
checkout before the P51-T4 static-only gate can run.

## Scope

- Parse the P51-T2 source manifest.
- Resolve each operator-provided pinned local checkout path without clone or
  fetch.
- Compare each observed HEAD against the pinned revision from the manifest.
- Record readiness status for all 12 selected P51-T2 sources.
- Record any `missing_pinned_local_checkout`, `checkout_revision_mismatch`, or
  `clone_or_fetch_required` blockers.
- Carry P50 warnings, xyflow caveats, and docc2context checkout caveats forward
  as review evidence.
- Decide whether the P51-T4 static-only gate is allowed to run.

## Boundaries

- Do not run a larger corpus batch in P51-T3.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat readiness output, AI output, static output, rerun output,
  planning output, or adapter output as registry truth.
