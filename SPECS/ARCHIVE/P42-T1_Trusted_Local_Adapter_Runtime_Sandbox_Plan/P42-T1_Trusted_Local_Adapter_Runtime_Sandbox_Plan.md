# P42-T1 Trusted Local Adapter Runtime Sandbox Plan

**Branch:** `feature/P42-T1-trusted-local-adapter-runtime-sandbox-plan`
**Status:** Planned
**Phase:** Phase 42. Trusted Local Adapter Runtime Sandbox

## Motivation

Phase 41 proves the no-execution readiness path: requests, preflight, disabled
runner reports, batch evidence handoff, and real local validation over pinned
repositories. The next boundary must be the sandbox contract for future runtime
execution, not implementation.

Real trusted local adapter execution needs explicit rules for adapter package
identity, process isolation, dependency isolation, filesystem access,
environment sealing, network policy, output verification, and audit records
before any adapter process can run. Capturing that plan first prevents future
adapter precision work from silently becoming an unsafe local execution engine.

## Goal

Document the language- and framework-agnostic trusted local adapter runtime
sandbox boundary that future implementation must satisfy, while keeping this
task documentation-only and preserving `adapterExecution: not_run`.

## Deliverables

1. Add GitHub documentation for the trusted local adapter runtime sandbox plan.
2. Add a DocC mirror for the same plan.
3. Define required sandbox layers:
   - explicit operator approval;
   - adapter package identity and pinning;
   - process isolation;
   - filesystem input and output allowlists;
   - sealed environment;
   - dependency isolation;
   - network-deny-by-default policy;
   - timeout, process, memory, and output budgets;
   - output digests and verification;
   - audit records and replayable receipts;
   - review-only authority.
4. Define the first follow-up task for a future machine-readable sandbox
   contract fixture.
5. Link the plan from runtime readiness docs, capabilities, roadmap, docs
   index, and DocC root.
6. Add regression coverage that proves the documentation exists, references the
   right boundaries, and does not imply enabled adapter execution.
7. Archive the task and review artifacts according to Flow.

## Acceptance Criteria

- The sandbox plan is explicitly language- and framework-agnostic.
- The plan preserves `adapterExecution: not_run` for the current system.
- The plan states that future runtime execution requires explicit operator
  approval and must not be enabled by default.
- The plan requires adapter package identity, pinned revisions or digests,
  process isolation, safe relative path policies, sealed environment,
  dependency isolation, network-deny-by-default policy, output budgets, output
  digests, audit records, and replayable approval.
- The plan states that runtime outputs are producer-side review evidence and
  never accept packages, accept relations, seed baselines, publish registry
  metadata, remove `preview_only`, or treat adapter output as registry truth.
- Tests validate the plan docs, DocC mirror, roadmap/capability references, and
  selected `next.md` task scaffold.

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
- Do not treat adapter output, runner reports, sandbox plans, or AI output as
  registry truth.

## Dependencies

- Phase 40 repository plugin adapter contract.
- Phase 41 trusted local adapter runtime readiness artifacts.
- P41-T6 real local trusted-adapter readiness validation.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- Static DocC generation command from the project docs build path.
- Coverage gate with `--cov-fail-under=90`.

## Review Notes

Review should focus on scope control:

- The plan must not promise or enable runtime execution.
- Runtime output must remain review evidence, not accepted truth.
- Future implementation requirements must be strong enough to prevent hidden
  dependency installation, package manager invocation, network discovery, or
  harvested code execution.
