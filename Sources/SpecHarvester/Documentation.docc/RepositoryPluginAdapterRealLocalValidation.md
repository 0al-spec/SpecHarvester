# Repository Plugin Adapter Real Local Validation

Status: Phase 40 real local validation.

P40-T7 records a real local adapter-contract validation over existing pinned
checkouts. It compares FastMCP, FastAPI, xyflow, and Gin with the P40-T6
adapter fixture matrix without loading or executing adapter code.

Fixture:

```text
tests/fixtures/repository_plugins/adapter_real_runs/p40-t7-real-local-adapter-contract-validation.example.json
```

## Contract Identity

The fixture declares:

```json
{
  "apiVersion": "spec-harvester.repository-plugin-adapter-real-local-validation/v0",
  "kind": "SpecHarvesterRepositoryPluginAdapterRealLocalValidation",
  "schemaVersion": 1,
  "authority": "producer_plugin_adapter_real_validation_only"
}
```

The run references the Phase 40 adapter manifest fixture, adapter preflight
fixture, and P40-T6 cross-ecosystem matrix:

```text
tests/fixtures/repository_plugins/adapter-manifest.example.json
tests/fixtures/repository_plugins/adapter-preflight-report.example.json
tests/fixtures/repository_plugins/adapter_cross_ecosystem/adapter-fixture-matrix.example.json
```

## Real Checkouts

| Repository | Revision | Matrix shape | Notes |
| --- | --- | --- | --- |
| FastMCP | `3b8538e2422a1c43fdb69661c610de7985b785f2` | `nested_package_roots` | Root and nested Python package manifests are present. |
| FastAPI | `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263` | `documentation_heavy_repository` | Root package manifest plus documentation config are present. |
| xyflow | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` | `workspace_or_multi_package` | Workspace root and member package manifests are present. |
| Gin | `5f4f9643258dc2a65e684b63f12c8d543c936c67` | `manifest_backed_single_package` | Single Go module manifest is present. |

The fixture stores `pathHint` values such as `../fastapi`, not absolute local
paths. The Git revisions are the stable review inputs; the local paths are only
operator hints for reproducing the run.

## Decisions

Each repository records:

- `allowedAdapters[]`;
- `rejectedAdapters[]`;
- `fallbackAdapters[]`;
- `blockedAdapters[]`;
- `diagnosticCodes[]`;
- `expectedAdapterEvidence`;
- `sidecarBoundary`.

The cases cover `adapter_allowed_static_manifest`,
`adapter_allowed_static_parser_profile`, `adapter_allowed_static_topology`,
`adapter_rejected_unsafe_or_ambiguous`,
`adapter_fallback_conservative_static_summary`,
`adapter_blocked_required_evidence_missing`, and
`adapter_blocked_runtime_required`.

The point is not to execute adapters. The point is to prove that real checkout
shape can be classified against adapter contract categories before any runtime
exists.

## Non-Authority Boundary

This run is producer-side review evidence only. It does not load third-party
adapter code, execute adapters, clone or fetch repositories, install
dependencies, invoke package managers, execute harvested code, run AI, accept
packages, accept relations, seed baselines, publish registry metadata, remove
`preview_only`, or treat adapter output as registry truth.

The top-level fixture and every repository case record
`adapterExecution: not_run`, `adapterCodeLoaded: false`,
`executedAdapterCount: 0`, `runtimeImplementedAdapterCount: 0`,
`appliedToDrafting: false`, and `registryAuthority: false`.

## Phase Result

P40-T7 closes Phase 40. The adapter contract now has language- and
framework-agnostic contract docs, manifest and preflight fixtures,
disabled-by-default execution policy, autonomous batch evidence handoff,
cross-ecosystem fixture matrix, and real local validation against pinned
checkouts.

The next phase should only add adapter runtime behavior if it preserves the
same explicit opt-in, path allowlist, no-network, no-package-manager, and
non-authority boundaries.
