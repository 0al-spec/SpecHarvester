# Next Task: P16-T13 — Public API Payload Records

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P16-T12
**Status:** Selected
**Selected:** 2026-05-26

## Description

Introduce a shared public API payload record object for validating cached
analyzer entrypoints, symbols, diagnostics, and evidence paths across Python and
Go public interface analyzers.

## Recently Archived

- P16-T12: Report Source Records Object (PASS, 2026-05-26)
- P16-T3: Package Identity and Namespace Normalization (PASS, 2026-05-26)
- P16-T11: Report Manifest Parser Refactor (PASS, 2026-05-26)

## Next Step

Run PLAN for `P16-T13`, then refactor duplicated public API payload validation
while preserving analyzer cache behavior.

