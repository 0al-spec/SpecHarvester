# P42-T8 Explicit Real Local Trusted Adapter Sandbox Run Request Fixture

## Summary

Add a deterministic
`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest` fixture that
records a future real local trusted adapter sandbox run review request while
still refusing to grant execution permission or registry authority.

## Motivation

P42-T7 makes real-run readiness explicit, but readiness evidence still is not a
request to run an adapter. Before any real local sandbox runner can exist, the
project needs a separate request artifact that binds the future review to:

- the P42-T6 synthetic sandbox verifier evidence;
- the P42-T7 readiness evidence;
- one adapter identity and digest;
- one target repository identity and revision;
- one sandbox policy identity and version;
- one declared output root and audit path;
- explicit operator approval requirements and non-authority statements.

The request fixture should be useful to future preflight/runtime tasks without
becoming an execution token, registry acceptance, or adapter output truth.

## Deliverables

- Add a machine-readable explicit real local sandbox run request fixture under
  `tests/fixtures/repository_plugins/`.
- Declare request identity:
  - `apiVersion:
    spec-harvester.explicit-real-local-trusted-adapter-sandbox-run-request/v0`;
  - `kind:
    SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest`;
  - `schemaVersion: 1`;
  - producer-side request-only authority.
- Reference P42-T6 verifier and P42-T7 readiness contracts as prerequisite
  evidence.
- Declare scoped operator approval requirements for a future real run:
  adapter id/digest, target repository id/revision, sandbox policy id/version,
  output root, audit record path, single-use scope, and non-reusable approval.
- Declare sandbox runtime, filesystem/output, audit, rollback, and review
  requirements.
- Preserve request-only execution boundary fields:
  no adapter code loaded, no process spawned, no dependency installation, no
  package manager invocation, no network access, no harvested-code execution,
  no AI execution, no registry authority, and no adapter output acceptance.
- Add tests that validate fixture identity, evidence references, approval
  scoping, execution boundary, and non-authority statements.
- Add GitHub docs, DocC docs, roadmap/capabilities links, Flow archive, review,
  and validation artifacts.

## Acceptance Criteria

- The fixture validates as deterministic JSON with stable identity, contract,
  evidence references, approval scope, runtime policy, output policy, audit
  policy, request boundary, validation summary, and non-authority statements.
- The fixture references both:
  - P42-T6 `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport`;
  - P42-T7 `SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport`.
- The fixture states that the request is ready for review only and is not:
  - execution permission;
  - operator approval for an actual run;
  - registry authority;
  - package or relation acceptance;
  - baseline seeding;
  - publication authority;
  - adapter output truth.
- Tests fail if the fixture drifts toward reusable approval, runtime
  permission, registry authority, missing evidence references, unsafe output
  path shape, or any real adapter execution.
- CLI/runtime behavior remains unchanged: no real adapter execution is
  implemented or enabled.
- Docs and DocC explain how P42-T8 fits after P42-T6/P42-T7 and before any
  future preflight/runtime task.

## Non-Goals

- Do not implement a real adapter runner.
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
- Do not treat the request fixture as execution permission.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_explicit_real_local_trusted_adapter_sandbox_run_request_fixture_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q`
- DocC static generation
