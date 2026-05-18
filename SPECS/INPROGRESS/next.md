# Recommended Task: P8-T2 - Add accepted-vs-candidate package diff report

**Priority:** P8
**Phase:** Accepted Specification Update Lifecycle
**Effort:** Medium
**Dependencies:** P8-T1
**Status:** Open
**Updated:** 2026-05-18
**Suggested Branch:** `feature/P8-T2-accepted-candidate-diff-report`
**Review Subject:** `p8_t2_accepted_candidate_diff_report`

**Current Phase:** SELECT

## Execution Progress

- `2026-05-18`: task selected from `SPECS/Workplan.md`.

## Description

Add a deterministic report that compares candidate `specpm.yaml` metadata
against currently accepted package metadata for the same package ID.

## Acceptance Criteria

- Report scans accepted and candidate roots without executing repository content.
- Report matches candidates to accepted packages by `metadata.id`.
- Report identifies new, unchanged, and changed package candidates.
- Report records changed metadata, added/removed intents, added/removed
  capabilities, and upstream artifact changes.
- Coverage and docs checks remain green.

## Recently Archived

- `P7-T4` Add a compact local smoke triage summary for batch and governance
  report output: PASS,
  `SPECS/ARCHIVE/P7-T4_Add_a_Compact_Local_Smoke_Triage_Summary_for_Batch_and_Governance_Report_Output/`.
- `P8-T1` Document accepted package update lifecycle and immutability policy:
  PASS,
  `SPECS/ARCHIVE/P8-T1_Document_accepted_package_update_lifecycle_and_immutability_policy/`.

## Next Step

Plan task `P8-T2` when ready.
