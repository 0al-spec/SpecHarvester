# P40-T3 Repository Plugin Adapter Preflight Report Fixture

## Status

Planned for execution on
`feature/P40-T3-repository-plugin-adapter-preflight-report-fixture`.

## Context

P40-T2 added the first
`SpecHarvesterRepositoryPluginAdapterManifest` fixture. That fixture declares
future adapter identities, roles, required evidence, declared outputs,
sandbox expectations, capability requests, and non-authority boundaries, but it
does not prove that a manifest has been checked against available static
evidence.

P40-T3 adds the first machine-readable preflight report fixture for that
boundary. The report is producer-side review evidence only. It must show how
an adapter manifest can be evaluated before any adapter code is loaded or run.

## Motivation

Future repository plugin adapters can improve evidence quality for popular
libraries, but the adapter layer must stay safe and explainable. Operators need
a report shape that answers:

- which adapter declarations are safe to consider;
- which are rejected because they violate manifest or authority rules;
- which can only fall back to lower-fidelity static output;
- which are blocked until required evidence or policy exists.

This lets SpecHarvester grow plugin precision without turning plugin metadata
into execution permission or registry truth.

## Deliverables

- Add `tests/fixtures/repository_plugins/adapter-preflight-report.example.json`
  with kind `SpecHarvesterRepositoryPluginAdapterPreflightReport`.
- Link the report to the P40-T2 adapter manifest and the Phase 39 static
  evidence envelope by safe relative paths and SHA-256 digests.
- Record `allowedAdapters[]`, `rejectedAdapters[]`, `fallbackAdapters[]`, and
  `blockedAdapters[]` decision examples.
- Record explicit boundary fields proving adapter code was not loaded or run.
- Add GitHub docs and DocC mirror pages for the fixture.
- Update capability, roadmap, subsystem, adapter-contract, and manifest-fixture
  docs so the new fixture is discoverable.
- Add regression tests for fixture shape, digest references, decision
  categories, execution boundary, and documentation links.
- Archive the task and move `next.md` to P40-T4.

## Acceptance Criteria

- The fixture has stable identity:
  - `apiVersion: spec-harvester.repository-plugin-adapter-preflight/v0`
  - `kind: SpecHarvesterRepositoryPluginAdapterPreflightReport`
  - `schemaVersion: 1`
  - `authority: producer_plugin_adapter_preflight_only`
- The fixture references the P40-T2 adapter manifest digest and the static
  evidence envelope digest.
- Safe P40-T2 adapter declarations can appear under `allowedAdapters[]`.
- Unsafe, undeclared, missing-evidence, and lower-fidelity cases are visible as
  `rejectedAdapters[]`, `blockedAdapters[]`, or `fallbackAdapters[]`.
- `summary.executedAdapterCount` is `0`.
- The report states that no adapter code was loaded, no third-party code was
  executed, no network was used, no dependencies were installed, and no
  registry authority was granted.
- Docs and tests describe the fixture as review-only producer evidence, not
  package acceptance, relation acceptance, baseline authority, registry
  publication, or permission to remove `preview_only`.

## Non-Goals

- Do not implement adapter loading or adapter execution.
- Do not change static plugin applicability evaluation.
- Do not change `autonomous-candidate-batch`.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output as registry truth.

## Validation Plan

- `python3 -m json.tool tests/fixtures/repository_plugins/adapter-preflight-report.example.json`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`

