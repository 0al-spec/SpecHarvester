# P31-T5 Deferred Selected Candidate Regeneration Requirements

**Status:** Planned
**Selected:** 2026-06-13
**Phase:** Phase 31. Selected Candidate SpecPM Intake Handoff

## Motivation

P30-T4 and P30-T5 intentionally kept six generated preview candidates out of
selected handoff:

- `xyflow.workspace`;
- `xyflow.react`;
- `xyflow.svelte`;
- `xyflow.system`;
- `cupertino.core`;
- `navigation_split_view.core`.

They are not failed forever. They are useful producer preview evidence, but
they need targeted regeneration or correction before they can safely enter a
future selected handoff proposal. Without an explicit policy, a future operator
could accidentally promote package-set, warning-bearing, or identity-drift
candidates just because they appear in a generated corpus.

## Goal

Record a reviewable, machine-readable regeneration requirements contract for
the deferred P30 candidates. The contract should explain what must be fixed,
regenerated, revalidated, and reclassified before a candidate can enter
selected handoff.

## Deliverables

- Add a GitHub docs page for deferred selected-candidate regeneration
  requirements.
- Add a DocC mirror page and link it from the root topics.
- Add a fixture under `tests/fixtures/` that records the six deferred
  candidates, their blocker class, required evidence, and non-authority
  boundary.
- Link the new requirement contract from selected handoff, preflight, handoff,
  roadmap, and docs index pages.
- Add docs-contract tests that pin the fixture shape, required candidate ids,
  regeneration classes, and boundary statements.
- Archive Flow artifacts and leave Phase 31 ready for follow-up selection.

## Acceptance Criteria

- The fixture identity is explicit and versioned.
- The fixture includes all six P30 deferred candidate ids.
- The fixture groups requirements for:
  - package-set identity regeneration;
  - warning-bearing enrichment regeneration or author-curated summary evidence;
  - package-id normalization / identity-drift resolution.
- The requirements state that selected handoff can only resume after regenerated
  evidence passes producer preflight with zero warnings/errors, static viewer
  output is present, `preview_only` remains intact, and registry acceptance
  remains `external_required`.
- The docs state that P31-T5 does not regenerate candidates and does not accept
  packages, accept relations, seed baselines, remove `preview_only`, publish
  registry metadata, or create a SpecPM pull request.
- `tests/test_docs_contracts.py` covers the new docs, fixture, and `next.md`
  transition.
- Project gates pass.

## Non-Goals

- No actual candidate regeneration.
- No LM Studio or SpecNode run.
- No selected handoff proposal rerun.
- No SpecPM repository changes.
- No accepted-source mutation.
- No registry publication.

## Archive Status

Archived: 2026-06-13
Verdict: PASS
