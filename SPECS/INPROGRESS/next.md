# Next Task: P42-T2 Trusted Local Adapter Sandbox Contract Fixture

**Status:** Planned
**Branch:** `feature/P42-T2-trusted-local-adapter-sandbox-contract-fixture`
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox
**Last Archived:** P42-T1 Trusted Local Adapter Runtime Sandbox Plan

## Recently Archived

- `P42-T1` documented the trusted local adapter runtime sandbox plan.
- GitHub docs are in
  `docs/TRUSTED_LOCAL_ADAPTER_RUNTIME_SANDBOX_PLAN.md`.
- DocC docs are in
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterRuntimeSandboxPlan.md`.
- The plan requires explicit operator approval, adapter package identity,
  process isolation, sealed environment, dependency isolation,
  network-deny-by-default policy, output digests, audit records, and
  review-only authority before any future adapter process can run.
- The current state remains `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `adapterProcessSpawned: false`,
  `executedAdapterCount: 0`, and `registryAuthority: false`.

## Task

Add a machine-readable `SpecHarvesterTrustedLocalAdapterSandboxContract`
fixture that records adapter package identity, sandbox policy identity, operator
approval requirements, filesystem/environment/network/dependency policy, output
verification, audit records, and non-authority statements before any runtime
implementation.

## Why This Is Next

P42-T1 defines the sandbox layers in documentation. The next step is to make
that boundary machine-readable so future preflight and runner work can validate
the same contract instead of relying on prose.

## Scope

- Add a JSON fixture for `SpecHarvesterTrustedLocalAdapterSandboxContract`.
- Record contract identity, adapter package identity, sandbox policy identity,
  operator approval requirements, process limits, filesystem policy,
  environment policy, dependency policy, network-deny-by-default policy,
  output verification requirements, audit record requirements, and
  non-authority statements.
- Link the fixture from GitHub docs, DocC, roadmap/capabilities, and tests.
- Preserve the no-execution boundary.

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
- Do not treat adapter output as registry truth.

## Phase 42. Trusted Local Adapter Runtime Sandbox

- [x] `P42-T1` Document the trusted local adapter runtime sandbox plan and add
  the next-task scaffold for turning Phase 41 no-execution readiness into a
  future explicitly approved sandboxed adapter runtime without enabling adapter
  execution yet.
- [ ] `P42-T2` Add a machine-readable
  `SpecHarvesterTrustedLocalAdapterSandboxContract` fixture that records
  adapter package identity, sandbox policy identity, operator approval
  requirements, filesystem/environment/network/dependency policy, output
  verification, audit records, and non-authority statements before any runtime
  implementation.

Motivation:

- The sandbox plan should become verifiable data before a sandbox preflight or
  runner implementation exists.
- Future adapter runtime work needs a stable contract for approval, isolation,
  dependency, network, output, and authority boundaries.

Goal:

- Make the P42 sandbox boundary machine-readable without enabling adapter
  execution.

Acceptance:

- The fixture records all required sandbox identity, policy, approval, output,
  audit, and non-authority fields.
- The fixture keeps `adapterExecution: not_run` and cannot be interpreted as
  runtime permission.
- Docs and tests prove the fixture remains producer-side review evidence only.
