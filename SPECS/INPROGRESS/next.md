# Next Task: P42-T6 Synthetic Trusted Local Adapter Sandbox Run Verifier

**Status:** Planned
**Branch:** `feature/P42-T6-synthetic-trusted-local-adapter-sandbox-run-verifier`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T5 Explicitly Approved Synthetic Trusted Local Adapter Sandbox Run Fixture

## Recently Archived

- `P42-T5` added
  `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRun`.
- The fixture is in
  `tests/fixtures/repository_plugins/synthetic-trusted-local-adapter-sandbox-run.example.json`.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_SYNTHETIC_SANDBOX_RUN_FIXTURE.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterSyntheticSandboxRunFixture.md`.
- The fixture binds operator approval to one adapter id/digest, one repository
  revision, one sandbox policy, one sandbox runner validation report, one output
  root, and declared synthetic output candidate digests.
- The fixture records synthetic output, diagnostics, and audit-record candidate
  files with safe relative paths, byte sizes, SHA-256 digests, producer run id,
  adapter id/digest, source input digests, and `outputIsRegistryTruth: false`.
- The fixture remains producer-side review evidence only and preserves
  `adapterExecution: synthetic_fixture_only`,
  `realAdapterProcessSpawned: false`,
  `thirdPartyAdapterCodeLoaded: false`, `executedAdapterCount: 0`,
  `dependencyInstallation: not_allowed`, `packageManagers: not_invoked`,
  `networkAccess: none`, and `registryAuthority: false`.

## Task

Add a synthetic trusted local adapter sandbox run verifier that validates the
P42-T5 fixture and linked output artifacts without enabling real adapter
execution.

## Why This Is Next

P42-T5 records the approved synthetic run shape as data. The next step is a
deterministic verifier that can check fixture identity, linked artifact digests,
operator approval binding, synthetic output byte sizes/digests, audit
requirements, and no-real-execution boundaries before any real local adapter run
work is considered.

## Scope

- Add synthetic sandbox run verifier logic and CLI surface.
- Validate P42-T5 fixture identity and authority.
- Validate safe relative paths, linked artifact SHA-256 digests, output byte
  sizes/digests, and audit record references.
- Validate operator approval binding and no-real-execution boundaries.
- Emit a machine-readable verifier report.
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
- [ ] `P42-T6` Add a synthetic trusted local adapter sandbox run verifier that
  checks P42-T5 fixture identity, linked artifact digests, approval binding,
  synthetic output byte sizes/digests, audit requirements, and no-real-execution
  boundaries without enabling real adapter execution.

Motivation:

- Synthetic approved run fixtures need deterministic verification before they
  can safely inform any future runtime work.
- The verifier should prove approval/output/audit shape while preserving the
  no-real-execution boundary.

Goal:

- Provide a machine-checkable producer-side review gate for synthetic trusted
  local adapter sandbox run fixtures.

Acceptance:

- The verifier checks fixture identity, linked digests, approval binding,
  synthetic output digests, audit requirements, and no-real-execution fields.
- The verifier emits a review-only report and cannot be interpreted as runtime
  permission or registry authority.
