# P42-T9 Explicit Real Local Trusted Adapter Sandbox Run Request Preflight Fixture

## Summary

Add a deterministic
`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequestPreflightReport`
fixture that validates the P42-T8 request fixture contract without granting
real adapter execution permission.

## Motivation

P42-T8 records a future real local trusted adapter sandbox run request. A
future runtime still needs a preflight artifact that proves the request shape is
safe before any runner can consume it. The preflight fixture should validate
request identity, prerequisite verifier/readiness evidence requirements,
operator approval scoping, runtime policy, filesystem/output/audit policy,
rollback/review requirements, and non-authority statements.

It must also reject or block request drift toward reusable approval, runtime
permission, registry authority, unsafe paths, missing evidence requirements,
network/package-manager use, harvested-code execution, AI execution, or adapter
process execution.

## Deliverables

- Add a machine-readable request preflight fixture under
  `tests/fixtures/repository_plugins/`.
- Reference the P42-T8
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest` fixture with
  a pinned SHA-256 digest.
- Validate:
  - request API version, kind, schema version, and authority;
  - P42-T6 verifier evidence requirements;
  - P42-T7 readiness evidence requirements;
  - scoped operator approval requirements;
  - adapter package identity and immutable digest requirements;
  - target repository identity and revision;
  - sandbox policy identity and version;
  - runtime policy;
  - filesystem/output safe relative path policy;
  - audit, rollback, and review requirements;
  - no-execution request boundary and non-authority statements.
- Declare rejected and blocked unsafe request shapes.
- Add GitHub docs, DocC docs, roadmap/capabilities links, Flow archive, review,
  and validation artifacts.

## Acceptance Criteria

- The preflight fixture uses:
  - `apiVersion:
    spec-harvester.explicit-real-local-trusted-adapter-sandbox-run-request-preflight/v0`;
  - `kind:
    SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequestPreflightReport`;
  - `schemaVersion: 1`;
  - producer-side preflight-only authority.
- The preflight fixture references the P42-T8 request fixture and verifies its
  digest.
- The result status is review-only and does not grant execution permission.
- The fixture includes accepted checks for request identity, evidence
  requirements, approval scope, runtime/output/audit policy, execution boundary,
  and non-authority statements.
- The fixture includes rejected/blocked examples for unsafe paths, missing
  evidence requirements, reusable approval, execution permission, adapter code
  loading, process spawning, network/package-manager use, harvested-code
  execution, AI execution, registry authority, and adapter output acceptance.
- Tests fail if the preflight fixture drifts toward execution permission,
  registry authority, package/relation acceptance, unsafe path shapes, or
  missing P42-T6/P42-T7 evidence requirements.
- CLI/runtime behavior remains unchanged: no real adapter execution is
  implemented or enabled.

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
- Do not treat preflight pass as execution permission.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_explicit_real_local_trusted_adapter_sandbox_run_request_preflight_fixture_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `python -m json.tool tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request-preflight.example.json >/dev/null`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q`
- DocC static generation
