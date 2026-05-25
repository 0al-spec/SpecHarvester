# Next Task: P16-T9 — Architecture Lint Guardrails

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P16-T6, P16-T7
**Status:** Selected

## Description

Add lightweight architecture lint guardrails for the planned Elegant Objects
refactor, covering helper/manager naming relapse, constructor I/O, static domain
helpers, and duplicated manifest parser patterns before broad report-layer
restructuring begins.

The linter should be deterministic, local-only, dependency-free, and advisory by
default so the current repository baseline can be inspected before any blocking
policy is introduced.

## Recently Archived

- P16-T7: Pylint Duplicate-Code Backend (PASS, 2026-05-25)
- P16-T6: Duplicate-Code Quality Report (PASS, 2026-05-25)

## Next Step

Plan and implement a small AST-based architecture linter with tests, docs, and
a non-blocking CI baseline command.
