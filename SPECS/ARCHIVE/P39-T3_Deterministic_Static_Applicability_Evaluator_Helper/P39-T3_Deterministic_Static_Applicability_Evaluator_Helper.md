# P39-T3 Deterministic Static Applicability Evaluator Helper

## Motivation

P39-T1 documented the static repository plugin applicability evaluator plan.
P39-T2 added the machine-readable
`SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` fixture.

The next step is deterministic helper behavior that compares declared plugin
input evidence requirements with available static evidence and emits a
`SpecHarvesterRepositoryPluginApplicabilityReport` shape.

## Goal

Implement a deterministic helper that reads a
`SpecHarvesterRepositoryPluginRegistry` payload and a
`SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` payload, then emits
selected, rejected, fallback, and blocked plugin decisions with summary counts,
diagnostics, producer-side authorities, safe evidence paths, and non-authority
statements.

## Deliverables

- Add a helper module or domain object for static repository plugin
  applicability evaluation.
- Add regression tests covering:
  - the P39-T2 fixture success path;
  - required evidence matching;
  - missing required evidence producing blocked or fallback decisions;
  - summary counts;
  - diagnostic codes;
  - safe evidence path preservation;
  - producer-side authorities and non-authority statements.
- Update GitHub docs and DocC docs to mention the helper and clarify that CLI
  exposure remains P39-T4.
- Update Flow state, archive artifacts, and review artifacts.

## Acceptance Criteria

- The helper emits `apiVersion:
  spec-harvester.repository-plugin-applicability/v0`.
- The helper emits `kind:
  SpecHarvesterRepositoryPluginApplicabilityReport`.
- The helper emits `authority: producer_plugin_applicability_only`.
- For each plugin in the registry, the helper emits exactly one decision in
  `selectedPlugins[]`, `rejectedPlugins[]`, `fallbackPlugins[]`, or
  `blockedPlugins[]`.
- When all required evidence kinds are available, the plugin is selected.
- When required evidence is missing and the plugin fallback behavior is
  `fallback`, the plugin is placed in `fallbackPlugins[]`.
- When required evidence is missing and fallback behavior is `skip`, the plugin
  is placed in `blockedPlugins[]`.
- Diagnostics include stable codes such as `plugin_selected`,
  `plugin_fallback`, and `plugin_blocked_required_evidence_missing`.
- The helper does not execute plugins and does not read repository source
  files.

## Non-Goals

- Do not add `repository-plugin-applicability-detect`.
- Do not change `autonomous-candidate-batch`.
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

- P38-T2 `SpecHarvesterRepositoryPluginRegistry`.
- P38-T3 `SpecHarvesterRepositoryPluginApplicabilityReport`.
- P39-T1 static evaluator plan.
- P39-T2 static evidence envelope fixture.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_repository_plugin_applicability_evaluator.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'static_plugin_evidence_envelope or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
