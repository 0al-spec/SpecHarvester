# Next Task: P16-T5 — Rerun Representative Local Validation Matrix

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P16-T1, P16-T2, P16-T3, P16-T4
**Status:** Suggested
**Suggested:** 2026-05-28

## Description

Rerun the representative local validation matrix after P16-T1 through P16-T4 and
document whether advisory counts, analyzer coverage, and failure classes improved
without committing generated `.smoke/` artifacts.

## Recently Archived

- P16-T4: Reduce Broad Duplicate Semantic Intent Claims (PASS, 2026-05-28)
- P16-T18: Duplicate-Code Practical-Minimum Audit (PASS, 2026-05-26)
- P16-T17: Real Repository Quality Rating Policy Objects (PASS, 2026-05-26)

## Rationale

P16-T4 filtered broad language-neutral semantic intents out of governance
duplicate findings. The next unchecked task should rerun the local matrix to
measure advisory-count and failure-class changes against the original P15-T4
baseline.

## Next Step

Run SELECT for `P16-T5`, then rerun the representative matrix using ignored
`.smoke/` outputs and archive only the compact validation findings.
