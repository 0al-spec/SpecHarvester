# Next Task: Phase 20 Complete

**Priority:** N/A
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Effort:** N/A
**Dependencies:** P20-T7
**Status:** Complete
**Active Branch:** `codex/p20-t7-codegraph-compatibility-guard`
**Last Archived:** P20-T7 CodeGraph Compatibility Guard

## Recently Archived

- `P20-T7` added the pinned `codegraph-compatibility-report` guard for
  validating the local `@colbymchenry/codegraph@0.9.7` compatibility fixture,
  package integrity metadata, `optional_preprovisioned` binary policy,
  `CODEGRAPH_NO_DOWNLOAD=1`, required JSON CLI commands with `--json`, and
  fixture-backed normalization into `source_graph_index` without installing
  CodeGraph, running npm/npx, accessing the network, or indexing third-party
  repositories in ordinary CI.
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

Phase 20 is complete. SpecHarvester now supports scoped source-unit harvesting,
Tuist manifest parsing, scoped validation fixtures, source-unit draft intent
boundaries, an explicit opt-in CodeGraph source graph adapter, and a pinned
CodeGraph compatibility guard.

The CodeGraph integration remains bounded: compatibility checking uses local
fixtures and optional explicitly provided executables only. Ordinary CI does not
install CodeGraph, run npm/npx, download tools, access the network, or index
third-party repositories.

## Next Step

Open the P20-T7 stacked PR above P20-T6 and wait for review/CI before selecting
any new phase.
