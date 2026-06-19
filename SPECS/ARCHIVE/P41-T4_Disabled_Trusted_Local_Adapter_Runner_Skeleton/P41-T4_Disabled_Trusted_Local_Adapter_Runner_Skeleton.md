# P41-T4 Disabled Trusted Local Adapter Runner Skeleton

**Branch:** `feature/P41-T4-disabled-trusted-local-adapter-runner-skeleton`
**Status:** Planned
**Phase:** Phase 41. Trusted Local Adapter Runtime Readiness

## Motivation

P41-T2 defines `SpecHarvesterTrustedLocalAdapterRunRequest`, and P41-T3
defines `SpecHarvesterTrustedLocalAdapterRunPreflightReport`. The next
readiness layer needs a concrete local skeleton that consumes those artifacts
and emits a runner report without enabling adapter execution.

This task is intentionally conservative. It proves the future runner boundary
is machine-readable before any runtime implementation exists. The skeleton
must not import adapter code, spawn adapter processes, install dependencies,
invoke package managers, execute harvested repository code, or run AI.

## Goal

Add a disabled-by-default trusted local adapter runner skeleton that validates
request and preflight identities, verifies the request/preflight linkage, and
emits a deterministic `SpecHarvesterTrustedLocalAdapterRunReport` with
`adapterExecution: not_run`, `adapterCodeLoaded: false`,
`executedAdapterCount: 0`, `runtimeImplemented: false`,
`appliedToDrafting: false`, and `registryAuthority: false`.

## Deliverables

1. Add a small runner helper and CLI entry point for a no-execution trusted
   local adapter run skeleton.
2. Validate the request artifact identity:
   `apiVersion`, `kind`, `schemaVersion`, `authority`, and non-authority
   boundaries.
3. Validate the preflight artifact identity:
   `apiVersion`, `kind`, `schemaVersion`, `authority`, and pass status.
4. Verify that the preflight report references the request path and SHA-256
   digest that the runner receives.
5. Emit a deterministic JSON report with a stable contract identity, request
   reference, preflight reference, disabled runtime state, and non-authority
   statements.
6. Reject identity or digest mismatches before emitting a pass-like report.
7. Add regression tests for success, request identity failure, preflight
   identity failure, digest mismatch, and CLI output.
8. Add GitHub docs and DocC docs for the runner skeleton.
9. Update index docs, capabilities, roadmap, readiness docs, Workplan, and
   `next.md`.

## Acceptance Criteria

- The runner skeleton is disabled by default and has no execution mode.
- The skeleton validates request and preflight identities before report
  emission.
- The skeleton validates the request digest recorded by preflight.
- The emitted report records:
  - `adapterExecution: not_run`
  - `adapterCodeLoaded: false`
  - `executedAdapterCount: 0`
  - `runtimeImplemented: false`
  - `appliedToDrafting: false`
  - `registryAuthority: false`
  - `requestIsExecutionPermission: false`
  - `preflightPassIsExecutionPermission: false`
  - `runnerReportIsExecutionPermission: false`
- The report is deterministic for the same input artifacts.
- Docs and DocC explain that the skeleton is not real adapter execution, not
  registry acceptance, and not adapter output truth.
- Existing tests, lint, format, DocC build, and coverage gates pass.

## Non-Goals

- Do not implement real adapter execution.
- Do not load third-party adapter code.
- Do not run adapter processes.
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

## Dependencies

- P41-T2 `SpecHarvesterTrustedLocalAdapterRunRequest` fixture.
- P41-T3 `SpecHarvesterTrustedLocalAdapterRunPreflightReport` fixture.
- P41-T1 trusted local adapter runtime readiness plan.
- Phase 40 repository plugin adapter contract and disabled execution policy.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_trusted_local_adapter_runner.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q`
