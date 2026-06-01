# P21-T2 Validation Report

**Task:** P21-T2 — Producer Receipt Emission
**Date:** 2026-06-02
**Branch:** `feature/P21-T2-producer-receipt-emission`
**Verdict:** PASS

## Scope Validated

- Added `producer-receipt.json` emission for drafted SpecPM candidate bundles.
- Added a dedicated producer receipt object that records subject metadata,
  producer identity, input references, configuration digest, generated output
  SHA-256 digests, validation placeholder, diagnostics placeholder, privacy
  state, audit evidence, and human review defaults.
- Integrated receipt writing into `draft_spec_package()` after generated
  candidate files are written.
- Preserved the self-hash boundary: `producer-receipt.json` is not listed in
  receipt `outputs[]`.
- Added tests for receipt shape, output digests, input digests,
  `public-interface-index.json` evidence, privacy defaults, and
  `humanReview` defaults.

## Quality Gates

| Gate | Command | Result |
|------|---------|--------|
| Targeted draft tests | `PYTHONPATH=src python -m pytest tests/test_collector.py -q -k 'draft_spec_package_writes_candidate_files or draft_spec_package_enriches_interfaces_from_public_interface_index'` | PASS — 2 passed, 78 deselected |
| Targeted collector/docs tests | `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_docs_contracts.py -q` | PASS — 108 passed |
| Full tests | `PYTHONPATH=src python -m pytest` | PASS — 476 passed, 1 skipped |
| Lint | `ruff check src tests` | PASS — All checks passed |
| Format | `ruff format --check src tests` | PASS — 80 files already formatted |
| Coverage | `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS — 476 passed, 1 skipped; total coverage 91.83% |
| Swift manifest | `swift package dump-package >/dev/null` | PASS |
| DocC build target | `swift build --target SpecHarvesterDocs` | PASS |

## Notes

- `validation.status` is emitted as `not_run` until P21-T3 adds
  `validation-report.json`.
- `diagnostics.status` is emitted as `clean` until P21-T3 adds
  `diagnostics.json`.
- `receiptId` is deterministic from subject, inputs, configuration, and outputs.
  `issuedAt` records the receipt write time and does not participate in
  `receiptId`.
