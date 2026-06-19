# P42-T13 Explicit Real Local Trusted Adapter Sandbox Operator Approval Binding Fixture

## Summary

Add a deterministic operator approval binding fixture for the explicit real
local trusted adapter sandbox path. The binding consumes the P42-T12 runtime
implementation review gate, records a bounded approval scope for a future run,
and still refuses adapter execution.

## Motivation

P42-T12 records runtime implementation prerequisites but intentionally does not
provide operator approval. Before any future runtime implementation task can
execute adapters, the approval scope needs a separate reviewable artifact:

```text
P42-T12 runtime implementation review gate
  -> operator approval binding fixture
  -> future runtime implementation only after review
```

This prevents prerequisite validation from becoming implicit approval and makes
the future approval scope auditable.

## Deliverables

- Add a machine-readable operator approval binding fixture under
  `tests/fixtures/repository_plugins/`.
- Reference the P42-T12 runtime implementation review gate with a pinned
  SHA-256 digest.
- Bind approval scope to:
  - adapter package identity;
  - target repository revision;
  - input artifact digests;
  - output directory;
  - runtime budgets;
  - network policy;
  - dependency policy;
  - audit requirements.
- Record that approval is bounded, non-reusable, review-only, and not consumed
  by a runtime.
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
- Add GitHub docs, DocC docs, roadmap/capabilities links, Flow archive, review,
  and validation artifacts.

## Acceptance Criteria

- The approval binding fixture uses:
  - `apiVersion:
    spec-harvester.explicit-real-local-trusted-adapter-sandbox-operator-approval-binding/v0`;
  - `kind:
    SpecHarvesterExplicitRealLocalTrustedAdapterSandboxOperatorApprovalBinding`;
  - `schemaVersion: 1`;
  - producer-side operator-approval-binding-only authority.
- The fixture references P42-T12 with a pinned SHA-256 digest and verified safe
  relative path.
- The fixture binds approval to adapter identity, repository revision, inputs,
  outputs, budgets, network policy, dependency policy, and audit requirements.
- The fixture marks approval as bounded and non-reusable.
- The fixture blocks adapter code loading, adapter imports, adapter process
  spawning, real runtime invocation, dependency installation,
  package-manager invocation, network access, harvested-code execution, AI
  execution, package acceptance, relation acceptance, baseline seeding,
  registry publishing, `preview_only` removal, and adapter output truth.
- Tests fail if the binding grants execution permission, grants registry
  authority, consumes approval by a runtime, or treats adapter output as truth.
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
- Do not treat P42-T12 as execution permission.
- Do not treat the approval binding as registry authority.
- Do not treat adapter output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_explicit_real_local_sandbox_operator_approval_binding_is_documented -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `python3 -m json.tool tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-operator-approval-binding.example.json >/dev/null`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- DocC static generation

---
**Archived:** 2026-06-19
**Verdict:** PASS
