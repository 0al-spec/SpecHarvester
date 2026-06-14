# Next Task: P31-T3 Real Selected Candidate Handoff Proposal Dry Run

**Status:** Selected
**Selected:** 2026-06-13
**Task:** P31-T3 Real Selected Candidate Handoff Proposal Dry Run
**Phase:** Phase 31. Selected Candidate SpecPM Intake Handoff
**Last Archived:** P31-T2 Selected Candidate Handoff Proposal Helper

## Recently Archived

- `P30-T5` recorded the selected handoff dry run in
  `docs/LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md`,
  `<doc:LimitedPopularLibrarySelectedHandoffDryRun>`, and
  `SpecHarvesterLimitedPopularLibrarySelectedHandoffDryRun`. The product
  verdict was `selected_handoff_dry_run_ready`, with passing producer
  preflight, static viewer evidence, required bundle file digests, and
  `external_required` registry acceptance decisions for the 3 selected
  candidates: `flask.core`, `gin.core`, and `docc2context.core`. The output
  remained `producer_preview_evidence_only` and not SpecPM acceptance. The P30
  split kept 6 deferred candidates out of selected handoff until regeneration:
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`,
  `cupertino.core`, and `navigation_split_view.core`.
- `P31-T1` defined `SpecHarvesterSelectedCandidateHandoffProposal` in
  `docs/SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`,
  `<doc:SelectedCandidateHandoffProposal>`, and the
  `spec-harvester.selected-candidate-handoff-proposal/v0` fixture. The
  contract records 3 selected candidates, 6 deferred candidates, required
  evidence roles, producer preflight status, static viewer status, and
  `external_required` registry acceptance decisions while staying
  `producer_preview_evidence_only` and not SpecPM acceptance.
- `P31-T2` implemented the `selected-candidate-handoff-proposal` helper. The
  helper reads a P30 selected handoff dry-run artifact plus optional
  candidate/preflight/viewer roots, then writes
  `SpecHarvesterSelectedCandidateHandoffProposal` JSON and Markdown handoff
  artifacts. It verifies selected candidates remain `previewOnly: true`, keeps
  producer preflight at `passed` with zero warnings and errors, requires static
  viewer status `ok`, and preserves `external_required` registry acceptance
  with `producer_preview_evidence_only` authority. It does not create a SpecPM
  pull request, accept packages, accept relations, seed baselines, remove
  `preview_only`, or publish registry metadata.

## Outcome

The selected candidate handoff contract and producer helper exist. The next
gap is practical evidence: the helper has not yet been run on the real P30
selected candidate artifacts to record a portable dry-run handoff proposal
fixture.

## Next Step

Implement `P31-T3`: run `selected-candidate-handoff-proposal` on the real P30
selected candidates (`flask.core`, `gin.core`, and `docc2context.core`) and
record the resulting JSON and Markdown handoff proposal fixture.

SpecPM acceptance remains out of scope. The dry-run fixture must remain
producer preview evidence only and must not mutate candidate bundles, create a
SpecPM pull request, accept packages, accept relations, seed baselines, remove
`preview_only`, or publish registry metadata.
