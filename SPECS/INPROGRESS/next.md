# Next Task: Phase 31 Complete

**Status:** Phase Complete
**Selected:** 2026-06-13
**Task:** Phase 31 Complete
**Phase:** Phase 31. Selected Candidate SpecPM Intake Handoff
**Last Archived:** P31-T5 Deferred Selected Candidate Regeneration Requirements

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
- `P31-T3` ran `selected-candidate-handoff-proposal` on the recorded P30-T5
  selected handoff dry-run evidence and committed
  `tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json`
  plus `docs/SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md`. The generated
  fixture records exactly the selected candidates `flask.core`, `gin.core`,
  and `docc2context.core`; keeps all six P30 deferred candidates excluded; and
  preserves `producer_preview_evidence_only`, `previewOnly: true`,
  zero-warning producer preflight, static viewer status `ok`, and
  `registryAcceptanceDecision.status: external_required`. It remains review
  evidence only and not SpecPM acceptance.
- `P31-T4` documented the SpecPM-side selected candidate handoff preflight
  expectations in `docs/SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md`
  and `<doc:SelectedCandidateHandoffPreflightExpectations>`. It defined the
  future `SpecPMSelectedCandidateHandoffPreflightReport` identity
  `specpm.selected-candidate-handoff-preflight/v0`, checked
  `SpecHarvesterSelectedCandidateHandoffProposal` identity,
  `producer_preview_evidence_only` authority, evidence roles, digests,
  selected/deferred candidate consistency, and non-authority boundaries. A pass
  remains review evidence and not package acceptance.
- `P31-T5` recorded deferred selected-candidate regeneration requirements in
  `docs/DEFERRED_SELECTED_CANDIDATE_REGENERATION_REQUIREMENTS.md`,
  `<doc:DeferredSelectedCandidateRegenerationRequirements>`, and the
  `SpecHarvesterDeferredSelectedCandidateRegenerationRequirements` fixture
  `p31-t5-deferred-selected-candidate-regeneration-requirements.example.json`.
  The fixture covers all six deferred P30 candidates, package-set identity
  regeneration, warning-bearing enrichment regeneration, identity-drift
  resolution, source digests, minimum proof before selected handoff, and the
  non-authority boundary. It remains regeneration requirements only and not
  package acceptance.

## Outcome

Phase 31 is complete. SpecHarvester now has a selected candidate handoff
contract, producer helper, real selected candidate handoff fixture, downstream
SpecPM preflight expectation document, and deferred candidate regeneration
requirements.

## Next Step

No Phase 31 task remains selected. The next operator should choose a new task
from the remaining workplan backlog, such as older refactoring work, CodeGraph
boundary work, or package-set proposal intake alignment, rather than extending
Phase 31 implicitly.
