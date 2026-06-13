# P32-T5 Refreshed Candidate-Layer Triage and Selected Handoff

**Status:** Planned
**Selected:** 2026-06-13
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness

## Motivation

P30-T5 selected only `flask.core`, `gin.core`, and `docc2context.core` for
handoff because six limited-corpus candidates still had package-set identity,
warning-bearing enrichment, or package-id drift blockers.

P32-T3 and P32-T4 recorded targeted regeneration evidence for those blockers:

- `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and `xyflow.system` now
  have package-set identity, relation topology, passing producer preflight, and
  static viewer evidence;
- `navigation_split_view.core` now has a canonical package id decision and can
  re-enter candidate-layer review;
- `cupertino.core` still has `refined_summary_missing` and must stay deferred.

Without a refreshed triage and selected handoff artifact, the operator has to
mentally merge P30, P32-T3, and P32-T4 evidence before asking SpecPM to run a
consumer-side preflight. That is fragile and easy to over-promote.

## Goal

Produce a machine-readable refreshed candidate-layer selected handoff artifact
that combines the original selected P30 candidates with regenerated P32
candidates that satisfy hard gates, while keeping unresolved candidates
explicitly deferred.

The artifact must remain producer preview evidence. It must not accept
packages, accept relations, seed baselines, remove `preview_only`, publish
registry metadata, mutate SpecPM, or create a SpecPM pull request.

## Deliverables

- Add a durable fixture under
  `tests/fixtures/refreshed_candidate_layer_selected_handoff/` with:
  - source fixture references and digests for P30-T5, P32-T3, and P32-T4;
  - selected candidates:
    `flask.core`, `gin.core`, `docc2context.core`, `xyflow.workspace`,
    `xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
    `navigation_split_view.core`;
  - deferred candidates, including `cupertino.core` with
    `refined_summary_missing`;
  - non-authority boundaries and expected next consumer-side gate.
- Add a GitHub docs page describing the refreshed triage, selected/deferred
  decisions, evidence sources, and stop conditions.
- Add a DocC mirror for the same policy and artifact shape.
- Link the report from the autonomous candidate tech-debt plan, deferred
  regeneration runbook, selected candidate handoff proposal docs, SpecPM
  handoff docs, roadmap, and docs index.
- Add docs-contract regression coverage for selected candidate identity,
  deferred candidate blockers, source fixture digests, authority boundaries,
  and `next.md` progression to P32-T6.
- Archive Flow artifacts and leave the next pointer on P32-T6.

## Acceptance Criteria

- The refreshed handoff fixture has
  `apiVersion: spec-harvester.refreshed-candidate-layer-selected-handoff/v0`
  and `kind: SpecHarvesterRefreshedCandidateLayerSelectedHandoff`.
- Source fixture digests match the committed P30-T5, P32-T3, and P32-T4
  fixtures.
- Exactly eight candidates are selected for refreshed selected handoff:
  `flask.core`, `gin.core`, `docc2context.core`, `xyflow.workspace`,
  `xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
  `navigation_split_view.core`.
- `cupertino.core` remains deferred with blocker `refined_summary_missing`.
- Every selected candidate records:
  - `candidateLayerDecision.status: candidate_layer_review_required`;
  - `selectedHandoffEligible: true`;
  - `producerPreflight.status: passed`;
  - `viewer.status: ok`;
  - `preview_only`;
  - `registryAcceptanceDecision.status: external_required`.
- The report says the next expected gate is SpecPM-side selected candidate
  handoff preflight.
- No SpecPM mutation, registry publication, package acceptance, relation
  acceptance, baseline seeding, or `preview_only` removal occurs.

## Non-Goals

- No new repository harvesting.
- No new LM Studio or AI enrichment run.
- No broad limited-corpus rerun.
- No generated candidate mutation.
- No SpecPM repository mutation.
- No package or relation acceptance.
- No baseline seeding.
- No registry publication.

