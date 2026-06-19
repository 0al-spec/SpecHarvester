# P42-T17 Disabled Explicit Real Local Trusted Adapter Sandbox Runtime Implementation Skeleton

## Summary

Add a deterministic disabled runtime implementation skeleton for the explicit
real local trusted adapter sandbox path. The skeleton consumes the P42-T16
runtime implementation review packet and records the future runtime surface
without loading adapter code, importing adapter modules, spawning processes, or
consuming approval.

## Motivation

P42-T16 records the implementation prerequisites, but it intentionally does not
name the future runtime implementation surface. Reviewers now need a disabled
skeleton that makes the future runtime shape explicit before any executable
runtime behavior exists:

```text
P42-T16 runtime implementation review packet
  -> disabled runtime implementation skeleton
  -> future implementation verifier/review
  -> future bounded real local adapter run
```

This keeps implementation design review separate from runtime execution and
prevents the project from treating a skeleton as permission to load or invoke
trusted local adapters.

## Deliverables

- Add a machine-readable disabled runtime implementation skeleton fixture under
  `tests/fixtures/repository_plugins/`.
- Reference P42-T16 with pinned digest:
  `sha256:f29f3deaaf7b3f1ebe140eb2eef09aab1716d0524138d95997e51b9f1b03f2a5`.
- Record disabled runtime surface fields for:
  - entrypoint isolation;
  - process launcher boundary;
  - dependency policy;
  - network policy;
  - output writer;
  - audit writer;
  - rollback handler;
  - approval consumption boundary.
- Preserve:
  - `implementationSkeletonIsExecutionPermission: false`;
  - `implementationSkeletonIsRegistryAuthority: false`;
  - `approvalConsumedByRuntime: false`;
  - `runtimeImplemented: false`;
  - `runtimeInvoked: false`;
  - `adapterCodeLoaded: false`;
  - `adapterCodeImportAttempted: false`;
  - `adapterProcessSpawned: false`;
  - `adapterOutputAccepted: false`.
- Add GitHub docs, DocC docs, roadmap/capabilities links, Flow archive, review,
  and validation artifacts.

## Acceptance Criteria

- The skeleton fixture uses:
  - `apiVersion:
    spec-harvester.disabled-explicit-real-local-trusted-adapter-sandbox-runtime-implementation-skeleton/v0`;
  - `kind:
    SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationSkeleton`;
  - `schemaVersion: 1`;
  - producer-side disabled-runtime-implementation-skeleton-only authority.
- The fixture references P42-T16 with a pinned SHA-256 digest and verified safe
  relative path.
- The fixture requires P42-T16 packet status `ready_for_implementation_review`
  and mode `runtime_implementation_review_packet_no_execution`.
- The fixture records disabled runtime surface fields but marks every executable
  field as blocked or not implemented.
- The fixture rejects missing review packet evidence, digest mismatch, execution
  permission, registry authority, approval consumption, adapter code loading,
  adapter imports, adapter process spawning, dependency installation, package
  manager invocation, network access, runtime invocation, runtime
  implementation, and adapter output as registry truth.
- Tests fail if the skeleton grants execution permission, grants registry
  authority, consumes approval by a runtime, loads/imports adapter code, spawns
  a process, implements or invokes runtime, or treats adapter output as truth.
- CLI/runtime behavior remains unchanged: no real adapter execution or runtime
  implementation is added.

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
- Do not treat P42-T16 as execution permission.
- Do not consume approval by a real runtime.
- Do not treat adapter output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_disabled_explicit_real_local_sandbox_runtime_implementation_skeleton_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `python3 -m json.tool tests/fixtures/repository_plugins/disabled-explicit-real-local-trusted-adapter-sandbox-runtime-implementation-skeleton.example.json >/dev/null`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q`
- DocC static generation
