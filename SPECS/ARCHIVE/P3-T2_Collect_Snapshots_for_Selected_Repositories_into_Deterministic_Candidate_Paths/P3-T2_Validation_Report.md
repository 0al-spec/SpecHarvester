# P3-T2 Validation Report

Task: Collect Snapshots for Selected Repositories into Deterministic Candidate Paths
Branch: `feature/P3-T2-collect-snapshots-for-selected-repositories-into-deterministic-candidate-paths`
Date: 2026-05-17
Verdict: PASS

## Implementation Summary

Implemented deterministic batch snapshot collection:

- Added `spec_harvester.batch_collection`.
- Added `BatchCollectOptions` and `collect_batch_snapshots`.
- Connected validated `inputs/*.yml` repository records to the existing
  `collect_local_repository` safe collector.
- Added local checkout resolution relative to the input manifest directory.
- Added deterministic candidate output paths under `out/<repository-id>/`.
- Rejected unknown selected IDs, duplicate selected IDs, missing checkout
  fields, missing checkout directories, and unsafe repository IDs for candidate
  directory names.
- Added `spec-harvester collect-batch <inputs> --out <candidates>` CLI command
  with repeated `--select` support.
- Added GitHub docs and DocC documentation for batch collection.
- Added focused batch API and CLI tests.

## Coverage Baseline

P3-T1 finished at 91.48% total coverage. P3-T2 finished at 91.81% total
coverage, so coverage improved.

## Validation Commands

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_batch_collection.py -q` | PASS, 8 passed |
| `PYTHONPATH=src python -m pytest tests/test_batch_collection.py tests/test_docs_contracts.py -q` | PASS, 10 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 86 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, 20 files already formatted |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 86 passed, total coverage 91.81% |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `git diff --check` | PASS |

## Trust Boundary Validation

- Batch collection only reads local operator-managed checkouts.
- No repository cloning was added.
- No network access was added.
- No package manager, dependency installation, build tool, package script, or
  repository code execution was added.
- Candidate output paths are derived from safe repository IDs, not checkout
  paths or repository content.
- Snapshot contents are produced through the existing allowlisted static
  collector.

## Residual Risks

- Batch collection requires operators to prepare and pin local checkouts before
  running the command.
- Repository IDs used for candidate directories are intentionally restricted to
  safe single path components.
- Public interface analysis and deterministic SpecPM drafting remain separate
  explicit steps.
