# Recommended Task: P6-T3 - Make namespace and upstream owner comparison case-insensitive

**Priority:** P6
**Phase:** Smoke-Test Feedback
**Effort:** Medium
**Dependencies:** P5-T3, P6-T1
**Status:** Open
**Updated:** 2026-05-18
**Suggested Branch:** `feature/P6-T3-make-namespace-upstream-owner-comparison-case-insensitive`
**Review Subject:** `p6_t3_namespace_owner_case_insensitive`

**Current Phase:** SELECT

## Description

The local smoke test feedback surfaced owner-case mismatches between
candidate manifest namespaces and upstream URLs (for example `SoundBlaster` vs
`soundblaster`) which can be treated as false positives in review reports.

Make namespace and upstream owner comparison case-insensitive in the namespace
review report while preserving all existing behavior around missing or conflicting
ownership evidence.

## Acceptance Criteria

- The namespace comparison in `src/spec_harvester/namespace_reports.py` ignores
  case for namespace strings derived from package records and upstream owners.
- Existing behavior around missing upstream info and explicit ownership conflicts is
  preserved.
- Review report output remains deterministic and sorted.
- Coverage remains above the project threshold.

## Recently Archived

- `P5-T2` Add namespace and upstream relationship review report: PASS,
  `SPECS/ARCHIVE/P5-T2_Add_Namespace_and_Upstream_Relationship_Review_Report/`.
- `P5-T3` Add license and provenance risk report: PASS,
  `SPECS/ARCHIVE/P5-T3_Add_License_and_Provenance_Risk_Report/`.
- `P6-T1` Discover nested Swift package manifests during static harvest: PASS,
  `SPECS/ARCHIVE/P6-T1_Discover_Nested_Swift_Package_Manifests_during_Static_Harvest/`.
- `P6-T2` Infer candidate license metadata from allowlisted LICENSE files: PASS,
  `SPECS/ARCHIVE/P6-T2_Infer_Candidate_License_Metadata_from_License_Files/`.

## Next Step

Plan task `P6-T3` when ready.
