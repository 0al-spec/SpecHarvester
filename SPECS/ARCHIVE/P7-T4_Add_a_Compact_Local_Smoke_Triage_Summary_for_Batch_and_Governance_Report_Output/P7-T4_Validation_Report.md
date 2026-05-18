# P7-T4 Validation Report

## Validation Run

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_smoke_triage.py tests/test_docs_contracts.py -q` | PASS, 5 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 137 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 90.31% total coverage |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Smoke Verification

Using the ignored `.smoke/output` workspace from the documented local smoke
fixture flow:

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m spec_harvester smoke-triage-summary --batch-validation .smoke/output/batch-validation.json --governance-claims .smoke/output/governance-claims.json --namespace-upstream .smoke/output/namespace-upstream.json --license-provenance .smoke/output/license-provenance.json --output .smoke/output/smoke-triage.json` | PASS, `status=attention_required`, `totalIssueCount=1`, `licenseIssueCount=1` |

## Result

Status: PASS

## Notes

- Added `smoke-triage-summary` as a read-only aggregation command over existing
  smoke report JSON files.
- Summary output keeps detailed report paths for drill-down review.
- Local smoke currently reports only the expected license/provenance signal:
  `absent_license_evidence` for `puzzle.core`.
