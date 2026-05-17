# Recommended Task: P3-T1 — Read Repository Source Manifests from inputs/*.yml

**Priority:** P3
**Phase:** Batch Harvesting
**Effort:** Medium
**Dependencies:** P0-T1, P1-T1, P2-T1
**Status:** Recommended
**Updated:** 2026-05-17
**Suggested Branch:** `feature/P3-T1-read-repository-source-manifests-from-inputs-yml`
**Suggested Review Subject:** `p3_t1_repository_source_manifests`

## Description

Add the first batch-harvesting input surface by reading repository source
manifests from `inputs/*.yml` without executing package content or contacting
repository package managers.

## Coverage Note

P2-T4 finished with 90.62% total coverage, matching the P2-T3 baseline.
Implementation tasks should continue to add focused tests so coverage does not
decline.

## Recently Archived

- `P2-T4` Document sandbox requirements for analyzers that need build tools:
  PASS,
  `SPECS/ARCHIVE/P2-T4_Document_Sandbox_Requirements_for_Analyzers_That_Need_Build_Tools/`.
- `P2-T3` Add parse diagnostics and partial-index behavior: PASS,
  `SPECS/ARCHIVE/P2-T3_Add_Parse_Diagnostics_and_Partial_Index_Behavior/`.

## Next Step

Run BRANCH for `P3-T1` when ready.
