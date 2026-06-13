# P33-T8 Next-Corpus Intake Readiness Decision

Status: Planned
Phase: Phase 33. Bounded Corpus Expansion Planning
Owner: SpecHarvester producer evidence, SpecPM maintainer intake boundary

## Motivation

P33-T7 made the selected next-corpus scope machine-preflightable by SpecPM. The
durable selected handoff artifact passed the SpecPM consumer gate with three
selected candidates, two deferred candidates, four required evidence roles, one
verified source digest, zero warnings, and zero errors.

The next step is not registry acceptance. The next step is to record an intake
readiness decision that says what maintainers can do with the selected scope
and what remains deferred.

## Goal

Record the next-corpus intake readiness decision using the passing P33-T7
durable selected handoff preflight result.

## Deliverables

- Add a machine-readable P33-T8 intake readiness decision fixture.
- Record selected candidates as ready for author/maintainer review:
  - `serena.core`;
  - `transmission.core`;
  - `specpm.core`.
- Preserve deferred candidates outside readiness:
  - `mcpm.system`;
  - `specgraph.system`.
- Reference committed P33-T7 durable handoff evidence and the passing SpecPM
  preflight result.
- Add GitHub docs, DocC docs, validation report, and docs-contract tests.
- Archive the task and mark Phase 33 complete unless the review discovers an
  actionable follow-up.

## Acceptance Criteria

- The decision fixture records:
  - selected candidate count `3`;
  - deferred candidate count `2`;
  - SpecPM preflight status `passed`;
  - warning count `0`;
  - error count `0`;
  - decision status
    `ready_for_author_maintainer_review_with_explicit_deferral`.
- The decision states that passing preflight is review evidence only and does
  not accept packages, accept relations, seed baselines, remove `preview_only`,
  publish registry metadata, create a SpecPM pull request, or replace
  maintainer review.
- The decision does not expand the corpus beyond the P33 source manifest and
  does not promote deferred candidates.
- Documentation and tests link the decision from Phase 33 docs, roadmap, docs
  index, and DocC.

## Non-Goals

- Do not run a new scrape.
- Do not rerun LM Studio or any model provider.
- Do not clone repositories, fetch remote state, install dependencies, or
  execute harvested repository code.
- Do not mutate generated candidate bundles.
- Do not accept packages or relations in SpecPM.
- Do not seed baselines, remove `preview_only`, publish registry metadata, or
  create a SpecPM pull request.

