# Next Task: P42-T8 Explicit Real Local Trusted Adapter Sandbox Run Request Fixture

**Status:** Planned
**Branch:** `feature/P42-T8-explicit-real-local-trusted-adapter-sandbox-run-request-fixture`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T7 Real Local Trusted Adapter Sandbox Run Readiness Gate

## Recently Archived

- `P42-T7` added
  `SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport`.
- The readiness CLI is
  `real-local-trusted-adapter-sandbox-run-readiness`.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_SANDBOX_RUN_READINESS.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterRealLocalSandboxRunReadiness.md`.
- The readiness gate checks P42-T6 verifier report identity, status,
  authority, linked artifact/output/audit verification summaries, operator
  approval binding, no-real-execution boundaries, and non-authority statements.
- The readiness report declares explicit real-run review prerequisites for
  operator approval, sandbox runtime, filesystem/output policy, audit policy,
  and rollback/review boundaries.
- The readiness gate remains producer-side review evidence only and preserves
  `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `adapterProcessSpawned: false`, `executedAdapterCount: 0`,
  `runtimeInvoked: false`, `readinessGateIsExecutionPermission: false`,
  `readyForExecution: false`, `registryAuthority: false`, and
  `adapterOutputAccepted: false`.

## Task

Add an explicit real local trusted adapter sandbox run request fixture that
records a future real-run review request without enabling real adapter
execution.

## Why This Is Next

P42-T7 makes the readiness gate explicit. The next step is a machine-readable
request fixture that binds a future real-run review request to the verifier and
readiness evidence, scoped operator approval requirements, runtime policy,
filesystem/output/audit declarations, and non-authority statements before any
runner implementation exists.

## Scope

- Add a machine-readable explicit real-run request fixture.
- Reference the P42-T6 verifier report contract and P42-T7 readiness report
  contract.
- Declare scoped operator approval requirements for a future real run.
- Declare sandbox runtime, filesystem, output, audit, rollback, and review
  requirements.
- Preserve no adapter code loading, no process spawning, no dependency
  installation, no package manager invocation, no network access, no harvested
  code execution, and no AI execution.
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
- Do not treat synthetic run verification as execution permission.
- Do not treat readiness as execution permission.
- Do not treat a request fixture as execution permission.

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
- [ ] `P42-T8` Add an explicit real local trusted adapter sandbox run request
  fixture that records a future real-run review request, scoped operator
  approval requirements, verifier/readiness references, runtime policy,
  filesystem/output/audit declarations, and non-authority statements while
  still refusing to load adapter code or spawn adapter processes.

Motivation:

- Real-run readiness needs a concrete request artifact before any runner can
  safely consume the approval boundary.
- The request fixture should bind future execution review to verifier/readiness
  evidence and prevent ambiguous, reusable, or registry-authoritative requests.

Goal:

- Provide a machine-readable explicit request fixture for future real local
  trusted adapter sandbox run review without granting execution permission.

Acceptance:

- The request fixture references verifier/readiness evidence contracts and
  declares scoped approval, runtime, filesystem/output, audit, and review
  requirements.
- The request fixture is review-only and cannot be interpreted as runtime
  permission or registry authority.
