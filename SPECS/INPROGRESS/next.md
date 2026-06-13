# Next Task: P32-T6 SpecPM Selected Candidate Handoff Preflight

**Status:** Planned
**Selected:** 2026-06-13
**Task:** P32-T6 SpecPM Selected Candidate Handoff Preflight
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness
**Last Archived:** P32-T5 Refreshed Candidate-Layer Triage and Selected Handoff

## Recently Archived

- `P32-T4` recorded the single-package deferred candidate regeneration dry run
  in `docs/SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md`,
  `<doc:SinglePackageDeferredCandidateRegenerationDryRun>`, and
  `tests/fixtures/single_package_deferred_candidate_regeneration/p32-t4-single-package-deferred-candidate-regeneration.example.json`.
  The run classified `navigation_split_view.core` as
  `candidate_layer_review_required` with `selectedHandoffEligible: true`, and
  kept `cupertino.core` at `needs_regeneration` because
  `refined_summary_missing` remains unresolved. The artifact remains producer
  preview evidence only.
- `P32-T5` recorded the refreshed selected handoff in
  `docs/REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md`,
  `<doc:RefreshedCandidateLayerSelectedHandoff>`, and
  `tests/fixtures/refreshed_candidate_layer_selected_handoff/p32-t5-refreshed-candidate-layer-selected-handoff.example.json`.
  The selected set is `flask.core`, `gin.core`, `docc2context.core`,
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
  `navigation_split_view.core`; `cupertino.core` remains deferred on
  `refined_summary_missing`. The artifact remains producer preview evidence
  only.

## Outcome

P32-T5 is complete. The limited corpus now has a single refreshed producer
handoff artifact with eight selected preview candidates and one explicit
deferred candidate. It preserves digest-backed evidence roles, producer
preflight status, static viewer evidence, `preview_only`, and
`external_required` registry acceptance boundaries.

## Next Step

Implement or coordinate `P32-T6`: add SpecPM-side selected candidate handoff
preflight for `SpecHarvesterRefreshedCandidateLayerSelectedHandoff` or the
compatible `SpecHarvesterSelectedCandidateHandoffProposal` consumer surface.

The expected report is:

```text
SpecPMSelectedCandidateHandoffPreflightReport
apiVersion: specpm.selected-candidate-handoff-preflight/v0
```

The gate should validate artifact identity, authority, selected/deferred
candidate consistency, evidence roles and digests, producer preflight status,
static viewer status, privacy boundary, `external_required` registry
decisions, and `cupertino.core` deferral.

Passing preflight must remain review evidence only. It does not accept
packages, does not accept relations, does not seed baselines, does not remove
`preview_only`, does not publish registry metadata, and does not create a
SpecPM pull request.
