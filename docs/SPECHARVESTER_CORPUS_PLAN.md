# SpecHarvester Corpus Plan

Status: Phase 35 contract.

`SpecHarvesterCorpusPlan` is the machine-readable planning artifact for curated
multi-ecosystem source batches. It records which repositories and package
families are selected, why they are selected, what is excluded or deferred, and
which non-authority boundaries apply before any autonomous harvesting run.

The plan is review evidence. It is not a registry artifact and does not accept
packages into SpecPM.

## Identity

The document identity is:

```json
{
  "apiVersion": "spec-harvester.corpus-plan/v0",
  "kind": "SpecHarvesterCorpusPlan",
  "schemaVersion": 1,
  "authority": "producer_corpus_plan_only"
}
```

Required top-level fields:

| Field | Meaning |
| --- | --- |
| `apiVersion` | Contract version. Current value: `spec-harvester.corpus-plan/v0`. |
| `kind` | Must be `SpecHarvesterCorpusPlan`. |
| `schemaVersion` | Integer schema version. Current value: `1`. |
| `authority` | Must be `producer_corpus_plan_only`. |
| `corpus` | Corpus metadata, quotas, counts, and command plan. |
| `sources[]` | Selected, deferred, or rejected source entries. |
| `nonAuthorityStatements[]` | Required explicit boundary statements. |

## Corpus Metadata

`corpus` records the batch-level plan:

```json
{
  "name": "author-ready-mvp-corpus",
  "purpose": "curated_author_ready_starter_specs",
  "selectionMode": "curated_with_registry_signals",
  "ecosystemQuotas": [
    {"ecosystem": "npm", "limit": 2},
    {"ecosystem": "pypi", "limit": 2}
  ],
  "summary": {
    "selectedSourceCount": 5,
    "deferredSourceCount": 1,
    "rejectedSourceCount": 1
  },
  "downstreamCommandPlan": {
    "command": "autonomous-candidate-batch",
    "requiresPinnedLocalCheckouts": true,
    "defaultAiMode": "operator_selected",
    "mayApplyAiEnrichment": true
  }
}
```

The command plan is advisory. It does not run the command and does not grant
credentials or registry authority.

## Source Entries

Each item in `sources[]` represents one repository/package-family selection
decision.

Every source entry is selected, deferred, or rejected.

Required fields:

| Field | Meaning |
| --- | --- |
| `id` | Stable source id inside the plan. |
| `status` | `selected`, `deferred`, or `rejected`. |
| `ecosystem` | Registry or ecosystem family, such as `npm`, `pypi`, `crates`, `go`, `maven`, `swift`, `rubygems`, or `packagist`. |
| `repository` | Public source repository identifier or URL. |
| `packageFamily` | Intended SpecPM package family target. |
| `categories[]` | Review categories such as `framework`, `ui_library`, `sdk`, `cli`, `parser`, `data_layer`, `runtime_library`, or `tooling`. |
| `localCheckout` | Required pinned local checkout expectation. |
| `selectedBecause[]` | Reason codes explaining inclusion. Empty for rejected entries. |
| `deferredBecause[]` | Reason codes explaining deferral. Empty for selected entries. |
| `rejectedBecause[]` | Reason codes explaining rejection. Empty for selected/deferred entries. |
| `excludedSubpackages[]` | Package-like children intentionally excluded or deferred. |
| `expectedAnalyzerCoverage[]` | Static analyzer expectations before collection. |
| `stopConditions[]` | Conditions that stop this source before candidate generation or handoff. |

## Reason Codes

`selectedBecause[]` should use stable reason codes:

- `high_dependency_centrality`;
- `high_registry_usage`;
- `public_api_rich`;
- `ecosystem_archetype`;
- `framework_core`;
- `ui_library`;
- `sdk_or_client_library`;
- `cli_surface`;
- `parser_or_schema_surface`;
- `data_layer_surface`;
- `runtime_library`;
- `security_supply_chain_relevant`;
- `author_review_value`;
- `source_available`;
- `license_clear`;
- `multi_package_repository`;
- `single_package_reference_shape`.

`deferredBecause[]`, `rejectedBecause[]`, and `excludedSubpackages[].reason`
should use stable reason codes:

- `internal_utility`;
- `types_only_package`;
- `generated_only_package`;
- `deprecated_source`;
- `example_package`;
- `test_fixture`;
- `build_tooling`;
- `registry_search_noise`;
- `missing_public_source`;
- `missing_pinned_checkout`;
- `unclear_license`;
- `ecosystem_quota_exceeded`;
- `needs_dedicated_archetype_policy`.

Follow-up tasks may add codes, but existing codes should remain stable for
review tooling.

## Local Checkout

`localCheckout` is a requirement, not an instruction to clone:

```json
{
  "required": true,
  "path": "../checkouts/fastapi",
  "revision": "0123456789abcdef0123456789abcdef01234567",
  "allowMutableRef": false
}
```

The path is operator-managed. The plan does not authorize SpecHarvester to
clone repositories, fetch remotes, install dependencies, run package scripts,
run harvested tests, execute harvested code, or contact registries during
harvesting.

## Excluded Subpackages

`excludedSubpackages[]` records noisy package-like children that should not
become primary package candidates in the planned corpus:

```json
{
  "name": "@example/internal-test-utils",
  "reason": "test_fixture",
  "decision": "exclude",
  "notes": "Fixture package used by upstream tests, not a public package family."
}
```

Allowed decisions:

- `exclude`;
- `defer`;
- `include_as_evidence_only`.

## Expected Analyzer Coverage

`expectedAnalyzerCoverage[]` records what the operator expects before running
collection and drafting:

```json
{
  "analyzer": "js_ts_public_api",
  "scope": "exports",
  "required": true
}
```

This is review planning, not an analyzer execution result.

## Stop Conditions

`stopConditions[]` defines when a source must stop before candidate generation,
selection, handoff, or registry-facing work:

- `missing_pinned_local_checkout`;
- `source_revision_mismatch`;
- `license_evidence_missing`;
- `primary_package_family_ambiguous`;
- `expected_analyzer_unavailable`;
- `selection_rationale_missing`;
- `privacy_or_secret_risk`;
- `harvested_code_execution_required`;
- `network_discovery_required`;
- `registry_authority_required`.

## Non-Authority Statements

Every plan must include these statements:

```json
[
  "does_not_clone_or_fetch_repositories",
  "does_not_install_dependencies",
  "does_not_execute_harvested_code",
  "does_not_publish_registry_metadata",
  "does_not_accept_packages",
  "does_not_accept_relations",
  "does_not_seed_baselines",
  "does_not_remove_preview_only",
  "does_not_treat_ai_output_as_registry_truth"
]
```

## Example Fixture

The regression fixture is:

```text
tests/fixtures/corpus_plan/p35-t2-corpus-plan.example.json
```

It demonstrates a small selected/deferred/rejected multi-ecosystem corpus plan
covering JavaScript/TypeScript, Python, Rust, Go, and Swift.

The first concrete seed corpus plan is documented in
[`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md)
and represented by:

```text
tests/fixtures/multi_ecosystem_seed_corpus_plan/p35-t4-seed-corpus-plan.example.json
```

## Follow-Up Work

This contract enables:

- `P35-T3`: [`CANDIDATE_SOURCE_CLASSIFIER_PLAN.md`](CANDIDATE_SOURCE_CLASSIFIER_PLAN.md);
- `P35-T4`: first multi-ecosystem seed corpus plan
  ([`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md));
- `P35-T5`: explainable corpus selection report;
- `P35-T6`: selected corpus dry-run readiness.
