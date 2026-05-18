# P8-T3 Validation Report

## Validation Run

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_accepted_candidate_impact.py tests/test_docs_contracts.py -q` | PASS, 9 passed |
| `PYTHONPATH=src python -m pytest tests/test_accepted_candidate_impact.py -q` | PASS, 5 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 152 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 90.69% total coverage |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Result

Status: PASS

## Notes

- Added deterministic impact classification over accepted-vs-candidate diff output.
- Added new report subcommand `accepted-candidate-impact-classification-report` with `--output`.
- Added/updated docs across GitHub Docs and DocC, plus mirrored DocC contracts test.
- Classification remains advisory and does not mutate or execute candidate/accepted package content.
