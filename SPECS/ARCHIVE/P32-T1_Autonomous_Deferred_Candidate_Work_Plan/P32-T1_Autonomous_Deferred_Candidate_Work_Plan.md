# P32-T1 Autonomous Deferred Candidate Work Plan

**Status:** Planned
**Selected:** 2026-06-13
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness

## Motivation

P29 closed the first autonomous candidate technical debt: single-package
fallbacks, bounded LM Studio JSON repair, and mixed-corpus quality gates. P30
and P31 then moved the limited popular-library corpus into selected/deferred
handoff evidence.

The remaining debt is no longer "can SpecHarvester produce any starter
package?" It is now "can SpecHarvester turn deferred preview candidates into
clean, handoff-ready evidence without accidentally becoming a broad automatic
framework scraper or a SpecPM registry authority?"

The current deferred candidates are known and bounded:

- `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and `xyflow.system`
  require package-set identity regeneration.
- `cupertino.core` requires warning-bearing enrichment regeneration or
  author-curated summary evidence.
- `navigation_split_view.core` requires identity-drift resolution.

## Goal

Record a concrete work plan that converts the P30/P31 deferred candidate
findings into ordered tasks with motivation, goal, repository owner, acceptance
criteria, and non-authority boundaries.

## Deliverables

- Update the autonomous candidate technical-debt plan with a current P32
  sequence.
- Add Phase 32 tasks to `SPECS/Workplan.md`.
- Update roadmap and DocC roadmap references.
- Update the DocC mirror for the technical-debt plan.
- Update `docs/README.md` or root DocC topics if needed.
- Add docs-contract assertions for the P32-T1 plan, current `next.md` state,
  workplan tasks, and non-authority boundaries.
- Archive Flow artifacts and leave the next pointer on a concrete P32 follow-up
  task.

## Acceptance Criteria

- The plan distinguishes completed P29 debt from current P30/P31 deferred
  candidate debt.
- The plan lists motivation and goal for each P32 follow-up task.
- The plan assigns repository ownership across SpecHarvester and SpecPM where
  appropriate.
- The plan covers package-set identity regeneration, warning-bearing
  enrichment regeneration or author-curated summary evidence, identity-drift
  resolution, refreshed triage, selected handoff rerun, and SpecPM-side
  consumer preflight.
- The plan explicitly says the work must not clone repositories, execute
  harvested code, install dependencies, publish registry metadata, remove
  `preview_only`, accept packages, accept relations, or treat AI output as
  registry truth.
- Project documentation tests pass.

## Non-Goals

- No actual candidate regeneration.
- No LM Studio run.
- No SpecPM repository change.
- No selected handoff proposal rerun.
- No registry publication.
- No acceptance decision for any package or relation.

## Archive Status

Archived: 2026-06-13
Verdict: PASS
