# P40-T7 Validation Report

## Summary

P40-T7 implementation passed local validation.

## Validated Behavior

- Added a machine-readable
  `SpecHarvesterRepositoryPluginAdapterRealLocalValidation` fixture.
- The fixture records four existing pinned local checkouts:
  - FastMCP at `3b8538e2422a1c43fdb69661c610de7985b785f2`;
  - FastAPI at `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263`;
  - xyflow at `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`;
  - Gin at `5f4f9643258dc2a65e684b63f12c8d543c936c67`.
- The fixture maps real evidence to P40-T6 matrix shapes:
  `nested_package_roots`, `documentation_heavy_repository`,
  `workspace_or_multi_package`, and `manifest_backed_single_package`.
- Each case records allowed, rejected, fallback, or blocked adapter decisions
  plus diagnostic codes.
- Each case records `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `appliedToDrafting: false`, and
  `registryAuthority: false`.
- The task does not implement adapter loading or execution.
- The task does not clone/fetch repositories, install dependencies, invoke
  package managers, execute harvested code, run AI, accept packages, accept
  relations, seed baselines, publish registry metadata, or remove
  `preview_only`.

## Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
```

Result: `122 passed`

```bash
PYTHONPATH=src pytest -q
```

Result: `793 passed, 1 skipped`

```bash
PYTHONPATH=src ruff check .
```

Result: passed

```bash
PYTHONPATH=src ruff format --check src tests
```

Result: `123 files already formatted`

```bash
git diff --check
```

Result: passed

```bash
swift build --target SpecHarvesterDocs
```

Result: passed
