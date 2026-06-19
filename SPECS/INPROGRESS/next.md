# Next Task: Phase 40 Complete

**Status:** Complete
**Branch:** `main`
**Phase:** Phase 40. Repository Plugin Adapter Contract
**Last Archived:** P40-T7 Real Local Adapter-Contract Validation

## Recently Archived

- `P40-T7` recorded real local adapter-contract validation over existing
  pinned local checkouts.
- The GitHub-facing documentation is
  `docs/REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md`.
- The DocC mirror is
  `Sources/SpecHarvester/Documentation.docc/RepositoryPluginAdapterRealLocalValidation.md`.
- The machine-readable fixture is
  `tests/fixtures/repository_plugins/adapter_real_runs/p40-t7-real-local-adapter-contract-validation.example.json`.
- The validation covers:
  - FastMCP as `nested_package_roots`;
  - FastAPI as `documentation_heavy_repository`;
  - xyflow as `workspace_or_multi_package`;
  - Gin as `manifest_backed_single_package`.
- Every case records `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `appliedToDrafting: false`, and
  `registryAuthority: false`.
- The validation remains producer-side evidence only and does not load or
  execute third-party adapter code.

## Phase 40 Complete

Phase 40 now has:

- a language- and framework-agnostic adapter contract;
- an adapter manifest fixture;
- an adapter preflight report fixture;
- disabled-by-default execution policy;
- autonomous batch adapter evidence handoff;
- a cross-ecosystem adapter fixture matrix;
- real local adapter-contract validation.

Future adapter runtime work must preserve explicit opt-in, path allowlists,
no dependency installation, no package manager invocation, no network
discovery, no harvested code execution, no AI-by-default, and non-authority
boundaries for package, relation, baseline, registry, and `preview_only`
decisions.
