# P38-T2 Repository Plugin Registry Fixture

## Motivation

P38-T1 documented the repository plugin subsystem contract, but the next
tasks need a concrete machine-readable registry shape before applicability
reports or autonomous batch sidecar evidence can be tested.

The registry fixture should make plugin declarations reviewable without
implementing plugin execution.

## Goal

Add a language- and framework-agnostic
`SpecHarvesterRepositoryPluginRegistry` fixture that records plugin ids,
versioned contracts, roles, input requirements, output artifacts, safety
constraints, applicability signals, fallback behavior, diagnostics, and
non-authority boundaries.

## Deliverables

- Add a fixture under `tests/fixtures/repository_plugins/`.
- Add a small domain module or fixture validation helper only if needed to
  keep tests clear.
- Update GitHub docs and DocC docs to reference the registry fixture.
- Update capabilities, roadmap, workplan/next references as needed.
- Add docs-contract regression coverage for the fixture shape and boundary.
- Record validation and archive the task through Flow.

## Acceptance Criteria

- The fixture has:
  - `apiVersion: spec-harvester.repository-plugins/v0`;
  - `kind: SpecHarvesterRepositoryPluginRegistry`;
  - `schemaVersion: 1`;
  - `authority: producer_plugin_registry_only`;
  - `plugins[]` records with plugin id, version, role, title, summary, input
    evidence kinds, output artifact kinds, safety constraints, applicability
    signals, fallback behavior, diagnostics, and non-authority statements.
- The fixture includes generic examples for at least:
  - parser profile role;
  - repository profile role;
  - evidence producer role;
  - topology helper role.
- The fixture remains language- and framework-agnostic; ecosystem names can
  appear only as examples or evidence kinds, not normative rules.
- The fixture states that registry records do not execute plugins, accept
  packages, accept relations, publish registry metadata, remove `preview_only`,
  or treat plugin declarations as registry truth.

## Non-Goals

- Do not implement plugin loading or plugin execution.
- Do not add the P38-T3 applicability report fixture.
- Do not connect registry output to autonomous candidate batch.
- Do not change parser profile behavior.
- Do not change repository profile scoring.
- Do not add ecosystem-specific plugin implementations.
- Do not run real repositories.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`

