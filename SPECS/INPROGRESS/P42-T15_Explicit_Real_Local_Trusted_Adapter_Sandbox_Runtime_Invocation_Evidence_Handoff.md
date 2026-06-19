# P42-T15 Explicit Real Local Trusted Adapter Sandbox Runtime Invocation Evidence Handoff

## Summary

Add a deterministic runtime invocation evidence handoff for the explicit real
local trusted adapter sandbox path. The handoff packages the P42-T13 operator
approval binding and P42-T14 disabled runtime invocation skeleton as portable
review evidence before any real adapter runtime implementation.

## Motivation

P42-T14 validates approval binding through a disabled invocation skeleton, but
reviewers need one portable artifact that ties together what was approved, what
the disabled invocation checked, and why execution remains blocked.

```text
P42-T13 operator approval binding
  + P42-T14 disabled runtime invocation skeleton
  -> runtime invocation evidence handoff
  -> future real runtime implementation review
```

This prevents a later runtime implementation review from relying on scattered
fixture files or treating disabled invocation evidence as execution permission.

## Deliverables

- Add a machine-readable runtime invocation evidence handoff fixture under
  `tests/fixtures/repository_plugins/`.
- Reference P42-T13 with pinned digest:
  `sha256:c1d60ef17d878ca0a6119d28d51a61898828f0d34f77460ba16b912d76386b95`.
- Reference P42-T14 with pinned digest:
  `sha256:626e9b8affbf6a668e3da13b32b7b3df8b4976e643eb3ccd9fe33df65fa1237d`.
- Package:
  - approval binding evidence;
  - disabled invocation evidence;
  - linked artifact digests;
  - approval scope summary;
  - audit requirements;
  - execution boundary;
  - non-authority statements.
- Preserve:
  - `handoffIsExecutionPermission: false`;
  - `handoffIsRegistryAuthority: false`;
  - `approvalConsumedByRuntime: false`;
  - `runtimeInvoked: false`;
  - `adapterCodeLoaded: false`;
  - `adapterCodeImportAttempted: false`;
  - `adapterProcessSpawned: false`;
  - `adapterOutputAccepted: false`.
- Add GitHub docs, DocC docs, roadmap/capabilities links, Flow archive, review,
  and validation artifacts.

## Acceptance Criteria

- The handoff fixture uses:
  - `apiVersion:
    spec-harvester.explicit-real-local-trusted-adapter-sandbox-runtime-invocation-evidence-handoff/v0`;
  - `kind:
    SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationEvidenceHandoff`;
  - `schemaVersion: 1`;
  - producer-side runtime-invocation-evidence-handoff-only authority.
- The fixture references P42-T13 and P42-T14 with pinned SHA-256 digests and
  verified safe relative paths.
- The fixture requires P42-T13 approval binding status
  `approval_bound_runtime_still_blocked`.
- The fixture requires P42-T14 invocation status `blocked_no_execution`.
- The fixture records that approval is not consumed by a runtime.
- The fixture rejects missing linked artifacts, digest mismatch, execution
  permission, registry authority, approval consumption, adapter code loading,
  adapter imports, adapter process spawning, dependency installation, package
  manager invocation, network access, runtime invocation, and adapter output as
  registry truth.
- Tests fail if the handoff grants execution permission, grants registry
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
- Do not treat P42-T13 or P42-T14 as execution permission.
- Do not consume approval by a real runtime.
- Do not treat adapter output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_explicit_real_local_sandbox_runtime_invocation_evidence_handoff_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `python3 -m json.tool tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-runtime-invocation-evidence-handoff.example.json >/dev/null`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- DocC static generation
