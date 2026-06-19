# Next Task: P42-T10 Disabled Explicit Real Local Trusted Adapter Sandbox Runner Skeleton

**Status:** Planned
**Branch:** `feature/P42-T10-disabled-explicit-real-local-trusted-adapter-sandbox-runner-skeleton`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T9 Explicit Real Local Trusted Adapter Sandbox Run Request Preflight Fixture

## Recently Archived

- `P42-T9` added
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequestPreflightReport`.
- The preflight fixture lives at
  `tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request-preflight.example.json`.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_PREFLIGHT_FIXTURE.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterExplicitRealLocalSandboxRunRequestPreflightFixture.md`.
- The preflight fixture references the P42-T8
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest` fixture and
  verifies its SHA-256 digest.
- The fixture validates request identity, P42-T6 verifier requirements, P42-T7
  readiness requirements, scoped operator approval binding, adapter package
  identity, target repository identity, sandbox policy identity, runtime policy,
  filesystem/output policy, audit policy, rollback/review boundaries, and
  non-authority statements.
- The fixture records accepted, rejected, blocked, and warning checks for unsafe
  paths, missing evidence requirements, reusable approval, execution permission
  drift, adapter code loading, adapter process spawning, harvested-code
  execution, AI execution, registry authority, and adapter output acceptance.
- The preflight result remains review evidence only and preserves
  `preflightPassIsExecutionPermission: false`,
  `preflightPassIsOperatorApproval: false`,
  `preflightPassIsRegistryAuthority: false`, `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `adapterProcessSpawned: false`,
  `executedAdapterCount: 0`, `runtimeInvoked: false`,
  `runtimeImplemented: false`, `registryAuthority: false`, and
  `adapterOutputAccepted: false`.

## Task

Add a disabled explicit real local trusted adapter sandbox runner skeleton that
validates the P42-T8 request and P42-T9 preflight fixture linkage without
loading adapter code or spawning adapter processes.

## Why This Is Next

P42-T9 proves that the explicit request can be preflighted as review evidence.
The next step is a disabled runner skeleton that proves a future runtime entry
point can consume the request/preflight pair, reject drift, and report why real
execution is still disabled.

## Scope

- Add a machine-readable disabled runner skeleton fixture/report.
- Validate P42-T8 request identity and digest linkage.
- Validate P42-T9 preflight identity, digest linkage, and passed review-only
  result.
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

## Phase 42. Trusted Local Adapter Runtime Sandbox

- [x] `P42-T1` Document the trusted local adapter runtime sandbox plan and add
  the next-task scaffold for turning Phase 41 no-execution readiness into a
  future explicitly approved sandboxed adapter runtime without enabling adapter
  execution yet.
- [x] `P42-T2` Add a machine-readable
  `SpecHarvesterTrustedLocalAdapterSandboxContract` fixture that records
  adapter package identity, sandbox policy identity, operator approval
  requirements, filesystem/environment/network/dependency policy, output
  verification, audit records, and non-authority statements before any runtime
  implementation.
- [x] `P42-T3` Add a trusted local adapter sandbox preflight report fixture that
  validates `SpecHarvesterTrustedLocalAdapterSandboxContract` identity,
  operator approval requirements, process/filesystem/environment/dependency/
  network policy, output verification, audit requirements, and non-authority
  boundaries before any sandbox runner implementation.
- [x] `P42-T4` Add disabled trusted local adapter sandbox runner validation that
  checks sandbox contract and sandbox preflight report linkage while preserving
  no adapter code loading, no process spawning, no dependency installation, no
  network access, and no registry authority.
- [x] `P42-T5` Add an explicitly approved synthetic trusted local adapter
  sandbox run fixture that records operator approval binding, sandbox runner
  validation input, synthetic adapter output candidates, output digests, audit
  records, and non-authority statements without running a real adapter process.
- [x] `P42-T6` Add a synthetic trusted local adapter sandbox run verifier that
  checks P42-T5 fixture identity, linked artifact digests, approval binding,
  synthetic output byte sizes/digests, audit requirements, and no-real-execution
  boundaries without enabling real adapter execution.
- [x] `P42-T7` Add a real local trusted adapter sandbox run readiness gate that
  checks the P42-T6 verifier report plus explicit real-run prerequisites,
  sandbox runtime availability, filesystem/output policy, audit requirements,
  and operator approval requirements while still refusing to load adapter code
  or spawn adapter processes.
- [x] `P42-T8` Add an explicit real local trusted adapter sandbox run request
  fixture that records a future real-run review request, scoped operator
  approval requirements, verifier/readiness references, runtime policy,
  filesystem/output/audit declarations, and non-authority statements while
  still refusing to load adapter code or spawn adapter processes.
- [x] `P42-T9` Add an explicit real local trusted adapter sandbox run request
  preflight fixture that validates the P42-T8 request identity, prerequisite
  verifier/readiness evidence requirements, scoped approval binding, runtime
  policy, filesystem/output/audit declarations, and non-authority statements
  while still refusing to grant execution permission or spawn adapter
  processes.
- [ ] `P42-T10` Add a disabled explicit real local trusted adapter sandbox
  runner skeleton that validates the P42-T8 request and P42-T9 preflight
  linkage while preserving no adapter code loading, no process spawning, no
  dependency installation, no network access, no registry authority, and no
  adapter output acceptance.

Motivation:

- The request/preflight pair needs a disabled consumer shape before a runtime can
  be implemented safely.
- The disabled runner skeleton should reject execution drift and prove that
  linkage validation can happen without adapter code loading or process spawn.

Goal:

- Provide the no-execution runner skeleton boundary that future real local
  trusted adapter execution must replace only after explicit review.

Acceptance:

- The disabled runner skeleton validates P42-T8 request and P42-T9 preflight
  identity/digest linkage.
- The skeleton reports execution disabled and cannot be interpreted as runtime
  permission, operator approval, registry authority, or adapter output
  acceptance.
