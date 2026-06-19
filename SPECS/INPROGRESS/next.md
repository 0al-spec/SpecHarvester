# Next Task: P42-T1 Trusted Local Adapter Runtime Sandbox Plan

**Status:** In Progress
**Branch:** `feature/P42-T1-trusted-local-adapter-runtime-sandbox-plan`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P41-T6 Real Local Trusted-Adapter Readiness Validation

## Recently Archived

- `P41-T6` recorded real local trusted-adapter readiness validation over
  FastMCP, FastAPI, xyflow, and Gin.
- The readiness fixture proved `autonomous-candidate-batch --skip-ai
  --trusted-local-adapter-run-report` can carry explicit
  `trustedLocalAdapterRunEvidence` without running adapters.
- The preserved boundary remains `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `adapterProcessSpawned: false`,
  `executedAdapterCount: 0`, `appliedToDrafting: false`, and
  `registryAuthority: false`.
- Phase 41 intentionally left real adapter execution unimplemented.

## Task

Document the trusted local adapter runtime sandbox plan and add the next-task
scaffold for turning Phase 41 no-execution readiness into a future explicitly
approved sandboxed adapter runtime without enabling adapter execution yet.

## Why This Is Next

The current system can validate run requests, preflight them, emit a disabled
runner report, attach that report to batch output, and validate the path over
real pinned local repositories. The remaining gap is not code execution; it is
the sandbox contract that must exist before any future adapter process can be
launched.

## Scope

- Define the sandbox/runtime boundary for future trusted local adapter
  execution.
- Specify required operator approval, adapter package identity, process
  isolation, filesystem allowlists, environment sealing, dependency isolation,
  network-deny-by-default policy, timeout/output budgets, output digests, and
  audit records.
- Document how runtime output remains producer-side review evidence.
- Add GitHub docs, DocC docs, roadmap/capability references, and docs-contract
  regression coverage.
- Add a next-task scaffold for the first future machine-readable sandbox
  contract fixture.

## Non-Goals

- Do not implement real adapter execution.
- Do not load third-party adapter code.
- Do not spawn adapter processes.
- Do not install dependencies.
- Do not invoke package managers.
- Do not allow network discovery.
- Do not execute harvested repository code.
- Do not run AI because of adapter execution.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output, runner reports, or sandbox plans as registry
  truth.

## Phase 42. Trusted Local Adapter Runtime Sandbox

- [ ] `P42-T1` Document the trusted local adapter runtime sandbox plan and add
  the next-task scaffold for turning Phase 41 no-execution readiness into a
  future explicitly approved sandboxed adapter runtime without enabling adapter
  execution yet.

Motivation:

- Phase 41 proves the no-execution path; Phase 42 must define the sandbox
  before implementation.
- Real adapter execution requires process isolation, adapter package identity,
  dependency isolation, environment sealing, output verification, and explicit
  approval.
- A sandbox plan keeps future adapters useful for repository-specific quality
  while preserving SpecPM/maintainer authority.

Goal:

- Establish the runtime sandbox contract boundary before any adapter process
  can run.

Acceptance:

- Docs and DocC define the runtime sandbox boundary and remaining gaps.
- No code path enables adapter execution.
- The plan preserves explicit operator approval, no network by default,
  no dependency installation by default, safe input/output policies, output
  digests, and review-only authority.
