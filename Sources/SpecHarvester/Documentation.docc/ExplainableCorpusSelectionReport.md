# Explainable Corpus Selection Report

`SpecHarvesterCorpusSelectionReport` explains why a curated corpus source is
selected, deferred, or rejected.

It sits after <doc:MultiEcosystemSeedCorpusPlan> and before any dry-run
readiness check. The report is review evidence, not registry authority.

## Identity

The report identity is:

- `apiVersion: spec-harvester.corpus-selection-report/v0`;
- `kind: SpecHarvesterCorpusSelectionReport`;
- `schemaVersion: 1`;
- `authority: producer_selection_report_only`.

The fixture is
`tests/fixtures/explainable_corpus_selection_report/p35-t5-selection-report.example.json`.

It references
`tests/fixtures/multi_ecosystem_seed_corpus_plan/p35-t4-seed-corpus-plan.example.json`.

## What It Explains

The report summarizes selected sources, deferred sources, rejected sources,
importance signals, exclusion reasons, quota decisions, classifier expectation
summaries, the downstream autonomous-batch command plan, and non-authority
statements.

The seed corpus plan remains the source of truth for local checkout
requirements, analyzer coverage, classifier expectations, and stop conditions.

## Selected Sources

The Phase 35 report includes:

- `react` in `npm`, targeting `react.workspace`;
- `fastapi` in `pypi`, targeting `fastapi.core`;
- `serde` in `crates`, targeting `serde.core`;
- `gin` in `go`, targeting `gin.core`;
- `swift-argument-parser` in `swift`, targeting
  `swift_argument_parser.core`.

Every selected source has `downstreamDisposition:
include_in_readiness_check` and still requires P35-T6 readiness before
collection or drafting.

## Deferred and Rejected Sources

Deferred sources include `types-react` for `types_only_package` policy and
`radix-ui-internal-primitives` for internal/plugin archetype policy.

`react-internal-test-utils` is rejected as `test_fixture` and
`registry_search_noise`.

## Quota Decisions

`quotaDecisions[]` records one decision per ecosystem:

- `npm` quota is filled by `react`;
- `pypi` quota is filled by `fastapi`;
- `crates` quota is filled by `serde`;
- `go` quota is filled by `gin`;
- `swift` quota is filled by `swift-argument-parser`.

Quota decisions are review evidence, not permission to crawl registries.

## Downstream Command Plan

The report records the future `autonomous-candidate-batch` command plan with
`requiresPinnedLocalCheckouts`, `requiresDryRunReadinessCheck`,
`defaultAiMode: operator_selected`, `mayApplyAiEnrichment`, and
`mustStopBeforeCollectionUntil: P35-T6 readiness check passes`.

This is a command plan, not a command invocation.

## Non-Authority Boundary

The report does not clone or fetch repositories, install dependencies, execute
harvested code, publish registry metadata, accept packages, accept relations,
seed baselines, remove `preview_only`, or treat AI output as registry truth.

## Follow-Up Work

This report enables `P35-T6` <doc:SelectedCorpusDryRunReadiness>.
