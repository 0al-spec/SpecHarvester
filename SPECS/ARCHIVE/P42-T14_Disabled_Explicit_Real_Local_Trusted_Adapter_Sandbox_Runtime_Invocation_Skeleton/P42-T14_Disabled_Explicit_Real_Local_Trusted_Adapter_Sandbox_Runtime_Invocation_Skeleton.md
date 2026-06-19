# P42-T14 Disabled Explicit Real Local Trusted Adapter Sandbox Runtime Invocation Skeleton

## Summary

Add a deterministic no-execution runtime invocation skeleton for the explicit
real local trusted adapter sandbox path. The skeleton consumes the P42-T13
operator approval binding, validates the approval scope, and emits a disabled
runtime invocation report without loading adapter code or spawning a process.

## Motivation

P42-T13 binds a future approval scope, but that binding is not execution
permission. Before any real runtime implementation can run adapters,
SpecHarvester needs a disabled invocation skeleton that proves the runtime will
validate the approval binding and still refuse execution until a later explicit
runtime implementation task.

```text
P42-T13 operator approval binding
  -> disabled runtime invocation skeleton
  -> future real runtime implementation only after review
```

## Deliverables

- Add a machine-readable disabled runtime invocation skeleton/report fixture
  under `tests/fixtures/repository_plugins/`.
- Reference the P42-T13 operator approval binding with pinned digest:
  `sha256:c1d60ef17d878ca0a6119d28d51a61898828f0d34f77460ba16b912d76386b95`.
- Validate approval binding identity, status, scope, adapter package identity,
  target repository revision, input artifact digests, output directory, runtime
  budgets, network policy, dependency policy, audit requirements, and
  non-authority statements.
- Preserve:
  - `runtimeInvocationAllowed: false`;
  - `adapterExecution: not_run`;
  - `adapterCodeLoaded: false`;
  - `adapterCodeImportAttempted: false`;
  - `adapterProcessSpawned: false`;
  - `approvalConsumedByRuntime: false`;
  - `dependencyInstallation: not_allowed`;
  - `packageManagers: not_invoked`;
  - `networkAccess: none`;
  - `registryAuthority: false`;
  - `adapterOutputAccepted: false`.
- Add GitHub docs, DocC docs, roadmap/capabilities links, Flow archive, review,
  and validation artifacts.

## Acceptance Criteria

- The skeleton/report fixture uses:
  - `apiVersion:
    spec-harvester.disabled-explicit-real-local-trusted-adapter-sandbox-runtime-invocation/v0`;
  - `kind:
    SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationReport`;
  - `schemaVersion: 1`;
  - producer-side disabled-runtime-invocation-only authority.
- The fixture references P42-T13 with a pinned SHA-256 digest and verified safe
  relative path.
- The fixture accepts only the P42-T13 bounded approval binding shape and
  rejects missing, mutable, reusable, unscoped, or execution-permission-like
  approval.
- The fixture records that approval is not consumed by a runtime.
- The fixture blocks adapter code loading, adapter imports, adapter process
  spawning, real runtime invocation, dependency installation,
  package-manager invocation, network access, harvested-code execution, AI
  execution, package acceptance, relation acceptance, baseline seeding,
  registry publishing, `preview_only` removal, and adapter output truth.
- Tests fail if the skeleton grants execution permission, grants registry
  authority, consumes approval by a runtime, loads/imports adapter code, spawns
  a process, or treats adapter output as truth.
- CLI/runtime behavior remains unchanged: no real adapter execution is
  implemented or enabled.

## Non-Goals

- Do not implement real adapter execution.
- Do not load third-party adapter code.
- Do not import adapter code.
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
- Do not treat P42-T13 as execution permission.
- Do not consume approval by a real runtime.
- Do not treat adapter output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_disabled_explicit_real_local_sandbox_runtime_invocation_skeleton_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `python3 -m json.tool tests/fixtures/repository_plugins/disabled-explicit-real-local-trusted-adapter-sandbox-runtime-invocation.example.json >/dev/null`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- DocC static generation

---
**Archived:** 2026-06-19
**Verdict:** PASS
