# Next Task: P39-T4 Repository Plugin Applicability Detect CLI

**Status:** Planned
**Branch:** `feature/P39-T4-repository-plugin-applicability-detect-cli`
**Phase:** Phase 39. Static Repository Plugin Applicability Evaluator
**Last Archived:** P39-T3 Deterministic Static Applicability Evaluator Helper

## Recently Archived

- `P39-T3` implemented
  `spec_harvester.repository_plugin_applicability.evaluate_repository_plugin_applicability`.
  The helper reads already-loaded
  `SpecHarvesterRepositoryPluginRegistry` and
  `SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` JSON objects, compares
  declared `inputEvidenceKinds[]` with available `evidenceKinds[]`, and emits
  `SpecHarvesterRepositoryPluginApplicabilityReport`.
- The helper preserves `producer_plugin_applicability_only` authority,
  selected/rejected/fallback/blocked decision arrays, stable diagnostics, safe
  relative evidence paths, SHA-256 digest validation, and non-authority
  statements.
- The helper does not load plugins, execute plugins, read repository source
  files, clone or fetch repositories, install dependencies, invoke package
  managers, execute harvested code, run AI, accept packages or relations,
  publish registry metadata, remove `preview_only`, or treat plugin decisions
  as registry truth.
- `P39-T2` added the machine-readable static plugin evidence envelope fixture
  in
  `tests/fixtures/repository_plugins/static-evidence-envelope.example.json`.
- `P39-T1` documented the static repository plugin applicability evaluator
  plan in `STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md`.

## Current Task

`P39-T4` should expose the P39-T3 helper through a deterministic
`repository-plugin-applicability-detect` CLI/report surface.

## Motivation

P39-T3 made applicability evaluation testable as a helper, but operators and
CI still need a stable command that can read a registry JSON file plus static
evidence envelope JSON file and write a reviewable
`repository-plugin-applicability-report.json` artifact.

## Non-Goals

P39-T4 must not change `autonomous-candidate-batch`, must not auto-attach the
generated report to candidate output, must not load third-party plugin code,
must not execute plugins, must not clone or fetch repositories, must not
install dependencies, must not invoke package managers, must not execute
harvested code, must not run AI, must not accept packages or relations, must
not publish registry metadata, must not remove `preview_only`, and must not
treat plugin decisions as registry truth.

## Planned Deliverables

- Add a `repository-plugin-applicability-detect` CLI command.
- Accept explicit `--registry` and `--static-evidence-envelope` inputs.
- Write `SpecHarvesterRepositoryPluginApplicabilityReport` JSON to `--out`.
- Print a compact summary for selected/rejected/fallback/blocked counts.
- Add CLI regression tests for success, bad input identity, unsafe paths, and
  missing evidence behavior.
- Update GitHub docs and DocC docs to document the command.
- Keep autonomous batch integration deferred to P39-T5.
- Archive the task through Flow.
