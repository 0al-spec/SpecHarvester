# Recommended Task: P8-T3 - Classify update proposals by metadata, interface, license, provenance, capability, and intent impact

**Priority:** P8
**Phase:** Accepted Specification Update Lifecycle
**Effort:** Medium
**Dependencies:** P8-T2
**Status:** Open
**Updated:** 2026-05-18
**Suggested Branch:** `feature/P8-T3-update-impact-classification`
**Review Subject:** `p8_t3_update_impact_classification`

**Current Phase:** SELECT

## Execution Progress

- `2026-05-18`: `P8-T2` completed and archived.

## Description

Classify accepted/candidate update diffs by metadata, interface, license,
provenance, capability, and intent impact so reviewers can prioritize update
proposal risk before SpecPM review.

## Acceptance Criteria

- Classification consumes accepted/candidate diff report output or equivalent
  deterministic comparison data.
- Classification separates metadata, interface, license, provenance, capability,
  and intent impact buckets.
- Classification remains advisory and does not mutate package content.
- Report output remains deterministic and reviewable.
- Coverage and docs checks remain green.

## Recently Archived

- `P7-T4` Add a compact local smoke triage summary for batch and governance
  report output: PASS,
  `SPECS/ARCHIVE/P7-T4_Add_a_Compact_Local_Smoke_Triage_Summary_for_Batch_and_Governance_Report_Output/`.
- `P8-T1` Document accepted package update lifecycle and immutability policy:
  PASS,
  `SPECS/ARCHIVE/P8-T1_Document_accepted_package_update_lifecycle_and_immutability_policy/`.
- `P8-T2` Add accepted-vs-candidate package diff report: PASS,
  `SPECS/ARCHIVE/P8-T2_Add_accepted-vs-candidate_package_diff_report/`.

## Next Step

Plan task `P8-T3` when ready.
