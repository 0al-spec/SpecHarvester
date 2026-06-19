# P41-T2 Trusted Local Adapter Run Request Fixture

**Branch:** `feature/P41-T2-trusted-local-adapter-run-request-fixture`
**Status:** Planned
**Phase:** Phase 41. Trusted Local Adapter Runtime Readiness

## Motivation

P41-T1 documented the readiness path from Phase 40 repository plugin adapter
contracts toward a future trusted local adapter runtime. Before any preflight
or no-execution runner can exist, SpecHarvester needs a stable request shape
that records exactly what an operator is asking to run, which static adapter
contracts it is tied to, which local evidence may be read, and which outputs
may be written.

This task creates that request contract as a fixture and documentation surface
only. It does not grant execution authority and does not implement adapter
loading, adapter processes, preflight logic, or a runner.

## Goal

Add a machine-readable
`SpecHarvesterTrustedLocalAdapterRunRequest` fixture that can become the root
input for future trusted local adapter run preflight while preserving the
disabled-by-default, review-only, non-authoritative boundary from Phase 40.

## Deliverables

1. Add a versioned
   `tests/fixtures/repository_plugins/trusted_local_adapter_run_request.example.json`
   fixture.
2. Reference the Phase 40 adapter manifest and adapter preflight report
   fixtures with SHA-256 digests.
3. Record explicit operator opt-in and the fact that the request is not
   permission to execute by itself.
4. Record declared input artifacts with safe relative paths and SHA-256
   digests.
5. Record safe relative read path allowlists and output directory policy.
6. Record resource budgets: timeout, max output bytes, max file count, and max
   diagnostics count.
7. Record environment, network, dependency, package manager, process, harvested
   code, and AI execution policy.
8. Record non-authority statements and follow-up tasks.
9. Add GitHub docs and DocC docs for the fixture.
10. Update index docs, capabilities, roadmap, and readiness docs.
11. Add regression tests covering the fixture shape and documentation links.

## Acceptance Criteria

- The fixture has `apiVersion`, `kind`, `schemaVersion`, stable authority, and
  contract metadata.
- The fixture references:
  - `tests/fixtures/repository_plugins/adapter-manifest.example.json`;
  - `tests/fixtures/repository_plugins/adapter-preflight-report.example.json`.
- Every artifact path in the fixture is POSIX relative, contains no `..`,
  contains no backslash, and has a `sha256:` digest.
- Operator opt-in is explicit and scoped to future trusted local preflight.
- Network access, dependency installation, package manager invocation,
  harvested code execution, AI execution, and unbounded process execution are
  denied.
- Output policy is limited to declared output directories and bounded size.
- The fixture states that request presence is not execution permission, not
  package acceptance, not relation acceptance, not baseline seeding, not
  registry publication, and not registry truth.
- Docs and DocC explain the request/preflight/runner boundary.
- `tests/test_docs_contracts.py` validates the fixture and docs.

## Non-Goals

- Do not implement adapter loading or execution.
- Do not run adapter processes.
- Do not implement trusted local adapter run preflight logic.
- Do not add a runner.
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

- P40-T2 `SpecHarvesterRepositoryPluginAdapterManifest` fixture.
- P40-T3 `SpecHarvesterRepositoryPluginAdapterPreflightReport` fixture.
- P41-T1 Trusted Local Adapter Runtime Readiness plan.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q`
