# Next Task: P35-T5 Explainable Corpus Selection Report

**Status:** Planned
**Phase:** Phase 35. Curated Multi-Ecosystem Corpus Selection
**Task:** `P35-T5` Add an explainable corpus selection report
**Last Archived:** P35-T4 Multi-Ecosystem Seed Corpus Plan

## Recently Archived

- `P35-T4` added
  [`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](../../docs/MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md)
  and the DocC mirror `MultiEcosystemSeedCorpusPlan`.
- The seed plan fixture
  `tests/fixtures/multi_ecosystem_seed_corpus_plan/p35-t4-seed-corpus-plan.example.json`
  uses `SpecHarvesterCorpusPlan` with `apiVersion:
  spec-harvester.corpus-plan/v0`, `schemaVersion: 1`, and
  `authority: producer_corpus_plan_only`.
- The selected seed set covers `react.workspace`, `fastapi.core`,
  `serde.core`, `gin.core`, and `swift_argument_parser.core`.
- The fixture records selected, deferred, and rejected sources plus
  `classifierExpectations`, expected analyzer coverage, stop conditions,
  operator-managed pinned local checkouts, and non-authority statements.

## Context

P35-T1 defined the source selection policy, P35-T2 defined the corpus plan
shape, P35-T3 defined source classification, and P35-T4 created the first
bounded seed corpus. P35-T5 should make that selection explainable as a review
report before any dry-run readiness check or autonomous batch run.

## Motivation

- Operators need to understand why a source was selected, deferred, or
  rejected without reading the full fixture by hand.
- The report should make importance signals, exclusion reasons, quota
  decisions, and the downstream autonomous-batch command plan explicit.
- The report should remain review evidence and must not imply collection,
  drafting, AI enrichment, SpecPM handoff, or registry acceptance.

## Goal

Add an explainable corpus selection report for the P35 seed corpus.

## Proposed Scope

- Document a machine-readable explainable selection report shape.
- Reference the P35-T4 seed corpus plan fixture.
- Record selected sources, deferred sources, rejected sources, importance
  signals, exclusion reasons, quota decisions, and the downstream
  autonomous-batch command plan.
- Preserve non-authority statements: the report does not run collection, does
  not publish registry metadata, does not accept packages, does not accept
  relations, does not remove `preview_only`, and does not treat AI output as
  registry truth.

## Acceptance

- The report is documented in GitHub Markdown and DocC.
- A regression fixture exists for the explainable report.
- Tests validate selected/deferred/rejected counts, source references,
  importance signals, exclusion reasons, quota decisions, command plan, and
  non-authority boundary.
- The next task remains `P35-T6` selected corpus dry-run readiness.
