# Next Task: P32-T4 Single-Package Deferred Candidate Regeneration Dry Run

**Status:** In Progress
**Selected:** 2026-06-13
**Task:** P32-T4 Single-Package Deferred Candidate Regeneration Dry Run
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness
**Last Archived:** P32-T3 Xyflow Package-Set Identity Regeneration Dry Run

## Recently Archived

- `P32-T2` added `docs/DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md` and
  `<doc:DeferredCandidateRegenerationRunbook>`. It maps
  `package_set_identity_regeneration`,
  `warning_bearing_enrichment_regeneration`, and
  `identity_drift_resolution` to safe local commands, expected artifacts, stop
  conditions, re-entry criteria, and non-authority boundaries for
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`,
  `cupertino.core`, and `navigation_split_view.core`.
- `P32-T3` recorded the xyflow-only package-set identity regeneration dry run
  in `docs/XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md`,
  `<doc:XyflowPackageSetIdentityRegenerationDryRun>`, and
  `tests/fixtures/xyflow_package_set_identity_regeneration/p32-t3-xyflow-package-set-identity-regeneration.example.json`.
  The run processed only `xyflow`, kept package-set identity
  `xyflow.workspace`, produced `xyflow.react`, `xyflow.svelte`, and
  `xyflow.system` members, preserved three `contains` relations, passed
  bundle-set preflight with warning count `0` and error count `0`, rendered the
  static viewer, kept `preview_only`, and recorded
  `candidate_layer_review_required` with `selectedHandoffEligible: true`.

## Outcome

P32-T3 is complete. The xyflow package-set identity blocker is resolved enough
for the regenerated xyflow candidates to re-enter candidate-layer review and a
future refreshed selected handoff, while remaining producer preview evidence
only.

## Next Step

Implement `P32-T4`: run single-package deferred candidate regeneration or
repair for `cupertino.core` and `navigation_split_view.core` using the P32-T2
runbook.

The run should resolve or explicitly keep deferred the Cupertino
`refined_summary_missing` warning and the NavigationSplitView identity drift
around `navigation-split-view.core` versus `navigation_split_view.core`. It
must preserve `preview_only`, keep registry acceptance external, avoid package
execution or dependency installation, and record whether each candidate can
enter refreshed candidate-layer review.
