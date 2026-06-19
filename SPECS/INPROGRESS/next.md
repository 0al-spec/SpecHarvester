# Next Task: P41-T3 Trusted Local Adapter Run Preflight Report Fixture

**Status:** Planned
**Branch:** `feature/P41-T3-trusted-local-adapter-run-preflight-report-fixture`
**Phase:** Phase 41. Trusted Local Adapter Runtime Readiness
**Last Archived:** P41-T2 Trusted Local Adapter Run Request Fixture

## Recently Archived

- `P41-T2` added the machine-readable
  `SpecHarvesterTrustedLocalAdapterRunRequest`.
- The fixture is
  `tests/fixtures/repository_plugins/trusted-local-adapter-run-request.example.json`.
- The GitHub-facing documentation is
  `docs/TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_FIXTURE.md`.
- The DocC mirror is
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterRunRequestFixture.md`.
- The request records adapter manifest/preflight references, explicit operator
  opt-in, declared input artifacts, safe relative read path allowlists, output
  policy, resource budgets, environment policy, network policy, dependency
  policy, package manager policy, process policy, and non-authority
  statements.
- The request keeps `requestIsExecutionPermission: false`,
  `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `appliedToDrafting: false`, and `registryAuthority: false`; trusted local
  adapter artifacts remain producer-side review evidence.

## Task

Add a machine-readable
`SpecHarvesterTrustedLocalAdapterRunPreflightReport` fixture that validates a
`SpecHarvesterTrustedLocalAdapterRunRequest` before any future execution path
and rejects unsafe paths, missing or mismatched digests, missing explicit
operator opt-in, undeclared input artifacts, undeclared output paths, network
access, dependency installation, package manager invocation, harvested code
execution, AI execution, unbounded process execution, and unbounded outputs.

## Why This Is Next

P41-T2 defines the trusted local adapter run request shape. The next artifact
must prove how that request is checked before any runner skeleton can consume
it. The preflight report should make failure modes explicit and state that
preflight pass is not execution permission.

## Scope

- Add a versioned
  `SpecHarvesterTrustedLocalAdapterRunPreflightReport` fixture.
- Reference the P41-T2 run request fixture with a SHA-256 digest.
- Validate request identity, schema version, authority, explicit operator
  opt-in, adapter manifest/preflight references, declared input artifacts,
  path policy, read allowlists, output policy, resource budgets, environment
  policy, network policy, dependency policy, package manager policy, process
  policy, execution boundary, and non-authority statements.
- Record accepted, rejected, blocked, and warning checks.
- Reject unsafe paths, missing or mismatched digests, undeclared input
  artifacts, undeclared output paths, network access, dependency installation,
  package manager invocation, harvested code execution, AI execution,
  unbounded process execution, and unbounded output policy.
- Document the fixture in GitHub docs and DocC.
- Keep adapter execution disabled.

## Non-Goals

- Do not implement adapter loading or execution.
- Do not run adapter processes.
- Do not add a runner.
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
- [ ] `P41-T3` Add a trusted local adapter run preflight report fixture that
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

- Future runner work needs a strict preflight report over P41-T2 requests
  before any no-execution runner skeleton can be introduced.
- The preflight fixture should make unsafe request shapes reviewable before
  implementation logic exists.

Goal:

- Define the machine-readable preflight report shape for trusted local adapter
  run requests while proving that preflight pass is not execution permission
  and adapter execution remains disabled.

Acceptance:

- The fixture has versioned identity and stable authority labels.
- The fixture references the P41-T2 request fixture with a SHA-256 digest.
- The fixture records checks for identity, explicit operator opt-in, safe
  paths, declared input artifacts, digests, output policy, resource budgets,
  environment policy, network policy, dependency policy, package manager
  policy, process policy, execution boundary, and non-authority statements.
- Unsafe paths, missing or mismatched digests, undeclared input artifacts,
  undeclared output paths, network access, dependency installation, package
  manager invocation, harvested code execution, AI execution, unbounded process
  execution, and unbounded outputs are rejected or blocked.
- Docs and DocC explain that preflight pass is not execution permission, not
  registry acceptance, and not adapter output truth.
