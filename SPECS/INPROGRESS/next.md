# Next Task: P39-T1 Static Repository Plugin Applicability Evaluator Plan

**Status:** Planned
**Branch:** `feature/P39-T1-static-plugin-applicability-evaluator-plan`
**Phase:** Phase 39. Static Repository Plugin Applicability Evaluator
**Last Archived:** P38-T6 Real Repository Plugin Evidence Run

## Recently Archived

- `P38-T6` recorded a real FastMCP plugin evidence run in
  `tests/fixtures/repository_plugins/real_runs/p38-t6-fastmcp-plugin-evidence-comparison.example.json`.
- Phase 38 is complete: repository plugin applicability is now described as a
  producer-side evidence contract, represented by registry/applicability
  fixtures, attached to autonomous batch output as a sidecar, covered by
  cross-ecosystem static examples, and validated on a pinned local FastMCP
  checkout.

## Current Task

`P39-T1` should document the static repository plugin applicability evaluator
plan.

The plan should describe how SpecHarvester can turn declared plugin registry
metadata plus collected static evidence into a deterministic
`SpecHarvesterRepositoryPluginApplicabilityReport`, without runtime plugin
loading or plugin execution.

## Motivation

P38 proved the shape of plugin applicability reports, but P38-T6 still used an
operator-authored sidecar. The next step is to make applicability derivation
deterministic from static artifacts such as `harvest.json`,
`workspace-inventory.json`, `repository-profile-detection.json`,
public-interface indexes, and operator labels.

## Non-Goals

P39-T1 must not implement the evaluator, add a CLI, change autonomous batch
behavior, load third-party plugin code, execute plugins, clone or fetch
repositories, install dependencies, invoke package managers, execute harvested
code, run AI, accept packages or relations, publish registry metadata, remove
`preview_only`, or treat plugin decisions as registry truth.

## Planned Deliverables

- Add a GitHub-facing plan for the static repository plugin applicability
  evaluator.
- Add a DocC mirror.
- Update capabilities, roadmap, and plugin subsystem docs to point to the new
  plan.
- Add regression coverage for the plan, next task state, and non-authority
  boundaries.
- Archive the task through Flow.
