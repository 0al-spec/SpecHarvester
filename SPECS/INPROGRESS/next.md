# Next Task: P20-T4 — Scoped Source Validation Fixtures

**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Effort:** 4-8 hours
**Dependencies:** P20-T1, P20-T2, P20-T3
**Status:** Queued
**Suggested:** 2026-05-31

## Description

Extend scoped-source validation with real monorepo smoke fixtures, including a
Tuist-managed Swift folder, a single-file target, and at least one non-Swift
folder target.

## Recently Archived

- P20-T3: CodeGraph Adapter Evaluation (PASS, 2026-05-31)
- P20-T2: Tuist Manifest Parsing (PASS, 2026-05-31)
- P20-T1: Scoped Source Target Harvesting (PASS, 2026-05-31)
- P17-T1: Procedural Style Metrics Report (PASS, 2026-05-29)
- P19-T1: Static Spec Renderer (PASS, 2026-05-29)

## Rationale

P20-T3 confirmed that third-party graph tooling should remain optional and
untrusted. Before adding adapters, scoped folder and file harvesting needs a
stable smoke matrix that captures the real repository shapes this feature is
meant to support.

## Next Step

Run SELECT for `P20-T4`, choose representative local fixtures, and add
deterministic validation coverage for scoped folder/file harvesting without
executing repository code.
