# Next Task: P21-T6 — SpecPM Handoff Documentation and Examples

**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Effort:** 3-6 hours
**Dependencies:** P21-T1, P21-T2, P21-T3, P21-T4, P21-T5
**Status:** Selected
**Suggested:** 2026-06-02
**Branch:** `feature/P21-T6-specpm-handoff-docs-examples`
**Stack Base:** `feature/P21-T5-static-viewer-producer-receipt-panels`

## Description

Add SpecPM handoff documentation and examples for generated candidate bundles,
including the distinction between SpecHarvester producing an evidence-rich
candidate, SpecPM validating package shape, maintainers approving acceptance,
and the public index publishing only reviewed sources.

## Recently Archived

- P21-T5: Static Viewer Producer Receipt Panels (PASS, 2026-06-02)
- P21-T4: Candidate Bundle Preflight Verifier (PASS, 2026-06-02)
- P21-T3: Validation and Diagnostics Report Emission (PASS, 2026-06-02)
- P21-T2: Producer Receipt Emission (PASS, 2026-06-02)
- P21-T1: Producer Candidate Bundle Output Planning (PASS, 2026-06-02)

## Rationale

P21-T1 through P21-T5 now produce and display the candidate bundle evidence
required by the SpecPM producer handoff contract. Maintainers still need a
single SpecHarvester-facing documentation page and examples that explain how to
generate, inspect, preflight, and review the bundle without treating generated
output as automatic SpecPM acceptance.

## Next Step

Run PLAN for `P21-T6`, inspect existing producer bundle and static renderer
docs, and add handoff documentation plus examples that preserve the
SpecHarvester/SpecPM trust boundary. Keep the PR stacked on P21-T5 until #106
lands.
