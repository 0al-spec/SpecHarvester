# P7-T1 Validation Report

## Validation Run

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_namespace_upstream_reports.py tests/test_license_provenance_risk_reports.py -q` | PASS, 14 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 125 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 90.33% total coverage |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Smoke Verification

Using the ignored `.smoke/output/candidates` workspace from the documented local
smoke fixture flow:

| Report | Result |
|--------|--------|
| `governance-upstream-report --candidates-root .smoke/output/candidates` | PASS, `issueCount=0`, `upstreamMismatchCount=0` |
| `governance-license-provenance-report --candidates-root .smoke/output/candidates` | PASS, no `upstream_namespace_mismatch`; remaining issue is expected `unknown_license` for `puzzle.core` |

## Result

Status: PASS

## Notes

- GitHub upstream references now expose both owner and repository name.
- Namespace checks accept package namespace matches against either owner or
  repository name case-insensitively.
- Existing malformed, missing, duplicate, and non-GitHub upstream behaviors are
  preserved.
