# P20-T6 CodeGraph Adapter Boundary

**Status:** Planned
**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Dependencies:** P20-T3, P20-T5

## Problem

P20-T3 found that CodeGraph can provide useful multi-language source graph
signals, but it is a third-party local binary with npm shim download behavior.
SpecHarvester needs an adapter boundary that can consume CodeGraph evidence
without making CodeGraph a default dependency or letting live tool execution
become implicit in harvest/draft flows.

## Goal

Implement an explicit opt-in CodeGraph adapter boundary that:

- never installs or downloads CodeGraph;
- can normalize existing CodeGraph JSON or SQLite evidence into a
  SpecHarvester-owned `source_graph_index` shape;
- records analyzer, executable, input, source target, and trust provenance;
- keeps the evidence assistive and untrusted by default.

## Deliverables

- Add a CodeGraph source graph adapter module with no import-time dependency on
  CodeGraph, npm, SQLite extensions, or repository code.
- Define the normalized `source_graph_index` payload shape with:
  - `schemaVersion`;
  - `kind`;
  - trust policy;
  - source target metadata;
  - input/provenance records;
  - summary counts;
  - bounded nodes, edges, and diagnostics.
- Add CLI coverage for normalizing a provided CodeGraph JSON file and, when
  practical with the Python standard library, a provided SQLite database path.
- Enforce safe relative paths, deterministic ordering, and size/count limits.
- Add tests for JSON normalization, SQLite normalization or a documented
  graceful skip path, unsafe path rejection, and unavailable-input failure.
- Document that P20-T7 owns pinned executable/version compatibility checks.

## Non-Goals

- Do not install CodeGraph.
- Do not run `npx`, npm install, GitHub downloads, or the CodeGraph shim.
- Do not index third-party repositories in ordinary CI.
- Do not make CodeGraph a default analyzer in batch collection.
- Do not treat `source_graph_index` as accepted SpecPM registry authority.
- Do not implement the P20-T7 pinned executable compatibility guard.

## Acceptance Criteria

- A maintainer can run a SpecHarvester command against an existing CodeGraph
  JSON or SQLite artifact and receive deterministic `source_graph_index` JSON.
- The normalized payload explicitly states `trustLevel:
  untrusted_optional_tool`, `executedRepositoryCode: false`, and `allowedNetwork:
  false`.
- Missing or unsafe inputs fail closed with structured diagnostics.
- No test requires CodeGraph, npm, network, or a repository build.
- Existing collector, drafter, SpecNode, and corpus tests keep passing.

## Validation Plan

- Targeted tests for the new adapter and CLI command.
- Full pytest suite.
- Ruff check and format check.
- Coverage gate with `--cov-fail-under=90`.
- Swift package manifest and docs target build.
- Advisory architecture lint if a new module or CLI command object is added.

---
**Archived:** 2026-06-14
**Verdict:** PASS
