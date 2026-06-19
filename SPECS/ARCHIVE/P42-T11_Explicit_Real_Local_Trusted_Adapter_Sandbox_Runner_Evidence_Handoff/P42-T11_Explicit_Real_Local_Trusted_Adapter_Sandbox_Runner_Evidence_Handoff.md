# P42-T11 Explicit Real Local Trusted Adapter Sandbox Runner Evidence Handoff

## Summary

Add a deterministic runner evidence handoff fixture for the explicit real local
trusted adapter sandbox path. The handoff packages the P42-T8 request, P42-T9
preflight, and P42-T10 disabled runner skeleton as portable review evidence
without loading adapter code, spawning adapter processes, or granting execution
or registry authority.

## Motivation

P42-T8 records a future real-run request, P42-T9 validates that request as
review-only preflight evidence, and P42-T10 proves the disabled runner skeleton
can validate request/preflight linkage. The next boundary is a handoff artifact:

```text
P42-T8 request
  + P42-T9 request preflight
  + P42-T10 disabled runner skeleton
  -> evidence handoff
  -> future reviewed runtime only after explicit approval
```

This keeps the linked artifacts portable for maintainer review while making it
machine-readable that the artifact set is not execution permission, not operator
approval, not registry authority, and not adapter output truth.

## Deliverables

- Add a machine-readable runner evidence handoff fixture under
  `tests/fixtures/repository_plugins/`.
- Reference the P42-T8 request fixture with a pinned SHA-256 digest.
- Reference the P42-T9 request preflight fixture with a pinned SHA-256 digest.
- Reference the P42-T10 disabled runner skeleton fixture with a pinned SHA-256
  digest.
- Validate artifact identity and digest agreement across the handoff set.
- Preserve:
  - no adapter code loading;
  - no adapter imports;
  - no adapter process spawning;
  - no dependency installation;
  - no package-manager invocation;
  - no network access;
  - no harvested-code execution;
  - no AI execution;
  - no package acceptance;
  - no relation acceptance;
  - no baseline seeding;
  - no registry metadata publishing;
  - no `preview_only` removal;
  - no adapter output acceptance.
- Declare accepted, rejected, blocked, warning, diagnostic, and non-authority
  statements for the handoff boundary.
- Add GitHub docs, DocC docs, roadmap/capabilities links, Flow archive, review,
  and validation artifacts.

## Acceptance Criteria

- The handoff fixture uses:
  - `apiVersion:
    spec-harvester.explicit-real-local-trusted-adapter-sandbox-runner-evidence-handoff/v0`;
  - `kind:
    SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunnerEvidenceHandoff`;
  - `schemaVersion: 1`;
  - producer-side runner-evidence-handoff-only authority.
- The fixture references P42-T8, P42-T9, and P42-T10 artifacts with pinned
  SHA-256 digests and verified safe relative paths.
- The fixture validates request/preflight/disabled-runner linkage and digest
  agreement.
- The handoff result status is review-only and does not grant execution
  permission, operator approval, registry authority, or adapter output truth.
- Tests fail if the handoff drifts toward adapter code loading, process
  spawning, dependency installation, package-manager invocation, network use,
  harvested-code execution, AI execution, package/relation acceptance, registry
  authority, adapter output truth, or reusable permission.
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
- Do not treat request/preflight/disabled-runner artifacts as execution
  permission.
- Do not treat the handoff as operator approval.
- Do not treat the handoff as registry authority.
- Do not treat adapter output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_explicit_real_local_sandbox_runner_evidence_handoff_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `python3 -m json.tool tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-runner-evidence-handoff.example.json >/dev/null`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- DocC static generation
