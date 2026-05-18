# P6-T1 Validation Report

## Branch

- `feature/P6-T1-discover-nested-swift-package-manifests`

## Validation Commands

- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src python -m spec_harvester.cli collect-batch smoke-inputs --out smoke-output-p6t1/candidates --report smoke-output-p6t1/batch-validation.json`

## Result

- `ruff check` - PASS.
- `ruff format --check` - PASS.
- `pytest` - PASS (`116` tests).
- Coverage - PASS (`90.21%`, threshold `90%`).
- Smoke batch - PASS (`4` collected, `0` skipped).

## Smoke Result

- `cupertino`: `fileCount=4`, `packageManifestCount=1`, confidence `high`.
- Overall smoke summary: `highConfidenceCount=4`, `mediumConfidenceCount=0`,
  `lowConfidenceCount=0`, `warningCount=0`.
