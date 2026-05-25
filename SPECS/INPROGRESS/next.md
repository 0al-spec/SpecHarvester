# Next Task: P16-T7 — Pylint Duplicate-Code Backend

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P16-T6
**Status:** Selected

## Description

Integrate an established duplicate-code detector backend, starting with Python
`pylint` `duplicate-code`/`R0801`, behind the existing
`SpecHarvesterCodeDuplicationReport` contract.

The built-in detector remains a lightweight fallback. The new backend should
provide a more standard quality signal and run as a non-blocking CI baseline
check until baseline suppression or fail-on-new-duplicates semantics are
defined.

## Recently Archived

- P16-T6: Duplicate-Code Quality Report (PASS, 2026-05-25)
- P16-T2: License Provenance Classification for Collected License Files (PASS, 2026-05-25)

## Next Step

Plan and implement the `pylint` backend, add regression coverage for parsing
`R0801` output, and wire an advisory CI baseline command.
