# P42-T7 Real Local Trusted Adapter Sandbox Run Readiness Gate

## Summary

Add a deterministic
`SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport` producer gate
that validates the P42-T6 verifier report and explicit real-run prerequisites
before any future real local trusted adapter sandbox execution implementation.

## Motivation

P42-T6 proves the synthetic sandbox run evidence is internally consistent. A
future real local adapter run still needs a separate readiness gate because
verified synthetic evidence is not execution permission.

The readiness gate should make explicit which prerequisites would be required
for a future real run: operator approval, sandbox runtime availability,
filesystem and output policy, audit requirements, dependency isolation, network
policy, and rollback/review boundaries. It must perform those checks without
loading adapter code, spawning a process, installing dependencies, invoking
package managers, using network access, executing harvested code, or granting
registry authority.

## Deliverables

- Add a machine-readable real-local sandbox readiness report builder.
- Add a CLI command that reads a P42-T6 verifier report and emits
  `SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport`.
- Validate:
  - P42-T6 verifier report identity, status, authority, and non-authority
    statements;
  - verifier fixture reference and linked artifact/output/audit verification
    counts;
  - explicit real-run operator approval prerequisites;
  - sandbox runtime availability requirements as declared readiness inputs
    without invoking any runtime;
  - filesystem/output/audit policy readiness;
  - no adapter code loading, no process spawning, no dependency installation,
    no package manager invocation, no network access, no harvested code
    execution, and no AI execution during the readiness gate.
- Emit a deterministic readiness report with review-only authority.
- Add GitHub docs, DocC docs, roadmap/capabilities links, and regression tests.
- Archive Flow artifacts and choose the next task.

## Acceptance Criteria

- A valid P42-T6 verifier report produces a deterministic readiness report with:
  - `apiVersion:
    spec-harvester.real-local-trusted-adapter-sandbox-run-readiness/v0`;
  - `kind:
    SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport`;
  - `schemaVersion: 1`;
  - `status: ready_for_explicit_real_run_review`;
  - producer-side review-only readiness authority.
- The readiness gate rejects malformed verifier identity/authority/status.
- The readiness gate rejects verifier drift that weakens no-real-execution or
  non-authority statements.
- The readiness report records that the readiness gate itself did not:
  - load adapter code;
  - spawn adapter processes;
  - install dependencies;
  - invoke package managers;
  - use network access;
  - execute harvested repository code;
  - run AI because of adapter execution.
- The readiness report records that it is not execution permission, not
  registry authority, and not package/relation acceptance.
- CLI, tests, docs, DocC, roadmap, capabilities, Workplan, archive, and review
  artifacts are updated through Flow.

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

## Validation Plan

- `PYTHONPATH=src pytest tests/test_trusted_local_adapter_real_local_sandbox_readiness.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_real_local_trusted_adapter_sandbox_run_readiness_gate_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q`
- DocC static generation
- CLI smoke using the P42-T6 verifier report generated from the P42-T5 fixture
