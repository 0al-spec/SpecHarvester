# P41-T3 Trusted Local Adapter Run Preflight Report Fixture

**Branch:** `feature/P41-T3-trusted-local-adapter-run-preflight-report-fixture`
**Status:** Planned
**Phase:** Phase 41. Trusted Local Adapter Runtime Readiness

## Motivation

P41-T2 added the
`SpecHarvesterTrustedLocalAdapterRunRequest` fixture. Before a disabled runner
skeleton can validate requests, the project needs a reviewable preflight report
shape that shows how a request is checked and how unsafe request variants are
rejected or blocked.

This task creates the preflight report fixture and documentation only. It does
not implement preflight execution logic, does not load adapter code, and does
not run adapter processes.

## Goal

Add a machine-readable
`SpecHarvesterTrustedLocalAdapterRunPreflightReport` fixture that validates a
trusted local adapter run request shape, references the P41-T2 request by
SHA-256 digest, records accepted/rejected/blocked/warning checks, and preserves
the boundary that preflight pass is not execution permission.

## Deliverables

1. Add a versioned
   `tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json`
   fixture.
2. Reference the P41-T2
   `trusted-local-adapter-run-request.example.json` fixture with SHA-256
   digest.
3. Record checks for identity, schema version, authority, explicit operator
   opt-in, adapter contract references, declared input artifacts, path policy,
   read allowlists, output policy, resource budgets, environment policy,
   network policy, dependency policy, package manager policy, process policy,
   execution boundary, and non-authority statements.
4. Record rejected or blocked examples for unsafe paths, missing or mismatched
   digests, undeclared input artifacts, undeclared output paths, network
   access, dependency installation, package manager invocation, harvested code
   execution, AI execution, unbounded process execution, and unbounded outputs.
5. Add GitHub docs and DocC docs for the fixture.
6. Update index docs, capabilities, roadmap, readiness docs, and request docs.
7. Add regression tests covering the fixture shape and documentation links.

## Acceptance Criteria

- The fixture has `apiVersion`, `kind`, `schemaVersion`, stable authority, and
  contract metadata.
- The fixture references the P41-T2 request fixture with a correct `sha256:`
  digest.
- Passing checks prove the request identity, opt-in, safe path, digest, budget,
  policy, execution-boundary, and non-authority fields are internally
  consistent.
- Rejected/blocked checks cover unsafe paths, missing or mismatched digests,
  undeclared input artifacts, undeclared output paths, network access,
  dependency installation, package manager invocation, harvested code
  execution, AI execution, unbounded process execution, and unbounded outputs.
- The fixture keeps `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `executedAdapterCount: 0`, `requestIsExecutionPermission: false`,
  `preflightPassIsExecutionPermission: false`, and `registryAuthority: false`.
- Docs and DocC explain that preflight pass is not execution permission, not
  registry acceptance, and not adapter output truth.

## Non-Goals

- Do not implement adapter loading or execution.
- Do not run adapter processes.
- Do not implement a trusted local adapter run preflight CLI.
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

- P41-T2 `SpecHarvesterTrustedLocalAdapterRunRequest` fixture.
- P40-T2 adapter manifest fixture.
- P40-T3 adapter preflight report fixture.
- P41-T1 readiness plan.

## Validation Plan

- `python3 -m json.tool tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q`
