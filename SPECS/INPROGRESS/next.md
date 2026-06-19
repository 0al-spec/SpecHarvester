# Next Task: P39-T2 Static Plugin Evidence Envelope Fixture

**Status:** Planned
**Branch:** `feature/P39-T2-static-plugin-evidence-envelope-fixture`
**Phase:** Phase 39. Static Repository Plugin Applicability Evaluator
**Last Archived:** P39-T1 Static Repository Plugin Applicability Evaluator Plan

## Recently Archived

- `P39-T1` documented the static repository plugin applicability evaluator plan
  in `STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md`. The plan defines a
  deterministic path from `SpecHarvesterRepositoryPluginRegistry` plus a
  static evidence envelope to
  `SpecHarvesterRepositoryPluginApplicabilityReport`, with
  selected/rejected/fallback/blocked decisions,
  `repository-plugin-applicability-detect` as the future CLI surface,
  `--repository-plugin-applicability` preserving explicit operator sidecar
  precedence, `appliedToDrafting: false`, `registryAuthority: false`, and
  producer-side evidence that is not registry truth.
- `P38-T6` recorded a real FastMCP plugin evidence run in
  `tests/fixtures/repository_plugins/real_runs/p38-t6-fastmcp-plugin-evidence-comparison.example.json`.
- Phase 38 is complete: repository plugin applicability is now described as a
  producer-side evidence contract, represented by registry/applicability
  fixtures, attached to autonomous batch output as a sidecar, covered by
  cross-ecosystem static examples, and validated on a pinned local FastMCP
  checkout.

## Current Task

`P39-T2` should add a machine-readable static plugin evidence envelope fixture.

The fixture should declare the bounded evidence available to a future static
applicability evaluator before it emits
`SpecHarvesterRepositoryPluginApplicabilityReport`.

## Motivation

P39-T1 defined the evaluator plan, but the next implementation layer needs a
stable input artifact. The envelope should make source manifest metadata,
`harvest.json`, `workspace-inventory.json`,
`repository-profile-detection.json`, public-interface indexes, parser profile
decisions, and operator labels explicit before any selection logic runs.

## Non-Goals

P39-T2 must not implement evaluator logic, add a CLI, change autonomous batch
behavior, load third-party plugin code, execute plugins, clone or fetch
repositories, install dependencies, invoke package managers, execute harvested
code, run AI, accept packages or relations, publish registry metadata, remove
`preview_only`, or treat plugin decisions as registry truth.

It must not add a CLI; `repository-plugin-applicability-detect` remains P39-T4
scope. It must not execute plugins, must not run AI, and must not accept
packages or relations.

## Planned Deliverables

- Add a fixture such as
  `tests/fixtures/repository_plugins/static-evidence-envelope.example.json`.
- Define identity fields, source identity, evidence paths, digests,
  `evidenceKinds[]`, advisory signals, and authority statements.
- Link the envelope back to `SpecHarvesterRepositoryPluginRegistry` and forward
  to `SpecHarvesterRepositoryPluginApplicabilityReport`.
- Document the fixture in GitHub docs and DocC.
- Add regression coverage for fixture shape, safe paths, digest format,
  available evidence kinds, and non-authority boundaries.
- Archive the task through Flow.
