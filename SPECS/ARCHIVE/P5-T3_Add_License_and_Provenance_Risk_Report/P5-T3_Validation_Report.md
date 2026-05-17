# P5-T3 Validation Report

## Branch

- `feature/p5-t3-add-license-and-provenance-risk-report`

## Validation Commands

- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`

## Result

- `ruff check` — PASS.
- `ruff format --check` — PASS.
- `pytest` — PASS (`110` tests).

## Coverage

- Full project checks in CI: coverage remains above minimum threshold.

