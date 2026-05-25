# Next Task: P16-T10 — SpecPackageManifest Object Seam

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P16-T9
**Status:** Selected

## Description

Introduce a behavior-rich `SpecPackageManifest` object for reading
`specpm.yaml` metadata, foreign artifacts, and claim sections as the first
Elegant Objects seam before report modules are rewritten.

This task should preserve existing report behavior. Existing report modules may
continue to use their procedural parsers until follow-up stacked PRs switch them
to the new object.

## Recently Archived

- P16-T9: Architecture Lint Guardrails (PASS, 2026-05-25)
- P16-T7: Pylint Duplicate-Code Backend (PASS, 2026-05-25)

## Next Step

Plan and implement the manifest object with characterization tests and keep
architecture lint baseline non-blocking.
