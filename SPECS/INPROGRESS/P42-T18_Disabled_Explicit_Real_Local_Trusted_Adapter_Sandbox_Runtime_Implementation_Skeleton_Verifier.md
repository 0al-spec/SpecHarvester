# P42-T18 Disabled Explicit Real Local Trusted Adapter Sandbox Runtime Implementation Skeleton Verifier

## Summary

Add a deterministic verifier report for the P42-T17 disabled explicit real local
trusted adapter sandbox runtime implementation skeleton. The verifier consumes
the P42-T17 fixture, checks its identity, pinned P42-T16 review packet linkage,
disabled runtime surface, no-execution boundary, no approval consumption, and
non-authority statements.

## Motivation

P42-T17 records the disabled runtime implementation surface, but future runtime
work should not treat that skeleton as reviewed input without a deterministic
verification artifact. P42-T18 creates that review gate while preserving the
same boundary: no adapter code loading, no adapter import, no process spawning,
no runtime invocation, no approval consumption, no registry authority, and no
adapter output truth.

## Boundary Flow

```text
P42-T16 runtime implementation review packet
  -> P42-T17 disabled runtime implementation skeleton
  -> P42-T18 disabled skeleton verifier
  -> future explicit runtime implementation review
  -> future bounded real local adapter run
```

## Deliverables

- Add a machine-readable verifier fixture under
  `tests/fixtures/repository_plugins/`.
- Reference the P42-T17 skeleton fixture with a pinned SHA-256 digest.
- Verify P42-T17 identity, schema version, authority, contract flags, linked
  P42-T16 review packet digest, disabled runtime surface count, check counts,
  execution boundary fields, diagnostics, and non-authority statements.
- Add GitHub docs and DocC docs for the verifier.
- Link the verifier from P42-T17 docs, runtime sandbox plan, roadmap,
  capabilities, docs index, and DocC root.
- Add regression coverage in `tests/test_docs_contracts.py`.
- Archive Flow artifacts and advance `SPECS/INPROGRESS/next.md`.

## Acceptance Criteria

- The verifier references P42-T17 with a pinned digest.
- The verifier checks P42-T17 `apiVersion`, `kind`, `schemaVersion`, and
  `authority`.
- The verifier checks P42-T17 keeps
  `implementationSkeletonIsExecutionPermission: false`,
  `implementationSkeletonIsRegistryAuthority: false`,
  `implementationSkeletonConsumesApproval: false`, and
  `implementationSkeletonImplementsRuntime: false`.
- The verifier checks P42-T17 execution boundary fields:
  `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `adapterCodeImportAttempted: false`, `adapterProcessSpawned: false`,
  `executedAdapterCount: 0`, `runtimeInvoked: false`,
  `runtimeImplemented: false`, `approvalConsumedByRuntime: false`,
  `registryAuthority: false`, and `adapterOutputAccepted: false`.
- The verifier itself keeps `verifierIsExecutionPermission: false`,
  `verifierIsRegistryAuthority: false`, `verifierConsumesApproval: false`,
  `verifierInvokesRuntime: false`, and `verifierAcceptsAdapterOutput: false`.
- Tests verify the fixture, docs, backlinks, and current next-task pointer.

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
- Do not treat P42-T17 as execution permission.
- Do not consume approval by a real runtime.
- Do not treat adapter output as registry truth.

## Validation Plan

- `python3 -m json.tool` for the verifier fixture.
- Targeted docs-contract regression test.
- Full docs-contract suite.
- `PYTHONPATH=src pytest -q`.
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q`.
- `PYTHONPATH=src ruff check .`.
- `PYTHONPATH=src ruff format --check src tests`.
- `git diff --check`.
- `swift package dump-package`.
- `swift build --target SpecHarvesterDocs`.
- DocC static generation.
