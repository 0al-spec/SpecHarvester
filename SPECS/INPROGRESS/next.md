# Next Task: P42-T12 Explicit Real Local Trusted Adapter Sandbox Runtime Implementation Review Gate

**Status:** In Progress
**Branch:** `feature/P42-T12-explicit-real-local-trusted-adapter-sandbox-runtime-implementation-review-gate`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T11 Explicit Real Local Trusted Adapter Sandbox Runner Evidence Handoff

## Recently Archived

- `P42-T11` added
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunnerEvidenceHandoff`.
- The handoff fixture lives at
  `tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-runner-evidence-handoff.example.json`.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNNER_EVIDENCE_HANDOFF.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterExplicitRealLocalSandboxRunnerEvidenceHandoff.md`.
- The handoff packages the P42-T8
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest`, P42-T9
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequestPreflightReport`,
  and P42-T10
  `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRunnerReport`
  fixtures with pinned SHA-256 digests.
- The handoff validates request/preflight/disabled-runner identity, digest
  agreement, preflight result status, disabled runner status, review-only
  artifact semantics, no execution permission, no operator approval, no
  registry authority, and no adapter output truth.
- The handoff keeps `handoffIsExecutionPermission: false`,
  `handoffIsOperatorApproval: false`, `handoffIsRegistryAuthority: false`,
  `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `adapterCodeImportAttempted: false`, `adapterProcessSpawned: false`,
  `executedAdapterCount: 0`, `runtimeInvoked: false`,
  `runtimeImplemented: false`, `registryAuthority: false`, and
  `adapterOutputAccepted: false`.

## Task

Add an explicit real local trusted adapter sandbox runtime implementation review
gate that consumes the P42-T11 evidence handoff, records runtime implementation
prerequisites, and refuses real adapter execution until a separate
operator-approved runtime task exists.

## Why This Is Next

P42-T11 packages request/preflight/disabled-runner evidence into a portable
handoff. The next safe layer is not a runtime implementation yet; it is a gate
that makes future runtime prerequisites machine-readable and keeps the evidence
handoff from becoming implicit execution permission.

## Scope

- Add a machine-readable runtime implementation review gate fixture.
- Reference the P42-T11 evidence handoff with a pinned digest.
- Validate that the handoff remains review-only and cannot be treated as
  execution permission, operator approval, registry authority, or adapter output
  truth.
- Record runtime implementation prerequisites:
  - explicit operator approval;
  - adapter package identity;
  - process isolation;
  - safe input allowlists;
  - sealed environment;
  - dependency isolation;
  - network-deny-by-default policy;
  - output digests;
  - audit records;
  - rollback policy;
  - review-only authority.
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
- Do not treat P42-T11 as execution permission.
- Do not treat the review gate as operator approval.
- Do not treat adapter output as registry truth.
