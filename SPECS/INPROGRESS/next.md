# Next Task: P42-T9 Explicit Real Local Trusted Adapter Sandbox Run Request Preflight Fixture

**Status:** Planned
**Branch:** `feature/P42-T9-explicit-real-local-trusted-adapter-sandbox-run-request-preflight-fixture`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T8 Explicit Real Local Trusted Adapter Sandbox Run Request Fixture

## Recently Archived

- `P42-T8` added
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest`.
- The request fixture lives at
  `tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request.example.json`.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_FIXTURE.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterExplicitRealLocalSandboxRunRequestFixture.md`.
- The request fixture references P42-T6
  `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport` and
  P42-T7 `SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport`
  contracts as review-time prerequisite evidence.
- The request fixture declares scoped future operator approval, adapter
  package identity, target repository identity, sandbox policy identity,
  runtime policy, filesystem/output policy, audit policy, rollback/review
  requirements, and non-authority statements.
- The request fixture remains producer-side request evidence only and
  preserves `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `adapterProcessSpawned: false`, `executedAdapterCount: 0`,
  `runtimeInvoked: false`, `requestIsExecutionPermission: false`,
  `requestIsOperatorApproval: false`, `readyForExecution: false`,
  `registryAuthority: false`, and `adapterOutputAccepted: false`.

## Task

Add an explicit real local trusted adapter sandbox run request preflight
fixture that validates the P42-T8 request fixture and prerequisite evidence
requirements without enabling real adapter execution.

## Why This Is Next

P42-T8 records a review request, but it deliberately does not validate actual
review-time evidence paths/digests or grant execution permission. The next step
is a preflight fixture that checks request identity, evidence requirements,
approval scope, runtime policy, filesystem/output/audit declarations, and
non-authority boundaries before any runner implementation exists.

## Scope

- Add a machine-readable request preflight fixture.
- Reference the P42-T8 request fixture.
- Validate request identity, authority, and schema version.
- Validate prerequisite verifier/readiness evidence requirements.
- Validate scoped approval binding requirements.
- Validate sandbox runtime, filesystem/output, audit, rollback, and review
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
- Do not treat the request fixture as execution permission.
- Do not treat preflight pass as execution permission.

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
- [ ] `P42-T9` Add an explicit real local trusted adapter sandbox run request
  preflight fixture that validates the P42-T8 request identity, prerequisite
  verifier/readiness evidence requirements, scoped approval binding, runtime
  policy, filesystem/output/audit declarations, and non-authority statements
  while still refusing to grant execution permission or spawn adapter
  processes.

Motivation:

- A request fixture needs a separate preflight artifact before any runner can
  safely consume it.
- The preflight fixture should reject ambiguous, reusable,
  registry-authoritative, or execution-authoritative request shapes before
  runtime work begins.

Goal:

- Provide a machine-readable explicit request preflight fixture for future real
  local trusted adapter sandbox run review without granting execution
  permission.

Acceptance:

- The preflight fixture references the P42-T8 request fixture and validates
  request identity, prerequisite evidence requirements, scoped approval,
  runtime/filesystem/output/audit/review policy, and non-authority statements.
- The preflight fixture is review-only and cannot be interpreted as runtime
  permission or registry authority.
