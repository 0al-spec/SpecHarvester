# Repository Plugin Registry Fixture

`SpecHarvesterRepositoryPluginRegistry` is the machine-readable fixture shape
for declaring producer-side repository plugin contracts. It does not load
plugins, execute plugins, or grant registry authority.

Fixture path:

```text
tests/fixtures/repository_plugins/generic-registry.example.json
```

## Identity

```json
{
  "apiVersion": "spec-harvester.repository-plugins/v0",
  "kind": "SpecHarvesterRepositoryPluginRegistry",
  "schemaVersion": 1,
  "authority": "producer_plugin_registry_only"
}
```

```text
registry record = declared producer-side plugin contract
registry record != executable plugin
registry record != accepted SpecPM package truth
```

A registry record is not executable plugin code and is not accepted SpecPM
package truth.

## Fields

The fixture declares `contract`, `roles[]`, `inputEvidenceKinds[]`,
`outputArtifactKinds[]`, `plugins[]`, `nonAuthorityStatements[]`, and
`followUp`.

Each plugin record declares `pluginId`, `version`, `role`, `authority`, `title`,
`summary`, `inputEvidenceKinds[]`, `outputArtifactKinds[]`, `safetyConstraints`,
`applicabilitySignals[]`, `conflictsWith[]`, `fallbackBehavior`,
`diagnostics[]`, and `nonAuthorityStatements[]`.

The P38-T2 fixture includes generic examples for `parser_profile`,
`repository_profile`, `evidence_producer`, `topology_helper`, and
`review_surface`.

Python, JavaScript, FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven, Gradle,
and other ecosystems are examples only, not normative plugin rules.

Each plugin record uses `authority: producer_side_evidence_only`, while the
top-level registry record uses `authority: producer_plugin_registry_only`.
This separates declared registry-record authority from the authority carried by
plugin output evidence.

## Static Evidence

Registry records can reference static evidence kinds such as
`source_manifest`, `harvest_snapshot`, `workspace_inventory`,
`public_interface_index`, `repository_profile_detection`,
`repository_parsing_profile_decision`, and `operator_label`.

Registry records must not require network discovery, package registry queries,
dependency installation, package manager execution, build outputs, imported
package execution, or live AI calls.

## Safety Constraints

Every plugin declaration must state:

```json
{
  "execution": "none",
  "networkAccess": "none",
  "packageManagers": "not_invoked",
  "dependencies": "not_installed",
  "harvestedCode": "not_executed",
  "ai": "not_invoked"
}
```

## Non-Authority Boundary

The registry fixture does not load third-party plugin code.

The registry fixture does not load third-party plugin code, execute plugins,
clone or fetch repositories, install dependencies, execute harvested code,
invoke package managers, run AI, accept packages, accept relations, publish
registry metadata, seed baselines, remove `preview_only`, treat plugin output
as registry truth, or treat AI output as registry truth.

## Follow-Ups

- `P38-T3`: add `SpecHarvesterRepositoryPluginApplicabilityReport` in
  <doc:RepositoryPluginApplicabilityReportFixture> and
  `tests/fixtures/repository_plugins/generic-applicability-report.example.json`.
- `P38-T4`: connect registry/applicability evidence to autonomous candidate
  batch as sidecar producer evidence.
- `P38-T5`: add cross-ecosystem plugin subsystem fixtures.
- `P38-T6`: run one real repository through the plugin evidence path.
