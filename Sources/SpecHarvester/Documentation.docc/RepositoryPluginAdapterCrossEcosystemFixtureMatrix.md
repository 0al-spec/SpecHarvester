# Repository Plugin Adapter Cross-Ecosystem Fixture Matrix

P40-T6 records a machine-readable
`SpecHarvesterRepositoryPluginAdapterCrossEcosystemFixtureMatrix` example for
repository plugin adapter contract scenarios across common repository shapes.

Fixture:

```text
tests/fixtures/repository_plugins/adapter_cross_ecosystem/adapter-fixture-matrix.example.json
```

## Matrix

| Case | Shape | Purpose |
| --- | --- | --- |
| `adapter.single_package.v0` | `manifest_backed_single_package` | Static parser-profile and manifest-summary adapter evidence for one root package. |
| `adapter.workspace_package_set.v0` | `workspace_or_multi_package` | Parser, manifest, and topology adapter evidence for a package-set layout. |
| `adapter.documentation_heavy.v0` | `documentation_heavy_repository` | Conservative fallback and blocked runtime-required adapters when static docs dominate. |
| `adapter.nested_package_roots.v0` | `nested_package_roots` | Nested manifest and topology evidence without naming a package manager. |
| `adapter.ambiguous_mixed_layout.v0` | `ambiguous_mixed_layout` | Rejection, fallback, and blocked decisions when root intent is ambiguous. |

## Contract Identity

The fixture declares `apiVersion:
spec-harvester.repository-plugin-adapter-fixture-matrix/v0`, `kind:
SpecHarvesterRepositoryPluginAdapterCrossEcosystemFixtureMatrix`,
`schemaVersion: 1`, and `authority:
producer_plugin_adapter_fixture_matrix_only`.

The matrix references
`tests/fixtures/repository_plugins/adapter-manifest.example.json` and
`tests/fixtures/repository_plugins/adapter-preflight-report.example.json`.

Each case records `expectedAdapterEvidence` with manifest/preflight counts,
`sidecarBoundary.appliedToDrafting: false`,
`sidecarBoundary.registryAuthority: false`,
`sidecarBoundary.adapterExecution: not_run`, and
`sidecarBoundary.adapterOutputAccepted: false`.

## Coverage

Across the matrix, fixtures cover `allowedAdapters[]`,
`rejectedAdapters[]`, `fallbackAdapters[]`, `blockedAdapters[]`,
`adapter_allowed_static_manifest`, `adapter_allowed_static_parser_profile`,
`adapter_allowed_static_topology`, `adapter_rejected_unsafe_or_ambiguous`,
`adapter_fallback_conservative_static_summary`,
`adapter_blocked_required_evidence_missing`, and
`adapter_blocked_runtime_required`.

## Non-Authority Boundary

This matrix is static producer-side review evidence. It does not load
third-party adapter code, execute adapters, clone or fetch repositories,
install dependencies, invoke package managers, execute harvested code, run AI,
accept packages, accept relations, publish registry metadata, remove
`preview_only`, or treat adapter output as registry truth.

Each case records `executedAdapterCount: 0`,
`runtimeImplementedAdapterCount: 0`, `adapterCodeLoaded: false`,
`adapterExecution: not_run`, `appliedToDrafting: false`, and
`registryAuthority: false`.

## Relationship to Adjacent Tasks

P40-T5 connects operator-supplied adapter manifest/preflight sidecars to
<doc:AutonomousCandidateBatch> as `repositoryPluginAdapterEvidence`. P40-T7
should run real local adapter-contract validation over existing pinned
checkouts while proving that adapters remain producer-side evidence only.
