# P42-T10 Disabled Explicit Real Local Trusted Adapter Sandbox Runner Skeleton

## Summary

Add a deterministic disabled runner skeleton fixture/report for the explicit
real local trusted adapter sandbox path. The skeleton validates that a future
runtime entry point can consume the P42-T8 request and P42-T9 preflight
artifacts without loading adapter code, spawning adapter processes, or granting
execution/registry authority.

## Motivation

P42-T8 records the explicit real-run request. P42-T9 validates that request as
review evidence. Before any actual runtime work exists, the project needs a
disabled runner skeleton that proves the consumer boundary:

```text
P42-T8 request
  + P42-T9 request preflight
  -> disabled runner skeleton
  -> future reviewed runtime only after explicit approval
```

This prevents future implementation from silently treating request/preflight
artifacts as execution permission. It also creates a stable test fixture for
linkage validation, blocked execution drift, auditability, and non-authority
statements.

## Deliverables

- Add a machine-readable disabled runner skeleton fixture under
  `tests/fixtures/repository_plugins/`.
- Reference the P42-T8 request fixture with a pinned SHA-256 digest.
- Reference the P42-T9 request preflight fixture with a pinned SHA-256 digest.
- Validate:
  - request API version, kind, schema version, authority, and digest;
  - preflight API version, kind, schema version, authority, digest, and passed
    review-only result;
  - request/preflight agreement on request identity and digest;
  - no-execution runtime boundary;
  - no adapter code loading, process spawning, dependency installation,
    package-manager invocation, network access, harvested-code execution, or AI
    execution;
  - no package acceptance, relation acceptance, baseline seeding, registry
    publishing, `preview_only` removal, or adapter output acceptance.
- Declare rejected and blocked drift shapes.
- Add GitHub docs, DocC docs, roadmap/capabilities links, Flow archive, review,
  and validation artifacts.

## Acceptance Criteria

- The skeleton fixture uses:
  - `apiVersion:
    spec-harvester.disabled-explicit-real-local-trusted-adapter-sandbox-runner/v0`;
  - `kind:
    SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRunnerReport`;
  - `schemaVersion: 1`;
  - producer-side disabled-runner-only authority.
- The fixture references the P42-T8 request fixture and verifies its digest.
- The fixture references the P42-T9 preflight fixture and verifies its digest.
- The fixture validates that the P42-T9 preflight points to the same P42-T8
  request digest.
- The result status is disabled/review-only and does not grant execution
  permission.
- Tests fail if the skeleton drifts toward adapter code loading, process
  spawning, dependency installation, package-manager invocation, network use,
  harvested-code execution, AI execution, package/relation acceptance, registry
  authority, adapter output truth, or reusable permission.
- CLI/runtime behavior remains unchanged: no real adapter execution is
  implemented or enabled.

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
- Do not treat the request fixture as execution permission.
- Do not treat preflight pass as execution permission.
- Do not treat the disabled runner skeleton as execution permission.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_disabled_explicit_real_local_sandbox_runner_skeleton_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `python3 -m json.tool tests/fixtures/repository_plugins/disabled-explicit-real-local-trusted-adapter-sandbox-runner.example.json >/dev/null`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- DocC static generation
