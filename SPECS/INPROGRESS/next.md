# Next Task: P31-T2 Selected Candidate Handoff Proposal Helper

**Status:** In Progress
**Selected:** 2026-06-13
**Task:** P31-T2 Selected Candidate Handoff Proposal Helper
**Phase:** Phase 31. Selected Candidate SpecPM Intake Handoff
**Last Archived:** P31-T1 Selected Candidate Handoff Proposal Contract

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

## Outcome

The selected candidate handoff contract exists, but it is still only a
documented shape and example fixture. Operators cannot yet generate the
portable JSON and Markdown handoff artifacts from real selected candidate
bundles.

## Next Step

Implement `P31-T2`: add a producer helper that reads selected candidate
bundles, producer preflight reports, static viewer outputs, and the selected
handoff dry-run source evidence, then emits JSON and Markdown handoff
artifacts matching `SpecHarvesterSelectedCandidateHandoffProposal`.

SpecPM acceptance out of scope. The helper must not mutate candidate bundles,
create a SpecPM pull request, accept packages, accept relations, seed
baselines, remove `preview_only`, or publish registry metadata.
