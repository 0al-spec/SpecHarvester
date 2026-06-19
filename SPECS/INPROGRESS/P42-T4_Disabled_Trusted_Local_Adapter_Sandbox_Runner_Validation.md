# P42-T4 Disabled Trusted Local Adapter Sandbox Runner Validation

## Summary

Add a disabled trusted local adapter sandbox runner validation surface that
checks linkage between the P42-T2
`SpecHarvesterTrustedLocalAdapterSandboxContract` fixture and the P42-T3
`SpecHarvesterTrustedLocalAdapterSandboxPreflightReport` fixture without
loading adapter code or running a sandboxed adapter process.

## Motivation

P42-T2 defines the sandbox contract and P42-T3 defines the review-only preflight
report. The next step is a deterministic validation step for future runner
inputs: it should prove that a runner can identify and link the approved
contract/preflight artifacts before any adapter execution capability exists.

This keeps the runtime boundary explicit. Passing validation is still not
operator approval, not execution permission, and not registry acceptance.

## Deliverables

- Add disabled trusted local adapter sandbox runner validation code.
- Add a CLI command that reads a sandbox contract and sandbox preflight report,
  validates identity and digest linkage, and emits a no-execution validation
  report.
- Preserve explicit no-execution fields:
  - `adapterExecution: not_run`;
  - `adapterCodeLoaded: false`;
  - `adapterProcessSpawned: false`;
  - `executedAdapterCount: 0`;
  - `registryAuthority: false`.
- Document the report shape in GitHub docs and DocC.
- Link the validation surface from sandbox plan/preflight docs, README,
  capabilities, roadmap, and tests.
- Add regression tests for the success path, CLI output, bad identity, and
  digest mismatch.
- Update workplan, next task, and archive artifacts through the Flow process.

## Acceptance Criteria

- The validation accepts the P42-T2 sandbox contract fixture and P42-T3 sandbox
  preflight report fixture.
- The validation rejects a contract with the wrong `apiVersion`, `kind`, or
  authority.
- The validation rejects a preflight report with the wrong `apiVersion`,
  `kind`, authority, or contract digest.
- The emitted report is machine-readable and includes:
  - `apiVersion`;
  - `kind`;
  - `schemaVersion: 1`;
  - producer-side review-only authority;
  - contract path/digest/kind/authority;
  - preflight path/digest/kind/authority;
  - runner disabled/no-execution state;
  - validation checks;
  - non-authority statements.
- The validation keeps all runtime authority disabled and cannot be interpreted
  as permission to load adapter code, spawn processes, install dependencies,
  invoke package managers, use network access, run AI, or publish registry
  data.
- Docs and tests prove the validation is producer-side review evidence only.

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
- Do not treat sandbox runner validation as registry truth.
- Do not treat adapter output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_trusted_local_adapter_sandbox_runner_validation_is_documented -q`
- `PYTHONPATH=src pytest tests/test_trusted_local_adapter_sandbox_runner.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing --cov-fail-under=90 -q`
- DocC static generation
