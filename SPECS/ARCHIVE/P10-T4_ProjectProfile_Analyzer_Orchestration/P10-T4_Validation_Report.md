# P10-T4 Validation Report

Task: `P10-T4` ProjectProfile Analyzer Orchestration
Date: 2026-05-20
Verdict: PASS

## Scope

- Added analyzer orchestration driven by `ProjectProfile.analyzerPlan`.
- Added opt-in `collect-batch --emit-interface-indexes` support.
- Added optional `--analyzer-cache-dir` support for per-repository analyzer
  caches.
- Wired existing built-in static analyzers:
  - `spec_harvester.python_public_api`
  - `spec_harvester.js_ts_public_api`
- Wrote `public-interface-index.json` beside `harvest.json` only when requested
  and at least one supported analyzer plan runs.
- Recorded per-repository `interfaceIndex` status, executed analyzers, skipped
  analyzer plans, diagnostics, output path, and summary in batch JSON output.
- Updated GitHub docs and DocC mirror for the opt-in analyzer orchestration
  flow.

## Quality Gates

- PASS: `ruff check src tests`
- PASS: `ruff format --check src tests`
- PASS: `PYTHONPATH=src python -m pytest tests/test_analyzer_orchestration.py tests/test_batch_collection.py tests/test_docs_contracts.py -q`
  - Result: 32 passed
- PASS: `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - Result: 198 passed
  - Coverage: 90.71%
- PASS: `swift package dump-package >/dev/null`
- PASS: `swift build --target SpecHarvesterDocs`
- PASS: local smoke `collect-batch --emit-interface-indexes`
  - Result: Python and JavaScript/TypeScript analyzers both executed.
  - Result: `public-interface-index.json` summary status `complete`.

## Notes

- Default `collect-batch` behavior is unchanged and does not run analyzers.
- Analyzer orchestration does not execute harvested package code, package
  managers, package scripts, dependency installers, build systems, external
  classifiers, or network operations.
- Unsupported and `manifest_only` analyzer plans are recorded as skipped rather
  than treated as errors.
