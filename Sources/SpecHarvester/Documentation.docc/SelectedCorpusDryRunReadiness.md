# Selected Corpus Dry-Run Readiness

`SpecHarvesterSelectedCorpusReadinessReport` records whether the selected
Phase 35 seed corpus can enter an `autonomous-candidate-batch` dry run.

It follows <doc:MultiEcosystemSeedCorpusPlan> and
<doc:ExplainableCorpusSelectionReport>. The report is review evidence, not
registry authority.

## Identity

The report identity is:

- `apiVersion: spec-harvester.selected-corpus-readiness/v0`;
- `kind: SpecHarvesterSelectedCorpusReadinessReport`;
- `schemaVersion: 1`;
- `authority: producer_readiness_report_only`.

The fixture is
`tests/fixtures/selected_corpus_readiness/p35-t6-readiness.example.json`.

## Verdict

The P35 readiness verdict is `blocked_pending_local_checkouts`.

That is intentional. P35-T6 does not inspect real repository checkouts. The
P35-T4 fixture contains review pins, but a later operator run must provide and
verify actual local checkout revisions before collection or drafting can start.

## Covered Sources

The report covers:

- `react` in `npm`, targeting `react.workspace`;
- `fastapi` in `pypi`, targeting `fastapi.core`;
- `serde` in `crates`, targeting `serde.core`;
- `gin` in `go`, targeting `gin.core`;
- `swift-argument-parser` in `swift`, targeting
  `swift_argument_parser.core`.

Each selected source is currently `blocked` by
`local_checkout_not_verified`.

## What It Checks

For every selected source, the readiness report records package-family target,
local checkout path, expected 40-character revision, `allowMutableRef: false`,
`verificationStatus: not_verified`, required analyzers, stop conditions,
blocking reasons, and operator action.

Required analyzer coverage includes `workspace_inventory`, `js_ts_public_api`,
`python_public_api`, `rust_public_api`, `go_public_api`, `swift_public_api`,
and `readme_semantic_hints`.

## Command Gate

The downstream command gate records `command: autonomous-candidate-batch`,
`allowed: false`,
`blockedUntil: all_selected_sources_have_verified_pinned_local_checkouts`,
`mustNotRunCollection: true`, `mustNotRunDrafting: true`,
`mustNotRunAiEnrichment: true`, and `mustNotCreateSpecPMHandoff: true`.

The report proves that the seed corpus is planned and explainable, but not yet
executable as an autonomous batch.

## Non-Authority Boundary

The readiness report does not clone or fetch repositories, install
dependencies, execute harvested code, run collection, run drafting, run AI
enrichment, create SpecPM handoff artifacts, publish registry metadata, accept
packages, accept relations, seed baselines, remove `preview_only`, or treat AI
output as registry truth.

## Phase Result

P35 now has a corpus selection policy, corpus plan contract, candidate source
classifier plan, concrete seed corpus plan, explainable selection report, and
dry-run readiness report.
