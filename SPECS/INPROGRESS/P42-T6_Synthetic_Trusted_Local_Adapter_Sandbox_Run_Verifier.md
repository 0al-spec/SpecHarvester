# P42-T6 Synthetic Trusted Local Adapter Sandbox Run Verifier

## Summary

Add a deterministic
`SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport` producer
gate for the P42-T5 synthetic sandbox run fixture. The verifier checks fixture
identity, linked artifact digests, approval binding, synthetic output
byte-size/digest metadata, audit references, and no-real-execution boundaries
without enabling adapter execution.

## Motivation

P42-T5 records an explicitly approved synthetic sandbox run as review evidence.
That artifact is useful only if downstream tooling can verify that the fixture
still matches the linked sandbox contract, sandbox preflight, runner validation,
synthetic outputs, diagnostics, and audit record bytes.

This task turns the synthetic fixture from "declared shape" into a
machine-checkable review gate. It preserves the key security boundary:
verification proves the evidence is internally consistent, but it is not
permission to run a real adapter and it is not registry authority.

## Deliverables

- Add verifier logic for
  `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRun`.
- Add a CLI command that emits
  `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport`.
- Validate:
  - fixture API version, kind, schema version, and authority;
  - safe relative paths for linked artifacts and output artifacts;
  - linked artifact SHA-256 digests;
  - operator approval binding to one adapter, repository revision, sandbox
    policy, runner validation report, and synthetic output root;
  - synthetic output byte sizes, digests, authority, adapter identity, and
    source input digest references;
  - audit record path/digest/reference requirements;
  - no-real-execution and non-authority statements.
- Document the verifier in GitHub docs and DocC.
- Link the verifier from capabilities, roadmap, sandbox fixture docs, and tests.
- Archive Flow artifacts and choose the next task.

## Acceptance Criteria

- A valid P42-T5 fixture produces a deterministic verifier report with:
  - `apiVersion:
    spec-harvester.synthetic-trusted-local-adapter-sandbox-run-verifier/v0`;
  - `kind: SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport`;
  - `schemaVersion: 1`;
  - `status: passed`;
  - producer-side review-only verifier authority.
- The verifier rejects malformed fixture identity/authority.
- The verifier rejects unsafe paths, missing linked artifacts, digest mismatch,
  output byte-size mismatch, bad approval binding, bad audit references, and
  any drift toward real adapter execution.
- The verifier report explicitly records:
  - no real adapter process spawned;
  - no third-party adapter code loaded;
  - no dependency installation;
  - no package manager invocation;
  - no network access;
  - no registry authority;
  - no adapter output accepted as registry truth.
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

## Validation Plan

- `PYTHONPATH=src pytest tests/test_trusted_local_adapter_synthetic_sandbox_run_verifier.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_synthetic_trusted_local_adapter_sandbox_run_verifier_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q`
- DocC static generation
- CLI smoke for the P42-T5 fixture
