# Next Task: P34-T1 AI Enrichment Candidate Patch Proposal

**Priority:** High
**Phase:** Phase 34. AI-Enabled Candidate Curation
**Effort:** Medium
**Dependencies:** P26-T4, P27-T2, P29-T5, P33-T4
**Status:** Active
**Active Branch:** `codex/p34-t1-ai-enrichment-application`
**Last Archived:** P20-T8 DocC Warning Cleanup

## Recently Archived

- `P20-T8` cleaned up stale DocC warnings by converting
  `AcceptedPackageUpdateProposals` from a symbol-page heading into a normal
  documentation article and by changing literal command references in
  `RealRepositoryQualityReport` from DocC symbol-style double-backtick markup
  to inline code markup. DocC static generation now completes with no
  `warning:` output for `AcceptedPackageUpdateProposals`,
  `python -m spec_harvester quality-report`, or `specpm validate`.
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

Live LM Studio/OpenAI-compatible enrichment can produce better
repository-specific summaries and capabilities than deterministic drafting, but
the improvements currently remain proposal JSON beside the generated bundle.

P34-T1 adds a deterministic helper that reads a clean
`SpecHarvesterPackageSetAIEnrichmentProposal`, copies a generated candidate
bundle to a review output directory, applies supported summary/capability/
interface enrichments, and emits a machine-readable patch report. The helper
must not mutate the source bundle, remove `preview_only`, accept packages,
accept relations, publish registry metadata, or treat model output as registry
truth.

## Next Step

Plan and implement P34-T1, then run the helper against the recorded FastAPI
AI enrichment smoke output to verify the AI-enabled review path.
