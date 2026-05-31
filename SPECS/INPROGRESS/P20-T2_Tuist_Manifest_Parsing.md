# P20-T2 Tuist Manifest Parsing

**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Status:** Planned
**Date:** 2026-05-31

## Problem

P20-T1 records `Project.swift`, `Workspace.swift`, and `Tuist.swift` as Tuist
manifest evidence, but it does not extract useful static metadata from them.
Scoped Swift folders in Tuist monorepos therefore still look like generic Swift
source units instead of named projects/targets with platform and source-glob
hints.

## Deliverables

- Add a deterministic text parser for Tuist manifests that never executes Tuist,
  Swift, package scripts, build tools, or repository code.
- Extract bounded metadata from common Tuist shapes:
  - project/workspace names;
  - target names;
  - product hints;
  - platform/destination hints;
  - source/resource glob strings.
- Attach parsed Tuist metadata to collected manifest file records.
- Feed ProjectProfile with Tuist project/target evidence while preserving
  existing Swift public API analyzer planning.
- Add regression tests for `Project.swift`, `Workspace.swift`, scoped folder
  collection, and parse-tolerant unsupported shapes.
- Update operator documentation and Flow archive artifacts.

## Non-Goals

- Do not execute Swift syntax, Tuist, SwiftPM, package managers, build tools, or
  repository code.
- Do not attempt to be a full Swift parser.
- Do not integrate `codegraph`; that remains `P20-T3`.
- Do not change SpecPM validation semantics.

## Acceptance Criteria

- `collect-local` records `tuist` metadata on Tuist manifest records when common
  static patterns are present.
- Unknown or complex Tuist syntax is tolerated by returning partial metadata
  rather than failing collection.
- Existing SwiftPM parsing and repository-root collection behavior remain
  compatible.
- Scoped folder targets can use parsed Tuist metadata as package/project
  evidence in generated candidate specs.
- Configured quality gates pass or any skipped gate is explicitly documented.
