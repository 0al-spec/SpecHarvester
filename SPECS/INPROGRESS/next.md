# Next Task: P42-T4 Disabled Trusted Local Adapter Sandbox Runner Validation

**Status:** Planned
**Branch:** `feature/P42-T4-disabled-trusted-local-adapter-sandbox-runner-validation`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T3 Trusted Local Adapter Sandbox Preflight Report Fixture

## Recently Archived

- `P42-T3` added the machine-readable
  `SpecHarvesterTrustedLocalAdapterSandboxPreflightReport` fixture.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_REPORT_FIXTURE.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterSandboxPreflightReportFixture.md`.
- The fixture is in
  `tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-preflight-report.example.json`.
- The fixture validates `SpecHarvesterTrustedLocalAdapterSandboxContract`
  identity and digest linkage, records
  `sandbox_preflight_passed_review_only`, accepted/rejected/blocked checks,
  no-execution state, and review-only non-authority statements.
- The current state remains `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `adapterProcessSpawned: false`,
  `executedAdapterCount: 0`, and `registryAuthority: false`.

## Task

Add disabled trusted local adapter sandbox runner validation that checks
`SpecHarvesterTrustedLocalAdapterSandboxContract` and
`SpecHarvesterTrustedLocalAdapterSandboxPreflightReport` linkage while
preserving no-execution behavior.

## Why This Is Next

P42-T2 and P42-T3 define the sandbox contract and preflight report. The next
step is a disabled validation surface that proves future runner inputs can be
linked and checked without loading adapter code, spawning processes, installing
dependencies, invoking package managers, enabling network access, or granting
registry authority.

## Scope

- Add disabled trusted local adapter sandbox runner validation.
- Validate contract/preflight linkage and digest compatibility.
- Emit or document a no-execution validation report shape.
- Preserve `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `adapterProcessSpawned: false`, `executedAdapterCount: 0`, and
  `registryAuthority: false`.
- Link docs, DocC, roadmap/capabilities, and tests.

## Non-Goals

- Do not implement real adapter execution.
- Do not load third-party adapter code.
- Do not spawn adapter processes.
- Do not install dependencies.
- Do not invoke package managers.
- Do not allow network discovery.
- Do not execute harvested repository code.
- Do not run AI because of adapter execution.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat sandbox runner validation as registry truth.
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
- [ ] `P42-T4` Add disabled trusted local adapter sandbox runner validation that
  checks sandbox contract and sandbox preflight report linkage while preserving
  no adapter code loading, no process spawning, no dependency installation, no
  network access, and no registry authority.

Motivation:

- Future runner work needs a deterministic no-execution validation step before
  any real adapter process can run.
- The validation surface should prove contract/preflight linkage while keeping
  all runtime authority disabled.

Goal:

- Validate the sandbox runner input boundary without enabling adapter
  execution.

Acceptance:

- The validation checks contract/preflight identity and digest linkage.
- The validation keeps `adapterExecution: not_run` and cannot be interpreted as
  runtime permission.
- Docs and tests prove the validation remains producer-side review evidence
  only.
