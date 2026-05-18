# P8-T2 Validation Report

## Validation Run

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_accepted_candidate_diff.py tests/test_docs_contracts.py -q` | PASS, 8 passed |
| `PYTHONPATH=src python -m pytest tests/test_accepted_candidate_diff.py -q` | PASS, 9 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 146 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 90.41% total coverage |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Result

Status: PASS

## Notes

- Added `accepted-candidate-diff-report` as a read-only local report over
  accepted and candidate `specpm.yaml` files.
- The report compares candidates with the latest accepted version for the same
  package ID by SemVer ordering.
- The first coverage run found a regression to 89.88%; additional targeted tests
  restored coverage to 90.41%.
