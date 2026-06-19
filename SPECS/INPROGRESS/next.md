# Next Task: P39-T6 Real Multi-Repository Static Evaluator Validation

**Status:** Planned
**Branch:** `feature/P39-T6-real-multi-repository-static-evaluator-validation`
**Phase:** Phase 39. Static Repository Plugin Applicability Evaluator
**Last Archived:** P39-T5 Repository Plugin Applicability Batch Integration

## Recently Archived

- `P39-T5` connected the deterministic repository plugin applicability
  evaluator to `autonomous-candidate-batch`.
- The batch now accepts explicit `--repository-plugin-registry` and
  `--repository-plugin-static-evidence-envelope` inputs as an opt-in
  auto-generated sidecar path.
- Explicit `--repository-plugin-applicability` remains the highest-precedence
  input and records `sourceMode: explicit_sidecar`.
- Auto-generated reports record `sourceMode: auto_static_evaluator`,
  selected/rejected/fallback/blocked/diagnostic counts, digest, diagnostic
  codes, `appliedToDrafting: false`, and `registryAuthority: false`.
- Regression tests cover default non-generation, opt-in generation, explicit
  sidecar precedence, partial auto-input rejection, and invalid static evidence
  rejection.
- The integration does not make plugin applicability automatic by default, does
  not override explicit sidecars, does not load or execute plugins, does not
  read repository source files, does not clone or fetch repositories, does not
  install dependencies, does not invoke package managers, does not execute
  harvested code, does not run AI, does not accept packages or relations, does
  not publish registry metadata, does not remove `preview_only`, and does not
  treat plugin decisions as registry truth.

## Current Task

`P39-T6` should run a real multi-repository static evaluator validation over
existing local checkouts, comparing FastMCP, FastAPI, and xyflow style
repository shapes.

## Motivation

P39-T5 proved the batch integration contract with fixtures. The next step is to
verify that the static evaluator and batch sidecar path behave sensibly across
real local repositories with different shapes:

- single-package Python/web framework style repositories;
- documentation-heavy Python repositories;
- JavaScript/TypeScript workspace/package-set repositories.

## Non-Goals

P39-T6 must not clone or fetch repositories, must not install dependencies,
must not run package managers, must not execute harvested code, must not invoke
AI, must not change parser/profile behavior, must not accept packages or
relations, must not publish registry metadata, must not remove `preview_only`,
and must not treat plugin decisions as registry truth.

## Planned Deliverables

- Reuse already available local checkouts for FastMCP, FastAPI, and xyflow when
  present.
- Build static evidence envelopes from existing collected outputs or fixture
  inputs.
- Run `repository-plugin-applicability-detect` and
  `autonomous-candidate-batch` opt-in sidecar generation where practical.
- Record a machine-readable real-run comparison fixture.
- Add docs/DocC notes summarizing outcomes and limitations.
- Add regression coverage for the comparison fixture shape and boundaries.
- Archive the task through Flow.
