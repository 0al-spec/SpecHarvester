# P12-T1 Validation Report

Task: `P12-T1 Strict License Filename Compatibility`
Date: 2026-05-21
Verdict: PASS

## Scope

Implemented deterministic recognition for root license-like filenames with safe
text extensions so strict public batch validation accepts common variants such
as `LICENSE.txt` while preserving the hard `missing_license_file` error for
repositories without license evidence.

## Regression Coverage

- Added strict batch regression for a repository with `LICENSE.txt`.
- Preserved strict batch regression for a repository without any license-like
  file.
- Added collector helper coverage for accepted variants (`LICENSE.txt`,
  `COPYING.md`, `copying.rst`) and rejected variants (`LICENSE.png`,
  `THIRD_PARTY_LICENSES.txt`).
- Updated human docs and DocC mirror wording for strict public license evidence.

## Quality Gates

| Gate | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest` | PASS, `209 passed in 3.54s` |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, `41 files already formatted` |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `209 passed`, total coverage `90.60%` |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Local Popular Repository Smoke

Command:

```bash
PYTHONPATH=src python -m spec_harvester collect-batch .smoke/inputs \
  --out .smoke/output/p12-t1-popular-candidates \
  --report .smoke/output/p12-t1-popular-batch-validation.json \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/analyzer-cache \
  --select flask --select gin
```

Result: PASS, batch `status: ok`.

Summary:

- `collectedCount: 2`
- `errorCount: 0`
- `warningCount: 0`
- `highConfidenceCount: 2`

Repository checks:

- `flask` at revision `954f5684e4841aad84a8eec7ace7b81a0d3f6831` produced
  `licenseFileCount: 1`; harvested license path is `LICENSE.txt`.
- `gin` at revision `5f4f9643258dc2a65e684b63f12c8d543c936c67` produced
  `licenseFileCount: 1`; harvested license path is `LICENSE`.

## Notes

- No SPDX lookup, package-manager execution, repository network access, or
  package scripts were added.
- Go public interface analyzer execution remains out of scope for this task and
  is tracked separately by `P12-T2`.
