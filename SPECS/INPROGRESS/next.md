# Next Task: P41-T2 Trusted Local Adapter Run Request Fixture

**Status:** Planned
**Branch:** `feature/P41-T2-trusted-local-adapter-run-request-fixture`
**Phase:** Phase 41. Trusted Local Adapter Runtime Readiness
**Last Archived:** P41-T1 Adapter Runtime Readiness Plan

## Recently Archived

- `P41-T1` documented trusted local adapter runtime readiness.
- The GitHub-facing documentation is
  `docs/TRUSTED_LOCAL_ADAPTER_RUNTIME_READINESS.md`.
- The DocC mirror is
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterRuntimeReadiness.md`.
- The plan defines the path for `SpecHarvesterTrustedLocalAdapterRunRequest`,
  trusted local adapter run preflight, disabled no-execution runner skeleton,
  review-only batch evidence handoff, and real local readiness validation.
- adapter execution remains disabled; trusted local adapter artifacts remain
  producer-side review evidence and have no registry authority.

## Task

Add a machine-readable `SpecHarvesterTrustedLocalAdapterRunRequest` fixture
that records operator opt-in, adapter manifest/preflight references, declared
input artifacts, safe relative read path allowlists, output directory policy,
resource budgets, environment policy, network policy, dependency policy,
package manager policy, and non-authority statements.

## Why This Is Next

P41-T1 defines the safe readiness path. The first concrete artifact should be
the request contract, because preflight, runner skeletons, and batch evidence
handoff need a stable request shape before they can validate or consume
anything.

## Scope

- Add a versioned `SpecHarvesterTrustedLocalAdapterRunRequest` fixture.
- Reference the Phase 40 adapter manifest and adapter preflight fixtures.
- Require explicit operator opt-in.
- Record declared input artifacts with safe relative paths and SHA-256 digests.
- Record safe relative read path allowlists.
- Record output directory policy, timeout budgets, maximum output sizes,
  environment policy, network policy, dependency policy, package manager
  policy, and process execution policy.
- Record non-authority statements.
- Document the fixture in GitHub docs and DocC.
- Keep adapter execution disabled.

## Non-Goals

- Do not implement adapter loading or execution.
- Do not run adapter processes.
- Do not implement preflight logic yet.
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
- [ ] `P41-T2` Add a machine-readable
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

- The trusted local adapter request is the root input for future preflight and
  no-execution runner work.
- The request contract must require opt-in, path limits, budgets, and
  non-authority output before any future execution mode exists.

Goal:

- Define the machine-readable request shape for future trusted local adapter
  execution while keeping execution disabled and non-authoritative.

Acceptance:

- The fixture has versioned identity and stable authority labels.
- The fixture records explicit operator opt-in.
- The fixture records safe relative paths, SHA-256 digests, path allowlists,
  budgets, environment policy, network policy, dependency policy, package
  manager policy, process execution policy, and non-authority statements.
- Docs and DocC explain that the request is not permission to execute by
  itself and is not registry acceptance.
