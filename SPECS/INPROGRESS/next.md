# Next Task: P21-T4 — Candidate Bundle Preflight Verifier

**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Effort:** 4-8 hours
**Dependencies:** P21-T1, P21-T2, P21-T3
**Status:** In Progress
**Suggested:** 2026-06-02

## Description

Add a local candidate bundle preflight verifier that checks required files,
receipt schema/profile, output hashes, validation report digest, diagnostics
digest, stable generated IDs, evidence links, and review status before a
generated bundle is proposed to SpecPM.

## Recently Archived

- P21-T3: Validation and Diagnostics Report Emission (PASS, 2026-06-02)
- P21-T2: Producer Receipt Emission (PASS, 2026-06-02)
- P21-T1: Producer Candidate Bundle Output Planning (PASS, 2026-06-02)
- P20-T4: Scoped Source Validation Fixtures (PASS, 2026-06-01)
- P20-T3: CodeGraph Adapter Evaluation (PASS, 2026-05-31)

## Rationale

P21-T2 and P21-T3 now emit the candidate bundle evidence files. The next step is
to verify the bundle deterministically before handoff, including hashes and
review-boundary fields, without treating producer evidence as automatic SpecPM
acceptance.

## Next Step

Run SELECT for `P21-T4`, define the preflight report shape and failure
semantics, then add a verifier command or helper with tests for missing files,
digest mismatch, malformed receipt fields, invalid review status, and self-hash
violations.
