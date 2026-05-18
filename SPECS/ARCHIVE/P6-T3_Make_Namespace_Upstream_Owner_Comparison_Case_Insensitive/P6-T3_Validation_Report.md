# P6-T3 Validation Report

## Validation Run

- `python -m pytest tests/test_namespace_upstream_reports.py`
- `ruff check src tests`
- `ruff format --check src tests`
- `pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`

## Result

- Status: PASS
- Notes: Case-only namespace-owner differences no longer generate false
  `upstream_namespace_mismatch` issues; mismatch reporting for missing data,
  conflicting artifacts, and malformed URIs remains unchanged.
