# P21-T3 Validation Report

**Task:** P21-T3 — Validation and Diagnostics Report Emission
**Date:** 2026-06-02
**Branch:** `feature/P21-T3-validation-diagnostics-report-emission`
**Verdict:** PASS

## Scope Validated

- Added `validation-report.json` emission for drafted candidate bundles.
- Added `diagnostics.json` emission for drafted candidate bundles.
- Added receipt output roles and SHA-256 digests for both report files.
- Added receipt `validation.reportPath` and `validation.reportDigest`.
- Added receipt `diagnostics.path`, `diagnostics.digest`, and compact
  diagnostics entries.
- Preserved the self-hash boundary: `producer-receipt.json` remains excluded
  from `outputs[]`.
- Added tests for report shape, report digest wiring, privacy notes, review
  boundary notes, clean diagnostics, and external input diagnostics.

## Quality Gates

| Gate | Command | Result |
|------|---------|--------|
| Targeted draft tests | `PYTHONPATH=src python -m pytest tests/test_collector.py -q -k 'draft_spec_package_writes_candidate_files or draft_spec_package_marks_external_snapshot_input or draft_spec_package_enriches_interfaces_from_public_interface_index'` | PASS — 3 passed, 78 deselected |
| Targeted collector/docs tests | `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_docs_contracts.py -q` | PASS — 109 passed |
| Full tests | `PYTHONPATH=src python -m pytest` | PASS — 477 passed, 1 skipped |
| Lint | `ruff check src tests` | PASS — All checks passed |
| Format | `ruff format --check src tests` | PASS — 81 files already formatted |
| Coverage | `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS — 477 passed, 1 skipped; total coverage 91.89% |
| Swift manifest | `swift package dump-package >/dev/null` | PASS |
| DocC build target | `swift build --target SpecHarvesterDocs` | PASS |

## Notes

- `validation-report.json` is a producer-side shape check, not SpecPM
  acceptance authority.
- `diagnostics.json` records privacy and human-review notes even when
  `diagnostics.status` is `clean`; clean means no warning/error diagnostics.
- Full bundle preflight remains assigned to P21-T4.
