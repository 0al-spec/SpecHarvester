# Next Task: P16-T14 — Semantic Keyword Taxonomy Object

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P16-T13
**Status:** Suggested

## Description

Introduce a shared semantic keyword taxonomy object for documentation/API/tooling
term groups currently duplicated between collector evidence extraction and draft
semantic cluster generation.

## Recently Archived

- P16-T13: Public API Payload Records (PASS, 2026-05-26)
- P16-T12: Report Source Records Object (PASS, 2026-05-26)
- P16-T3: Package Identity and Namespace Normalization (PASS, 2026-05-26)

## Next Step

Run SELECT for `P16-T14`, then refactor the remaining `pylint` duplicate-code
cluster in `collector.py` and `drafter.py` without changing semantic evidence
output.

