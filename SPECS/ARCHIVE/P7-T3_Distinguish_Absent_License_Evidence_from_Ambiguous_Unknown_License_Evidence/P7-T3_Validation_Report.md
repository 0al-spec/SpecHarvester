# P7-T3 Validation Report

## Validation Run

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_license_provenance_risk_reports.py -q` | PASS, 63 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 135 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 90.34% total coverage |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Smoke Verification

Using the ignored `.smoke/output/candidates` workspace from the documented local
smoke fixture flow:

| Report | Result |
|--------|--------|
| `governance-license-provenance-report --candidates-root .smoke/output/candidates` | PASS, `issuesByCode.absent_license_evidence=1`, no generic `unknown_license` issue for `puzzle.core` |

## Result

Status: PASS

## Notes

- Generated candidate manifests now include `metadata.licenseEvidence` with a
  deterministic source classification.
- License/provenance records surface the same classification for reviewers.
- `UNKNOWN` with `source: absent` is reported as `absent_license_evidence`.
- `UNKNOWN` with `source: ambiguous_license_file` is reported as
  `ambiguous_unknown_license`.
- Legacy manifests without `metadata.licenseEvidence` retain `unknown_license`.
