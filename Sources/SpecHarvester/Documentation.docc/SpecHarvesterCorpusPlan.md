# SpecHarvester Corpus Plan

`SpecHarvesterCorpusPlan` is the machine-readable planning artifact for curated
multi-ecosystem source batches.

It records which repositories and package families are selected, why they are
selected, which package-like children are excluded or deferred, and which
non-authority boundaries apply before autonomous harvesting runs.

The plan is review evidence. It is not a registry artifact and does not accept
packages into SpecPM.

## Identity

Current identity:

```json
{
  "apiVersion": "spec-harvester.corpus-plan/v0",
  "kind": "SpecHarvesterCorpusPlan",
  "schemaVersion": 1,
  "authority": "producer_corpus_plan_only"
}
```

Required top-level sections are `corpus`, `sources[]`, and
`nonAuthorityStatements[]`.

## Corpus Metadata

`corpus` records:

- corpus name;
- purpose;
- selection mode;
- per-ecosystem quotas;
- selected, deferred, and rejected counts;
- downstream autonomous-batch command plan.

The command plan is advisory. It does not execute anything and does not grant
credentials or registry authority.

## Source Entries

Each source entry records:

- stable source id;
- status: `selected`, `deferred`, or `rejected`;
- ecosystem;
- repository;
- package family;
- categories;
- pinned local checkout expectation;
- selected-because reason codes;
- deferred or rejected reason codes;
- excluded subpackages;
- expected analyzer coverage;
- stop conditions.

Stable field names include `selectedBecause`, `deferredBecause`,
`rejectedBecause`, `excludedSubpackages`, `expectedAnalyzerCoverage`, and
`stopConditions`.

Every source entry is selected, deferred, or rejected.

The selection unit is still repository/package-family, not an isolated registry
search result.

## Reason Codes

Selected source reason codes include `high_dependency_centrality`,
`high_registry_usage`, `public_api_rich`, `ecosystem_archetype`,
`framework_core`, `ui_library`, `sdk_or_client_library`, `cli_surface`,
`parser_or_schema_surface`, `data_layer_surface`, `runtime_library`,
`security_supply_chain_relevant`, `author_review_value`, `source_available`,
`license_clear`, `multi_package_repository`, and
`single_package_reference_shape`.

Deferral, rejection, and excluded-subpackage reason codes include
`internal_utility`, `types_only_package`, `generated_only_package`,
`deprecated_source`, `example_package`, `test_fixture`, `build_tooling`,
`registry_search_noise`, `missing_public_source`, `missing_pinned_checkout`,
`unclear_license`, `ecosystem_quota_exceeded`, and
`needs_dedicated_archetype_policy`.

## Local-Only Boundary

`localCheckout` is a requirement, not a clone instruction. A plan must not
authorize SpecHarvester to clone repositories, fetch remotes, install
dependencies, run package scripts, run harvested tests, execute harvested code,
or contact registries during harvesting.

## Required Non-Authority Statements

Every plan must include:

- `does_not_clone_or_fetch_repositories`;
- `does_not_install_dependencies`;
- `does_not_execute_harvested_code`;
- `does_not_publish_registry_metadata`;
- `does_not_accept_packages`;
- `does_not_accept_relations`;
- `does_not_seed_baselines`;
- `does_not_remove_preview_only`;
- `does_not_treat_ai_output_as_registry_truth`.

## Fixture

The example fixture is
`tests/fixtures/corpus_plan/p35-t2-corpus-plan.example.json`.

It covers JavaScript/TypeScript, Python, Rust, Go, and Swift, and records
selected, deferred, and rejected source decisions.

## Follow-Up Work

This contract enables `P35-T3` candidate source classification, `P35-T4` seed
corpus planning, `P35-T5` explainable selection reports, and `P35-T6` dry-run
readiness checks.
