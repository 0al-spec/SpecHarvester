# Next Task: P30-T4 Candidate-Layer Triage Report

**Status:** In Progress
**Selected:** 2026-06-13
**Task:** P30-T4 Candidate-Layer Triage Report
**Phase:** Phase 30. Limited Popular-Library Scraping Batch
**Last Archived:** P30-T3 Live LM Studio Limited Corpus Batch

## Recently Archived

- Prior completed boundary: `P28-T5 First-Submission or Seeded-Baseline
  Workflow`.
- Prior role-profile boundary: `P28-T4 Package-Set Role Selection Profiles`.
- Prior refresh context: `P28-T2` ran real `xyflow`, and the later
  TanStack/query refresh at `feb1efd804c1262106f72c8adc1d82a8ce9cfbb0`
  established `no_contract_delta` and first-submission handling before the P30
  limited corpus expansion.
- `P29-T6` recorded the post-mitigation corpus quality gate in
  `docs/AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md`,
  `<doc:AutonomousCandidateCorpusQualityGate>`, and
  `SpecHarvesterAutonomousCandidateCorpusQualityGate`. Flask produced
  `flask.core`, Gin produced `gin.core`, and xyflow retained
  `xyflow.workspace` plus member package candidates. The product verdict is
  `ready_for_limited_popular_library_scraping`: deterministic preflight passed
  for all three repositories, live LM Studio used `openai/gpt-oss-20b`, draft
  warnings were bounded to `excluded_package_unknown` and
  `package_set_id_missing`, JSON repair `not_needed`, and the result remains
  `producer_preview_evidence_only`, `preview_only`, and not automatic SpecPM
  acceptance.
- `P30-T1` defined the limited popular-library corpus plan in
  `docs/LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md`,
  `<doc:LimitedPopularLibraryCorpusPlan>`, and
  `inputs/limited-popular-libraries/repositories.yml`. The seed corpus includes
  `flask.core`, `gin.core`, `xyflow.workspace`, `cupertino.core`,
  `navigation-split-view.core`, and `docc2context.core`. The plan records
  source-manifest shape, selection criteria, operator runbook, stop conditions,
  candidate-layer triage states, and non-authority boundaries before any
  larger scrape.
- `P30-T2` recorded the deterministic limited popular-library corpus run in
  `docs/LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md`,
  `<doc:LimitedPopularLibraryDeterministicBatch>`, and
  `SpecHarvesterLimitedPopularLibraryDeterministicBatch`. The `--skip-ai` run
  processed all 6 repositories, collected all 6, generated 9 preview candidates
  and 3 relation proposals, passed all 6 bundle-set preflights, skipped AI
  draft/enrichment for every repository, and preserved
  `producer_preview_evidence_only`. The product verdict is
  `ready_for_live_lm_studio_limited_corpus`, with one candidate-layer review
  finding: `package_id_hint_mismatch` where `navigation-split-view.core`
  normalized to `navigation_split_view.core`. This is not SpecPM acceptance.
- `P30-T3` recorded the live LM Studio limited corpus run in
  `docs/LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md`,
  `<doc:LimitedPopularLibraryLiveLMStudioBatch>`, and
  `SpecHarvesterLimitedPopularLibraryLiveLMStudioBatch`. The run used
  `openai/gpt-oss-20b`, processed all 6 repositories, preserved 9 preview
  candidates and 3 relation proposals, passed all 6 preflights, produced AI
  draft output with 2 completed and 4 warning statuses, produced AI enrichment
  output with 5 completed and 1 warning status, needed no JSON repair
  (`not_needed`), and recorded provider total tokens `138700`. The product
  verdict is `ready_for_candidate_layer_triage`. Findings for P30-T4 are
  `excluded_package_unknown`, `package_set_id_missing`,
  `refined_summary_missing`, and the carried-forward
  `package_id_hint_mismatch`. The output remains
  `producer_preview_evidence_only` and not SpecPM acceptance.

## Outcome

The limited P30 corpus now has both deterministic and live LM Studio producer
evidence. The live provider path completed, but model-layer warnings and the
NavigationSplitView package-id normalization finding need classification before
any selected SpecPM handoff dry run.

## Next Step

Implement `P30-T4`: produce a candidate-layer triage report that classifies
each generated preview package and model finding as
`candidate_layer_review_required`, `needs_regeneration`, `blocked`, or
`not_for_intake`. The triage should decide which issues are generator bugs,
schema gaps, model noise, expected author-review items, or blockers.
