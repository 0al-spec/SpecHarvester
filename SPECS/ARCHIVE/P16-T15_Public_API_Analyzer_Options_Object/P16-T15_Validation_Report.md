# P16-T15 Validation Report

Task: `P16-T15 — Public API Analyzer Options Object`
Branch: `feature/P16-T15-public-api-analyzer-options`
Date: 2026-05-26
Verdict: PASS

## Summary

- Added `PublicApiAnalyzerOptions` as the shared request-context object for
  public API analyzers.
- Refactored Python, Go, and JS/TS analyzers to keep source-compatible public
  wrappers while routing root validation, package ID fallback, source revision,
  and cache construction through the shared object.
- Added direct regression coverage for legacy keyword calls, direct options
  calls, unexpected keyword rejection, mixed object/keyword rejection, cache
  construction, package fallback, and source-root validation.

## Duplicate-Code Metrics

- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t15-dup-builtin.json`
  - ATTENTION: `duplicateBlockCount=9`, `duplicateOccurrenceCount=18`
  - The analyzer option-shape cluster is removed.
  - Remaining advisory clusters are in upstream report issue generation and
    `real_repo_quality_report.py` rating guards.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t15-dup-pylint.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`

## Architecture-Lint Metrics

- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t15-architecture-lint.json`
  - ATTENTION: `issueCount=1`
  - Existing advisory: `manifest_parser_pattern` in
    `src/spec_harvester/license_provenance_reports.py`.
  - This issue is unrelated to the public API analyzer options object.

## Quality Gates

- `PYTHONPATH=src python -m pytest tests/test_public_api_analyzer_options.py tests/test_python_public_api.py tests/test_go_public_api.py tests/test_js_ts_public_api.py tests/test_analyzer_orchestration.py -q`
  - PASS: `40 passed`
- `PYTHONPATH=src python -m pytest`
  - PASS: `407 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `407 passed, 1 skipped`
  - Coverage: `91.57%`
- `ruff check src tests`
  - PASS
- `ruff format --check src tests`
  - PASS: `65 files already formatted`
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Follow-Up Candidates

- P16-T16 should address the remaining upstream report issue-generation
  duplicate clusters across namespace and license provenance reports.
- P16-T17 should address the remaining real repository quality rating guard
  duplicate clusters.
