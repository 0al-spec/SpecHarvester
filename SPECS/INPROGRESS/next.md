# Next Task: P16-T18 — Duplicate-Code Practical-Minimum Audit

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 1-2 hours
**Dependencies:** P16-T17
**Status:** Suggested
**Suggested:** 2026-05-26
**Selected:** 2026-05-26
**Branch:** `feature/P16-T18-duplicate-code-practical-minimum-audit`
**Review Subject:** `p16_t18_duplicate_code_practical_minimum_audit`

## Description

Run a duplicate-code practical-minimum audit after P16-T15 through P16-T17 and
document whether any remaining duplicate-code windows are intentional detector
noise or require another refactor.

## Recently Archived

- P16-T17: Real Repository Quality Rating Policy Objects (PASS, 2026-05-26)
- P16-T16: Upstream Issue Evaluation Object (PASS, 2026-05-26)
- P16-T15: Public API Analyzer Options Object (PASS, 2026-05-26)

## Rationale

P16-T17 reduced both builtin and `pylint` duplicate-code reports to zero
duplicate blocks for `src/spec_harvester`. The next useful step is to record the
practical-minimum baseline and decide whether the duplicate-reduction goal can
move from refactoring to periodic audit.

## Next Step

Run PLAN for `P16-T18`, then capture the duplicate-code baseline, architecture
lint advisory state, and follow-up decision.
