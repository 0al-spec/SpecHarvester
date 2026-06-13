# Next Task: P32-T1 Autonomous Deferred Candidate Work Plan

**Status:** In Progress
**Selected:** 2026-06-13
**Task:** P32-T1 Autonomous Deferred Candidate Work Plan
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness
**Last Archived:** P26-T3 Package-Set Proposal Intake Checklist

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

## Outcome

Phase 26 is complete. The next selected task turns the current autonomous
candidate technical debt into a concrete work plan. P29 fixed the original
Flask/Gin/xyflow runner debt, while P30/P31 exposed the next debt boundary:
selected candidates are handoff-ready, but deferred candidates still require
targeted regeneration, identity cleanup, or author-curated evidence before
SpecPM intake.

## Next Step

Implement `P32-T1`: update the autonomous candidate technical-debt plan,
roadmap, workplan, and docs-contract tests with a bounded sequence for
deferred candidate regeneration and SpecPM intake readiness.

The plan should cover `xyflow.*` package-set identity regeneration,
`cupertino.core` warning-bearing enrichment or author summary evidence,
`navigation_split_view.core` identity-drift resolution, refreshed triage,
selected handoff rerun, and the SpecPM-side consumer preflight boundary.
