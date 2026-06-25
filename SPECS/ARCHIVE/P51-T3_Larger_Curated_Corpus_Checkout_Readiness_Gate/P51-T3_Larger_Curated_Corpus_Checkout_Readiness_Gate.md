# P51-T3 Larger Curated Corpus Checkout Readiness Gate

**Status:** Planned
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T3`
**Created:** 2026-06-25T12:45:14+03:00
**Depends On:** `P51-T2` Larger Curated Corpus Source Plan and Manifest Criteria
**Reasoning Effort:** medium

## Goal

Run the larger curated corpus checkout readiness gate against the P51-T2
source manifest and record whether the selected sources are ready for the
P51-T4 static-only gate.

## Context

`P51-T2` authored the 12-repository source manifest:

```text
inputs/p51-larger-curated-corpus/repositories.yml
```

It also recorded the source-plan fixture:

```text
tests/fixtures/larger_curated_corpus_source_plan/p51-t2-larger-curated-corpus-source-plan.example.json
```

`P51-T3` is the first verification task after source-plan authoring. It may
inspect local git checkout metadata, but it must not run the static-only or
AI-enabled corpus gates.

## Deliverables

- A machine-readable checkout readiness gate fixture for all 12 selected
  sources.
- GitHub and DocC documentation explaining readiness outcome, per-source
  verification, caveats, and next gate.
- Contract tests proving every selected source has readiness evidence tied to
  the P51-T2 manifest and pinned revision.
- A validation report recording the exact checks that were run.

## Readiness Criteria

Each selected source is ready only when:

- the manifest entry parses successfully;
- the operator-local checkout path resolves without clone or fetch;
- the checkout is a git repository;
- the observed local HEAD equals the pinned manifest revision;
- any caveats are recorded without hiding the source from later triage.

## Acceptance Criteria

- All 12 selected P51-T2 sources have readiness records.
- Missing checkout, revision mismatch, clone/fetch requirement, and unclear
  checkout state are modeled as blockers.
- If every selected source is present and revision-matched, the fixture marks
  P51-T4 static-only gate as allowed.
- `SPECS/INPROGRESS/next.md` selects `P51-T4` after archive.
- Contract tests cover fixture identity, source-plan linkage, manifest linkage,
  readiness counts, source records, caveats, boundaries, docs, Workplan, and
  next task state.

## Non-Goals

- Do not run `autonomous-candidate-batch`.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat readiness output as registry truth.
