# Repository Plugin Applicability Report Fixture

`SpecHarvesterRepositoryPluginApplicabilityReport` is the machine-readable
fixture shape for deterministic repository plugin applicability decisions. It
consumes the P38-T2 `SpecHarvesterRepositoryPluginRegistry` fixture as declared
plugin contract input and static local evidence as decision input.

Fixture path:

```text
tests/fixtures/repository_plugins/generic-applicability-report.example.json
```

## Identity

```json
{
  "apiVersion": "spec-harvester.repository-plugin-applicability/v0",
  "kind": "SpecHarvesterRepositoryPluginApplicabilityReport",
  "schemaVersion": 1,
  "authority": "producer_plugin_applicability_only"
}
```

```text
applicability report = producer-side decision evidence
applicability report != plugin execution
applicability report != accepted package truth
```

## Inputs

The report references the P38-T2 `SpecHarvesterRepositoryPluginRegistry`
fixture at `tests/fixtures/repository_plugins/generic-registry.example.json`,
source manifest metadata, static local evidence paths, and static evidence
kinds such as `source_manifest`, `harvest_snapshot`, `workspace_inventory`,
`repository_profile_detection`, `repository_parsing_profile_decision`, and
`operator_label`.

The report must not depend on network discovery, package registry queries,
dependency installation, package manager execution, imported package
execution, build outputs, or live AI calls.

## Decision Sets

The fixture records `selectedPlugins[]`, `rejectedPlugins[]`,
`fallbackPlugins[]`, `blockedPlugins[]`, `diagnostics[]`, and
`nonAuthorityStatements[]`.

Each decision includes `pluginId`, `role`, `decision`, `decisionAuthority`,
`pluginOutputAuthority`, `confidence`, `reasonCodes[]`, `evidencePaths[]`, and
`outputArtifactKinds[]`.

`decisionAuthority` is always `producer_plugin_applicability_only`.
`pluginOutputAuthority` is always `producer_side_evidence_only`.

The P38-T3 fixture intentionally includes selected, rejected, fallback, and
blocked decisions so later code can test all four result categories.
`spec_harvester.generic.package_topology.v0` is blocked in this fixture because
its declared `manifest_summary` input evidence is unavailable; applicability
reports must not select plugins when required declared inputs are missing.

## Diagnostics

Diagnostics are machine-readable review evidence. The fixture uses stable
codes such as `plugin_selected`, `plugin_fallback`,
`plugin_rejected_low_confidence`, and
`plugin_blocked_required_evidence_missing`.

Diagnostics explain which plugin caused the finding and which static evidence
paths informed the decision.

## Non-Authority Boundary

The applicability report fixture does not load third-party plugin code,
execute plugins, run plugin code, clone or fetch repositories, install
dependencies, execute harvested code, invoke package managers, run AI, change
parser profile behavior, change repository profile scoring, accept packages,
accept relations, publish registry metadata, seed baselines, remove
`preview_only`, treat plugin decisions as registry truth, or treat AI output as
registry truth.

## Follow-Ups

- `P38-T4`: connect plugin registry and applicability output to autonomous
  candidate batch as sidecar producer evidence.
- `P38-T5`: add <doc:RepositoryPluginCrossEcosystemFixtures> as static
  cross-ecosystem applicability examples.
- `P38-T6`: run one real repository through the plugin evidence path.
