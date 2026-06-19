# Next Task: P41-T5 Trusted Local Adapter Run Evidence Handoff

**Status:** In Progress
**Branch:** `feature/P41-T5-trusted-local-adapter-run-evidence-handoff`
**Phase:** Phase 41. Trusted Local Adapter Runtime Readiness
**Last Archived:** P41-T4 Disabled Trusted Local Adapter Runner Skeleton

## Recently Archived

- `P41-T4` added the disabled `trusted-local-adapter-runner-skeleton` CLI.
- The runner emits `SpecHarvesterTrustedLocalAdapterRunReport` as
  producer-side review evidence.
- The GitHub-facing documentation is
  `docs/TRUSTED_LOCAL_ADAPTER_RUNNER_SKELETON.md`.
- The DocC mirror is
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterRunnerSkeleton.md`.
- The skeleton validates `SpecHarvesterTrustedLocalAdapterRunRequest` and
  `SpecHarvesterTrustedLocalAdapterRunPreflightReport`, verifies request
  digest linkage, and keeps `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `adapterProcessSpawned: false`,
  `executedAdapterCount: 0`, `runnerReportIsExecutionPermission: false`,
  `appliedToDrafting: false`, and `registryAuthority: false`.
- Trusted local adapter run reports remain producer-side review evidence, not
  execution permission, not adapter output truth, and not registry authority.

## Task

Connect trusted local adapter run reports to `autonomous-candidate-batch` as
explicit review-only producer evidence while preserving the default static
evaluator and existing adapter sidecar paths.

## Why This Is Next

P41-T2 defines the run request, P41-T3 defines the run preflight report, and
P41-T4 defines the disabled no-execution runner report. The next step is to
make that report attachable to autonomous batch output as sidecar evidence
without changing drafting behavior or treating the report as adapter output.

## Scope

- Add an opt-in `autonomous-candidate-batch` input for
  `SpecHarvesterTrustedLocalAdapterRunReport`.
- Copy the trusted local adapter run report into batch output as explicit
  review-only producer evidence.
- Preserve the default static evaluator path when no run report is supplied.
- Preserve existing `repositoryPluginApplicability` and
  `repositoryPluginAdapterEvidence` sidecar behavior.
- Record copied path, SHA-256 digest, report identity, no-execution boundary,
  and non-authority statements in the batch report.
- Keep `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `adapterProcessSpawned: false`, `executedAdapterCount: 0`,
  `appliedToDrafting: false`, and `registryAuthority: false`.
- Document the batch evidence handoff in GitHub docs and DocC.

## Non-Goals

- Do not implement real adapter execution.
- Do not run adapter processes.
- Do not load third-party adapter code.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI because of this sidecar.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output as registry truth.
- Do not replace static plugin applicability evaluation.

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
- [x] `P41-T4` Implement a disabled-by-default trusted local adapter runner
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

- Future trusted local adapter reports need a visible producer evidence handoff
  path before any real execution mode is considered.
- Operators should be able to attach no-execution runner evidence to batch
  output without changing candidate drafting or registry authority.

Goal:

- Add an opt-in batch sidecar path for trusted local adapter run reports while
  preserving no-execution and non-authority boundaries.

Acceptance:

- Batch output can include a copied trusted local adapter run report only when
  the operator supplies one explicitly.
- The copied report has a SHA-256 digest and validated identity in the batch
  report.
- Existing default static evaluator and adapter evidence sidecar paths still
  work without trusted local adapter run evidence.
- The sidecar records `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `adapterProcessSpawned: false`,
  `executedAdapterCount: 0`, `appliedToDrafting: false`, and
  `registryAuthority: false`.
- Docs and DocC explain that trusted local adapter run evidence is review-only
  producer evidence, not adapter output truth and not registry acceptance.
