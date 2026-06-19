# P39-T3 Validation Report

## Summary

Status: PASS.

P39-T3 adds a deterministic static repository plugin applicability helper. The
helper derives `SpecHarvesterRepositoryPluginApplicabilityReport` from a
`SpecHarvesterRepositoryPluginRegistry` payload and a
`SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` payload without loading
plugins, executing plugins, reading repository source files, invoking package
managers, running AI, or changing autonomous batch behavior.

## Validation

- `PYTHONPATH=src pytest tests/test_repository_plugin_applicability_evaluator.py -q`
  - `4 passed`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'static_plugin_evidence_envelope or static_repository_plugin_applicability_evaluator_plan or current_next_task'`
  - `2 passed, 112 deselected`
- `PYTHONPATH=src pytest -q`
  - `772 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - `772 passed, 1 skipped`
  - coverage `91.08%`
- `PYTHONPATH=src ruff check .`
  - passed
- `PYTHONPATH=src ruff format --check src tests`
  - passed
- `git diff --check`
  - passed
- `swift build --target SpecHarvesterDocs`
  - passed

## Acceptance Notes

- Report identity is `apiVersion:
  spec-harvester.repository-plugin-applicability/v0`, `kind:
  SpecHarvesterRepositoryPluginApplicabilityReport`, `schemaVersion: 1`, and
  `authority: producer_plugin_applicability_only`.
- Every registry plugin receives exactly one decision across
  `selectedPlugins[]`, `rejectedPlugins[]`, `fallbackPlugins[]`, or
  `blockedPlugins[]`.
- Complete declared input evidence selects a plugin.
- Missing input evidence with `fallbackBehavior.decision: fallback` emits a
  fallback decision.
- Missing input evidence with `fallbackBehavior.decision: skip` emits a
  blocked decision.
- Unsafe evidence paths and invalid SHA-256 digests are rejected before report
  construction.
- CLI exposure remains deferred to P39-T4.
