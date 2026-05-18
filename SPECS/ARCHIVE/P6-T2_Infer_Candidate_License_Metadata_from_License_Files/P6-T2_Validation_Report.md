# P6-T2 Validation Report

## Validation Run

- `python -m pytest tests/test_collector.py`
- `ruff check src tests`
- `ruff format --check src tests`

## Result

- Status: PASS
- Notes: behavior is deterministic and bounded to allowlisted files already collected by
  the static harvest process.
