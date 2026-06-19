# Next Task: P42-T11 Explicit Real Local Trusted Adapter Sandbox Runner Evidence Handoff

**Status:** Planned
**Branch:** `feature/P42-T11-explicit-real-local-trusted-adapter-sandbox-runner-evidence-handoff`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T10 Disabled Explicit Real Local Trusted Adapter Sandbox Runner Skeleton

## Recently Archived

- `P42-T10` added
  `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRunnerReport`.
- The disabled runner skeleton fixture lives at
  `tests/fixtures/repository_plugins/disabled-explicit-real-local-trusted-adapter-sandbox-runner.example.json`.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNNER_SKELETON.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterDisabledExplicitRealLocalSandboxRunnerSkeleton.md`.
- The skeleton references the P42-T8
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest` fixture and
  the P42-T9
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequestPreflightReport`
  fixture with pinned SHA-256 digests.
- The skeleton validates request/preflight digest agreement, preflight result
  status, `preflight_passed_review_only` decision semantics, no-execution
  boundaries, no consumed operator approval, disabled adapter execution,
  disabled adapter code loading, disabled process spawning, disabled runtime
  side effects, disabled registry authority, and disabled adapter output
  acceptance.
- The skeleton records accepted, rejected, blocked, and warning checks for
  missing inputs, digest mismatch, non-review-only preflight decisions,
  execution permission drift, operator approval consumption, network access,
  dependency installation, package manager invocation, package/relation
  acceptance, baseline seeding, `preview_only` removal, and adapter output as
  registry truth.
- The skeleton result remains review evidence only and preserves
  `runnerIsExecutionPermission: false`, `runnerIsOperatorApproval: false`,
  `runnerIsRegistryAuthority: false`, `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `adapterCodeImportAttempted: false`,
  `adapterProcessSpawned: false`, `executedAdapterCount: 0`,
  `runtimeInvoked: false`, `runtimeImplemented: false`,
  `registryAuthority: false`, and `adapterOutputAccepted: false`.

## Task

Add an explicit real local trusted adapter sandbox runner evidence handoff
fixture that packages the P42-T8 request, P42-T9 preflight, and P42-T10
disabled runner skeleton as review evidence without enabling real adapter
execution.

## Why This Is Next

P42-T10 proves the disabled consumer skeleton can validate request/preflight
linkage. The next safe layer is a handoff artifact that can carry the request,
preflight, and disabled skeleton report together for maintainer review without
turning the skeleton into execution permission.

## Scope

- Add a machine-readable runner evidence handoff fixture.
- Reference P42-T8 request, P42-T9 preflight, and P42-T10 disabled runner
  skeleton with pinned digests.
- Validate artifact identity and digest agreement across the handoff set.
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
- Do not treat request/preflight/disabled-runner artifacts as execution
  permission.
- Do not treat adapter output as registry truth.

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
- [x] `P42-T10` Add a disabled explicit real local trusted adapter sandbox
  runner skeleton that validates the P42-T8 request and P42-T9 preflight
  linkage while preserving no adapter code loading, no process spawning, no
  dependency installation, no network access, no registry authority, and no
  adapter output acceptance.
- [ ] `P42-T11` Add an explicit real local trusted adapter sandbox runner
  evidence handoff fixture that packages the P42-T8 request, P42-T9 preflight,
  and P42-T10 disabled runner skeleton as review evidence while preserving no
  adapter execution, no registry authority, and no adapter output truth.

Motivation:

- Request/preflight/disabled-runner artifacts need a portable handoff boundary
  before any future runtime implementation can be reviewed.
- The handoff should keep all linked artifacts review-only and make authority
  boundaries machine-readable.

Goal:

- Provide the review evidence handoff boundary for the explicit real local
  trusted adapter sandbox runner path.

Acceptance:

- The handoff fixture references P42-T8, P42-T9, and P42-T10 artifacts with
  pinned digests.
- The handoff fixture cannot be interpreted as execution permission, operator
  approval, registry authority, package/relation acceptance, or adapter output
  truth.
