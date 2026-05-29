# P17-T1 Validation Report

Task: `P17-T1 — Procedural Style Metrics Report`
Date: 2026-05-29
Branch: `feature/P17-T1-procedural-style-metrics`
Verdict: PASS

## Summary

- Added `SpecHarvesterProceduralStyleReport` generation for local Python source.
- Added `procedural-style-report` CLI with optional output and
  `--fail-on-hotspots`.
- Added deterministic file metrics, hotspot detection, skipped-file reporting,
  and largest top-level function reporting.
- Added GitHub docs and DocC mirror for the new report.
- Added docs contract coverage so GitHub docs and DocC stay aligned.

## Behavioral Validation

- `PYTHONPATH=src python -m pytest tests/test_procedural_style_report.py tests/test_docs_contracts.py -q`
  - PASS: 34 passed.
- `PYTHONPATH=src python -m spec_harvester procedural-style-report --path src/spec_harvester --output /tmp/p17t1-procedural-style.json`
  - PASS: deterministic report emitted successfully.
  - Current baseline summary:
    - `topLevelFunctionCount=463`
    - `topLevelFunctionSpan=9918`
    - `methodCount=59`
    - `methodSpan=603`
    - `classCount=50`
    - `behaviorRichClassCount=13`
    - `dtoOnlyClassCount=28`
    - `exceptionLikeClassCount=5`
    - `hotspotCount=13`
  - Largest top-level function: `src/spec_harvester/cli.py:build_parser`
    with span `589`.
  - Largest hotspot modules include `specnode_refinement.py`, `drafter.py`,
    `cli.py`, `collector.py`, and `code_duplication_report.py`.

## Quality Gates

- `PYTHONPATH=src python -m pytest`
  - PASS: 435 passed, 1 skipped.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 435 passed, 1 skipped, total coverage 91.75%.
- `ruff check src tests`
  - PASS.
- `ruff format --check src tests`
  - PASS: 70 files already formatted.
- `swift package dump-package >/dev/null`
  - PASS.
- `swift build --target SpecHarvesterDocs`
  - PASS.
- `git diff --check`
  - PASS.

## Boundaries

- No production refactor was performed in this task; the report only measures
  procedural concentration.
- No repository code is imported or executed.
- No non-Python language is analyzed by this report.
- Hotspot policy remains advisory by default and is opt-in for failure mode.
