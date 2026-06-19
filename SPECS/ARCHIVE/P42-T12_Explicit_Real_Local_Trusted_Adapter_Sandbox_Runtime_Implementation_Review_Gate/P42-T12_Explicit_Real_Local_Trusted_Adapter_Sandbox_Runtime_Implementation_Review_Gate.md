# P42-T12 Explicit Real Local Trusted Adapter Sandbox Runtime Implementation Review Gate

## Summary

Add a deterministic runtime implementation review gate fixture for the explicit
real local trusted adapter sandbox path. The gate consumes the P42-T11 evidence
handoff, records the prerequisites that a future runtime implementation must
satisfy, and keeps real adapter execution blocked until a separate
operator-approved runtime task exists.

## Motivation

P42-T11 packages request, preflight, and disabled-runner evidence into a
portable review artifact. That still must not become implicit permission to
load adapter code or spawn a process. The next boundary is a review gate:

```text
P42-T11 evidence handoff
  -> runtime implementation review gate
  -> future operator approval binding
  -> future runtime implementation only after review
```

This gives maintainers a machine-readable checklist for runtime implementation
readiness before any code path can execute adapters.

## Deliverables

- Add a machine-readable runtime implementation review gate fixture under
  `tests/fixtures/repository_plugins/`.
- Reference the P42-T11 evidence handoff fixture with a pinned SHA-256 digest.
- Validate that the handoff remains review-only and cannot be treated as:
  - execution permission;
  - operator approval;
  - registry authority;
  - adapter output truth.
- Record runtime implementation prerequisites:
  - explicit operator approval;
  - adapter package identity;
  - process isolation;
  - safe input allowlists;
  - sealed environment;
  - dependency isolation;
  - network-deny-by-default policy;
  - output digests;
  - audit records;
  - rollback policy;
  - review-only authority.
- Declare accepted, rejected, blocked, warning, diagnostic, and non-authority
  statements for the review-gate boundary.
- Add GitHub docs, DocC docs, roadmap/capabilities links, Flow archive, review,
  and validation artifacts.

## Acceptance Criteria

- The review gate fixture uses:
  - `apiVersion:
    spec-harvester.explicit-real-local-trusted-adapter-sandbox-runtime-implementation-review-gate/v0`;
  - `kind:
    SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewGate`;
  - `schemaVersion: 1`;
  - producer-side runtime-implementation-review-gate-only authority.
- The fixture references P42-T11 with a pinned SHA-256 digest and verified safe
  relative path.
- The fixture records every required runtime implementation prerequisite.
- The fixture blocks adapter code loading, adapter imports, adapter process
  spawning, real runtime invocation, dependency installation, package-manager
  invocation, network access, harvested-code execution, AI execution, package
  acceptance, relation acceptance, baseline seeding, registry publishing,
  `preview_only` removal, and adapter output truth.
- Tests fail if the review gate grants execution permission, consumes operator
  approval, grants registry authority, or treats P42-T11 as adapter output
  truth.
- CLI/runtime behavior remains unchanged: no real adapter execution is
  implemented or enabled.

## Non-Goals

- Do not implement real adapter execution.
- Do not load third-party adapter code.
- Do not import adapter code.
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
- Do not treat P42-T11 as execution permission.
- Do not treat the review gate as operator approval.
- Do not treat adapter output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_explicit_real_local_sandbox_runtime_implementation_review_gate_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `python3 -m json.tool tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-runtime-implementation-review-gate.example.json >/dev/null`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- DocC static generation
