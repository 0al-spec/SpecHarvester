# Next Task: P33-T6 Next-Corpus SpecPM Preflight and Intake Decision

**Status:** Selected
**Selected:** 2026-06-14
**Task:** P33-T6 Next-Corpus SpecPM Preflight and Intake Decision
**Phase:** Phase 33. Bounded Corpus Expansion Planning
**Last Archived:** P33-T5 Next-Corpus Candidate-Layer Triage

## Recently Archived

- `P33-T4` recorded the live local-model next-corpus dry run in
  `docs/NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md`,
  `<doc:NextCorpusLiveLocalModelBatch>`, and
  `tests/fixtures/next_corpus_live_local_model_batch/p33-t4-next-corpus-live-local-model.example.json`.
  The fixture identity is `SpecHarvesterNextCorpusLiveLocalModelBatch` with
  `apiVersion: spec-harvester.next-corpus-live-local-model-batch/v0`. It used
  `openai/gpt-oss-20b`, processed five repositories, produced five preview
  candidates, zero relation proposals, five bundle-set preflights, five AI
  draft proposals, five AI enrichment proposals, zero JSON repair needs, zero
  JSON repair exhaustion, and 76291 provider tokens. It reached
  `ready_for_candidate_layer_triage` while preserving package-id review signals
  and adding `ai_draft_no_proposal_subjects` plus
  `ai_draft_warning_diagnostics` findings. It remains review evidence only,
  does not accept packages, does not accept relations, and does not remove
  `preview_only`.
- `P33-T5` recorded the next-corpus candidate-layer triage in
  `docs/NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md`,
  `<doc:NextCorpusCandidateLayerTriage>`, and
  `tests/fixtures/next_corpus_candidate_layer_triage/p33-t5-next-corpus-candidate-layer-triage.example.json`.
  The fixture identity is `SpecHarvesterNextCorpusCandidateLayerTriage` with
  `apiVersion: spec-harvester.next-corpus-candidate-layer-triage/v0`. It
  selected three selected candidates for P33-T6: `serena.core`,
  `transmission.core`, and `specpm.core`. It kept two deferred candidates:
  `mcpm.system` and `specgraph.system`. It recorded zero blocked candidates
  and zero not-for-intake candidates. It carried forward
  `ai_draft_no_proposal_subjects`, `ai_draft_warning_diagnostics`, and
  `package_id_hint_changed_by_package_set_selection` while reaching
  `ready_for_p33_t6_selected_handoff_preflight`. It remains review evidence
  only, does not accept packages, does not accept relations, and does not
  remove `preview_only`.

## Current Selection

Implement `P33-T6`: run or coordinate SpecPM-side preflight for the selected
handoff evidence from P33-T5 and record the next intake readiness decision.

The selected handoff scope is limited to:

- `serena.core`;
- `transmission.core`;
- `specpm.core`.

Deferred candidates must stay outside P33-T6 selected handoff preflight:

- `mcpm.system`;
- `specgraph.system`.

The task should record whether the selected handoff evidence is ready for
SpecPM maintainer review, remains producer-only review evidence, or needs
another bounded follow-up.

## Boundaries

This task must not run a new scrape, must not rerun LM Studio, must not clone
repositories, must not fetch remote state, must not install dependencies, must
not execute harvested code, must not run package scripts, must not publish
registry metadata, must not accept packages, must not accept relations, must
not seed baselines, must not remove `preview_only`, or treat AI output as
registry truth.

It must not accept packages and must not publish registry metadata.
