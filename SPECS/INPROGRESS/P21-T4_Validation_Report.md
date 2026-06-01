# P21-T4 Validation Report

**Task:** P21-T4 — Candidate Bundle Preflight Verifier
**Date:** 2026-06-02
**Branch:** `feature/P21-T4-candidate-bundle-preflight-verifier`
**Verdict:** PASS

## Scope Validated

- Added local candidate bundle preflight verifier.
- Added CLI command `preflight-candidate-bundle`.
- Verified required bundle files, receipt identity/profile, output digests,
  report digests, review status, bundle-local input digests, receipt self-hash
  exclusion, and manifest/receipt subject alignment.
- Added regression tests for valid generated bundles, digest mismatch,
  self-hash violation, invalid review status, missing bundle-local input, and
  CLI non-zero failure.

## Quality Gates

| Gate | Command | Result |
|------|---------|--------|
| Targeted preflight tests | `PYTHONPATH=src python -m pytest tests/test_collector.py -q -k 'candidate_bundle_preflight or cli_preflight_candidate_bundle'` | PASS — 6 passed, 81 deselected |
| Lint | `ruff check src tests` | PASS — All checks passed |
| Format | `ruff format --check src tests` | PASS — 82 files already formatted |
| Full tests | `PYTHONPATH=src python -m pytest` | PASS — 483 passed, 1 skipped |
| Coverage | `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS — 483 passed, 1 skipped; total coverage 91.59% |
| Swift manifest | `swift package dump-package >/dev/null` | PASS |
| DocC build target | `swift build --target SpecHarvesterDocs` | PASS |

## Notes

- The verifier is producer-side preflight evidence, not SpecPM registry
  authority.
- The CLI exits `1` when the preflight report status is not `passed`.
- Public index acceptance remains gated by `humanReview` and maintainer review;
  preflight does not publish or accept generated packages.
