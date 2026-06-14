# Multi-Ecosystem Seed Corpus Plan

The multi-ecosystem seed corpus plan is the first concrete
`SpecHarvesterCorpusPlan` instance for autonomous popular-library harvesting.

It applies <doc:CorpusSelectionPolicy>, <doc:SpecHarvesterCorpusPlan>, and
<doc:CandidateSourceClassifierPlan> to a bounded source set before collection,
drafting, AI enrichment, or SpecPM handoff runs.

The seed plan is review evidence. It is not registry authority and does not
publish registry metadata, accept packages, or accept relations into SpecPM.

## Fixture

The fixture is
`tests/fixtures/multi_ecosystem_seed_corpus_plan/p35-t4-seed-corpus-plan.example.json`.

It uses:

- `apiVersion: spec-harvester.corpus-plan/v0`;
- `kind: SpecHarvesterCorpusPlan`;
- `schemaVersion: 1`;
- `authority: producer_corpus_plan_only`.

## Selected Sources

The first seed corpus selects five repository/package-family targets:

- `react` in `npm`, targeting `react.workspace`;
- `fastapi` in `pypi`, targeting `fastapi.core`;
- `serde` in `crates`, targeting `serde.core`;
- `gin` in `go`, targeting `gin.core`;
- `swift-argument-parser` in `swift`, targeting
  `swift_argument_parser.core`.

The plan covers JavaScript/TypeScript, Python, Rust, Go, and Swift while
remaining bounded and reviewable.

## Deferred and Rejected Sources

The plan records non-selected decisions too:

- `types-react` is deferred as a `types_only_package`;
- `radix-ui-internal-primitives` is deferred for dedicated archetype policy;
- `react-internal-test-utils` is rejected as `test_fixture` and
  `registry_search_noise`.

Recording deferred and rejected sources prevents the seed corpus from becoming
a raw popularity scrape.

## Classifier Expectations

Every source entry includes `classifierExpectations[]` aligned with
`SpecHarvesterCandidateSourceClassificationPlan`.

Representative expectations:

- `react.workspace`: `package_set_root` with `select_primary`;
- `react-dom`: `primary_package` with `select_member`;
- `@types/react`: `types_only_package` with `defer`;
- examples, fixtures, tooling, and internal utilities: `include_as_evidence_only`,
  `exclude`, or `defer`.

## Local Checkout Requirement

Every selected source requires an operator-managed pinned local checkout with
`allowMutableRef: false` and `revisionRequiredBeforeRun: true`.

The plan does not clone repositories, fetch remotes, install dependencies, run
package scripts, run harvested tests, execute harvested code, or contact
registries.

## Stop Conditions

Selected sources include stop conditions such as
`missing_pinned_local_checkout`, `source_revision_mismatch`,
`license_evidence_missing`, `primary_package_family_ambiguous`,
`expected_analyzer_unavailable`, and `selection_rationale_missing`.

## Non-Authority Boundary

The seed corpus plan does not publish registry metadata, accept packages,
accept relations, seed baselines, remove `preview_only`, or treat AI output as
registry truth.

## Follow-Up Work

This plan enables `P35-T5` <doc:ExplainableCorpusSelectionReport> and `P35-T6`
dry-run readiness checks.
