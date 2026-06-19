# Next Task: P40-T1 Repository Plugin Adapter Contract

**Status:** Planned
**Branch:** `feature/P40-T1-repository-plugin-adapter-contract`
**Phase:** Phase 40. Repository Plugin Adapter Contract
**Last Archived:** P39-T6 Real Multi-Repository Static Evaluator Validation

## Recently Archived

- `P39-T6` recorded real multi-repository static evaluator validation for
  FastMCP, FastAPI, and xyflow local checkouts.
- The durable fixture is
  `tests/fixtures/repository_plugins/real_runs/p39-t6-multi-repository-static-evaluator-validation.example.json`.
- All three local checkouts were available and clean:
  - `fastmcp` -> `generic.single_package.v0`;
  - `fastapi` -> `generic.single_package.v0`;
  - `xyflow` -> `generic.package_set.v0`.
- Each case exercised both `repository-plugin-applicability-detect` and
  `autonomous-candidate-batch --repository-plugin-registry
  --repository-plugin-static-evidence-envelope`.
- Each generated sidecar recorded `sourceMode: auto_static_evaluator`,
  `appliedToDrafting: false`, and `registryAuthority: false`.
- The validation did not clone or fetch repositories, install dependencies,
  invoke package managers, execute harvested code, invoke AI, change
  parser/profile behavior, accept packages or relations, publish registry
  metadata, remove `preview_only`, or treat plugin decisions as registry truth.

## Task

Document a language- and framework-agnostic repository plugin adapter contract.

## Why This Is Next

Phase 39 can now derive repository plugin applicability from static evidence.
The next layer is the adapter boundary: future plugins must declare identity,
inputs, outputs, execution mode, sandbox expectations, diagnostics, and
authority limits before any runtime adapter path exists.

## Scope

- Define adapter identity, manifest versioning, roles, input evidence,
  output artifacts, execution modes, sandbox expectations, diagnostics, and
  non-authority statements.
- Keep Python, JavaScript, FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven,
  Gradle, and other ecosystems as examples, not normative rules.
- Keep static applicability evaluation as the default safe path.
- Require explicit future operator opt-in before any non-static adapter
  execution mode can be used.

## Non-Goals

- Do not implement adapter loading or execution.
- Do not load third-party adapter code.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output as registry truth.
