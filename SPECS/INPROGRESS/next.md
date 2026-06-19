# Next Task: P42-T13 Explicit Real Local Trusted Adapter Sandbox Operator Approval Binding Fixture

**Status:** In Progress
**Branch:** `feature/P42-T13-explicit-real-local-trusted-adapter-sandbox-operator-approval-binding-fixture`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T12 Explicit Real Local Trusted Adapter Sandbox Runtime Implementation Review Gate

## Recently Archived

- `P42-T12` added
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewGate`.
- The review gate fixture lives at
  `tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-runtime-implementation-review-gate.example.json`.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_REVIEW_GATE.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterExplicitRealLocalSandboxRuntimeImplementationReviewGate.md`.
- The gate references the P42-T11
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunnerEvidenceHandoff`
  fixture with a pinned SHA-256 digest.
- The gate validates handoff status `ready_for_review`, handoff review-only
  semantics, no handoff execution permission, no handoff operator approval, no
  handoff registry authority, no adapter output truth, and no runtime side
  effects.
- The gate records runtime implementation prerequisites: explicit operator
  approval, adapter package identity, process isolation, safe input allowlists,
  sealed environment, dependency isolation, network-deny-by-default policy,
  output digests, audit records, rollback policy, and review-only authority.
- The gate keeps `gateIsExecutionPermission: false`,
  `gateIsOperatorApproval: false`, `gateIsRegistryAuthority: false`,
  `runtimeImplementationAllowed: false`, `runtimeInvocationAllowed: false`,
  `operatorApprovalConsumed: false`, `operatorApprovalProvided: false`,
  `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `adapterCodeImportAttempted: false`, `adapterProcessSpawned: false`,
  `runtimeInvoked: false`, `runtimeImplemented: false`,
  `registryAuthority: false`, and `adapterOutputAccepted: false`.

## Task

Add an explicit real local trusted adapter sandbox operator approval binding
fixture that binds a future approval scope to P42-T12 runtime prerequisites
while still refusing adapter execution.

## Why This Is Next

P42-T12 records runtime implementation prerequisites but intentionally does not
provide operator approval. The next safe layer is an approval binding artifact
that scopes what a future operator-approved run would be allowed to use without
loading adapter code or spawning a process.

## Scope

- Add a machine-readable operator approval binding fixture.
- Reference the P42-T12 review gate with a pinned digest.
- Bind approval scope to:
  - adapter package identity;
  - target repository revision;
  - input artifact digests;
  - output directory;
  - runtime budgets;
  - network policy;
  - dependency policy;
  - audit requirements.
- Preserve no adapter code loading, no process spawning, no dependency
  installation, no package manager invocation, no network access, no harvested
  code execution, and no AI execution.
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
- Do not treat P42-T12 as execution permission.
- Do not treat the approval binding as registry authority.
- Do not treat adapter output as registry truth.
