# P20-T7 CodeGraph Compatibility Guard

**Status:** Planned
**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Dependencies:** P20-T6

## Problem

P20-T6 added an adapter that normalizes existing CodeGraph JSON or SQLite
evidence. SpecHarvester still needs an offline compatibility guard that records
the pinned CodeGraph interface expectations and verifies the mapping into
`source_graph_index` without indexing third-party repositories in ordinary CI.

## Goal

Add a pinned CodeGraph compatibility guard that verifies:

- expected CodeGraph package metadata;
- binary availability contract;
- required JSON-producing CLI flags;
- fixture-backed normalized schema mapping.

The guard must remain offline and must not install CodeGraph, run npm/npx, or
index repositories in CI.

## Deliverables

- Add a pinned CodeGraph compatibility fixture with expected package name,
  version, integrity, binary contract, required JSON CLI commands, and sample
  JSON records consumed by the adapter.
- Add a compatibility report builder/CLI command that validates the fixture and
  normalized `source_graph_index` mapping.
- If an executable path is explicitly provided, verify only local availability
  and version-output compatibility; otherwise report the executable check as
  skipped, not failed.
- Add docs/DocC coverage for the compatibility guard and its no-indexing CI
  boundary.
- Add regression tests for passing fixture validation, missing command flag
  failure, normalized mapping failure, and optional executable skip behavior.

## Non-Goals

- Do not install CodeGraph.
- Do not run npm, `npx`, GitHub downloads, or the CodeGraph shim.
- Do not index third-party repositories.
- Do not require a live CodeGraph executable in ordinary CI.
- Do not change the `source_graph_index` adapter payload shape unless a mapping
  bug is found.

## Acceptance Criteria

- The compatibility guard emits a deterministic JSON report.
- The report verifies the pinned package version/integrity metadata from the
  local fixture.
- The report verifies required JSON CLI command expectations:
  `status`, `query`, `files`, `callers`, `callees`, `impact`, and `affected`.
- The report validates that fixture records normalize into
  `schemaVersion: spec-harvester-codegraph-v1` and `kind: source_graph_index`.
- CI can run the guard without CodeGraph, npm, network, or repository indexing.

## Validation Plan

- Targeted tests for the compatibility report and CLI command.
- Full pytest suite.
- Ruff check and format check.
- Coverage gate with `--cov-fail-under=90`.
- Swift package manifest and docs target build.
- Advisory architecture lint for the new module/command path.

---
**Archived:** 2026-06-14
**Verdict:** PASS
