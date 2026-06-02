# P22-T1 Validation Report

**Task:** P22-T1 — Candidate Bundle End-to-End Smoke
**Date:** 2026-06-02
**Branch:** `feature/P22-T1-candidate-bundle-e2e-smoke`
**Verdict:** PASS

## Scope Validated

- Added an end-to-end smoke for the local producer path:
  collect -> draft -> preflight -> render.
- The smoke builds a local fixture repository, collects `harvest.json`, drafts
  a candidate bundle, verifies producer-side preflight, renders the static
  viewer, and compares viewer producer evidence with the generated receipt and
  reports.
- The smoke keeps generated candidate output test-local and does not execute
  harvested repository code.

## Quality Gates

| Gate | Command | Result |
|------|---------|--------|
| E2E smoke | `PYTHONPATH=src python -m pytest tests/test_candidate_bundle_e2e.py -q` | PASS — 1 passed |
| Lint | `ruff check src tests` | PASS — All checks passed |
| Format | `ruff format --check src tests` | PASS — 83 files already formatted |
| Full tests | `PYTHONPATH=src python -m pytest` | PASS — 489 passed, 1 skipped |
| Swift manifest | `swift package dump-package >/dev/null` | PASS |
| DocC build target | `swift build --target SpecHarvesterDocs` | PASS |

## Notes

- This smoke is producer-side confidence only. It does not add SpecPM-side
  proposal policy or registry acceptance.
- The next useful step is SpecPM-side documentation for treating producer
  candidate bundles as proposal evidence without trusting generated receipts as
  registry authority.
