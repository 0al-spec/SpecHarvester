# P6-T4 Validation Report

## Validation Run

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q` | PASS, 3 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 121 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 90.34% total coverage |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Result

Status: PASS

## Notes

- Added reproducible local smoke fixture documentation for Cupertino, xyflow,
  docc2context, and Puzzle.
- Added DocC mirror documentation so GitHub Pages docs can expose the same local
  smoke fixture workflow.
- Added ignore rules for `.smoke/`, `smoke-inputs/`, and `smoke-output*/`.
- Added a documentation contract test for fixture paths, report commands,
  repository names, and trust-boundary controls.
