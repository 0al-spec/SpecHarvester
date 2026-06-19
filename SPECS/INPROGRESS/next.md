# Next Task: P41-T4 Disabled Trusted Local Adapter Runner Skeleton

**Status:** In Progress
**Branch:** `feature/P41-T4-disabled-trusted-local-adapter-runner-skeleton`
**Phase:** Phase 41. Trusted Local Adapter Runtime Readiness
**Last Archived:** P41-T3 Trusted Local Adapter Run Preflight Report Fixture

## Recently Archived

- `P41-T3` added the machine-readable
  `SpecHarvesterTrustedLocalAdapterRunPreflightReport`.
- The fixture is
  `tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json`.
- The GitHub-facing documentation is
  `docs/TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_REPORT_FIXTURE.md`.
- The DocC mirror is
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterRunPreflightReportFixture.md`.
- The preflight report references
  `SpecHarvesterTrustedLocalAdapterRunRequest`, records accepted, rejected,
  blocked, and warning checks, and keeps
  `preflightPassIsExecutionPermission: false`,
  `adapterExecution: not_run`, `adapterCodeLoaded: false`, and
  `registryAuthority: false`.
- Trusted local adapter preflight artifacts remain producer-side review
  evidence, not execution permission and not registry authority.

## Task

Implement a disabled-by-default trusted local adapter runner skeleton that can
validate a request and emit a no-execution report while proving it does not
load third-party adapter code and does not run adapter processes.

## Why This Is Next

P41-T2 defines the request shape and P41-T3 defines the preflight report shape.
The next step is a no-execution runner skeleton that consumes those contracts
without enabling real adapter execution. This creates a practical local
validation surface for future runtime work while preserving
`adapterExecution: not_run` and `adapterCodeLoaded: false`.

## Scope

- Add a disabled-by-default runner skeleton entry point or helper.
- Validate `SpecHarvesterTrustedLocalAdapterRunRequest` identity and
  `SpecHarvesterTrustedLocalAdapterRunPreflightReport` identity.
- Emit a deterministic no-execution report.
- Record that the runner does not load third-party adapter code and does not
  run adapter processes.
- Preserve `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `executedAdapterCount: 0`, `runtimeImplemented: false`,
  `appliedToDrafting: false`, and `registryAuthority: false`.
- Document the skeleton in GitHub docs and DocC.
- Keep the output as producer-side review evidence only.

## Non-Goals

- Do not implement real adapter execution.
- Do not run adapter processes.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output as registry truth.

## Phase 41. Trusted Local Adapter Runtime Readiness

- [x] `P41-T1` Document the trusted local adapter runtime readiness plan and
  add the next-task scaffold for turning Phase 40 adapter contracts into a
  future opt-in runtime without enabling adapter execution yet.
- [x] `P41-T2` Add a machine-readable
  `SpecHarvesterTrustedLocalAdapterRunRequest` fixture that records operator
  opt-in, adapter manifest/preflight references, declared input artifacts,
  safe relative read path allowlists, output directory policy, resource
  budgets, environment policy, network policy, dependency policy, package
  manager policy, and non-authority statements.
- [x] `P41-T3` Add a trusted local adapter run preflight report fixture that
  validates run requests before execution and rejects unsafe paths, missing
  digests, missing operator opt-in, network access, dependency installation,
  package manager invocation, harvested code execution, unbounded process
  execution, and undeclared outputs.
- [ ] `P41-T4` Implement a disabled-by-default trusted local adapter runner
  skeleton that can validate a request and emit a no-execution report without
  loading third-party adapter code or running adapter processes.
- [ ] `P41-T5` Connect trusted local adapter run reports to
  `autonomous-candidate-batch` as explicit review-only producer evidence while
  preserving the default static evaluator and existing adapter sidecar paths.
- [ ] `P41-T6` Run a real local trusted-adapter readiness validation over
  existing pinned checkouts, comparing FastMCP, FastAPI, xyflow, and Gin while
  proving no adapter process, package manager, dependency installer, network
  discovery, harvested code, or AI execution occurred.

Motivation:

- Future runtime work needs a concrete local skeleton that consumes request and
  preflight report artifacts before any real execution mode can be discussed.
- The skeleton should make no-execution behavior testable and reviewable.

Goal:

- Add a disabled no-execution runner skeleton that validates request/preflight
  inputs and emits a report while preserving the no-runtime and no-authority
  boundaries.

Acceptance:

- The skeleton is disabled by default and does not run adapter processes.
- The skeleton validates request and preflight identities.
- The skeleton emits a deterministic no-execution report.
- The report records `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `executedAdapterCount: 0`, `runtimeImplemented: false`,
  `appliedToDrafting: false`, and `registryAuthority: false`.
- Docs and DocC explain that the skeleton is not real adapter execution and
  not registry acceptance.
