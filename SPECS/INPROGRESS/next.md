# Next Task: P20-T5 — Source Unit Intent Drafting

**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Effort:** 4-8 hours
**Dependencies:** P20-T1, P20-T2, P20-T4
**Status:** Queued
**Suggested:** 2026-06-01

## Description

Teach drafting/refinement prompts to distinguish repository, package, folder
module, and single-file source-unit intent so generated specs do not overclaim
package-manager ownership when only scoped evidence exists.

## Recently Archived

- P20-T4: Scoped Source Validation Fixtures (PASS, 2026-06-01)
- P20-T3: CodeGraph Adapter Evaluation (PASS, 2026-05-31)
- P20-T2: Tuist Manifest Parsing (PASS, 2026-05-31)
- P20-T1: Scoped Source Target Harvesting (PASS, 2026-05-31)
- P17-T1: Procedural Style Metrics Report (PASS, 2026-05-29)

## Rationale

P20-T4 now provides deterministic scoped-source fixtures. The next risk is
semantic overclaiming: folder and file source units should be described as
source units unless package-manager evidence actually exists.

## Next Step

Run SELECT for `P20-T5`, inspect current drafting/refinement wording, and add
tests that prevent scoped folder/file specs from claiming package-manager
ownership without matching evidence.
