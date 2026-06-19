# P42-T3 Trusted Local Adapter Sandbox Preflight Report Fixture

## Summary

Add a machine-readable
`SpecHarvesterTrustedLocalAdapterSandboxPreflightReport` fixture that validates
the P42-T2 `SpecHarvesterTrustedLocalAdapterSandboxContract` before any sandbox
runner implementation exists.

## Motivation

P42-T2 makes the trusted local adapter sandbox contract explicit as data. The
next boundary is a review-only preflight report that records which contract
shape is acceptable, which unsafe shapes must be rejected, and which runtime
steps remain blocked before adapter code can be loaded or processes can be
spawned.

The preflight fixture is still not execution permission. It is a gate shape for
future tooling and a review artifact for maintainers.

## Deliverables

- Add
  `tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-preflight-report.example.json`.
- Document the fixture in GitHub docs and DocC.
- Link the fixture from sandbox contract fixture docs, sandbox plan, README,
  capabilities, roadmap, and tests.
- Add regression coverage that validates fixture identity, contract digest
  linkage, accepted/rejected/blocked checks, no-execution fields, and
  non-authority statements.
- Update workplan, next task, and archive artifacts through the Flow process.

## Acceptance Criteria

- The fixture has:
  - `apiVersion: spec-harvester.trusted-local-adapter-sandbox-preflight/v0`;
  - `kind: SpecHarvesterTrustedLocalAdapterSandboxPreflightReport`;
  - `schemaVersion: 1`;
  - producer-side review-only authority.
- The fixture references
  `SpecHarvesterTrustedLocalAdapterSandboxContract` by safe relative path,
  kind, authority, and SHA-256 digest.
- The fixture records:
  - `result.status: passed`;
  - `decision: sandbox_preflight_passed_review_only`;
  - `preflightPassIsExecutionPermission: false`;
  - accepted checks for contract identity, digest linkage, operator approval
    requirements, process/filesystem/environment/dependency/network policy,
    output verification, audit requirements, execution boundary, and
    non-authority statements;
  - rejected unsafe-shape checks;
  - blocked runtime checks.
- The fixture preserves:
  - `adapterExecution: not_run`;
  - `adapterCodeLoaded: false`;
  - `adapterProcessSpawned: false`;
  - `executedAdapterCount: 0`;
  - `registryAuthority: false`.
- Docs and tests prove the fixture is producer-side review evidence only.

## Non-Goals

- Do not implement real adapter execution.
- Do not implement a sandbox runner.
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
- Do not treat sandbox preflight as registry truth.
- Do not treat adapter output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_trusted_local_adapter_sandbox_preflight_report_fixture_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing --cov-fail-under=90 -q`
- DocC static generation
