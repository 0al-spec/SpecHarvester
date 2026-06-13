# Next Task: P20-T5 Scoped Source-Unit Draft Intent Boundaries

**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Effort:** Medium
**Dependencies:** P20-T4, P17-T6
**Status:** Selected
**Active Branch:** `codex/p20-t5-scoped-source-unit-draft-intent-boundaries`
**Last Archived:** P17-T6 SpecNode Refinement Orchestration Objects

## Recently Archived

- `P17-T6` moved bounded SpecNode retry orchestration behind
  `SpecNodeRefinementRetrySequence` while preserving
  `run_specnode_refinement_retry_orchestration`, provider interfaces,
  provider-unavailable fallback payloads, semantic review validation, retry
  directive construction, retry attempt records, final digest binding, and
  retry-run validation. The procedural-style smoke recorded
  behaviorRichClassCount: 1 and reduced `specnode_refinement.py`
  topLevelFunctionSpan from 1690 to 1551.
- `P17-T5` moved single-package draft bundle materialization behind
  `SinglePackageDraftBundle` while preserving `DraftOptions`,
  `draft_spec_package`, generated `specpm.yaml`, boundary specs,
  `harvest.json`, optional public interface indexes, producer validation and
  diagnostics reports, author-ready quality reports, producer receipts,
  wrapper result fields, output roles, digests, and the receipt self-hash
  boundary. The procedural-style smoke recorded behaviorRichClassCount: 1 and
  reduced `drafter.py` topLevelFunctionSpan from 1665 to 1550.
- `P20-T4` extended scoped-source validation with real monorepo smoke fixtures,
  including a Tuist-managed Swift folder, a single-file target, and a non-Swift
  folder target, giving P20-T5 concrete scoped evidence cases to preserve.

## Description

Teach drafting/refinement prompts to distinguish repository, package, folder
module, and single-file source-unit intent so generated specs do not overclaim
package-manager ownership when only scoped evidence exists.

This resumes Phase 20 after the Phase 17 EO refactoring stack. Keep the change
focused on source-unit intent boundaries for draft and refinement behavior, not
on CodeGraph integration or new source graph evidence.

## Next Step

Run the BRANCH and PLAN commands for P20-T5.
