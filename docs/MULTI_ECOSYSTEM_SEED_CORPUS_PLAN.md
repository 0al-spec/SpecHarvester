# Multi-Ecosystem Seed Corpus Plan

Status: Phase 35 seed plan.

The multi-ecosystem seed corpus plan is the first concrete
`SpecHarvesterCorpusPlan` instance for autonomous popular-library harvesting.
It applies the corpus selection policy and candidate source classifier plan to a
small reviewable source set before any collection, drafting, AI enrichment, or
SpecPM handoff runs.

The seed plan is review evidence. It is not registry authority and does not
publish registry metadata, accept packages, or accept relations into SpecPM.

## Identity

The seed fixture uses the existing corpus-plan contract:

```json
{
  "apiVersion": "spec-harvester.corpus-plan/v0",
  "kind": "SpecHarvesterCorpusPlan",
  "schemaVersion": 1,
  "authority": "producer_corpus_plan_only"
}
```

The fixture is:

```text
tests/fixtures/multi_ecosystem_seed_corpus_plan/p35-t4-seed-corpus-plan.example.json
```

It references:

- [`SPECHARVESTER_CORPUS_PLAN.md`](SPECHARVESTER_CORPUS_PLAN.md);
- [`CANDIDATE_SOURCE_CLASSIFIER_PLAN.md`](CANDIDATE_SOURCE_CLASSIFIER_PLAN.md).

## Selected Seed Sources

The first seed corpus selects five repository/package-family targets:

| Source | Ecosystem | Repository | Package family | Why selected |
| --- | --- | --- | --- | --- |
| `react` | `npm` | `https://github.com/facebook/react` | `react.workspace` | framework core, high registry usage, package-set shape |
| `fastapi` | `pypi` | `https://github.com/fastapi/fastapi` | `fastapi.core` | framework core, public API richness, author review value |
| `serde` | `crates` | `https://github.com/serde-rs/serde` | `serde.core` | dependency centrality, schema/data-layer surface |
| `gin` | `go` | `https://github.com/gin-gonic/gin` | `gin.core` | web framework archetype and public API surface |
| `swift-argument-parser` | `swift` | `https://github.com/apple/swift-argument-parser` | `swift_argument_parser.core` | Swift CLI archetype and public API surface |

This is intentionally small. It covers JavaScript/TypeScript, Python, Rust, Go,
and Swift without turning SpecHarvester into a registry-wide crawler.

## Deferred and Rejected Sources

The plan also records sources that are not selected:

| Source | Status | Reason |
| --- | --- | --- |
| `types-react` | `deferred` | type-only package requiring a dedicated archetype policy |
| `radix-ui-internal-primitives` | `deferred` | useful UI ecosystem signal, but internal/plugin package boundaries need policy |
| `react-internal-test-utils` | `rejected` | `test_fixture` and `registry_search_noise` |

Recording these decisions is part of the product behavior. A useful corpus plan
must explain what it does not harvest, not just list selected repositories.

## Classifier Expectations

Every source entry includes `classifierExpectations[]` from
`SpecHarvesterCandidateSourceClassificationPlan`.

Examples:

- `react.workspace` should classify as `package_set_root` with
  `select_primary`;
- `react-dom` should classify as `primary_package` with `select_member`;
- `@types/react` should classify as `types_only_package` with `defer`;
- examples, fixtures, tooling, and internal utilities should classify as
  `include_as_evidence_only`, `exclude`, or `defer`.

These expectations are planning constraints for later runs. They do not execute
the classifier.

## Local Checkout Requirement

Every selected source requires an operator-managed pinned local checkout:

```json
{
  "required": true,
  "path": "../checkouts/react",
  "revision": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "allowMutableRef": false,
  "revisionRequiredBeforeRun": true
}
```

The fixture revisions are review pins for the plan fixture. A real run must
replace them with actual 40-character checkout revisions and fail readiness if
the local checkout does not match.

The plan does not clone repositories, fetch remotes, install dependencies, run
package scripts, run harvested tests, execute harvested code, or contact
registries.

## Expected Analyzer Coverage

Selected sources declare expected analyzer coverage before collection:

- `workspace_inventory` and `js_ts_public_api` for the React package set;
- `python_public_api` for FastAPI;
- `rust_public_api` for Serde;
- `go_public_api` for Gin;
- `swift_public_api` for Swift Argument Parser;
- `readme_semantic_hints` for intent review where useful.

If a required analyzer is unavailable, later dry-run readiness must stop before
candidate generation.

## Stop Conditions

Selected sources include explicit stop conditions such as:

- `missing_pinned_local_checkout`;
- `source_revision_mismatch`;
- `license_evidence_missing`;
- `primary_package_family_ambiguous`;
- `expected_analyzer_unavailable`;
- `selection_rationale_missing`.

These stop conditions preserve the author-ready draft boundary: the corpus can
be prepared for a future autonomous run, but it cannot silently turn an
unverified source into a SpecPM package, remove `preview_only`, or treat AI
output as registry truth.

## Non-Authority Boundary

The seed corpus plan includes the standard non-authority statements:

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

This plan enables:

- `P35-T5`: explainable corpus selection report
  ([`EXPLAINABLE_CORPUS_SELECTION_REPORT.md`](EXPLAINABLE_CORPUS_SELECTION_REPORT.md));
- `P35-T6`: selected corpus dry-run readiness check.
