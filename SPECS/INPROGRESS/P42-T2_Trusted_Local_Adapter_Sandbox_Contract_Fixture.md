# P42-T2 Trusted Local Adapter Sandbox Contract Fixture

## Summary

Add a machine-readable
`SpecHarvesterTrustedLocalAdapterSandboxContract` fixture for the Phase 42
trusted local adapter runtime sandbox boundary. This turns the P42-T1 prose
plan into reviewable data without enabling adapter execution.

## Motivation

P42-T1 defines the sandbox layers required before SpecHarvester can run trusted
local adapter code. Future preflight and runner tasks need a stable contract
that records the same boundary as data: adapter package identity, sandbox
policy identity, explicit operator approval, process/filesystem/environment/
dependency/network constraints, output verification, audit requirements, and
non-authority statements.

The fixture must make the future runtime safer by constraining it before
implementation, not by granting permission to execute.

## Deliverables

- Add
  `tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-contract.example.json`.
- Document the fixture in GitHub docs and DocC.
- Link the fixture from sandbox plan, readiness docs, README, capabilities, and
  roadmap.
- Add regression coverage that validates the fixture shape, required boundary
  fields, docs links, and no-execution/non-authority claims.
- Update workplan, next task, and archive artifacts through the Flow process.

## Acceptance Criteria

- The fixture has:
  - `apiVersion: spec-harvester.trusted-local-adapter-sandbox-contract/v0`;
  - `kind: SpecHarvesterTrustedLocalAdapterSandboxContract`;
  - `schemaVersion: 1`;
  - producer-side review-only authority.
- The fixture records adapter package identity, sandbox policy identity,
  operator approval requirements, process policy, filesystem policy,
  environment policy, dependency policy, network-deny-by-default policy, output
  verification requirements, audit requirements, diagnostics, and follow-up
  tasks.
- The fixture preserves no-execution fields:
  - `adapterExecution: not_run`;
  - `adapterCodeLoaded: false`;
  - `adapterProcessSpawned: false`;
  - `executedAdapterCount: 0`;
  - `registryAuthority: false`.
- The fixture explicitly states that it does not accept packages, accept
  relations, seed baselines, publish registry metadata, remove `preview_only`,
  or treat adapter output/sandbox contracts as registry truth.
- Docs and tests prove the fixture is producer-side review evidence only.

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
- Do not treat adapter output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_trusted_local_adapter_sandbox_contract_fixture_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing --cov-fail-under=90 -q`
- DocC static generation
