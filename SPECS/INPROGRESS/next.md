# Next Task: P16-T11 — Report Manifest Parser Refactor

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P16-T10
**Status:** Selected

## Description

Refactor accepted diff and namespace upstream reports to read manifests through
`SpecPackageManifest`, reducing duplicated manifest parser code while preserving
report JSON behavior.

## Recently Archived

- P16-T10: SpecPackageManifest Object Seam (PASS, 2026-05-26)
- P16-T9: Architecture Lint Guardrails (PASS, 2026-05-25)

## Next Step

Plan and replace the duplicated parser bodies in accepted diff and namespace
reports with `SpecPackageManifest` behavior, then compare architecture lint
baseline before and after.
