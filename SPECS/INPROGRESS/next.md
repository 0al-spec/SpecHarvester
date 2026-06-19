# Next Task: P41-T1 Adapter Runtime Readiness Plan

**Status:** In Progress
**Branch:** `feature/P41-T1-adapter-runtime-readiness-plan`
**Phase:** Phase 41. Trusted Local Adapter Runtime Readiness
**Last Archived:** P40-T7 Real Local Adapter-Contract Validation

## Recently Archived

- `P40-T7` recorded real local adapter-contract validation over existing
  pinned local checkouts.
- The machine-readable fixture is
  `tests/fixtures/repository_plugins/adapter_real_runs/p40-t7-real-local-adapter-contract-validation.example.json`.
- The validation covers FastMCP as `nested_package_roots`, FastAPI as
  `documentation_heavy_repository`, xyflow as `workspace_or_multi_package`,
  and Gin as `manifest_backed_single_package`.
- Every case records `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `appliedToDrafting: false`, and
  `registryAuthority: false`.
- The validation remains producer-side evidence only and does not load or
  execute third-party adapter code.

## Task

Document the trusted local adapter runtime readiness plan and add the
next-task scaffold for turning Phase 40 adapter contracts into a future opt-in
runtime without enabling adapter execution yet.

## Why This Is Next

Phase 40 is complete. It defines the adapter contract and proves the no-runtime
boundary with fixtures and real local checkouts. The next step is to plan the
safe transition toward a future trusted local adapter runtime before creating
any run request, preflight report, or runner skeleton.

## Scope

- Add Phase 41 to `SPECS/Workplan.md`.
- Define P41 tasks for trusted local adapter run request, preflight, disabled
  no-execution skeleton, batch evidence handoff, and real local readiness
  validation.
- Document motivation, goal, acceptance criteria, and non-authority boundaries.
- Keep adapter execution disabled.
- Select P41-T2 as the next task after archive.
- Update regression docs tests for the new planning state.

## Non-Goals

- Do not implement adapter loading or execution.
- Do not add a runner in this task.
- Do not create trusted local adapter run request fixtures in this task.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output as registry truth.

## Phase 41. Trusted Local Adapter Runtime Readiness

- [ ] `P41-T1` Document the trusted local adapter runtime readiness plan and
  add the next-task scaffold for turning Phase 40 adapter contracts into a
  future opt-in runtime without enabling adapter execution yet.
- [ ] `P41-T2` Add a machine-readable
  `SpecHarvesterTrustedLocalAdapterRunRequest` fixture that records operator
  opt-in, adapter manifest/preflight references, declared input artifacts,
  safe relative read path allowlists, output directory policy, resource
  budgets, environment policy, network policy, dependency policy, package
  manager policy, and non-authority statements.
- [ ] `P41-T3` Add a trusted local adapter run preflight report fixture that
  validates run requests before execution and rejects unsafe paths, missing
  digests, missing operator opt-in, network access, dependency installation,
  package manager invocation, harvested code execution, unbounded process
  execution, and undeclared outputs.
- [ ] `P41-T4` Implement a disabled-by-default trusted local adapter runner
  skeleton that can validate a request and emit a no-execution report without
  loading third-party adapter code or running adapter processes.
- [ ] `P41-T5` Connect trusted local adapter run reports to
  `autonomous-candidate-batch` as explicit review-only producer evidence while
  preserving the default static evaluator and existing adapter sidecar paths.
- [ ] `P41-T6` Run a real local trusted-adapter readiness validation over
  existing pinned checkouts, comparing FastMCP, FastAPI, xyflow, and Gin while
  proving no adapter process, package manager, dependency installer, network
  discovery, harvested code, or AI execution occurred.

Motivation:

- Future adapter runtime work needs a safe request/preflight boundary before
  any adapter process can be launched.
- Operator opt-in, path allowlists, resource budgets, and no-authority output
  handling should be documented before implementation starts.
- The next phase should improve ecosystem-specific precision without turning
  SpecHarvester into a hidden execution runtime.

Goal:

- Establish Phase 41 as the readiness path from Phase 40 contracts toward a
  future trusted local adapter runtime while preserving disabled-by-default
  execution and review-only producer evidence.

Acceptance:

- Phase 41 is present in Workplan.
- P41-T1 has a PRD, validation, archive, and review artifact.
- P41-T2 is selected as the next task after archive.
- No adapter loading or execution is implemented.
- Docs/tests capture the same no-runtime and non-authority boundaries as
  Phase 40.
