# Next Task: P30-T2 Deterministic Limited Corpus Batch

**Status:** Selected
**Selected:** 2026-06-13
**Task:** P30-T2 Deterministic Limited Corpus Batch
**Phase:** Phase 30. Limited Popular-Library Scraping Batch
**Last Archived:** P30-T1 Limited Popular-Library Corpus Plan

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
  `inputs/limited-popular-libraries.example.yml`. The seed corpus includes
  `flask.core`, `gin.core`, `xyflow.workspace`, `cupertino.core`,
  `navigation-split-view.core`, and `docc2context.core`. The plan records
  source-manifest shape, selection criteria, operator runbook, stop conditions,
  candidate-layer triage states, and non-authority boundaries before any
  larger scrape.

## Outcome

The limited corpus expansion now has a committed manifest and runbook. The next
step is to execute the deterministic `--skip-ai` path and record actual corpus
outcomes before any live LM Studio calls.

## Next Step

Implement `P30-T2`: run deterministic `--skip-ai` scraping over the selected
limited popular-library corpus and record collection, candidate, relation,
preflight, and stop-policy outcomes.
