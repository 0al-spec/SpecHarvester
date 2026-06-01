# P21-T5 Validation Report

**Task:** P21-T5 — Static Viewer Producer Receipt Panels
**Date:** 2026-06-02
**Branch:** `feature/P21-T5-static-viewer-producer-receipt-panels`
**Stack Base:** `feature/P21-T4-candidate-bundle-preflight-verifier`
**Verdict:** PASS

## Scope Validated

- Added read-only static renderer payload support for `producer-receipt.json`,
  `validation-report.json`, and `diagnostics.json`.
- Added producer evidence panels for receipt metadata, producer identity,
  subject, input provenance, output digests, validation status, diagnostics
  status, privacy/security caveats, and human review status.
- Preserved trust-boundary copy: generated evidence is review material only, not
  SpecPM acceptance or public index publication authority.
- Preserved renderer behavior when producer artifacts are absent.

## Quality Gates

| Gate | Command | Result |
|------|---------|--------|
| Static renderer tests | `PYTHONPATH=src python -m pytest tests/test_static_spec_renderer.py -q` | PASS — 10 passed |
| Lint | `ruff check src tests` | PASS — All checks passed |
| Format | `ruff format --check src tests` | PASS — 82 files already formatted |
| Full tests | `PYTHONPATH=src python -m pytest` | PASS — 487 passed, 1 skipped |
| Coverage | `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS — 487 passed, 1 skipped; total coverage 91.51% |
| Swift manifest | `swift package dump-package >/dev/null` | PASS |
| DocC build target | `swift build --target SpecHarvesterDocs` | PASS |

## Notes

- The viewer does not validate or accept generated candidates. It only displays
  bundle evidence for human review.
- Missing producer artifacts render as `producer.status: not_provided` and do
  not fail static rendering.
