# Next Task: P21-T1 — Producer Candidate Bundle Output Planning

**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Effort:** 2-4 hours
**Dependencies:** SpecPM Producer Candidate Bundle Contract documentation
**Status:** In Progress
**Suggested:** 2026-06-02

## Description

Align SpecHarvester's output planning with the SpecPM Producer Candidate Bundle
Contract. The task should document the required candidate bundle layout,
`producer-receipt.json` profile, generated output digest expectations, human
review boundary, and rejection diagnostics that later P21 implementation tasks
must satisfy.

## Recently Archived

- P20-T4: Scoped Source Validation Fixtures (PASS, 2026-06-01)
- P20-T3: CodeGraph Adapter Evaluation (PASS, 2026-05-31)
- P20-T2: Tuist Manifest Parsing (PASS, 2026-05-31)
- P20-T1: Scoped Source Target Harvesting (PASS, 2026-05-31)
- P17-T1: Procedural Style Metrics Report (PASS, 2026-05-29)

## Rationale

SpecPM now documents a producer candidate bundle contract. SpecHarvester needs a
local planning contract before implementation so P21-T2 through P21-T6 emit and
validate the same machine-verifiable handoff shape without implying automatic
SpecPM acceptance.

## Next Step

Create the P21-T1 PRD, add SpecHarvester-facing output planning documentation,
and add lightweight documentation contract tests that lock the required
candidate bundle shape and self-hash boundary.
