# Next Task: P32-T2 Deferred Candidate Regeneration Runbook

**Status:** In Progress
**Selected:** 2026-06-13
**Task:** P32-T2 Deferred Candidate Regeneration Runbook
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness
**Last Archived:** P32-T1 Autonomous Deferred Candidate Work Plan

## Recently Archived

- `P31-T5` recorded deferred selected-candidate regeneration requirements in
  `docs/DEFERRED_SELECTED_CANDIDATE_REGENERATION_REQUIREMENTS.md`,
  `<doc:DeferredSelectedCandidateRegenerationRequirements>`, and the
  `SpecHarvesterDeferredSelectedCandidateRegenerationRequirements` fixture
  `p31-t5-deferred-selected-candidate-regeneration-requirements.example.json`.
  The fixture covers all six deferred P30 candidates, package-set identity
  regeneration, warning-bearing enrichment regeneration, identity-drift
  resolution, source digests, minimum proof before selected handoff, and the
  non-authority boundary. It remains regeneration requirements only and not
  package acceptance.
- `P26-T3` documented the package-set proposal intake checklist in
  `docs/PACKAGE_SET_PROPOSAL_INTAKE_CHECKLIST.md` and
  `<doc:PackageSetProposalIntakeChecklist>`. It names
  `SpecHarvesterPackageSetHandoffProposal`,
  `spec-harvester.package-set-handoff-proposal/v0`, required package-set and
  member evidence roles, `registryAcceptanceDecision.status:
  external_required`, `producerAuthority: evidence_only`, and the rule that
  package member acceptance is separate from relation acceptance.
- `P32-T1` updated `docs/AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md` and
  `<doc:AutonomousCandidateTechDebtPlan>` as the current Phase 32 plan. It
  distinguishes completed P29 debt from current P30/P31 deferred-candidate
  debt, names all six deferred candidates, defines P32-T1 through P32-T7 with
  repository owners, and keeps broad autonomous scraping, package acceptance,
  relation acceptance, registry publication, baseline seeding, dependency
  installation, and harvested-code execution out of scope.

## Outcome

P32-T1 is complete. The deferred candidate work plan now defines the bounded
sequence for turning P30/P31 deferred candidates into regenerated, repaired, or
explicitly still-deferred evidence before any broader autonomous scraping.

## Next Step

Implement `P32-T2`: add the deferred candidate regeneration runbook.

The runbook should map `package_set_identity_regeneration`,
`warning_bearing_enrichment_regeneration`, and `identity_drift_resolution` to
safe local commands, expected artifacts, stop conditions, and non-authority
boundaries before any regeneration run is attempted.
