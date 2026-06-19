# P41-T1 Adapter Runtime Readiness Plan

Status: Planned
Phase: Phase 41. Trusted Local Adapter Runtime Readiness

## Motivation

Phase 40 defines the repository plugin adapter contract, manifest and preflight
fixtures, disabled-by-default execution policy, batch evidence handoff, fixture
matrix coverage, and real local validation. That is enough to discuss future
adapters, but not enough to safely introduce any local adapter process.

Before SpecHarvester can run even trusted local adapters, the project needs a
readiness phase that defines request shape, preflight shape, no-execution
runner behavior, evidence handoff, and real local validation. This task creates
that phase and selects the first concrete follow-up without enabling runtime
execution.

## Goal

Add Phase 41 to the Workplan and documentation as the path from Phase 40
adapter contracts toward a future trusted local adapter runtime, while keeping
adapter execution disabled and producer-side evidence non-authoritative.

## Deliverables

- Add Phase 41 tasks to `SPECS/Workplan.md`.
- Add GitHub docs for the trusted local adapter runtime readiness plan.
- Add a DocC mirror for the readiness plan.
- Link the readiness plan from docs index, DocC root, capabilities, roadmap,
  and adjacent Phase 40 adapter docs.
- Update docs-contract regression tests for Phase 41 and the selected P41-T2
  next task state.
- Archive P41-T1 and select P41-T2 after archive.

## Acceptance Criteria

- Phase 41 contains tasks for:
  - trusted local adapter run request fixture;
  - trusted local adapter run preflight fixture;
  - disabled no-execution runner skeleton;
  - autonomous batch evidence handoff;
  - real local trusted-adapter readiness validation.
- The plan states that adapter execution remains disabled by default.
- The plan requires explicit operator opt-in before future execution.
- The plan requires safe relative path allowlists, declared input artifacts,
  digests, resource budgets, and environment policy.
- The plan rejects network access, dependency installation, package manager
  invocation, harvested code execution, AI execution, unsafe paths, missing
  digests, and undeclared outputs before execution.
- The plan states that runtime artifacts remain producer-side review evidence
  and never accept packages, accept relations, seed baselines, publish registry
  metadata, remove `preview_only`, or treat adapter output as registry truth.

## Non-Goals

- Do not implement adapter loading or execution.
- Do not add a runner in this task.
- Do not create trusted local adapter run request fixtures in this task.
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

## Validation

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
