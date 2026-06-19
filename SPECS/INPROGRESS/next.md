# Next Task: P39-T5 Repository Plugin Applicability Batch Integration

**Status:** Planned
**Branch:** `feature/P39-T5-repository-plugin-applicability-batch-integration`
**Phase:** Phase 39. Static Repository Plugin Applicability Evaluator
**Last Archived:** P39-T4 Repository Plugin Applicability Detect CLI

## Recently Archived

- `P39-T4` added `repository-plugin-applicability-detect`.
- The command reads explicit `--registry` and
  `--static-evidence-envelope` JSON files, writes the full
  `SpecHarvesterRepositoryPluginApplicabilityReport` to `--out`, and prints a
  compact JSON summary with selected/rejected/fallback/blocked/diagnostic
  counts.
- CLI regression tests cover success, invalid registry identity, unsafe static
  evidence paths, and missing evidence fallback behavior.
- The command does not change `autonomous-candidate-batch`, does not
  auto-attach generated reports, does not load or execute plugins, does not
  read repository source files, does not clone or fetch repositories, does not
  install dependencies, does not invoke package managers, does not execute
  harvested code, does not run AI, does not accept packages or relations, does
  not publish registry metadata, does not remove `preview_only`, and does not
  treat plugin decisions as registry truth.
- `P39-T3` implemented the deterministic helper:
  `spec_harvester.repository_plugin_applicability.evaluate_repository_plugin_applicability`.

## Current Task

`P39-T5` should integrate static evaluator output into
`autonomous-candidate-batch` as an opt-in auto sidecar path.

## Motivation

Operators can now generate a plugin applicability report through a standalone
CLI. The next step is to let autonomous batch create and record that report
when the operator explicitly opts in, while preserving the existing explicit
`--repository-plugin-applicability` sidecar as the highest-precedence input.

## Non-Goals

P39-T5 must not make plugin applicability automatic by default, must not
override explicit `--repository-plugin-applicability`, must not load
third-party plugin code, must not execute plugins, must not clone or fetch
repositories, must not install dependencies, must not invoke package managers,
must not execute harvested code, must not run AI, must not accept packages or
relations, must not publish registry metadata, must not remove `preview_only`,
and must not treat plugin decisions as registry truth.

## Planned Deliverables

- Add explicit opt-in autonomous batch inputs for registry plus static evidence
  envelope based applicability detection.
- Preserve explicit `--repository-plugin-applicability` precedence over any
  auto-generated report.
- Store auto-generated applicability output as sidecar producer evidence with
  `appliedToDrafting: false` and `registryAuthority: false`.
- Add regression tests for opt-in success, explicit sidecar precedence,
  non-default behavior, and invalid auto-detection inputs.
- Update GitHub docs and DocC docs.
- Keep real multi-repository validation deferred to P39-T6.
- Archive the task through Flow.
