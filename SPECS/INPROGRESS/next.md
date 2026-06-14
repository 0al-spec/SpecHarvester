# Next Task: P32-T3 Xyflow Package-Set Identity Regeneration Dry Run

**Status:** In Progress
**Selected:** 2026-06-13
**Task:** P32-T3 Xyflow Package-Set Identity Regeneration Dry Run
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness
**Last Archived:** P32-T2 Deferred Candidate Regeneration Runbook

## Recently Archived

- `P32-T1` updated `docs/AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md` and
  `<doc:AutonomousCandidateTechDebtPlan>` as the current Phase 32 plan. It
  distinguishes completed P29 debt from current P30/P31 deferred-candidate
  debt, names all six deferred candidates, defines P32-T1 through P32-T7 with
  repository owners, and keeps broad autonomous scraping, package acceptance,
  relation acceptance, registry publication, baseline seeding, dependency
  installation, and harvested-code execution out of scope.
- `P32-T2` added `docs/DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md` and
  `<doc:DeferredCandidateRegenerationRunbook>`. It maps
  `package_set_identity_regeneration`,
  `warning_bearing_enrichment_regeneration`, and
  `identity_drift_resolution` to safe local commands, expected artifacts, stop
  conditions, re-entry criteria, and non-authority boundaries for
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`,
  `cupertino.core`, and `navigation_split_view.core`.

## Outcome

P32-T2 is complete. The deferred candidate regeneration runbook now defines
the safe operator path for local pinned checkouts, bounded model calls,
reviewable output roots, candidate-layer triage, expected artifacts, and hard
stop conditions before any deferred candidate can re-enter selected handoff.

## Next Step

Implement `P32-T3`: run the xyflow package-set identity regeneration dry run
using the P32-T2 runbook.

The dry run should cover `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`,
and `xyflow.system`; preserve the `xyflow.workspace` package-set identity;
verify the contains topology; run producer preflight; render the static
viewer; and keep `preview_only` plus `external_required` intact. The outcome
should record whether the regenerated xyflow candidates can enter selected
handoff or must remain deferred.
