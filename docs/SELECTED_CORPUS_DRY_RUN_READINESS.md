# Selected Corpus Dry-Run Readiness

Status: Phase 35 readiness report.

`SpecHarvesterSelectedCorpusReadinessReport` records whether the selected
Phase 35 seed corpus can enter an `autonomous-candidate-batch` dry run. It
follows the seed corpus plan and explainable selection report:

- [`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md);
- [`EXPLAINABLE_CORPUS_SELECTION_REPORT.md`](EXPLAINABLE_CORPUS_SELECTION_REPORT.md).

The readiness report is review evidence. It is not registry authority.

## Identity

The report identity is:

```json
{
  "apiVersion": "spec-harvester.selected-corpus-readiness/v0",
  "kind": "SpecHarvesterSelectedCorpusReadinessReport",
  "schemaVersion": 1,
  "authority": "producer_readiness_report_only"
}
```

The fixture is:

```text
tests/fixtures/selected_corpus_readiness/p35-t6-readiness.example.json
```

## Verdict

The P35 readiness verdict is:

```text
blocked_pending_local_checkouts
```

That is intentional. P35-T6 does not inspect real repository checkouts. The
P35-T4 fixture contains review pins, but a later operator run must provide and
verify actual local checkout revisions before collection or drafting can start.

## Covered Sources

The report covers all selected seed sources:

| Source | Ecosystem | Package family | Readiness |
| --- | --- | --- | --- |
| `react` | `npm` | `react.workspace` | `blocked` |
| `fastapi` | `pypi` | `fastapi.core` | `blocked` |
| `serde` | `crates` | `serde.core` | `blocked` |
| `gin` | `go` | `gin.core` | `blocked` |
| `swift-argument-parser` | `swift` | `swift_argument_parser.core` | `blocked` |

Each source is blocked by `local_checkout_not_verified`.

## What It Checks

For every selected source, the readiness report records:

- package-family target;
- required local checkout path;
- expected 40-character revision;
- `allowMutableRef: false`;
- `verificationStatus: not_verified`;
- required analyzers;
- stop conditions;
- blocking reasons;
- operator action.

Required analyzer coverage includes:

- `workspace_inventory` and `js_ts_public_api` for React;
- `python_public_api` and `readme_semantic_hints` for FastAPI;
- `rust_public_api` and `readme_semantic_hints` for Serde;
- `go_public_api` and `readme_semantic_hints` for Gin;
- `swift_public_api` and `readme_semantic_hints` for Swift Argument Parser.

## Command Gate

The downstream command gate records:

```json
{
  "command": "autonomous-candidate-batch",
  "allowed": false,
  "blockedUntil": "all_selected_sources_have_verified_pinned_local_checkouts",
  "mustNotRunCollection": true,
  "mustNotRunDrafting": true,
  "mustNotRunAiEnrichment": true,
  "mustNotCreateSpecPMHandoff": true
}
```

The report therefore proves that the Phase 35 seed corpus is planned and
explainable, but not yet executable as an autonomous batch.

## Non-Authority Boundary

The readiness report does not clone or fetch repositories, install
dependencies, execute harvested code, run collection, run drafting, run AI
enrichment, create SpecPM handoff artifacts, publish registry metadata, accept
packages, accept relations, seed baselines, remove `preview_only`, or treat AI
output as registry truth.

It also records the standard machine-readable non-authority statements:

- `does_not_clone_or_fetch_repositories`;
- `does_not_install_dependencies`;
- `does_not_execute_harvested_code`;
- `does_not_publish_registry_metadata`;
- `does_not_accept_packages`;
- `does_not_accept_relations`;
- `does_not_seed_baselines`;
- `does_not_remove_preview_only`;
- `does_not_treat_ai_output_as_registry_truth`.

## Phase Result

P35 now has:

- a corpus selection policy;
- a corpus plan contract;
- a candidate source classifier plan;
- a concrete seed corpus plan;
- an explainable selection report;
- a dry-run readiness report.

The next product step is not broader scraping. It is operator-provided pinned
local checkouts followed by a readiness rerun.
