# Next Task: P42-T5 Explicitly Approved Synthetic Trusted Local Adapter Sandbox Run Fixture

**Status:** Planned
**Branch:** `feature/P42-T5-explicitly-approved-synthetic-trusted-local-adapter-sandbox-run-fixture`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T4 Disabled Trusted Local Adapter Sandbox Runner Validation

## Recently Archived

- `P42-T4` added `trusted-local-adapter-sandbox-runner-validation`.
- The validation emits
  `SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport`.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterSandboxRunnerValidation.md`.
- The CLI validates
  `SpecHarvesterTrustedLocalAdapterSandboxContract` and
  `SpecHarvesterTrustedLocalAdapterSandboxPreflightReport` identity and digest
  linkage.
- The validation remains producer-side review evidence only and preserves
  `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `adapterProcessSpawned: false`, `executedAdapterCount: 0`, and
  `registryAuthority: false`.

## Task

Add an explicitly approved synthetic trusted local adapter sandbox run fixture
that records the next approved-run boundary without running a real adapter
process.

## Why This Is Next

P42-T2 defined the sandbox contract, P42-T3 defined the sandbox preflight
report, and P42-T4 added disabled runner validation. The next incremental step
is a synthetic approved run fixture that proves what explicit operator approval,
runner validation input, synthetic output candidates, output digests, audit
records, and non-authority statements must look like before any real local
adapter execution can be considered.

## Scope

- Add a machine-readable synthetic approved sandbox run fixture.
- Bind operator approval to one adapter, one repository, one sandbox policy,
  one runner validation report, and one output directory.
- Include synthetic adapter output candidate references with safe relative
  paths, byte sizes, and SHA-256 digests.
- Include replayable audit record requirements.
- Preserve no real adapter process execution.
- Preserve producer-side review-only authority.
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
- Do not treat sandbox runner validation as execution permission.

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
- [ ] `P42-T5` Add an explicitly approved synthetic trusted local adapter
  sandbox run fixture that records operator approval binding, sandbox runner
  validation input, synthetic adapter output candidates, output digests, audit
  records, and non-authority statements without running a real adapter process.

Motivation:

- Future real adapter execution must have an approved-run artifact shape before
  any real process can run.
- The synthetic fixture should prove approval and output-audit shape without
  adding execution capability.

Goal:

- Define the approved synthetic run boundary that sits between disabled runner
  validation and any future real local adapter run.

Acceptance:

- The fixture binds approval to specific contract/preflight/runner validation
  artifacts.
- The fixture records synthetic outputs with digests and audit records.
- The fixture keeps real adapter execution disabled and remains review evidence
  only.
