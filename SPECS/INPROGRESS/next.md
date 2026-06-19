# Next Task: P42-T7 Real Local Trusted Adapter Sandbox Run Readiness Gate

**Status:** Planned
**Branch:** `feature/P42-T7-real-local-trusted-adapter-sandbox-run-readiness-gate`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T6 Synthetic Trusted Local Adapter Sandbox Run Verifier

## Recently Archived

- `P42-T6` added
  `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport`.
- The verifier CLI is
  `synthetic-trusted-local-adapter-sandbox-run-verifier`.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_SYNTHETIC_SANDBOX_RUN_VERIFIER.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterSyntheticSandboxRunVerifier.md`.
- The verifier checks P42-T5 fixture identity, linked artifact digests,
  operator approval binding, synthetic output byte sizes/digests, audit
  references, and no-real-execution boundaries.
- The verifier rejects unsafe paths, missing linked artifacts, digest mismatch,
  output byte-size mismatch, bad approval binding, bad audit references, and
  real-execution drift.
- The verifier remains producer-side review evidence only and preserves
  `adapterExecution: synthetic_fixture_only`,
  `realAdapterProcessSpawned: false`,
  `thirdPartyAdapterCodeLoaded: false`, `executedAdapterCount: 0`,
  `dependencyInstallation: not_allowed`, `packageManagers: not_invoked`,
  `networkAccess: none`,
  `syntheticRunVerificationIsExecutionPermission: false`, and
  `registryAuthority: false`.

## Task

Add a real local trusted adapter sandbox run readiness gate that validates the
P42-T6 verifier report plus explicit real-run prerequisites before any future
real adapter execution implementation.

## Why This Is Next

P42-T6 proves synthetic run evidence is internally consistent. Before a real
local adapter process can be considered, SpecHarvester needs a separate
readiness gate that checks runtime prerequisites, explicit operator approval
requirements, sandbox availability, output/audit policy, and rollback boundary
without loading adapter code or spawning a process.

## Scope

- Add a machine-readable real-local sandbox readiness gate/report.
- Validate the P42-T6 verifier report identity and authority.
- Validate explicit real-run operator approval prerequisites.
- Validate sandbox runtime availability requirements without invoking the
  runtime.
- Validate filesystem/output/audit policy readiness.
- Validate no adapter code loading, no process spawning, no dependency
  installation, no package manager invocation, and no network access during the
  readiness gate.
- Emit a machine-readable readiness report.
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
- [ ] `P42-T7` Add a real local trusted adapter sandbox run readiness gate that
  checks the P42-T6 verifier report plus explicit real-run prerequisites,
  sandbox runtime availability, filesystem/output policy, audit requirements,
  and operator approval requirements while still refusing to load adapter code
  or spawn adapter processes.

Motivation:

- Real adapter execution requires a separate readiness gate after synthetic
  evidence verification.
- Readiness should make runtime prerequisites explicit before any process
  execution implementation exists.
- The gate should preserve least privilege and review-only authority.

Goal:

- Provide a machine-checkable readiness report for future real local trusted
  adapter sandbox runs without granting execution permission.

Acceptance:

- The readiness gate checks verifier report identity, real-run prerequisites,
  sandbox runtime requirements, filesystem/output/audit policy, and
  no-execution boundaries.
- The readiness report is review-only and cannot be interpreted as runtime
  permission or registry authority.
