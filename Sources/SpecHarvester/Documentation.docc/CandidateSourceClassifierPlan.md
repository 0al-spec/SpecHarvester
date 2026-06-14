# Candidate Source Classifier Plan

The candidate source classifier plan defines how SpecHarvester should classify
package-like source units before drafting.

It complements <doc:SpecHarvesterCorpusPlan>: the corpus plan chooses
repositories and package families, while the classifier plan explains which
source units may become candidates, which are deferred, which are excluded, and
which remain evidence-only.

This is a producer review artifact. It is not a classifier implementation and
does not accept packages into SpecPM.

## Identity

```json
{
  "apiVersion": "spec-harvester.source-classification-plan/v0",
  "kind": "SpecHarvesterCandidateSourceClassificationPlan",
  "schemaVersion": 1,
  "authority": "producer_classification_plan_only"
}
```

## Source Classes

The plan defines these source classes:

- `package_set_root`;
- `primary_package`;
- `plugin_package`;
- `example_package`;
- `tooling_package`;
- `types_only_package`;
- `generated_artifact`;
- `internal_utility`;
- `deprecated_source`;
- `evidence_only`.

## Actions

Allowed actions are `select_primary`, `select_member`, `defer`, `exclude`, and
`include_as_evidence_only`.

Only `package_set_root` and `primary_package` are primary by default.
`plugin_package` requires explicit plugin coverage. `example_package`,
`tooling_package`, `types_only_package`, `generated_artifact`,
`internal_utility`, `deprecated_source`, and `evidence_only` must remain
deferred, excluded, or evidence-only unless a later policy explicitly changes
that boundary.

## Inputs

The classifier should use local, reviewable inputs:

- `SpecHarvesterCorpusPlan` source entries;
- repository source manifests;
- workspace inventory;
- package manifests;
- static evidence paths;
- explicit operator overrides.

## Output Shape

Each decision records `sourceId`, `unitId`, `class`, `action`, `reasonCodes`,
`evidencePaths`, `confidence`, and `stopConditions`.

Allowed confidence values are `high`, `medium`, `low`, and `blocked`.

## Stop Conditions

Classification stops before candidate generation when package family identity
is ambiguous, network discovery is required, harvested code execution is
required, generated provenance is missing, plugin host policy is missing,
deprecated package rationale is missing, selected primary license evidence is
missing, or operator override evidence is missing.

## Non-Authority Boundary

The classifier plan does not clone or fetch repositories, install
dependencies, execute harvested code, publish registry metadata, accept
packages, accept relations, seed baselines, remove `preview_only`, or treat AI
output as registry truth.

In short: it does not clone repositories, install dependencies, execute
harvested code, publish registry metadata, accept packages, accept relations,
remove `preview_only`, or treat classifier output as registry truth.

## Fixture

The example fixture is
`tests/fixtures/source_classifier_plan/p35-t3-source-classifier-plan.example.json`.

## Follow-Up Work

This plan enables `P35-T4` <doc:MultiEcosystemSeedCorpusPlan>, `P35-T5`
explainable corpus selection reports, and `P35-T6` selected corpus dry-run
readiness.
