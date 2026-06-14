# Candidate Source Classifier Plan

Status: Phase 35 planning contract.

The candidate source classifier plan defines how SpecHarvester should classify
package-like source units before drafting. It complements
[`SPECHARVESTER_CORPUS_PLAN.md`](SPECHARVESTER_CORPUS_PLAN.md): the corpus plan
chooses repositories and package families, while the classifier plan explains
which source units inside those repositories may become candidates, which are
deferred, which are excluded, and which remain evidence-only.

This is a producer review artifact. It is not a classifier implementation and
does not accept packages into SpecPM.

## Identity

The planned machine-readable classification report shape is:

```json
{
  "apiVersion": "spec-harvester.source-classification-plan/v0",
  "kind": "SpecHarvesterCandidateSourceClassificationPlan",
  "schemaVersion": 1,
  "authority": "producer_classification_plan_only"
}
```

## Source Classes

| Class | Meaning | Default action |
| --- | --- | --- |
| `package_set_root` | Repository or workspace root representing an aggregate package family. | `select_primary` |
| `primary_package` | User-facing library package that can become a SpecPM candidate. | `select_primary` or `select_member` |
| `plugin_package` | Extension package that depends on a host library or framework. | `defer` unless the corpus plan explicitly selects plugin coverage |
| `example_package` | Demo or sample package. | `exclude` or `include_as_evidence_only` |
| `tooling_package` | Build, lint, test, codegen, or repository-maintenance tooling. | `defer` or `include_as_evidence_only` |
| `types_only_package` | Type definitions or type-only facade without runtime behavior. | `defer` |
| `generated_artifact` | Generated package, checked-in output, fixture bundle, or generated API surface. | `defer` until provenance is clear |
| `internal_utility` | Package-like internal helper not intended as public package family. | `exclude` or `include_as_evidence_only` |
| `deprecated_source` | Deprecated package or package family. | `defer` or `exclude` |
| `evidence_only` | Source unit useful as evidence but not a package candidate. | `include_as_evidence_only` |

## Actions

Allowed classification actions:

- `select_primary`: may become the root or single primary candidate;
- `select_member`: may become a member candidate under a package-set root;
- `defer`: needs a later task, archetype policy, or human decision;
- `exclude`: should not enter candidate generation;
- `include_as_evidence_only`: may support another candidate but must not become
  its own package candidate.

## Inputs

The classifier should use only local, reviewable inputs:

- `SpecHarvesterCorpusPlan` source entries;
- repository source manifests;
- workspace inventory;
- package manifests;
- static evidence paths;
- explicit operator overrides.

It must not clone repositories, fetch remotes, install dependencies, run
package scripts, run harvested tests, execute harvested code, or contact
registries during classification.

## Output Shape

Each classification decision should record:

```json
{
  "sourceId": "react",
  "unitId": "react.workspace",
  "class": "package_set_root",
  "action": "select_primary",
  "reasonCodes": ["workspace_root", "public_package_family"],
  "evidencePaths": ["workspace-inventory.json", "package.json"],
  "confidence": "high",
  "stopConditions": []
}
```

Allowed confidence values:

- `high`;
- `medium`;
- `low`;
- `blocked`.

## Reason Codes

Selection reason codes:

- `workspace_root`;
- `public_package_family`;
- `package_manifest_public`;
- `export_surface_present`;
- `documented_user_facing_api`;
- `corpus_plan_selected`;
- `operator_override_selected`.

Deferral or exclusion reason codes:

- `internal_utility`;
- `example_package`;
- `test_fixture`;
- `tooling_package`;
- `types_only_package`;
- `generated_artifact`;
- `deprecated_source`;
- `package_family_ambiguous`;
- `host_plugin_policy_missing`;
- `generated_provenance_missing`;
- `license_evidence_missing`;
- `operator_override_deferred`;
- `operator_override_excluded`.

## Operator Overrides

Operator overrides are allowed only as explicit review evidence. They should
record:

- operator-provided decision;
- reason;
- evidence path or note;
- whether the override is temporary;
- whether the source must be revisited before SpecPM handoff.

Overrides do not accept packages, accept relations, publish registry metadata,
or remove `preview_only`.

## Stop Conditions

Classification must stop before candidate generation when:

- package family identity is ambiguous;
- a source requires network discovery;
- a source requires harvested code execution;
- a generated artifact lacks provenance;
- a plugin requires a missing host package policy;
- a deprecated package lacks explicit review rationale;
- license evidence is missing for a selected primary package;
- operator override evidence is missing.

## Non-Authority Boundary

The classifier plan does not:

- clone or fetch repositories;
- install dependencies;
- execute harvested code;
- publish registry metadata;
- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- treat AI output as registry truth.

In short: it does not clone repositories, install dependencies, execute
harvested code, publish registry metadata, accept packages, accept relations,
remove `preview_only`, or treat classifier output as registry truth.

## Example Fixture

The regression fixture is:

```text
tests/fixtures/source_classifier_plan/p35-t3-source-classifier-plan.example.json
```

It demonstrates primary, member, plugin, example, tooling, type-only, generated,
internal, deprecated, and evidence-only classification decisions.

## Follow-Up Work

This plan enables:

- `P35-T4`: first multi-ecosystem seed corpus plan;
- `P35-T5`: explainable corpus selection report;
- `P35-T6`: selected corpus dry-run readiness.
