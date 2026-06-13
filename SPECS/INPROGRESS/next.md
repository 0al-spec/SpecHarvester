# Next Task: P32-T7 Limited Corpus Intake Readiness Decision

**Status:** Selected
**Selected:** 2026-06-13
**Task:** P32-T7 Limited Corpus Intake Readiness Decision
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness
**Last Archived:** P32-T6 SpecPM Selected Candidate Handoff Preflight

## Recently Archived

- `P32-T5` recorded the refreshed selected handoff in
  `docs/REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md`,
  `<doc:RefreshedCandidateLayerSelectedHandoff>`, and
  `tests/fixtures/refreshed_candidate_layer_selected_handoff/p32-t5-refreshed-candidate-layer-selected-handoff.example.json`.
  The selected set is `flask.core`, `gin.core`, `docc2context.core`,
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
  `navigation_split_view.core`; `cupertino.core` remains deferred on
  `refined_summary_missing`. The artifact remains producer preview evidence
  only and is the source input for the SpecPM-side selected candidate handoff
  preflight consumer gate.
- `P32-T6` recorded the merged SpecPM selected candidate handoff preflight in
  [`0al-spec/SpecPM#140`](https://github.com/0al-spec/SpecPM/pull/140). The
  command `specpm producer-bundle preflight-selected-candidate-handoff` emits
  `SpecPMSelectedCandidateHandoffPreflightReport` and passed against the P32-T5
  fixture with eight selected candidates, one deferred candidate
  (`cupertino.core`), and three source digests verified. The report is review
  evidence only: it does not accept packages, does not accept relations, does
  not seed baselines, does not remove `preview_only`, does not publish registry
  metadata, and does not create a SpecPM pull request.

## Outcome

P32-T6 is complete. The refreshed selected handoff evidence is now
machine-checkable by SpecPM before maintainers decide whether the limited
corpus is ready for author review, needs more regeneration, or should stop
before broader autonomous scraping.

## Next Step

Implement `P32-T7`: record the limited corpus intake readiness decision.

The decision should use:

- P32-T5 producer evidence;
- the P32-T6 `SpecPMSelectedCandidateHandoffPreflightReport` result;
- the selected candidates `flask.core`, `gin.core`, `docc2context.core`,
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
  `navigation_split_view.core`;
- the explicit deferred candidate `cupertino.core` with
  `refined_summary_missing`.

The decision must remain non-authoritative. It may say the selected candidates
are ready for author/maintainer review, but it must not accept packages, accept
relations, seed baselines, remove `preview_only`, publish registry metadata, or
create a SpecPM pull request.
