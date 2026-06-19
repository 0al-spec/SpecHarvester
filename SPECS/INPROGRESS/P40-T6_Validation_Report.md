# P40-T6 Validation Report

## Summary

P40-T6 implementation passed local validation.

## Validated Behavior

- Added a machine-readable
  `SpecHarvesterRepositoryPluginAdapterCrossEcosystemFixtureMatrix` fixture.
- The fixture covers exactly five repository shapes:
  - `manifest_backed_single_package`;
  - `workspace_or_multi_package`;
  - `documentation_heavy_repository`;
  - `nested_package_roots`;
  - `ambiguous_mixed_layout`.
- The fixture references the P40-T2 adapter manifest fixture and P40-T3
  adapter preflight report fixture with SHA-256 digests.
- Each case records expected manifest/preflight evidence, static evidence
  paths, allowed/rejected/fallback/blocked adapter decisions, counts,
  diagnostics, and non-authority statements.
- Each case records `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `appliedToDrafting: false`, and
  `registryAuthority: false`.
- The task does not implement adapter loading or execution.
- The task does not clone/fetch repositories, install dependencies, invoke
  package managers, execute harvested code, run AI, accept packages, accept
  relations, publish registry metadata, or remove `preview_only`.

## Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
```

Result: `121 passed`

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
PYTHONPATH=src pytest -q
```

Result: `792 passed, 1 skipped`

```bash
PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q
```

Result: `792 passed, 1 skipped`, total coverage `91%`

```bash
swift build --target SpecHarvesterDocs
```

Result: passed
