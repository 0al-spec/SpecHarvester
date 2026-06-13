# Next Task: P33-T5 Next-Corpus Candidate-Layer Triage

**Status:** Selected
**Selected:** 2026-06-14
**Task:** P33-T5 Next-Corpus Candidate-Layer Triage
**Phase:** Phase 33. Bounded Corpus Expansion Planning
**Last Archived:** P33-T4 Live Local-Model Next-Corpus Dry Run

## Recently Archived

- `P33-T3` recorded the deterministic next-corpus dry run in
  `docs/NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md`,
  `<doc:NextCorpusDeterministicDryRun>`, and
  `tests/fixtures/next_corpus_deterministic_dry_run/p33-t3-next-corpus-deterministic-dry-run.example.json`.
  The fixture identity is `SpecHarvesterNextCorpusDeterministicDryRun` with
  `apiVersion: spec-harvester.next-corpus-deterministic-dry-run/v0`. It
  processed five repositories, produced five preview candidates, zero relation
  proposals, and five bundle-set preflights. It recorded `mcpm.system` and
  `specgraph.system` package-id review signals and is ready for P33-T4 live
  local-model review. It remains review evidence only, does not accept
  packages, does not accept relations, and does not remove `preview_only`.
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

## Current Selection

Implement `P33-T5`: produce candidate-layer triage for the next corpus.

The triage must classify every P33-T4 candidate into selected, deferred,
blocked, and not-for-intake states. It must carry forward the P33-T4 live
local-model findings:

- `ai_draft_no_proposal_subjects` for `serena` and `transmission`;
- `ai_draft_warning_diagnostics` for `mcpm-sh` and `specpm`;
- package-id review signals for `mcpm-sh` and `specgraph`;
- the clean enrichment status for all five repositories.

The output should state which candidates, if any, are ready for selected
handoff evidence and which require regeneration, explicit author review, or
exclusion from intake.

## Boundaries

This task must not run a new scrape, must not rerun LM Studio, must not clone
repositories, must not fetch remote state, must not install dependencies, must
not execute harvested code, must not run package scripts, must not publish
registry metadata, must not accept packages, must not accept relations, must
not seed baselines, must not remove `preview_only`, must not create a SpecPM
pull request, or treat AI output as registry truth.

It must not accept packages and must not publish registry metadata.
