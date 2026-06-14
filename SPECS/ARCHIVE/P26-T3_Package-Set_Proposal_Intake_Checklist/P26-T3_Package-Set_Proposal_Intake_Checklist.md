# P26-T3 Package-Set Proposal Intake Checklist

**Status:** Planned
**Selected:** 2026-06-13
**Phase:** Phase 26. Package-Set SpecPM Handoff Automation

## Motivation

P26-T1 added `SpecHarvesterPackageSetHandoffProposal`, and P26-T2 made
package-set proposal artifacts safe to attach without write credentials. The
remaining gap is the producer-side documentation of what SpecPM maintainers
should check before accepting package-set members or relations.

Without an explicit intake checklist, package-set evidence can look more
authoritative than it is. SpecHarvester can show member packages, relation
proposals, bundle-set preflight, viewer output, and external acceptance
decision boundaries, but SpecPM remains the authority for package acceptance,
relation acceptance, registry metadata, and maintainer approval.

## Goal

Define the SpecPM-facing package-set proposal intake checklist and evidence
roles required before maintainers accept package members or relations from a
`SpecHarvesterPackageSetHandoffProposal`.

## Deliverables

- Add a GitHub docs page for package-set proposal intake checklist.
- Add a DocC mirror page and link it from the root topics.
- Link the checklist from package-set handoff proposal docs, SpecPM handoff
  docs, proposal automation docs, roadmap, and docs index.
- Add docs-contract tests that pin checklist terms, evidence roles, acceptance
  boundaries, and `next.md` state.
- Archive Flow artifacts and leave the next pointer in a neutral selection
  state for the remaining backlog.

## Acceptance Criteria

- The checklist names `SpecHarvesterPackageSetHandoffProposal` and
  `spec-harvester.package-set-handoff-proposal/v0`.
- The checklist requires package-set identity, member package evidence,
  relation proposal evidence, bundle-set preflight, viewer links, and
  `authorReadyDraftSummary` review.
- The checklist distinguishes package member acceptance from relation
  acceptance.
- The checklist records required evidence roles, including
  `package_set_draft`, `package_relation_proposals`, `bundle_set_preflight`,
  `package_set_viewer`, `member_candidate_bundle`, `member_manifest`,
  `member_boundary_spec`, `member_producer_receipt`, `member_validation_report`,
  `member_diagnostics`, `member_quality_report`, and
  `package_relation_summary`.
- The checklist preserves `registryAcceptanceDecision.status:
  external_required`, `public_index_acceptance`, and
  `package_relation_acceptance` boundaries.
- The checklist states that producer evidence does not accept packages, accept
  relations, publish registry metadata, mutate SpecPM sources, remove
  `preview_only`, or replace maintainer review.
- Project gates pass.

## Non-Goals

- No CLI or helper behavior changes.
- No package-set proposal fixture regeneration.
- No SpecPM repository changes.
- No registry mutation.
- No package or relation acceptance.

## Archive Status

Archived: 2026-06-13
Verdict: PASS
