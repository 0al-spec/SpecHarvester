# P32-T4 Single-Package Deferred Candidate Regeneration Dry Run

**Status:** Planned
**Selected:** 2026-06-13
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness

## Motivation

P32-T3 resolved the xyflow package-set identity blocker enough for refreshed
candidate-layer review. Two P30 deferred single-package candidates remain:

- `cupertino.core`, blocked by warning-bearing enrichment output
  (`refined_summary_missing`);
- `navigation_split_view.core`, blocked by identity drift between
  `navigation-split-view.core` and `navigation_split_view.core`.

Without a recorded single-package dry run, the limited corpus cannot progress
toward refreshed selected handoff evidence.

## Goal

Run a bounded dry run for `cupertino` and `navigation-split-view`, record
whether each candidate can re-enter candidate-layer review, and document the
NavigationSplitView canonical id decision.

For NavigationSplitView, the canonical package id for this run is
`navigation_split_view.core`, matching the generated and validated candidate
identity from P30/P31 evidence. The legacy source-manifest hint
`navigation-split-view.core` is retained only as the rejected or aliased drift
id, and the current source manifest must be updated before the rerun.

## Deliverables

- Verify `inputs/limited-popular-libraries/repositories.yml` and both local
  checkouts before running regeneration.
- Update the current NavigationSplitView manifest hint to
  `navigation_split_view.core` so the rerun starts from the chosen canonical
  id rather than reproducing the old drift.
- Run `autonomous-candidate-batch --select cupertino --select
  navigation-split-view` into a fresh
  `.smoke/p32-deferred-regeneration/<attempt-id>/single-package` output root.
- Render static viewers for regenerated candidate bundles.
- Re-run candidate bundle preflight for both generated candidates.
- Add a machine-readable fixture under
  `tests/fixtures/single_package_deferred_candidate_regeneration/`.
- Add a GitHub docs page and DocC mirror summarizing the dry run, evidence,
  canonical id decision, candidate-layer verdicts, and non-authority boundary.
- Link the report from the deferred regeneration runbook, autonomous candidate
  tech-debt plan, selected candidate handoff docs, SpecPM handoff docs,
  roadmap, and docs index.
- Add docs-contract tests covering source revisions, `refined_summary_missing`,
  canonical id resolution, preflight/viewer proof, `preview_only`, external
  registry acceptance, and non-authority boundaries.
- Archive Flow artifacts and leave the next pointer on P32-T5.

## Acceptance Criteria

- Source manifest validation passes before the dry run.
- The local Cupertino checkout exists, is a git worktree, is clean, and
  matches revision `65dcae238d30cfbd0d9d15ae10f7b8c67575c19b`.
- The local NavigationSplitView checkout exists, is a git worktree, is clean,
  and matches revision `2c88df50b8f587560b91f6027e9ea275aee17060`.
- The dry run is scoped to exactly `cupertino` and `navigation-split-view`.
- `cupertino.core` either has clean regenerated enrichment without
  `refined_summary_missing`, or the fixture explicitly keeps it deferred and
  explains the remaining warning.
- NavigationSplitView records `navigation_split_view.core` as canonical and
  `navigation-split-view.core` as the rejected or aliased drift id.
- Each regenerated candidate has producer preflight `passed` with warning
  count `0` and error count `0`, or remains explicitly deferred with the
  blocking reason.
- Static viewer output is present for every candidate that passes preflight.
- Each generated candidate remains `preview_only`.
- Registry acceptance remains `external_required`.
- No SpecPM PR is created, no package or relation is accepted, no baseline is
  seeded, and no registry metadata is published.

## Non-Goals

- No xyflow rerun.
- No broad limited-corpus rerun.
- No accepted-source mutation.
- No SpecPM repository mutation.
- No package or relation acceptance.
- No baseline seeding.
- No removal of `preview_only`.
- No registry publication.
