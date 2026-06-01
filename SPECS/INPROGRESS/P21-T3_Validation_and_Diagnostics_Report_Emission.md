# P21-T3 — Validation and Diagnostics Report Emission

**Status:** In Progress
**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Date:** 2026-06-02

## Problem

P21-T2 emits `producer-receipt.json`, but validation and diagnostics are still
receipt-local placeholders. SpecPM's producer candidate bundle contract expects
`validation-report.json` and `diagnostics.json` as separate machine-readable
artifacts so reviewers and future preflight tooling can inspect validation
state, warnings, privacy notes, evidence gaps, and rejection risks without
trusting prose.

## Goals

- Emit `validation-report.json` during candidate draft generation.
- Emit `diagnostics.json` during candidate draft generation.
- Add both files to receipt `outputs[]` with roles `validation_report` and
  `diagnostics`.
- Add `validation.reportPath` and `validation.reportDigest` to
  `producer-receipt.json`.
- Add `diagnostics.path`, `diagnostics.digest`, and compact entries to
  `producer-receipt.json`.
- Keep reports deterministic and compact.
- Add regression tests that report digests in the receipt match generated file
  bytes.

## Non-Goals

- Do not implement the full P21-T4 preflight verifier.
- Do not invoke SpecPM validation as authority during draft generation.
- Do not change registry acceptance, publication, or maintainer-review policy.
- Do not extend the static viewer; that remains P21-T5.
- Do not embed raw private source bodies, private prompts, tokens, credentials,
  or local-only confidential paths.

## Deliverables

- Validation report object/schema for producer-side draft checks.
- Diagnostics report object/schema for producer-side warnings and caveats.
- Draft integration that writes both report files before the receipt is emitted.
- Receipt integration for report output digests and report references.
- Tests for report presence, shape, digest wiring, privacy notes, and clean
  default diagnostics.
- Validation report with exact quality gate results.

## Acceptance Criteria

- Drafted candidates contain `validation-report.json` and `diagnostics.json`.
- Receipt `outputs[]` includes both report files with matching SHA-256 digests.
- Receipt `validation.reportPath` is `validation-report.json`, and
  `validation.reportDigest` matches the report bytes.
- Receipt `diagnostics.path` is `diagnostics.json`, and `diagnostics.digest`
  matches the report bytes.
- Clean draft output reports `validation.status: valid` and
  `diagnostics.status: clean`.
- Diagnostics report contains privacy/security notes and review-boundary notes
  without implying automatic SpecPM acceptance.
- Existing tests, lint, format, coverage, Swift manifest, and DocC build pass.
