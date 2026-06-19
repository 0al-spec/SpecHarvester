# Next Task: P41-T6 Real Local Trusted-Adapter Readiness Validation

**Status:** In Progress
**Branch:** `feature/P41-T6-real-local-trusted-adapter-readiness-validation`
**Phase:** Phase 41. Trusted Local Adapter Runtime Readiness
**Last Archived:** P41-T5 Trusted Local Adapter Run Evidence Handoff

## Recently Archived

- `P41-T5` added `autonomous-candidate-batch
  --trusted-local-adapter-run-report`.
- Batch output can now copy a
  `SpecHarvesterTrustedLocalAdapterRunReport` to
  `reports/trusted-local-adapter-run-evidence/trusted-local-adapter-run-report.json`.
- Batch reports now include `trustedLocalAdapterRunEvidence` and
  `trustedLocalAdapterRunEvidenceSidecarCount`.
- The sidecar records source/copied SHA-256 digests, report identity,
  diagnostic codes, runner status, and no-execution boundary fields.
- The handoff keeps `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `adapterProcessSpawned: false`,
  `executedAdapterCount: 0`, `appliedToDrafting: false`, and
  `registryAuthority: false`.
- Invalid authority-bearing or execution-bearing trusted run reports are
  rejected before batch output is emitted.
- The batch still preserves the default static evaluator path and existing
  repository plugin sidecar paths.

## Task

Run a real local trusted-adapter readiness validation over existing pinned
checkouts, comparing FastMCP, FastAPI, xyflow, and Gin while proving that no
adapter process, package manager, dependency installer, network discovery,
harvested code, or AI execution occurred.

## Why This Is Next

P41-T2 through P41-T5 define the request, preflight, disabled runner report, and
batch evidence handoff. The remaining readiness question is practical: can the
full no-execution evidence path be run over representative real repositories
without accidentally enabling adapter execution or weakening the static default
path?

## Scope

- Use existing pinned local checkouts for FastMCP, FastAPI, xyflow, and Gin when
  available.
- Build or reuse trusted local adapter run request/preflight/report artifacts
  for each repository shape.
- Attach trusted local adapter run reports to `autonomous-candidate-batch`
  output through `--trusted-local-adapter-run-report`.
- Compare readiness output across documentation-heavy, Python web framework,
  JavaScript/TypeScript package-set, and Go single-package shapes.
- Record a durable real-run validation fixture and GitHub/DocC documentation.
- Prove all relevant boundaries remain no-execution:
  - `adapterExecution: not_run`
  - `adapterCodeLoaded: false`
  - `adapterProcessSpawned: false`
  - `executedAdapterCount: 0`
  - no dependency installation
  - no package manager invocation
  - no network discovery
  - no harvested code execution
  - no AI execution because of the adapter sidecar
  - `appliedToDrafting: false`
  - `registryAuthority: false`

## Non-Goals

- Do not implement real adapter execution.
- Do not run adapter processes.
- Do not load third-party adapter code.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI because of this validation.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output or runner reports as registry truth.

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
- [x] `P41-T5` Connect trusted local adapter run reports to
  `autonomous-candidate-batch` as explicit review-only producer evidence while
  preserving the default static evaluator and existing adapter sidecar paths.
- [ ] `P41-T6` Run a real local trusted-adapter readiness validation over
  existing pinned checkouts, comparing FastMCP, FastAPI, xyflow, and Gin while
  proving no adapter process, package manager, dependency installer, network
  discovery, harvested code, or AI execution occurred.

Motivation:

- The contracts are now wired together, but the end-to-end no-execution path
  needs real repository evidence before any future runtime work.
- Representative repository shapes should prove the sidecar remains review
  evidence and does not alter autonomous drafting.

Goal:

- Produce durable validation evidence that the trusted local adapter readiness
  path works over real pinned checkouts without executing adapters.

Acceptance:

- A real-run validation fixture covers FastMCP, FastAPI, xyflow, and Gin, or
  explicitly records missing local checkouts as skipped with reasons.
- Every recorded run preserves no-execution and non-authority fields.
- Batch output records trusted local adapter run evidence only through explicit
  operator input.
- Existing static evaluator and adapter sidecar paths remain unchanged.
- Docs and DocC explain the practical validation and remaining runtime gap.
