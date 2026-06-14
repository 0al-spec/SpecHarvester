# Next Task: P33-T2 Next-Corpus Source Manifest Fixture

**Status:** Selected
**Selected:** 2026-06-13
**Task:** P33-T2 Next-Corpus Source Manifest Fixture
**Phase:** Phase 33. Bounded Corpus Expansion Planning
**Last Archived:** P33-T1 Bounded Corpus Expansion Plan

## Recently Archived

- `P32-T7` recorded the limited corpus intake readiness decision in
  `docs/LIMITED_CORPUS_INTAKE_READINESS_DECISION.md`,
  `<doc:LimitedCorpusIntakeReadinessDecision>`, and
  `tests/fixtures/limited_corpus_intake_readiness_decision/p32-t7-limited-corpus-intake-readiness-decision.example.json`.
  The fixture identity is
  `SpecHarvesterLimitedCorpusIntakeReadinessDecision`, and the decision is
  `ready_for_author_maintainer_review_with_explicit_deferral`: selected
  preview candidates `flask.core`, `gin.core`, `docc2context.core`,
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
  `navigation_split_view.core` are ready for author/maintainer review,
  `cupertino.core` remains deferred on `refined_summary_missing`, and broader
  autonomous scraping requires a separate follow-up task.
- `P33-T1` recorded the bounded corpus expansion plan in
  `docs/BOUNDED_CORPUS_EXPANSION_PLAN.md`,
  `<doc:BoundedCorpusExpansionPlan>`, and
  `tests/fixtures/bounded_corpus_expansion_plan/p33-t1-bounded-corpus-expansion-plan.example.json`.
  The fixture identity is `SpecHarvesterBoundedCorpusExpansionPlan` with
  `apiVersion: spec-harvester.bounded-corpus-expansion-plan/v0`. It caps the
  next batch at a five-repository limit, requires a source manifest, defines
  deterministic and live-model validation gates, candidate-layer triage,
  SpecPM-side selected handoff preflight, stop conditions, and keeps the result
  as review evidence only. It does not accept packages, does not accept
  relations, and does not remove `preview_only`.

## Current Selection

Implement `P33-T2`: add the next-corpus source manifest fixture.

The fixture must define:

- no more than five repositories;
- repository IDs;
- local checkout paths;
- pinned revisions;
- selection rationale;
- expected package shape;
- no network discovery behavior.

## Boundaries

This task must not clone repositories, fetch remote state, install
dependencies, execute harvested code, run package scripts, publish registry
metadata, accept packages, accept relations, seed baselines, remove
`preview_only`, or treat AI output as registry truth.
