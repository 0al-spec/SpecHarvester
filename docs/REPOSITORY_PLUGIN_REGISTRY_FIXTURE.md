# Repository Plugin Registry Fixture

Status: Phase 38 fixture contract.

`SpecHarvesterRepositoryPluginRegistry` is the machine-readable fixture shape
for declaring producer-side repository plugin contracts. It does not load
plugins, execute plugins, or grant registry authority.

Fixture path:

```text
tests/fixtures/repository_plugins/generic-registry.example.json
```

## Identity

The fixture identity is:

```json
{
  "apiVersion": "spec-harvester.repository-plugins/v0",
  "kind": "SpecHarvesterRepositoryPluginRegistry",
  "schemaVersion": 1,
  "authority": "producer_plugin_registry_only"
}
```

The registry authority means:

```text
registry record = declared producer-side plugin contract
registry record != executable plugin
registry record != accepted SpecPM package truth
```

A registry record is not executable plugin code and is not accepted SpecPM
package truth.

## Required Top-Level Fields

| Field | Purpose |
| --- | --- |
| `contract` | Describes fixture purpose, input authority, output authority, and selection authority. |
| `roles[]` | Enumerates supported plugin roles such as `parser_profile`, `repository_profile`, `evidence_producer`, `topology_helper`, and `review_surface`. |
| `inputEvidenceKinds[]` | Declares allowed static input evidence categories. |
| `outputArtifactKinds[]` | Declares bounded output artifact categories. |
| `plugins[]` | Lists versioned plugin declarations. |
| `nonAuthorityStatements[]` | Records trust and safety boundaries for the whole registry. |
| `followUp` | Points to later Flow tasks for applicability reports, batch integration, fixtures, and real runs. |

## Plugin Records

Every `plugins[]` item must declare:

- `pluginId`;
- `version`;
- `role`;
- `authority`;
- `title`;
- `summary`;
- `inputEvidenceKinds[]`;
- `outputArtifactKinds[]`;
- `safetyConstraints`;
- `applicabilitySignals[]`;
- `conflictsWith[]`;
- `fallbackBehavior`;
- `diagnostics[]`;
- `nonAuthorityStatements[]`.

The P38-T2 fixture includes generic examples for:

- `parser_profile`;
- `repository_profile`;
- `evidence_producer`;
- `topology_helper`;
- `review_surface`.

These examples are language- and framework-agnostic. Ecosystem names may appear
as future evidence sources or validation examples, but Python, JavaScript,
FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven, Gradle, and other ecosystems
are not normative plugin rules.

Each plugin record uses `authority: producer_side_evidence_only`, while the
top-level registry record uses `authority: producer_plugin_registry_only`.
This separates declared registry-record authority from the authority carried by
plugin output evidence.

## Static Evidence Boundary

Registry records can reference static evidence kinds such as:

- `source_manifest`;
- `harvest_snapshot`;
- `workspace_inventory`;
- `public_interface_index`;
- `repository_profile_detection`;
- `repository_parsing_profile_decision`;
- `operator_label`.

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

The registry fixture states that it does not:

- load third-party plugin code;
- execute plugins;
- clone or fetch repositories;
- install dependencies;
- execute harvested code;
- invoke package managers;
- run AI;
- accept packages;
- accept relations;
- publish registry metadata;
- seed baselines;
- remove `preview_only`;
- treat plugin output as registry truth;
- treat AI output as registry truth.

## Relationship to Later Tasks

- `P38-T3` adds `SpecHarvesterRepositoryPluginApplicabilityReport` in
  [`REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md`](REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md)
  and
  `tests/fixtures/repository_plugins/generic-applicability-report.example.json`.
- `P38-T4` should connect registry/applicability evidence to autonomous
  candidate batch as sidecar producer evidence.
- `P38-T5` should add cross-ecosystem plugin subsystem fixtures.
- `P38-T6` should run one real repository through the plugin evidence path.
