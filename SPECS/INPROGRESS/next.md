# Selected Task: P2-T3 — Add Parse Diagnostics and Partial-Index Behavior

**Priority:** P2
**Phase:** Analyzer Policy and Cache
**Effort:** Medium
**Dependencies:** P1-T1, P1-T2, P1-T3, P2-T1, P2-T2
**Status:** Selected
**Updated:** 2026-05-17
**Branch:** `feature/P2-T3-add-parse-diagnostics-and-partial-index-behavior`
**Review Subject:** `p2_t3_parse_diagnostics_partial_index`

## Description

Strengthen analyzer diagnostic behavior so parse failures and partial-index
cases are represented consistently, remain deterministic, and never require
repository code execution.

## Coverage Note

P2-T2 finished with 90.57% total coverage. This task should avoid further
coverage decline by adding focused tests for new diagnostic and partial-index
branches, not only relying on the global `--cov-fail-under=90` gate.

## Recently Archived

- `P2-T2` Add per-file analyzer cache keyed by file digest and analyzer
  version: PASS,
  `SPECS/ARCHIVE/P2-T2_Add_Per_File_Analyzer_Cache_Keyed_by_File_Digest_and_Analyzer_Version/`.
- `P2-T1` Add analyzer trust policy fields to harvest snapshots: PASS,
  `SPECS/ARCHIVE/P2-T1_Add_Analyzer_Trust_Policy_Fields_to_Harvest_Snapshots/`.

## Next Step

Run PLAN for `P2-T3` and create
`SPECS/INPROGRESS/P2-T3_Add_Parse_Diagnostics_and_Partial_Index_Behavior.md`.
