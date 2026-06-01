# Next Task: P21-T3 — Validation and Diagnostics Report Emission

**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Effort:** 4-8 hours
**Dependencies:** P21-T1, P21-T2
**Status:** Queued
**Suggested:** 2026-06-02

## Description

Emit `validation-report.json` and `diagnostics.json` alongside generated
`specpm.yaml`, `specs/*.spec.yaml`, and `producer-receipt.json`. The reports
should make validation result, warnings/errors, privacy/security notes,
unstable-ID warnings, evidence-link gaps, and namespace/version overlap
diagnostics machine-readable.

## Recently Archived

- P21-T2: Producer Receipt Emission (PASS, 2026-06-02)
- P21-T1: Producer Candidate Bundle Output Planning (PASS, 2026-06-02)
- P20-T4: Scoped Source Validation Fixtures (PASS, 2026-06-01)
- P20-T3: CodeGraph Adapter Evaluation (PASS, 2026-05-31)
- P20-T2: Tuist Manifest Parsing (PASS, 2026-05-31)

## Rationale

P21-T2 now emits `producer-receipt.json` with validation and diagnostics
placeholders. The next task should materialize the referenced machine-readable
reports and update the receipt to include their output roles and digests.

## Next Step

Run SELECT for `P21-T3`, define compact validation/diagnostics report schemas,
write both files during draft generation, and add regression tests that receipt
`outputs[]`, `validation.reportDigest`, and `diagnostics.digest` match the
generated report bytes.
