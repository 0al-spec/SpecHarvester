# Next Task: P32-T5 Refreshed Candidate-Layer Triage and Selected Handoff

**Status:** In Progress
**Selected:** 2026-06-13
**Task:** P32-T5 Refreshed Candidate-Layer Triage and Selected Handoff
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness
**Last Archived:** P32-T4 Single-Package Deferred Candidate Regeneration Dry Run

## Recently Archived

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
- `P32-T4` recorded the single-package deferred candidate regeneration dry run
  in `docs/SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md`,
  `<doc:SinglePackageDeferredCandidateRegenerationDryRun>`, and
  `tests/fixtures/single_package_deferred_candidate_regeneration/p32-t4-single-package-deferred-candidate-regeneration.example.json`.
  The run classified `navigation_split_view.core` as
  `candidate_layer_review_required` with `selectedHandoffEligible: true`, and
  kept `cupertino.core` at `needs_regeneration` because
  `refined_summary_missing` remains unresolved. The artifact remains producer
  preview evidence only.

## Outcome

P32-T4 is complete. The limited corpus now has regenerated evidence for the
xyflow package-set candidates and the NavigationSplitView single-package
candidate. Cupertino remains explicitly deferred until regenerated enrichment
or author-curated summary evidence resolves its missing refined summary.

## Next Step

Implement `P32-T5`: produce refreshed candidate-layer triage and selected
handoff evidence for regenerated candidates that satisfy hard gates.

The refreshed triage should include:

- original selected candidates from P30-T5: `flask.core`, `gin.core`, and
  `docc2context.core`;
- regenerated eligible candidates from P32-T3 and P32-T4:
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
  `navigation_split_view.core`;
- explicitly deferred candidates such as `cupertino.core` with the remaining
  blocker `refined_summary_missing`.

The selected handoff must preserve `preview_only`,
`producer_preview_evidence_only`, static viewer evidence, producer preflight
status, digest-backed evidence roles, and `external_required` registry
acceptance decisions. It must not accept packages, accept relations, seed
baselines, remove `preview_only`, publish registry metadata, or create a
SpecPM pull request.
