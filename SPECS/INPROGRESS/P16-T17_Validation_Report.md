# P16-T17 Validation Report

Date: 2026-05-26
Branch: `feature/P16-T17-real-repo-quality-rating-policy`
Verdict: PASS

## Summary

- Added behavior-rich real repository rating policy objects for draft preflight,
  intent rating, and capability evidence rating.
- Preserved existing quality report JSON behavior and private rating helper
  entrypoints.
- Reduced both builtin and `pylint` duplicate-code reports to zero duplicate
  blocks for `src/spec_harvester`.

## Duplicate-Code Metrics

- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t17-dup-builtin.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t17-dup-pylint.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`

## Quality Gates

- `PYTHONPATH=src python -m pytest tests/test_real_repo_quality_report.py -q`
  - PASS: 77 passed
- `PYTHONPATH=src python -m pytest`
  - PASS: 415 passed, 1 skipped
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 415 passed, 1 skipped, total coverage 91.85%
- `ruff check src tests`
  - PASS
- `ruff format --check src tests`
  - PASS: 68 files already formatted
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Advisory Checks

- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t17-architecture-lint.json`
  - ATTENTION: one existing advisory `manifest_parser_pattern` in
    `src/spec_harvester/license_provenance_reports.py`

## Notes

- The remaining architecture lint advisory is unrelated to the rating-policy
  refactor and predates this task.
- P16-T18 remains the planned practical-minimum duplicate-code audit after this
  refactor lands.
