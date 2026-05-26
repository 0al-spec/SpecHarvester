# Next Task: P16-T15 — Public API Analyzer Options Object

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P16-T14
**Status:** Selected
**Selected:** 2026-05-26

## Description

Introduce a shared public API analyzer options object for common
source/package/output/trust inputs currently repeated across Python, Go, and
JS/TS public interface analyzers.

## Recently Archived

- P16-T14: Semantic Keyword Taxonomy Object (PASS, 2026-05-26)
- P16-T13: Public API Payload Records (PASS, 2026-05-26)
- P16-T12: Report Source Records Object (PASS, 2026-05-26)

## Rationale

P16-T14 reduced the trusted `pylint` duplicate-code backend to zero duplicate
blocks. The builtin advisory backend still reports one analyzer option-shape
cluster plus report-layer clusters outside the semantic taxonomy scope.

## Next Step

Create the P16-T15 PRD, then refactor the shared analyzer option shape without
obscuring language-specific analyzer behavior.
