# P39-T1 Static Repository Plugin Applicability Evaluator Plan

## Motivation

Phase 38 established repository plugin applicability as explicit
producer-side evidence. It added registry/applicability fixtures, autonomous
batch sidecar recording, cross-ecosystem examples, and a real FastMCP sidecar
run.

The remaining gap is that applicability reports are still hand-authored or
operator-supplied. SpecHarvester needs a deterministic plan for deriving
`SpecHarvesterRepositoryPluginApplicabilityReport` from already collected
static evidence.

## Goal

Document the static repository plugin applicability evaluator before
implementation.

The plan must explain how SpecHarvester can read declared plugin registry
metadata plus bounded static evidence and produce selected, rejected, fallback,
and blocked plugin decisions without loading or executing plugin code.

## Deliverables

- Add a GitHub-facing plan document for the static evaluator.
- Add a DocC mirror for the plan.
- Update capabilities, roadmap, repository plugin subsystem docs, and
  applicability fixture docs to reference the plan.
- Update `SPECS/Workplan.md` and `SPECS/INPROGRESS/next.md` with Phase 39
  task state.
- Add docs regression coverage for identity, planned inputs, evaluator
  decisions, precedence rules, follow-up tasks, and non-authority boundaries.
- Archive the task through Flow.

## Acceptance Criteria

- The plan explicitly states the evaluator is static and deterministic.
- The plan lists the allowed static inputs:
  - plugin registry fixture;
  - source manifest metadata;
  - `harvest.json`;
  - `workspace-inventory.json`;
  - `repository-profile-detection.json`;
  - public-interface indexes;
  - optional parser profile decisions;
  - operator labels.
- The plan defines decision outputs:
  - `selectedPlugins[]`;
  - `rejectedPlugins[]`;
  - `fallbackPlugins[]`;
  - `blockedPlugins[]`;
  - `diagnostics[]`.
- The plan defines precedence:
  - explicit operator sidecar first;
  - static evaluator second;
  - documented generic fallback last.
- The plan explains that missing required input evidence must not silently
  select a plugin.
- The plan is language- and framework-agnostic.
- The plan does not claim package acceptance, relation acceptance, registry
  publication, parser behavior changes, repository profile scoring changes, or
  `preview_only` removal.

## Non-Goals

- Do not implement the evaluator.
- Do not add a CLI.
- Do not change `autonomous-candidate-batch` behavior.
- Do not load third-party plugin code.
- Do not execute plugins.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat plugin decisions as registry truth.

## Dependencies

- P38-T2 `SpecHarvesterRepositoryPluginRegistry` fixture.
- P38-T3 `SpecHarvesterRepositoryPluginApplicabilityReport` fixture.
- P38-T4 autonomous batch sidecar recording.
- P38-T5 cross-ecosystem applicability examples.
- P38-T6 real FastMCP sidecar run.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'static_repository_plugin_applicability_evaluator or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
