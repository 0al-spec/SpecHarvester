# P38-T3 Repository Plugin Applicability Report Fixture

## Motivation

P38-T2 declared available repository plugin contracts, but the subsystem still
needs a machine-readable decision artifact that explains which plugins apply
to a repository shape and why. Without that report shape, autonomous candidate
batch cannot later consume plugin selection as reviewable sidecar evidence.

## Goal

Add a `SpecHarvesterRepositoryPluginApplicabilityReport` fixture that evaluates
generic plugin declarations from the P38-T2 registry fixture against static
repository evidence and records selected, rejected, fallback, and blocked
decisions without running plugin code.

## Deliverables

- Add a fixture under `tests/fixtures/repository_plugins/`.
- Add GitHub docs and DocC docs for the applicability report fixture.
- Link the report fixture from the registry fixture docs, subsystem contract,
  docs index, DocC root, capabilities, and roadmap.
- Add docs-contract regression coverage for report shape, decision records,
  diagnostics, safety boundaries, and P38 next-task states.
- Record validation and archive the task through Flow.

## Acceptance Criteria

- The fixture has:
  - `apiVersion: spec-harvester.repository-plugin-applicability/v0`;
  - `kind: SpecHarvesterRepositoryPluginApplicabilityReport`;
  - `schemaVersion: 1`;
  - `authority: producer_plugin_applicability_only`;
  - a reference to the P38-T2 `SpecHarvesterRepositoryPluginRegistry` fixture;
  - static evidence summary;
  - selected, rejected, fallback, and blocked plugin decision records;
  - diagnostics and reason codes;
  - non-authority statements.
- Decisions are deterministic and based only on static evidence.
- The fixture includes at least one selected, one rejected, one fallback, and
  one blocked decision.
- The fixture keeps ecosystem names as examples, not normative rules.
- The fixture states that applicability reports do not execute plugins, load
  third-party code, change parser behavior, change repository profile scoring,
  accept packages, accept relations, publish registry metadata, remove
  `preview_only`, or treat plugin decisions as registry truth.

## Non-Goals

- Do not implement plugin execution.
- Do not implement runtime applicability evaluation.
- Do not connect applicability reports to autonomous candidate batch.
- Do not change parser profile behavior.
- Do not change repository profile scoring.
- Do not add ecosystem-specific plugins.
- Do not run real repositories.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`

