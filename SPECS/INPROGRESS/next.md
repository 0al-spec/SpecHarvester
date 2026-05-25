# Next Task: P16-T3 — Package Identity and Namespace Normalization

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P15-T4, P15-T5
**Status:** Suggested

## Description

Normalize package identity and namespace/upstream comparisons across hyphen,
underscore, separator, and case variants so generated package IDs like
`navigation_split_view.core` do not create low-signal namespace advisories for
upstream repositories such as `NavigationSplitView`.

## Recently Archived

- P16-T6: Duplicate-Code Quality Report (PASS, 2026-05-25)
- P16-T2: License Provenance Classification for Collected License Files (PASS, 2026-05-25)
- P16-T1: Quality Report Public Interface Coverage (PASS, 2026-05-24)

## Next Step

Run SELECT for `P16-T3`, then add a focused regression around
hyphen/underscore/case normalization in namespace/upstream governance reports.
