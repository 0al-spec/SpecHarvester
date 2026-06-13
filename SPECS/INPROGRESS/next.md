# Next Task: P29-T3 Corpus Baseline and Gap Report

**Status:** In Progress
**Selected:** 2026-06-13
**Task:** P29-T3 Corpus Baseline and Gap Report
**Phase:** Phase 29. Autonomous Candidate Harvest MVP
**Last Archived:** P29-T2 SpecPM Candidate-Layer Intake Policy

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

## Outcome

SpecHarvester now has both an autonomous batch runner and a SpecPM-facing
candidate-layer intake policy. Producer output can be reviewed as evidence
without implying accepted registry authority.

## Next Step

Implement `P29-T3`: record the Flask, Gin, and xyflow autonomous batch corpus
baseline and gap report.

The baseline should capture deterministic `--skip-ai` outcomes and a live
LM Studio outcome when available. It should record candidate counts, relation
counts, preflight status, author-ready stop-policy status, and AI status. It
must explicitly mark Flask and Gin as `single_package_fallback_needed`, mark
malformed model JSON as `ai_json_repair_needed` when observed, and preserve the
boundary that no generated preview candidate is promoted to SpecPM acceptance.
