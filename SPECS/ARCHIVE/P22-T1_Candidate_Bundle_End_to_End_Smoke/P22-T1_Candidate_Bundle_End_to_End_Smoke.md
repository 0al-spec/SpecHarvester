# P22-T1 — Candidate Bundle End-to-End Smoke

**Status:** Complete
**Priority:** P1
**Phase:** Phase 22. Producer Bundle End-to-End Smoke
**Date:** 2026-06-02

## Problem

Phase 21 added producer receipts, validation reports, diagnostics reports,
bundle preflight, static viewer panels, and handoff documentation as separate
steps. Without an end-to-end smoke, those pieces could drift while individual
unit tests still passed.

## Goals

- Add a local smoke that exercises the real producer path:
  collect -> draft -> preflight -> render.
- Use only local fixture files and trusted SpecHarvester APIs.
- Assert the generated candidate passes producer-side preflight.
- Assert the rendered static viewer payload exposes producer evidence from the
  same candidate bundle.

## Non-Goals

- Do not add SpecPM registry acceptance policy.
- Do not execute harvested repository code, install dependencies, or use
  network access.
- Do not commit generated candidate output.
- Do not treat producer evidence as SpecPM acceptance authority.

## Deliverables

- `tests/test_candidate_bundle_e2e.py` with a local fixture repository.
- Workplan and next-task updates showing Phase 22 completion.
- Validation report with exact quality gate results.

## Acceptance Criteria

- The smoke fails if receipt, report, preflight, or viewer wiring drifts.
- The generated bundle passes producer preflight.
- The rendered payload agrees with the receipt on package identity, output
  hashes, validation status, diagnostics status, and human-review boundary.
- Existing test, lint, format, Swift manifest, and DocC build gates pass.
