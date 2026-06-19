# Next Task: P42-T17 Disabled Explicit Real Local Trusted Adapter Sandbox Runtime Implementation Skeleton

**Status:** Planned
**Branch:** `feature/P42-T17-disabled-explicit-real-local-trusted-adapter-sandbox-runtime-implementation-skeleton`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T16 Explicit Real Local Trusted Adapter Sandbox Runtime Implementation Review Packet

## Recently Archived

- `P42-T16` added
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewPacket`.
- The runtime implementation review packet fixture lives at
  `tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-runtime-implementation-review-packet.example.json`.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_REVIEW_PACKET.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterExplicitRealLocalSandboxRuntimeImplementationReviewPacket.md`.
- The packet references the P42-T15
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationEvidenceHandoff`
  fixture with a pinned SHA-256 digest.
- The packet records implementation prerequisites for adapter package identity,
  runtime entrypoint isolation, process spawning policy, dependency policy,
  network policy, output digest verification, audit records, rollback policy,
  and approval consumption rules.
- The packet keeps `packetIsExecutionPermission: false`,
  `packetIsRegistryAuthority: false`, `packetConsumesApproval: false`,
  `packetImplementsRuntime: false`, `operatorApprovalConsumed: false`,
  `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `adapterCodeImportAttempted: false`, `adapterProcessSpawned: false`,
  `runtimeInvoked: false`, `runtimeImplemented: false`,
  `networkAccess: none`, `registryAuthority: false`, and
  `adapterOutputAccepted: false`.

## Task

Add a disabled explicit real local trusted adapter sandbox runtime
implementation skeleton that consumes the P42-T16 review packet and records the
future runtime implementation surface while still refusing adapter code loading,
adapter imports, process spawning, runtime invocation, and approval
consumption.

## Why This Is Next

P42-T16 records the implementation prerequisites, but the project still needs a
disabled skeleton that names the future runtime surface without introducing
executable runtime behavior. The skeleton should make implementation shape
reviewable before any adapter code can be loaded or invoked.

## Scope

- Add a machine-readable disabled runtime implementation skeleton fixture.
- Reference P42-T16 with a pinned digest.
- Record disabled runtime surface fields for entrypoint isolation, process
  launcher boundary, dependency policy, network policy, output writer, audit
  writer, rollback handler, and approval consumption boundary.
- Preserve no adapter code loading, no adapter import, no process spawning, no
  dependency installation, no package manager invocation, no network access, no
  harvested code execution, and no AI execution.
- Preserve no package acceptance, no relation acceptance, no baseline seeding,
  no registry metadata publishing, no `preview_only` removal, and no adapter
  output truth.
- Link docs, DocC, roadmap/capabilities, and tests.

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
