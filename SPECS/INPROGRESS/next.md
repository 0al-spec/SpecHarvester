# Recommended Task: P6-T4 - Add reproducible local smoke-test fixture documentation

**Priority:** P6
**Phase:** Smoke-Test Feedback
**Effort:** Medium
**Dependencies:** P5-T3, P6-T1
**Status:** Open
**Updated:** 2026-05-18
**Suggested Branch:** `feature/P6-T4-add-reproducible-local-smoke-test-fixture-documentation`
**Review Subject:** `p6_t4_smoke_test_fixture_docs`

**Current Phase:** SELECT

## Description

Formalize how local smoke tests are authored, executed, and documented for
repeatability across machines and repositories.

Create deterministic fixture instructions and canonical artifact folders so repeat
runs do not pollute repository state or depend on ad-hoc file placement.

## Acceptance Criteria

- Repository-level documentation explains smoke fixture directories and command
  conventions.
- Reproducible command snippets are available for the locally validated Cupertino,
  xyflow, docc2context, and Puzzle repositories.
- Generated smoke output is clearly separated from committed artifacts and ignored
  by version control by default.
- The process remains local-only and low-cost to rerun.

## Recently Archived

- `P5-T2` Add namespace and upstream relationship review report: PASS,
  `SPECS/ARCHIVE/P5-T2_Add_Namespace_and_Upstream_Relationship_Review_Report/`.
- `P5-T3` Add license and provenance risk report: PASS,
  `SPECS/ARCHIVE/P5-T3_Add_License_and_Provenance_Risk_Report/`.
- `P6-T1` Discover nested Swift package manifests during static harvest: PASS,
  `SPECS/ARCHIVE/P6-T1_Discover_Nested_Swift_Package_Manifests_during_Static_Harvest/`.
- `P6-T2` Infer candidate license metadata from allowlisted LICENSE files: PASS,
  `SPECS/ARCHIVE/P6-T2_Infer_Candidate_License_Metadata_from_License_Files/`.
- `P6-T3` Make namespace and upstream owner comparison case-insensitive: PASS,
  `SPECS/ARCHIVE/P6-T3_Make_Namespace_Upstream_Owner_Comparison_Case_Insensitive/`.

## Next Step

Plan task `P6-T4` when ready.
