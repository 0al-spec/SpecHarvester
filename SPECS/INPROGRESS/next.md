# Selected Task: P2-T4 — Document Sandbox Requirements for Analyzers That Need Build Tools

**Priority:** P2
**Phase:** Analyzer Policy and Cache
**Effort:** Medium
**Dependencies:** P2-T1, P2-T2, P2-T3
**Status:** Selected
**Updated:** 2026-05-17
**Branch:** `feature/P2-T4-document-sandbox-requirements-for-analyzers-that-need-build-tools`
**Review Subject:** `p2_t4_analyzer_sandbox_requirements`

## Description

Document sandbox requirements for analyzers that cannot stay purely static and
need metadata-only build tools, while preserving the no package-script,
no-network, no-untrusted-code-execution trust boundary.

## Coverage Note

P2-T3 finished with 90.62% total coverage, improving on the P2-T2 baseline of
90.57%. Future implementation tasks should continue to avoid coverage decline
by adding focused tests for any new behavior.

## Recently Archived

- `P2-T3` Add parse diagnostics and partial-index behavior: PASS,
  `SPECS/ARCHIVE/P2-T3_Add_Parse_Diagnostics_and_Partial_Index_Behavior/`.
- `P2-T2` Add per-file analyzer cache keyed by file digest and analyzer
  version: PASS,
  `SPECS/ARCHIVE/P2-T2_Add_Per_File_Analyzer_Cache_Keyed_by_File_Digest_and_Analyzer_Version/`.

## Next Step

Run PLAN for `P2-T4` and create
`SPECS/INPROGRESS/P2-T4_Document_Sandbox_Requirements_for_Analyzers_That_Need_Build_Tools.md`.
