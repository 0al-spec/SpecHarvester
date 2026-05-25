# Next Task: P16-T6 — Duplicate-Code Quality Report

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P16-T2
**Status:** Selected

## Description

Add an advisory duplicate-code quality report that detects repeated
implementation blocks in repository source, starts non-blocking for baseline
collection, and can later be promoted to a fail-on-new-duplicates CI gate.

The immediate trigger is review feedback where duplicated license filename
allowlists and predicates could have drifted silently between collector and
license provenance reporting code.

## Recently Archived

- P16-T2: License Provenance Classification for Collected License Files (PASS, 2026-05-25)
- P16-T1: Quality Report Public Interface Coverage (PASS, 2026-05-24)

## Next Step

Plan and implement a deterministic, local-only duplicate-code report with
regression coverage and an explicit non-blocking default.
