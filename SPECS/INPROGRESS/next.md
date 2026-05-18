# Recommended Task: P8-T1 - Document accepted package update lifecycle and immutability policy

**Priority:** P8
**Phase:** Accepted Specification Update Lifecycle
**Effort:** Medium
**Dependencies:** P7-T4
**Status:** Open
**Updated:** 2026-05-18
**Suggested Branch:** `feature/P8-T1-accepted-update-lifecycle-docs`
**Review Subject:** `p8_t1_accepted_update_lifecycle_docs`

**Current Phase:** ARCHIVE

## Execution Progress

- `2026-05-18`: task selected from `SPECS/Workplan.md`.
- `2026-05-18`: PRD created in `SPECS/INPROGRESS/...`.
- `2026-05-18`: accepted package update lifecycle documentation implemented in
  `docs/` and DocC mirrors.
- `2026-05-18`: validation report written to
  `SPECS/ARCHIVE/P8-T1_Document_accepted_package_update_lifecycle_and_immutability_policy/`.

## Description

Accepted SpecPM package metadata needs an explicit update lifecycle now that
SpecHarvester can generate, validate, and smoke-triage candidate metadata from
pinned upstream revisions.

Document how accepted package versions remain immutable, when upstream changes
should produce a new candidate/version, and how metadata corrections or errata
should be handled without pretending upstream content changed.

## Acceptance Criteria

- Documentation defines accepted package immutability expectations.
- Documentation separates upstream updates from metadata corrections.
- The lifecycle records expected audit trail fields for future automation:
  source revision, evidence digests, old/new package version, changed claims,
  validation status, and reviewer notes.
- The lifecycle keeps SpecPM review/merge as the acceptance boundary.
- Coverage and docs checks remain green.

## Recently Archived

- `P7-T3` Distinguish absent license evidence from ambiguous unknown license
  evidence: PASS,
  `SPECS/ARCHIVE/P7-T3_Distinguish_Absent_License_Evidence_from_Ambiguous_Unknown_License_Evidence/`.
- `P7-T4` Add a compact local smoke triage summary for batch and governance
  report output: PASS,
  `SPECS/ARCHIVE/P7-T4_Add_a_Compact_Local_Smoke_Triage_Summary_for_Batch_and_Governance_Report_Output/`.

## Next Step

Next task in sequence: `P8-T2`.
