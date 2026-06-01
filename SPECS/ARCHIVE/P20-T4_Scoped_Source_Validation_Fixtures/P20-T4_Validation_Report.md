# P20-T4 Validation Report

**Date:** 2026-06-01
**Task:** P20-T4 — Scoped Source Validation Fixtures
**Verdict:** PASS

## Implemented Coverage

- Added a synthetic scoped-source monorepo matrix covering:
  - Tuist-managed Swift folder target.
  - Python folder target.
  - Python single-file target.
- Verified scoped targets inherit root license evidence.
- Verified collected files stay inside the selected target and do not include
  sibling modules or sibling files.
- Verified `public-interface-index.json` output stays scoped to selected
  folder/file targets.
- Added single-file Python public API analyzer support so file targets can emit
  deterministic interface evidence without scanning sibling files.

## Quality Gates

- `PYTHONPATH=src python -m pytest tests/test_batch_collection.py tests/test_python_public_api.py -q`
  - PASS: `35 passed`
- `ruff check src tests && ruff format --check src tests`
  - PASS: `All checks passed!`, `79 files already formatted`
- `PYTHONPATH=src python -m pytest`
  - PASS: `474 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `474 passed, 1 skipped`; total coverage `91.77%`
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Trust Boundary

The fixture matrix uses only synthetic local files and deterministic static
analyzers. No repository code, package scripts, Tuist, build tools, network
calls, or third-party graph tools are executed.
