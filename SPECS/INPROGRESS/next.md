# Next Task: P20-T6 CodeGraph Adapter Boundary

**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Effort:** Medium
**Dependencies:** P20-T3, P20-T5
**Status:** Ready
**Last Archived:** P20-T5 Scoped Source-Unit Draft Intent Boundaries

## Recently Archived

- `P20-T5` added deterministic source-unit intent boundaries for repository,
  package, folder/module, and single-file draft targets, surfaced those
  boundaries in generated summaries, scope includes, constraints, provenance,
  and SpecNode `compactModelInput`, and preserved the rule that scoped evidence
  must not be upgraded into repository-level or package-manager ownership
  claims without supporting package manifest evidence.
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

## Description

Implement an explicit opt-in CodeGraph adapter boundary that never installs or
downloads tools, records analyzer and executable provenance, and normalizes JSON
or SQLite graph evidence into a SpecHarvester-owned `source_graph_index`
evidence shape.

This continues Phase 20 after source-unit intent boundaries. Keep the change
focused on the adapter trust boundary and normalized evidence contract; do not
make CodeGraph a default analyzer and do not index third-party projects unless
the operator explicitly opts in.

## Next Step

Run the BRANCH and PLAN commands for P20-T6 after the P20-T5 stacked PR is
reviewed or when the maintainer asks to continue the stack.
