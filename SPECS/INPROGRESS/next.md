# Recommended Task: P3-T2 — Collect Snapshots for Selected Repositories into Deterministic Candidate Paths

**Priority:** P3
**Phase:** Batch Harvesting
**Effort:** Medium
**Dependencies:** P3-T1, P0-T1, P2-T1
**Status:** Recommended
**Updated:** 2026-05-17
**Suggested Branch:** `feature/P3-T2-collect-snapshots-for-selected-repositories-into-deterministic-candidate-paths`
**Suggested Review Subject:** `p3_t2_batch_snapshot_collection`

## Description

Use validated repository source manifests to collect snapshots for selected
local checkouts into deterministic candidate paths without executing package
content or contacting package managers.

## Coverage Note

P3-T1 finished with 91.40% total coverage, improving on the P2-T4 baseline of
90.62%. Future implementation tasks should continue to add focused tests so
coverage does not decline.

## Recently Archived

- `P3-T1` Read repository source manifests from `inputs/*.yml`: PASS,
  `SPECS/ARCHIVE/P3-T1_Read_Repository_Source_Manifests_from_inputs_yml/`.
- `P2-T4` Document sandbox requirements for analyzers that need build tools:
  PASS,
  `SPECS/ARCHIVE/P2-T4_Document_Sandbox_Requirements_for_Analyzers_That_Need_Build_Tools/`.

## Next Step

Run BRANCH for `P3-T2` when ready.
