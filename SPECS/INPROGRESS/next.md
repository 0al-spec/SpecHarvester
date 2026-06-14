# Next Task: P35-T6 Selected Corpus Dry-Run Readiness

**Status:** In Progress
**Phase:** Phase 35. Curated Multi-Ecosystem Corpus Selection
**Task:** `P35-T6` Run or document selected corpus plan dry-run readiness
**Branch:** `feature/P35-T6-selected-corpus-readiness`
**Last Archived:** P35-T5 Explainable Corpus Selection Report

## Recently Archived

- `P35-T5` added
  [`EXPLAINABLE_CORPUS_SELECTION_REPORT.md`](../../docs/EXPLAINABLE_CORPUS_SELECTION_REPORT.md)
  and the DocC mirror `ExplainableCorpusSelectionReport`.
- The report fixture
  `tests/fixtures/explainable_corpus_selection_report/p35-t5-selection-report.example.json`
  defines `SpecHarvesterCorpusSelectionReport` with `apiVersion:
  spec-harvester.corpus-selection-report/v0`, `schemaVersion: 1`, and
  `authority: producer_selection_report_only`.
- The report references the P35-T4 seed corpus plan, summarizes selected,
  deferred, and rejected sources, records importance signals, exclusion
  reasons, quota decisions, and the downstream autonomous-batch command plan.
- The report preserves the non-authority boundary: no clone/fetch,
  dependency installation, harvested code execution, registry publication,
  package acceptance, relation acceptance, baseline seeding, `preview_only`
  removal, or AI output as registry truth.

## Context

P35-T1 defined selection policy, P35-T2 defined the corpus plan shape, P35-T3
defined source classification, P35-T4 created the seed plan, and P35-T5 made
that selection explainable. P35-T6 should now prove whether the selected
sources are ready for a dry run before collection or drafting starts.

## Motivation

- The selected seed corpus must not move into autonomous collection unless
  every selected source has a pinned local checkout.
- The readiness check should verify package-family targets, expected analyzer
  coverage, and explicit stop conditions for each selected source.
- The result should remain review evidence and must not publish registry
  metadata or accept packages.

## Goal

Run or document selected corpus plan dry-run readiness for the P35 seed corpus.

## Proposed Scope

- Verify or document readiness for the selected sources from the P35-T4 seed
  corpus plan.
- Check pinned local checkout requirements, package-family targets, expected
  analyzer coverage, and explicit stop conditions.
- Record whether the corpus is ready for `autonomous-candidate-batch` or
  blocked pending operator-provided local checkouts.
- Preserve non-authority statements: the report does not publish registry
  metadata, does not accept packages or relations, does not seed baselines,
  does not remove `preview_only`, and does not treat AI output as registry
  truth.

## Acceptance

- A readiness artifact or documented dry-run readiness report exists.
- The report covers all five selected source ids from P35-T4.
- The report explicitly handles missing or unverified pinned local checkouts.
- Tests validate package-family targets, analyzer expectations, stop
  conditions, readiness status, and non-authority boundary.
- Phase 35 can be marked complete only if the readiness evidence proves the
  acceptance criteria and the workplan has no remaining P35 tasks.
