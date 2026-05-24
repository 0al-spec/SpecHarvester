# P16-T1 Validation Report

Task: `P16-T1`
Date: 2026-05-24
Branch: `feature/P16-T1-quality-report-public-interface-coverage`

## Implementation Summary

- Updated `quality-report` analyzer coverage derivation to inspect
  candidate-local `public-interface-index.json`.
- The public interface index is counted only after validating it as
  `SpecHarvesterPublicInterfaceIndex`.
- Valid public interface index artifacts add `publicInterfaceIndex` and any
  declared analyzer ids to `analyzersUsed`.
- Invalid, missing, or unreadable public interface index artifacts are ignored
  and do not create false analyzer coverage.
- Updated GitHub and DocC quality-report documentation plus docs contract
  coverage for the new behavior.

## Regression Coverage

- Candidate with `harvest.json` but no analyzer fields plus valid
  `public-interface-index.json` now receives analyzer coverage from the index.
- Candidate with harvest analyzer evidence plus valid public interface index
  reaches `strong` coverage.
- Invalid public interface index artifacts do not affect coverage.
- End-to-end `build_package_quality_record` coverage verifies the candidate
  artifact path is used.

## Safety

- `quality-report` remains read-only and local-only.
- No repository code, package scripts, dependency installers, builds, tests,
  package managers, registry calls, SpecNode providers, or model calls are run.
- No generated `.smoke/` artifacts were committed.

## Quality Gates

- `PYTHONPATH=src python -m pytest tests/test_real_repo_quality_report.py tests/test_docs_contracts.py -q`:
  92 passed
- `PYTHONPATH=src python -m pytest`: 353 passed, 1 skipped
- `ruff check src tests`: passed
- `ruff format --check src tests`: passed
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  353 passed, 1 skipped; total coverage 90.61%
- `swift package dump-package >/dev/null`: passed
- `swift build --target SpecHarvesterDocs`: passed
