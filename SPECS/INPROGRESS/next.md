# Next Task: P1-T1 — Define PublicInterfaceIndex Snapshot Schema

**Priority:** P1
**Phase:** Public Interface Indexing
**Effort:** Medium
**Dependencies:** P0-T1
**Status:** Selected
**Selected:** 2026-05-17
**Branch:** `feature/P1-T1-public-interface-index-schema`

## Description

Define the deterministic `PublicInterfaceIndex` evidence shape that future
static analyzers will emit into harvest snapshots without executing repository
content.

## Expected Artifacts

- `src/spec_harvester/interface_index.py`
- Tests covering deterministic schema construction and validation
- `SPECS/INPROGRESS/P1-T1_Define_PublicInterfaceIndex_Snapshot_Schema.md`
- `SPECS/INPROGRESS/P1-T1_Validation_Report.md`

## Next Step

Run the PLAN command to generate the implementation-ready PRD.
