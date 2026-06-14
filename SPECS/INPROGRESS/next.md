# Next Task: P20-T7 CodeGraph Compatibility Guard

**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Effort:** Medium
**Dependencies:** P20-T6
**Status:** Ready
**Last Archived:** P20-T6 CodeGraph Adapter Boundary

## Recently Archived

- `P20-T6` added the explicit opt-in `codegraph-source-graph-index` boundary
  for normalizing pre-existing CodeGraph JSON or SQLite evidence into
  `source_graph_index`, including untrusted optional-tool provenance, input and
  executable digests, safe-path enforcement, deterministic ordering, bounded
  nodes/edges, diagnostics, GitHub docs, and DocC coverage without installing
  CodeGraph, running npm, downloading tools, or indexing repositories in CI.
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

## Description

Add a pinned CodeGraph interface compatibility guard that verifies the expected
package version, binary availability contract, CLI JSON flags, and normalized
schema mapping without indexing third-party projects in ordinary CI.

This is the compatibility layer for the P20-T6 adapter boundary. Keep it focused
on pinned metadata, fixture-backed CLI surface expectations, and normalized
schema mapping. Do not add live repository indexing to ordinary CI.

## Next Step

Run the BRANCH and PLAN commands for P20-T7 after the P20-T6 stacked PR is
reviewed or when the maintainer asks to continue the stack.
