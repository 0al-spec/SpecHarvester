# Next Task: P21-T5 — Static Viewer Producer Receipt Panels

**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Effort:** 4-8 hours
**Dependencies:** P21-T1, P21-T2, P21-T3, P21-T4
**Status:** Selected
**Suggested:** 2026-06-02
**Branch:** `feature/P21-T5-static-viewer-producer-receipt-panels`
**Stack Base:** `feature/P21-T4-candidate-bundle-preflight-verifier`

## Description

Extend the static candidate viewer to show producer receipt, input provenance,
output hashes, validation status, diagnostics summary, privacy/security caveats,
and human review boundary without implying automatic SpecPM acceptance.

## Recently Archived

- P21-T4: Candidate Bundle Preflight Verifier (PASS, 2026-06-02)
- P21-T3: Validation and Diagnostics Report Emission (PASS, 2026-06-02)
- P21-T2: Producer Receipt Emission (PASS, 2026-06-02)
- P21-T1: Producer Candidate Bundle Output Planning (PASS, 2026-06-02)
- P20-T4: Scoped Source Validation Fixtures (PASS, 2026-06-01)

## Rationale

P21-T2 through P21-T4 now emit and verify producer handoff evidence. The viewer
should make that evidence reviewable for humans while preserving the trust
boundary: generated receipt evidence does not equal SpecPM acceptance.

## Next Step

Run PLAN for `P21-T5`, then inspect the static renderer payload/assets and add
read-only panels for receipt provenance, hashes, validation, diagnostics,
privacy, and human review status. Keep the PR stacked on P21-T4 until #105 is
merged into `main`.
