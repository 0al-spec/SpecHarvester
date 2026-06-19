# P41-T6 Real Local Trusted-Adapter Readiness Validation

**Branch:** `feature/P41-T6-real-local-trusted-adapter-readiness-validation`
**Status:** Planned
**Phase:** Phase 41. Trusted Local Adapter Runtime Readiness

## Motivation

P41-T2 through P41-T5 define the trusted local adapter request, preflight,
disabled runner report, and explicit batch evidence handoff. Those contracts
are useful only if the full path can be exercised against representative real
repository shapes without accidentally enabling adapter execution or weakening
the static default evaluator path.

This validation is the practical readiness checkpoint before any future runtime
work. It should compare existing pinned local checkouts for FastMCP, FastAPI,
xyflow, and Gin while keeping adapter output strictly non-authoritative and
disabled.

## Goal

Produce durable validation evidence that the trusted local adapter readiness
path can be run over real pinned checkouts while preserving all no-execution,
no-network, no-dependency-installation, and non-authority boundaries.

## Deliverables

1. Verify the availability and pinned revisions of local FastMCP, FastAPI,
   xyflow, and Gin checkouts, recording skipped repositories explicitly if any
   checkout is missing.
2. Reuse the trusted local adapter run request, preflight, and disabled runner
   report artifacts as the trusted-local-adapter input path.
3. Exercise `autonomous-candidate-batch` with explicit
   `--trusted-local-adapter-run-report` input over the representative real
   repository shapes.
4. Add a durable validation fixture that records repository shape coverage,
   checkout status, batch evidence sidecar linkage, and no-execution counters.
5. Add regression coverage for the fixture so future changes cannot silently
   turn readiness evidence into adapter execution or registry authority.
6. Update GitHub docs and DocC to explain the practical validation, the
   representative corpus, and the remaining runtime gap.
7. Update roadmap/workplan/current task pointers for the next Phase 41 step.

## Acceptance Criteria

- The validation fixture covers FastMCP, FastAPI, xyflow, and Gin, or records
  missing local checkouts as skipped with reasons.
- Every recorded repository entry preserves:
  - `adapterExecution: not_run`
  - `adapterCodeLoaded: false`
  - `adapterProcessSpawned: false`
  - `executedAdapterCount: 0`
  - `appliedToDrafting: false`
  - `registryAuthority: false`
- Aggregate counters record zero adapter processes, package manager
  invocations, dependency installations, network discovery, harvested code
  execution, and AI execution caused by the trusted local adapter path.
- Batch output records trusted local adapter run evidence only through explicit
  operator input.
- Existing static evaluator and repository plugin adapter sidecar paths remain
  unchanged.
- Docs and DocC state that this is readiness evidence, not real adapter
  execution, not adapter output truth, and not SpecPM registry acceptance.

## Non-Goals

- Do not implement real adapter execution.
- Do not load third-party adapter code.
- Do not run adapter processes.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI because of this validation.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat runner reports as registry truth.
- Do not replace the static evaluator.

## Dependencies

- P41-T2 `SpecHarvesterTrustedLocalAdapterRunRequest`.
- P41-T3 `SpecHarvesterTrustedLocalAdapterRunPreflightReport`.
- P41-T4 disabled trusted local adapter runner report.
- P41-T5 `autonomous-candidate-batch --trusted-local-adapter-run-report`.
- Existing P40 real local adapter contract validation corpus.

## Validation Plan

- Run a real local readiness smoke over available FastMCP, FastAPI, xyflow, and
  Gin checkouts.
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- Static DocC generation command from the project docs build path.

## Review Notes

Review should focus on authority and execution boundaries:

- The fixture must not imply that any adapter ran.
- The batch sidecar must remain explicit operator-provided evidence.
- The validation must not normalize skipped or missing checkouts into success.
- The report must keep real runtime implementation as a future gap.
