# Next Task: P20-T8 DocC Warning Cleanup

**Priority:** Medium
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Effort:** Small
**Dependencies:** P20-T7
**Status:** Active
**Active Branch:** `codex/p20-t8-docc-warning-cleanup`
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

## Description

DocC static generation currently succeeds but emits stale warnings:

- `AcceptedPackageUpdateProposals` is referenced as a DocC page from multiple
  pages but its article is written as a symbol page heading.
- `RealRepositoryQualityReport` uses DocC symbol-style double-backtick markup
  for literal CLI commands: `python -m spec_harvester quality-report` and
  `specpm validate`.

P20-T8 should remove those warnings without changing runtime behavior,
registry behavior, package generation, or SpecPM handoff contracts.

## Acceptance

- `AcceptedPackageUpdateProposals` resolves as a DocC documentation page from
  `SpecHarvester`, `GettingStarted`, and `Workflow`.
- Literal CLI commands in `RealRepositoryQualityReport` are rendered as code,
  not treated as DocC symbol references.
- `swift package --allow-writing-to-directory ./.docc-build generate-documentation ...`
  completes without those stale warnings.
- Python tests, docs contract tests, ruff, format check, and `git diff --check`
  remain green.

## Next Step

Inspect the affected DocC pages, apply minimal Markdown fixes, and record a
validation report showing that DocC warning output is clean for the targeted
warnings.
