# Explainable Corpus Selection Report

Status: Phase 35 report contract.

`SpecHarvesterCorpusSelectionReport` explains why a curated corpus source is
selected, deferred, or rejected. It sits after the
[`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md)
fixture and before any dry-run readiness check.

The report is review evidence. It is not registry authority and does not run
collection, draft packages, enrich candidates with AI, create SpecPM handoff
artifacts, clone or fetch repositories, install dependencies, execute
harvested code, publish registry metadata, accept packages, accept relations,
remove `preview_only`, or treat AI output as registry truth.

## Identity

The report identity is:

```json
{
  "apiVersion": "spec-harvester.corpus-selection-report/v0",
  "kind": "SpecHarvesterCorpusSelectionReport",
  "schemaVersion": 1,
  "authority": "producer_selection_report_only"
}
```

The fixture is:

```text
tests/fixtures/explainable_corpus_selection_report/p35-t5-selection-report.example.json
```

It references the P35-T4 seed plan:

```text
tests/fixtures/multi_ecosystem_seed_corpus_plan/p35-t4-seed-corpus-plan.example.json
```

## What It Explains

The report summarizes:

- selected sources;
- deferred sources;
- rejected sources;
- importance signals;
- exclusion reasons;
- quota decisions;
- classifier expectation summaries;
- downstream autonomous-batch command plan;
- non-authority statements.

It does not repeat every analyzer expectation from the seed plan. The seed plan
remains the source of truth for local checkout requirements, analyzer coverage,
classifier expectations, and stop conditions.

## Selected Sources

The Phase 35 report includes five selected sources:

| Source | Ecosystem | Package family | Selection explanation |
| --- | --- | --- | --- |
| `react` | `npm` | `react.workspace` | core UI framework, multi-package repository, package-set calibration target |
| `fastapi` | `pypi` | `fastapi.core` | Python framework core with public API richness and author review value |
| `serde` | `crates` | `serde.core` | Rust schema/data serialization archetype with dependency centrality |
| `gin` | `go` | `gin.core` | compact Go web framework archetype |
| `swift-argument-parser` | `swift` | `swift_argument_parser.core` | focused Swift CLI library archetype |

Every selected source has `downstreamDisposition:
include_in_readiness_check`. It still requires P35-T6 readiness before
collection or drafting.

## Deferred and Rejected Sources

Deferred sources:

- `types-react`: `types_only_package` and
  `needs_dedicated_archetype_policy`;
- `radix-ui-internal-primitives`: `internal_utility`,
  `needs_dedicated_archetype_policy`, and `ecosystem_quota_exceeded`.

Rejected sources:

- `react-internal-test-utils`: `test_fixture` and
  `registry_search_noise`.

These entries make the corpus auditable. The report should show which popular
or related packages were intentionally not harvested.

## Quota Decisions

`quotaDecisions[]` records one decision per ecosystem. For Phase 35:

- `npm` quota is filled by `react`; type-only, internal/plugin, and fixture-like
  packages remain non-selected;
- `pypi` quota is filled by `fastapi`;
- `crates` quota is filled by `serde`;
- `go` quota is filled by `gin`;
- `swift` quota is filled by `swift-argument-parser`.

Quota decisions are review evidence, not permission to crawl registries.

## Downstream Command Plan

The report records the future command plan:

```json
{
  "command": "autonomous-candidate-batch",
  "requiresPinnedLocalCheckouts": true,
  "requiresDryRunReadinessCheck": true,
  "defaultAiMode": "operator_selected",
  "mayApplyAiEnrichment": true,
  "mustStopBeforeCollectionUntil": "P35-T6 readiness check passes"
}
```

This is a command plan, not a command invocation.

## Non-Authority Boundary

The report keeps the standard Phase 35 boundary:

- `does_not_clone_or_fetch_repositories`;
- `does_not_install_dependencies`;
- `does_not_execute_harvested_code`;
- `does_not_publish_registry_metadata`;
- `does_not_accept_packages`;
- `does_not_accept_relations`;
- `does_not_seed_baselines`;
- `does_not_remove_preview_only`;
- `does_not_treat_ai_output_as_registry_truth`.

## Follow-Up Work

This report enables `P35-T6`: selected corpus dry-run readiness
([`SELECTED_CORPUS_DRY_RUN_READINESS.md`](SELECTED_CORPUS_DRY_RUN_READINESS.md)).
