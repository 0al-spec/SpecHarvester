# P33-T1 Bounded Corpus Expansion Plan

**Status:** Planned
**Selected:** 2026-06-13
**Phase:** Phase 33. Bounded Corpus Expansion Planning

## Motivation

Phase 32 closed the deferred-candidate regeneration and intake-readiness loop
for the current limited corpus. It deliberately stopped before broader
autonomous scraping: selected candidates are ready for author/maintainer
review, `cupertino.core` remains explicitly deferred, and nothing has registry
authority.

The next risk is scope creep. If SpecHarvester expands from a small calibrated
corpus into popular repositories without a new manifest, repository count,
validation gate, and stop policy, it becomes an uncontrolled framework scraper
instead of a producer of reviewable starter package evidence.

## Goal

Record a bounded corpus expansion plan that defines the next work sequence
before any new scrape runs.

## Deliverables

- Add a canonical bounded corpus expansion plan document.
- Add a DocC mirror and link it from the root documentation.
- Add a machine-readable example fixture that records the expansion policy,
  repository count limit, gate sequence, and authority boundary.
- Update roadmap, docs index, Workplan, and current `next.md`.
- Add docs-contract tests that cover the plan, fixture identity, gate sequence,
  stop conditions, and non-authority boundary.
- Archive Flow artifacts and leave `next.md` on the next concrete Phase 33
  task.

## Acceptance Criteria

- The plan defines source manifest requirements before any next-corpus run.
- The plan defines a repository count limit and selection rationale.
- The plan defines deterministic, live-model, candidate-layer, and SpecPM-side
  preflight gates.
- The plan defines stop conditions for failed hard gates, provider
  unavailability, digest drift, identity drift, source manifest mismatch, and
  registry-authority ambiguity.
- The plan keeps author/maintainer review external and prevents automatic
  SpecPM registry acceptance.
- The plan states that the next expansion is local-only and must not clone,
  fetch, install dependencies, execute harvested code, publish registry
  metadata, accept packages, accept relations, seed baselines, remove
  `preview_only`, or treat AI output as registry truth.
- Project docs-contract tests pass.

## Non-Goals

- No new repository scrape.
- No source manifest fixture implementation beyond the plan example.
- No deterministic corpus run.
- No live local-model run.
- No selected handoff artifact generation.
- No SpecPM repository change.
- No registry publication or package acceptance.

## Review Subject

`p33_t1_bounded_corpus_expansion_plan`
