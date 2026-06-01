# P20-T4 — Scoped Source Validation Fixtures

**Status:** Completed
**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Date:** 2026-06-01

## Problem

SpecHarvester can harvest scoped repository roots, folders, and files, but the
current coverage is split across focused unit tests. Phase 20 needs a stable
validation matrix that represents the real monorepo shapes motivating scoped
source-unit specs.

## Goals

- Add deterministic scoped-source fixture coverage for a Tuist-managed Swift
  folder, a single-file target, and a non-Swift folder target.
- Verify inherited root license evidence for scoped targets.
- Verify source target metadata is preserved in `harvest.json` and batch output.
- Verify interface analyzer output stays scoped to the selected folder or file.
- Preserve the no-execution trust boundary: no repository code, package scripts,
  Tuist, build tools, network calls, or third-party graph tools are executed.

## Non-Goals

- Do not add live local repository smoke output.
- Do not add CodeGraph integration or CodeGraph live tests.
- Do not change drafting prompt behavior for source-unit intent; that remains
  `P20-T5`.
- Do not broaden analyzer execution beyond existing deterministic static
  analyzers.

## Deliverables

- A synthetic monorepo validation fixture in tests that covers:
  - Tuist-managed Swift folder target.
  - Single-file source target.
  - Non-Swift folder target.
- Assertions for `harvest.json`, `public-interface-index.json`, and batch result
  metadata.
- Validation report with exact project quality gate results.

## Acceptance Criteria

- Scoped folder/file collection does not include unrelated sibling module files.
- Root license evidence is inherited for scoped folder and file targets.
- Tuist folder metadata is collected without executing Tuist or Swift.
- Python/non-Swift folder interface evidence is emitted only for selected files.
- Single-file target interface evidence is emitted for that file only.
- Full tests, ruff, coverage, Swift manifest, and DocC build pass.
