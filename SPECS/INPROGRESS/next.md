# Next Task: P13-T2 — Clean-Context Semantic Review Pass

**Priority:** P1
**Phase:** Phase 13. Prompted Refinement Quality Loop
**Effort:** 8 hours
**Dependencies:** P13-T1
**Status:** Selected
**Workplan:** `SPECS/Workplan.md` — Phase 13, `P13-T2`

## Description

Add a clean-context semantic review pass for generated `SpecNodeRefinementResult`
proposals. A second model should see only the deterministic evidence bundle, the
generated candidate or patch proposal, and a strict review rubric, then emit
typed findings instead of mutating the candidate directly.

## Next Step

Run the PLAN command to generate the implementation-ready PRD.
