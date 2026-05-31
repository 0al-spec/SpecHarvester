# Next Task: P20-T3 — CodeGraph Adapter Evaluation

**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Effort:** 4-8 hours
**Dependencies:** P20-T2
**Status:** Queued
**Suggested:** 2026-05-31

## Description

Evaluate `codegraph` as an optional local evidence adapter for multi-language
source graph extraction, recording analyzer version, source digests, trust
policy, schema stability, licensing, and performance before any default pipeline
integration.

## Recently Archived

- P20-T2: Tuist Manifest Parsing (PASS, 2026-05-31)
- P20-T1: Scoped Source Target Harvesting (PASS, 2026-05-31)
- P17-T1: Procedural Style Metrics Report (PASS, 2026-05-29)
- P19-T1: Static Spec Renderer (PASS, 2026-05-29)
- P18-T1: Swift Public API Analyzer (PASS, 2026-05-29)

## Rationale

P20-T2 improves deterministic Tuist evidence, but broad multi-language folder
specification still needs a wider source graph strategy. `codegraph` may provide
useful local graph evidence, but it must be evaluated as an optional untrusted
adapter before integration.

## Next Step

Run SELECT for `P20-T3`, inspect `codegraph` installation/output contracts, and
write an evaluation artifact before adding any production adapter code.
