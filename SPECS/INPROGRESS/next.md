# Next Task: P29-T6 Corpus Quality Gate After Fallbacks

**Status:** In Progress
**Selected:** 2026-06-13
**Task:** P29-T6 Corpus Quality Gate After Fallbacks
**Phase:** Phase 29. Autonomous Candidate Harvest MVP
**Last Archived:** P29-T5 LM Studio JSON Repair and Retry

## Recently Archived

- Prior completed boundary: `P28-T5 First-Submission or Seeded-Baseline
  Workflow`.
- Prior role-profile boundary: `P28-T4 Package-Set Role Selection Profiles`.
- Prior refresh context: `P28-T2` ran real `xyflow`, and the later
  TanStack/query refresh at `feb1efd804c1262106f72c8adc1d82a8ce9cfbb0`
  established `no_contract_delta` handling before seeded-baseline intake.
- `P29-T1` added `autonomous-candidate-batch`, an MVP runner over repository
  source manifests and local public checkouts. It orchestrates deterministic
  collection, workspace inventory, public interface indexes, package-set draft,
  bundle-set preflight, optional local LM Studio AI draft/enrichment proposals,
  and `SpecHarvesterAutonomousCandidateBatchReport`.
- The default autonomous role profile is `autonomous_popular_mvp`, selecting
  workspace, `core_runtime`, React/Svelte binding, and generic member package
  roles while excluding examples, tests, fixtures, and private tooling from
  primary candidate output.
- Live LM Studio smoke with `openai/gpt-oss-20b` passed on a local fixture:
  `3` candidates, `2` relations, preflight `passed`, AI draft `completed`, and
  AI enrichment `completed`.
- Real `xyflow` smoke at `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` passed
  with 4 candidates, 3 relations, preflight `passed`, and
  `authorReadyDraftSummary.decision: stop_for_author_review`.
- Follow-up corpus check over local Flask, Gin, and xyflow found two concrete
  technical-debt items captured in
  `docs/AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`: Flask and Gin collect public
  evidence but produce `0` package candidates without a single-package
  fallback, and live LM Studio output can still need bounded JSON repair/retry
  when the model returns malformed JSON.
- `P29-T2` documented
  `docs/AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md` and
  `<doc:AutonomousCandidateIntakePolicy>`. The policy defines
  `candidate_layer_review_required`, `needs_regeneration`, `blocked`, and
  `not_for_intake` review guidance for autonomous batch output. It names
  `SpecHarvesterAutonomousCandidateBatchReport`,
  `SpecHarvesterPackageSetAIDraftProposal`,
  `SpecHarvesterPackageSetAIEnrichmentProposal`, `bundle-set-preflight.json`,
  `authorReadyDraftSummary`, and `stopPolicySummary` as review inputs while
  preserving `producer_preview_evidence_only` authority.
- The P29-T2 policy explicitly states that candidate-layer review cannot accept
  packages, accept relations, seed baselines, remove `preview_only`, publish
  registry metadata, or replace SpecPM validation and maintainer review.
- `P29-T3` recorded the Flask, Gin, and xyflow corpus baseline in
  `docs/AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`,
  `<doc:AutonomousCandidateCorpusBaseline>`, and
  `SpecHarvesterAutonomousCandidateCorpusBaseline`. The baseline captured
  deterministic `--skip-ai` outcomes, live LM Studio statuses, candidate counts,
  relation counts, preflight status, and non-authority boundaries.
- The P29-T3 baseline showed `pipelineHealth: deterministic_pipeline_passed`
  and `candidateQuality: needs_follow_up`: Flask and Gin produced `0`
  candidates and `0` relations with `single_package_fallback_needed`, while
  xyflow produced `4` candidates and `3` relations with
  `stop_for_author_review` plus the live LM Studio `ai_json_repair_needed`
  diagnostic.
- `P29-T4` implemented the deterministic single-package candidate fallback and
  documented it in `docs/SINGLE_PACKAGE_CANDIDATE_FALLBACK.md` and
  `<doc:SinglePackageCandidateFallback>`. Flask-style Python fixtures now
  produce `flask.core`; Gin-style Go fixtures produce `gin.core` through
  `autonomous-candidate-batch`; both keep `0` relation proposals and record
  `selectionReason: single_package_source_manifest_fallback`.
- The P29-T4 fallback preserves `preview_only`,
  `producer_preview_evidence_only`, producer receipt, validation report,
  diagnostics, author-ready quality report, and SpecPM registry acceptance
  boundaries.
- `P29-T5` implemented bounded LM Studio/OpenAI-compatible JSON repair/retry
  for live package-set AI draft and enrichment proposal generation. Proposal
  receipts now record `jsonRepairNeeded`, `jsonRepairAttemptCount`, and
  `jsonRepairStatus`; diagnostics include `ai_json_repair_needed` and
  `ai_json_repair_exhausted`; autonomous batch AI records expose
  `diagnosticCodes` and `jsonRepair` summaries without persisting raw prompts,
  raw provider responses, secrets, or chain-of-thought.

## Outcome

SpecHarvester now has both concrete P29 technical-debt mitigations from the
first mixed corpus run: deterministic single-package fallback for Flask/Gin-style
repositories and bounded local model JSON repair diagnostics for LM
Studio/OpenAI-compatible proposal generation.

## Next Step

Implement `P29-T6`: re-run the mixed local Flask/Gin/xyflow corpus after
fallback and repair support, record whether each repository produces at least
one reviewable preview candidate, verify deterministic preflight, capture live
LM Studio status when available, and decide whether the autonomous candidate MVP
is ready for larger popular-library scraping.
