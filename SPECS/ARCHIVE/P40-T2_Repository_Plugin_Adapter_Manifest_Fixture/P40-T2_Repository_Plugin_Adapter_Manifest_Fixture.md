# P40-T2 Repository Plugin Adapter Manifest Fixture

## Motivation

P40-T1 documented the repository plugin adapter boundary, but the contract is
still prose-only. Future adapter preflight, execution policy, batch sidecars,
and cross-ecosystem validation need a stable machine-readable manifest example
that captures the fields an adapter must declare before it can participate in
the producer pipeline.

## Goal

Add the first `SpecHarvesterRepositoryPluginAdapterManifest` fixture and
document its shape.

The fixture must remain language- and framework-agnostic. It may use generic
adapter examples, but it must not make Python, JavaScript, FastAPI, FastMCP,
npm, Cargo, Go, SwiftPM, Maven, Gradle, or any other ecosystem normative.

## Deliverables

- Add `tests/fixtures/repository_plugins/adapter-manifest.example.json`.
- Add GitHub-facing fixture documentation.
- Add a DocC mirror for the fixture documentation.
- Link the fixture from the adapter contract, docs index, DocC root,
  capabilities, roadmap, and repository plugin subsystem docs.
- Add docs-contract regression coverage for fixture identity, fields, safe
  path policy, execution policy, declared outputs, capability requests,
  non-authority statements, and next-task state.
- Archive and review the task through Flow.

## Acceptance Criteria

- The fixture declares:
  - `apiVersion: spec-harvester.repository-plugin-adapter/v0`;
  - `kind: SpecHarvesterRepositoryPluginAdapterManifest`;
  - `schemaVersion: 1`;
  - `authority: producer_plugin_adapter_manifest_only`.
- The fixture records adapter ids, contract versions, adapter versions,
  supported roles, required and optional evidence kinds, declared outputs,
  execution mode, sandbox requirements, capability requests, diagnostics, and
  non-authority statements.
- The fixture references the existing static evidence envelope fixture as a
  declared input, not as runtime execution permission.
- The fixture has safe relative paths and SHA-256 digests where paths are
  declared.
- The fixture keeps `defaultEnabled: false`, `requiresOperatorOptIn: true`,
  `appliedToDrafting: false`, and `registryAuthority: false`.
- The fixture does not implement adapter preflight, adapter loading, adapter
  execution, autonomous batch integration, package acceptance, relation
  acceptance, registry publication, baseline seeding, `preview_only` removal,
  or AI execution.

## Non-Goals

- Do not implement adapter preflight.
- Do not implement adapter loading or execution.
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

## Test-First Plan

1. Add docs-contract assertions for the adapter manifest fixture and P40-T2
   `next.md` state.
2. Add the fixture with explicit identity, input evidence, output artifacts,
   execution, sandbox, capability, diagnostics, and follow-up metadata.
3. Add GitHub and DocC docs plus cross-links from existing plugin docs.
4. Run focused docs-contract tests, then full pytest, lint, format,
   diff-check, Swift docs build, and coverage.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'adapter_manifest or current_next_task'`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
