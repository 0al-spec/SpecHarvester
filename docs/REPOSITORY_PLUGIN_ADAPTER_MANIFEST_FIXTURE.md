# Repository Plugin Adapter Manifest Fixture

Status: Phase 40 fixture contract.

`SpecHarvesterRepositoryPluginAdapterManifest` is the machine-readable fixture
shape for declaring future repository plugin adapters before any adapter
preflight or execution path exists.

Fixture path:

```text
tests/fixtures/repository_plugins/adapter-manifest.example.json
```

## Identity

```json
{
  "apiVersion": "spec-harvester.repository-plugin-adapter/v0",
  "kind": "SpecHarvesterRepositoryPluginAdapterManifest",
  "schemaVersion": 1,
  "authority": "producer_plugin_adapter_manifest_only"
}
```

The manifest authority means:

```text
adapter manifest = declared producer-side adapter contract
adapter manifest != adapter preflight
adapter manifest != adapter execution permission
adapter manifest != accepted SpecPM package truth
adapter manifest != registry authority
```

## Relationship to Static Evidence

The fixture references the existing static evidence envelope and generic
plugin registry fixtures:

```text
tests/fixtures/repository_plugins/static-evidence-envelope.example.json
tests/fixtures/repository_plugins/generic-registry.example.json
```

Those references are declared input artifacts. They do not grant permission to
load adapter code or run adapters.

## Required Top-Level Fields

| Field | Purpose |
| --- | --- |
| `contract` | Describes purpose, contract version, input authority, output authority, preflight authority, and default execution state. |
| `pathPolicy` | Defines safe path requirements for declared artifact paths. |
| `declaredInputArtifacts[]` | Lists static input artifacts with path, digest, authority, and required status. |
| `supportedRoles[]` | Enumerates adapter roles such as `parser_profile`, `repository_profile`, `evidence_producer`, `topology_helper`, and `review_surface`. |
| `inputEvidenceKinds[]` | Declares static evidence kinds adapters may request. |
| `outputArtifactKinds[]` | Declares review-only adapter output categories. |
| `adapters[]` | Lists versioned adapter declarations. |
| `sidecarBoundary` | Records `appliedToDrafting`, `registryAuthority`, preflight, and execution status. |
| `summary` | Counts adapter declarations, roles, input artifacts, output kinds, and disabled runtime state. |
| `nonAuthorityStatements[]` | Records trust and safety boundaries for the manifest. |
| `followUp` | Points to later Flow tasks for preflight, execution policy, batch integration, fixture matrix, and real validation. |

The fixture records `preflightAuthority:
producer_plugin_adapter_preflight_only` for the future P40-T3 preflight report
without claiming that preflight has run.

## Adapter Records

Each `adapters[]` item declares:

- `adapterId`;
- `contractVersion`;
- `adapterVersion`;
- `roles[]`;
- `title`;
- `summary`;
- `authority`;
- `inputEvidence.requiredKinds[]`;
- `inputEvidence.optionalKinds[]`;
- `outputs[]`;
- `execution`;
- `sandboxRequirements`;
- `capabilityRequests`;
- `diagnostics[]`;
- `nonAuthorityStatements[]`.

The P40-T2 fixture includes generic examples for:

- `spec_harvester.adapters.generic.parser_profile_summary.v0`;
- `spec_harvester.adapters.generic.manifest_summary.v0`;
- `spec_harvester.adapters.generic.package_topology_hint.v0`.

These examples are language- and framework-agnostic. Ecosystem names can
appear in future validation cases, but Python, JavaScript, FastAPI, FastMCP,
npm, Cargo, Go, SwiftPM, Maven, Gradle, and other ecosystems are not normative
adapter rules.

## Execution Boundary

Every example adapter uses:

```json
{
  "mode": "static_only",
  "defaultEnabled": false,
  "requiresOperatorOptIn": true,
  "adapterCodeLoaded": false,
  "runtimeImplemented": false
}
```

In prose, the required execution labels are `mode: static_only`,
`defaultEnabled: false`, `requiresOperatorOptIn: true`,
`adapterCodeLoaded: false`, and `runtimeImplemented: false`.

The fixture is a declaration. It does not implement adapter preflight, load
third-party adapter code, execute adapters, or grant execution authority.

## Sandbox and Capability Requests

Every adapter record must declare sandbox requirements:

- `readPathPolicy`;
- `writePathPolicy`;
- `networkAccess`;
- `dependencyInstallation`;
- `packageManagers`;
- `harvestedCodeExecution`;
- `processExecution`;
- `environmentAccess`;
- `timeoutMs`;
- `maxOutputBytes`.

Every adapter record must also declare capability requests for filesystem
reads, filesystem writes, network, process, and AI. The P40-T2 fixture only
requests reads of declared input artifacts and requests no writes, network,
process, or AI capabilities.

## Output Boundary

Declared outputs use `authority: producer_adapter_output_only` and are review
evidence only. The fixture declares:

- `adapter_parser_profile_summary`;
- `adapter_manifest_summary`;
- `adapter_topology_hint`;
- `adapter_review_panel_data`;
- `adapter_diagnostics`.

No adapter output category is accepted package truth, accepted relation truth,
registry metadata, baseline authority, or permission to remove `preview_only`.

## Non-Authority Boundary

The adapter manifest fixture does not implement adapter preflight, load
third-party adapter code, execute adapters, clone or fetch repositories,
install dependencies, invoke package managers, execute harvested code, run AI,
change static plugin applicability evaluation, change autonomous batch
behavior, accept packages, accept relations, seed baselines, publish registry
metadata, remove `preview_only`, treat adapter output as registry truth, or
treat AI output as registry truth.

## Relationship to Later Tasks

- `P40-T3` adds
  [`SpecHarvesterRepositoryPluginAdapterPreflightReport`](REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md).
- `P40-T4` defines
  [adapter execution policy](REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md).
- `P40-T5` connects adapter evidence to autonomous candidate batch.
- `P40-T6` records
  [`REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md`](REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md)
  as cross-ecosystem adapter contract fixtures.
- `P40-T7` records real local adapter-contract validation in
  [`REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md`](REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md).
