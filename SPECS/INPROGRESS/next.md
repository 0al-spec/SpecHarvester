# Next Task: P30-T1 Limited Popular-Library Corpus Plan

**Status:** Selected
**Selected:** 2026-06-13
**Task:** P30-T1 Limited Popular-Library Corpus Plan
**Phase:** Phase 30. Limited Popular-Library Scraping Batch
**Last Archived:** P29-T6 Corpus Quality Gate After Fallbacks

## Recently Archived

- Prior completed boundary: `P28-T5 First-Submission or Seeded-Baseline
  Workflow`.
- Prior role-profile boundary: `P28-T4 Package-Set Role Selection Profiles`.
- Prior refresh context: `P28-T2` ran real `xyflow`, and the later
  TanStack/query refresh at `feb1efd804c1262106f72c8adc1d82a8ce9cfbb0`
  established `no_contract_delta` and first-submission handling before the P30
  limited corpus expansion.
- `P29-T1` added `autonomous-candidate-batch`, an MVP runner over repository
  source manifests and local public checkouts. It orchestrates deterministic
  collection, workspace inventory, public interface indexes, package-set draft,
  bundle-set preflight, optional local LM Studio AI draft/enrichment proposals,
  and `SpecHarvesterAutonomousCandidateBatchReport`.
- `P29-T2` documented
  `docs/AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md` and
  `<doc:AutonomousCandidateIntakePolicy>`, preserving
  `producer_preview_evidence_only` authority for autonomous output.
- `P29-T3` recorded the Flask, Gin, and xyflow corpus baseline in
  `docs/AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`,
  `<doc:AutonomousCandidateCorpusBaseline>`, and
  `SpecHarvesterAutonomousCandidateCorpusBaseline`.
- `P29-T4` implemented deterministic single-package fallback. Flask-style
  Python fixtures now produce `flask.core`; Gin-style Go fixtures produce
  `gin.core` through `autonomous-candidate-batch`.
- `P29-T5` implemented bounded LM Studio/OpenAI-compatible JSON repair/retry
  for live package-set AI draft and enrichment proposal generation.
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

## Outcome

Autonomous Candidate Harvest MVP is complete for the current scope. The next
phase should expand the corpus only through bounded local checkouts, pinned
revisions, explicit run limits, and candidate-layer review.

## Next Step

Implement `P30-T1`: define the limited popular-library corpus expansion plan,
source-manifest shape, selection criteria, operator runbook, and non-authority
boundaries before running a larger scrape.
