# P10-T1 Validation Report

Status: Passed
Updated: 2026-05-19
Task: `P10-T1` ProjectProfile Schema

## Scope

Implemented initial `projectProfile` evidence in harvest snapshots:

- Versioned schema marker.
- Ranked language and ecosystem evidence.
- Manifest evidence with parser, digest, package manager, confidence, and path.
- Advisory analyzer plan entries.
- Diagnostics for unsupported or missing package manifest evidence.

## Validation

- `ruff check src tests`
  - Result: Passed.
- `ruff format --check src tests`
  - Result: Passed.
- `PYTHONPATH=src python -m pytest tests/test_collector.py -q`
  - Result: Passed, 61 tests.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - Result: Passed, 180 tests.
  - Coverage: 90.66%.
- `swift package dump-package >/dev/null`
  - Result: Passed.
- `swift build --target SpecHarvesterDocs`
  - Result: Passed.

## Notes

- Initial formatting and lint checks reported line wrapping issues in
  `collector.py`; formatting and manual wrapping resolved them before final
  validation.
- No package scripts, dependency installers, build systems from harvested
  repositories, or network probes were executed.
