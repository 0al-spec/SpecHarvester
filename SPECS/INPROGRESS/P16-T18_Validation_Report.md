# P16-T18 Validation Report

Date: 2026-05-26
Branch: `feature/P16-T18-duplicate-code-practical-minimum-audit`
Verdict: PASS

## Summary

- Captured the duplicate-code practical-minimum baseline after P16-T17.
- Confirmed both duplicate-code backends report zero duplicate blocks.
- Documented that no additional duplicate-code refactor is warranted now.

## Duplicate-Code Metrics

- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t18-dup-builtin.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t18-dup-pylint.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`

## Quality Gates

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

- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t18-architecture-lint.json`
  - ATTENTION: one existing advisory `manifest_parser_pattern` in
    `src/spec_harvester/license_provenance_reports.py`

## Notes

- The architecture lint advisory is unrelated to duplicate-code refactoring.
- No generated `.smoke/` artifacts were created or committed.
