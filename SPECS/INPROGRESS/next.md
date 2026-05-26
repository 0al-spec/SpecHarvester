# Next Task: P16-T17 — Real Repository Quality Rating Policy Objects

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P16-T16
**Status:** Selected
**Suggested:** 2026-05-26
**Selected:** 2026-05-26
**Branch:** `feature/P16-T17-real-repo-quality-rating-policy`
**Review Subject:** `p16_t17_real_repo_quality_rating_policy_objects`

## Description

Introduce behavior-rich real repository quality rating policy objects for
duplicated draft/spec/source scoring guard clauses.

## Recently Archived

- P16-T16: Upstream Issue Evaluation Object (PASS, 2026-05-26)
- P16-T15: Public API Analyzer Options Object (PASS, 2026-05-26)
- P16-T14: Semantic Keyword Taxonomy Object (PASS, 2026-05-26)

## Rationale

P16-T16 removed upstream issue-generation duplicate clusters. The builtin
duplicate-code backend now reports only `real_repo_quality_report.py` rating
guard clusters.

## Next Step

Run PLAN for `P16-T17`, then refactor duplicated real repository quality rating
guards into explicit policy objects.
