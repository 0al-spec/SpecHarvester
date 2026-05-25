# P16-T2 Validation Report

Task: `P16-T2`
Date: 2026-05-25
Branch: `feature/P16-T2-license-provenance-classification`

## Implementation Summary

- Added governance classification for `UNKNOWN` licenses with collected standard
  license-file evidence.
- `source: ambiguous_license_file` plus standard paths such as `LICENSE`,
  `LICENSE.txt`, `LICENSE.md`, `COPYING`, or `COPYING.rst` now reports
  `collected_unknown_license_evidence` with low severity.
- Truly ambiguous paths such as `LICENSE.custom` still report
  `ambiguous_unknown_license`.
- `source: absent` still reports `absent_license_evidence`.
- Updated GitHub and DocC license provenance documentation plus docs contract
  coverage.

## Regression Coverage

- Unknown license with absent evidence remains `absent_license_evidence`.
- Unknown license with non-standard license-like path remains
  `ambiguous_unknown_license`.
- Unknown license with `LICENSE.txt` becomes
  `collected_unknown_license_evidence`.
- Standard collected license filename variants are covered:
  `LICENSE`, `LICENSE.txt`, `LICENSE.md`, `COPYING`, and `COPYING.rst`.

## Safety

- Strict missing-license behavior remains part of batch validation and is not
  changed by this governance report task.
- No repository code, package scripts, dependency installers, builds, tests,
  package managers, registry calls, SpecNode providers, or model calls are run.
- No generated `.smoke/` artifacts were committed.

## Quality Gates

- `PYTHONPATH=src python -m pytest tests/test_license_provenance_risk_reports.py tests/test_docs_contracts.py -q`:
  31 passed
- `PYTHONPATH=src python -m pytest`: 356 passed, 1 skipped
- `ruff check src tests`: passed
- `ruff format --check src tests`: passed
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  356 passed, 1 skipped; total coverage 90.65%
- `swift package dump-package >/dev/null`: passed
- `swift build --target SpecHarvesterDocs`: passed
