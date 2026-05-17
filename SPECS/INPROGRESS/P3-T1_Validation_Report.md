# P3-T1 Validation Report

Task: Read Repository Source Manifests from inputs/*.yml
Branch: `feature/P3-T1-read-repository-source-manifests-from-inputs-yml`
Date: 2026-05-17
Verdict: PASS

## Implementation Summary

Implemented the first batch source input surface:

- Added `spec_harvester.source_manifest`.
- Added dependency-free parsing for the supported `inputs/*.yml` subset.
- Added validation for repository ids, repository URL schemes, `revision`/`ref`
  exclusivity, disabled entries, labels, and duplicate ids across manifests.
- Added deterministic normalization of repository source records with source
  manifest path and entry index.
- Added `spec-harvester source-manifests <inputs>` CLI JSON preview command.
- Added GitHub docs and DocC documentation for repository source manifests.
- Added focused parser and CLI tests.

## Coverage Baseline

P2-T4 finished at 90.62% total coverage. P3-T1 finished at 91.40% total
coverage, so coverage improved.

## Validation Commands

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_source_manifest.py -q` | PASS, 9 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 76 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, 18 files already formatted |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 76 passed, total coverage 91.40% |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `git diff --check` | PASS |

## Trust Boundary Validation

- Manifest reading only parses local operator-provided files.
- No repository cloning was added.
- No network access was added.
- No package manager, dependency installation, or package script execution was
  added.
- No batch collection was added; P3-T2 remains responsible for snapshot
  collection.

## Residual Risks

- The YAML subset is intentionally narrow and supports only `inputs/*.yml`.
- The CLI currently previews normalized records; it does not perform collection.
- Future P3 tasks must define deterministic candidate output paths and checkout
  handling before batch collection is enabled.
