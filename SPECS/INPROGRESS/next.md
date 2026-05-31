# Next Task: P17-T2 — CLI Command Objects

**Priority:** P1
**Phase:** Phase 17. Elegant Objects Refactoring Strategy
**Effort:** 4-8 hours
**Dependencies:** P17-T1
**Status:** Queued
**Suggested:** 2026-05-29

## Description

Split the CLI execution shell from domain command behavior by introducing small
command objects for selected `code-duplication-report`, `architecture-lint`,
and report-generation flows while preserving parser flags, JSON error output,
and exit-code behavior.

## Recently Archived

- P17-T1: Procedural Style Metrics Report (PASS, 2026-05-29)
- P19-T1: Static Spec Renderer (PASS, 2026-05-29)
- P18-T1: Swift Public API Analyzer (PASS, 2026-05-29)
- P16-T8: Evaluate Multi-Language Duplicate-Code Detector (PASS, 2026-05-28)
- P16-T5: Rerun Representative Local Validation Matrix (PASS, 2026-05-28)

## Rationale

P17-T1 now provides a deterministic baseline for procedural concentration,
including the `cli.py` hotspot. The next EO refactor should attack that hotspot
directly by pulling execution behavior out of the procedural CLI shell while
preserving its public command contract.

## Next Step

Run SELECT for `P17-T2`, define the first command-object seams, and keep parser
definition behavior stable while moving execution logic into named objects.
