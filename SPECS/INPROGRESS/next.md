# Next Task: P42-T3 Trusted Local Adapter Sandbox Preflight Report Fixture

**Status:** Planned
**Branch:** `feature/P42-T3-trusted-local-adapter-sandbox-preflight-report-fixture`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T2 Trusted Local Adapter Sandbox Contract Fixture

## Recently Archived

- `P42-T2` added the machine-readable
  `SpecHarvesterTrustedLocalAdapterSandboxContract` fixture.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_FIXTURE.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterSandboxContractFixture.md`.
- The fixture is in
  `tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-contract.example.json`.
- The fixture records adapter package identity, sandbox policy identity,
  operator approval requirements, process/filesystem/environment/dependency/
  network policy, output verification, audit requirements, diagnostics, and
  non-authority statements.
- The current state remains `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `adapterProcessSpawned: false`,
  `executedAdapterCount: 0`, and `registryAuthority: false`.

## Task

Add a machine-readable
`SpecHarvesterTrustedLocalAdapterSandboxPreflightReport` fixture that validates
the `SpecHarvesterTrustedLocalAdapterSandboxContract` before any sandbox runner
implementation.

## Why This Is Next

P42-T2 makes the sandbox contract machine-readable. The next step is to define
the preflight report shape that validates the contract identity, approval
requirements, isolation policies, output verification, audit requirements, and
non-authority boundaries before any future runner can consume it.

## Scope

- Add a JSON fixture for
  `SpecHarvesterTrustedLocalAdapterSandboxPreflightReport`.
- Validate sandbox contract identity and digest linkage.
- Record accepted, rejected, and blocked checks for operator approval
  requirements, process policy, filesystem policy, environment policy,
  dependency policy, network-deny-by-default policy, output verification, audit
  requirements, and non-authority boundaries.
- Link the fixture from GitHub docs, DocC, roadmap/capabilities, and tests.
- Preserve the no-execution boundary.

## Non-Goals

- Do not implement real adapter execution.
- Do not implement a sandbox runner.
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
- Do not treat sandbox preflight as registry truth.
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
- [ ] `P42-T3` Add a trusted local adapter sandbox preflight report fixture that
  validates `SpecHarvesterTrustedLocalAdapterSandboxContract` identity,
  operator approval requirements, process/filesystem/environment/dependency/
  network policy, output verification, audit requirements, and non-authority
  boundaries before any sandbox runner implementation.

Motivation:

- The sandbox contract should have a review-only preflight report before any
  sandbox runner implementation exists.
- Future runtime work needs a stable way to reject unsafe contract shapes before
  adapter code can be loaded or process execution can be considered.

Goal:

- Make the P42 sandbox contract preflight boundary machine-readable without
  enabling adapter execution.

Acceptance:

- The fixture validates sandbox contract identity, digest linkage, policy
  fields, approval requirements, output verification, audit requirements, and
  non-authority statements.
- The fixture keeps `adapterExecution: not_run` and cannot be interpreted as
  runtime permission.
- Docs and tests prove the fixture remains producer-side review evidence only.
