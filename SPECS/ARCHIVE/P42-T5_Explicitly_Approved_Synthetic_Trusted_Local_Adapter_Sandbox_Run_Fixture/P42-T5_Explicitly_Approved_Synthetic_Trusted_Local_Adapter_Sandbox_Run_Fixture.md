# P42-T5 Explicitly Approved Synthetic Trusted Local Adapter Sandbox Run Fixture

## Summary

Add a machine-readable
`SpecHarvesterSyntheticTrustedLocalAdapterSandboxRun` fixture that records the
approved-run boundary after P42-T4 disabled sandbox runner validation while
still avoiding real adapter execution.

## Motivation

P42-T2 defines the sandbox contract, P42-T3 defines the sandbox preflight
report, and P42-T4 validates their linkage through a disabled no-execution
runner validation report. Before any future real adapter process can run,
SpecHarvester needs an approved-run artifact shape that binds operator approval
to a specific adapter, repository, sandbox policy, runner validation input, and
output directory.

This task records that boundary as synthetic fixture evidence only. It proves
the approval, output, digest, audit, and non-authority shape without loading
adapter code, spawning a process, installing dependencies, using network
access, or accepting generated output as registry truth.

## Deliverables

- Add a machine-readable synthetic approved sandbox run fixture under
  `tests/fixtures/repository_plugins/`.
- Bind the fixture to:
  - `SpecHarvesterTrustedLocalAdapterSandboxContract`;
  - `SpecHarvesterTrustedLocalAdapterSandboxPreflightReport`;
  - `SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport`;
  - one adapter package identity;
  - one repository identity/revision;
  - one sandbox policy identity;
  - one declared output root.
- Include synthetic adapter output candidate references with safe relative
  paths, byte sizes, SHA-256 digests, producer run id, adapter id/digest, input
  digests, and diagnostics status.
- Include replayable audit record requirements and non-authority statements.
- Document the fixture in GitHub docs and DocC.
- Link the fixture from sandbox runner validation docs, sandbox plan, README,
  capabilities, roadmap, and tests.
- Add regression coverage for identity, approval binding, output digests,
  audit fields, no-real-execution state, and non-authority boundaries.
- Update workplan, next task, and archive artifacts through Flow.

## Acceptance Criteria

- The fixture has:
  - `apiVersion: spec-harvester.synthetic-trusted-local-adapter-sandbox-run/v0`;
  - `kind: SpecHarvesterSyntheticTrustedLocalAdapterSandboxRun`;
  - `schemaVersion: 1`;
  - producer-side review-only authority.
- The fixture references the P42-T2/P42-T3/P42-T4 artifacts by safe relative
  path, kind, authority, and SHA-256 digest.
- The operator approval block binds exactly one adapter, one repository
  revision, one sandbox policy, one runner validation report, and one output
  root.
- Synthetic output references use safe relative paths, byte sizes, SHA-256
  digests, adapter identity, input digests, diagnostics status, and candidate
  evidence authority.
- The execution boundary records:
  - `adapterExecution: synthetic_fixture_only`;
  - `realAdapterProcessSpawned: false`;
  - `thirdPartyAdapterCodeLoaded: false`;
  - `dependencyInstallation: not_allowed`;
  - `packageManagers: not_invoked`;
  - `networkAccess: none`;
  - `registryAuthority: false`.
- Docs and tests prove the fixture is producer-side review evidence only and
  cannot be interpreted as registry truth or permission for arbitrary real
  adapter execution.

## Non-Goals

- Do not implement real adapter execution.
- Do not load third-party adapter code.
- Do not spawn real adapter processes.
- Do not install dependencies.
- Do not invoke package managers.
- Do not allow network discovery.
- Do not execute harvested repository code.
- Do not run AI because of adapter execution.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat synthetic adapter output as registry truth.
- Do not treat sandbox runner validation as execution permission.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_synthetic_trusted_local_adapter_sandbox_run_fixture_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q`
- DocC static generation
