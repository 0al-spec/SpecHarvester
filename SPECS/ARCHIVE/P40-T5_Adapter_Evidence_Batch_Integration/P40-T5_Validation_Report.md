# P40-T5 Validation Report

## Summary

P40-T5 implementation passed local validation.

## Validated Behavior

- `autonomous-candidate-batch` keeps existing behavior when adapter evidence is
  not supplied.
- Adapter manifest and adapter preflight inputs are opt-in.
- Supplying only one adapter evidence input fails before report generation.
- Supplying both inputs records `repositoryPluginAdapterEvidence` in the batch
  report.
- The copied adapter manifest and preflight sidecars are written under
  `reports/repository-plugin-adapter-evidence/`.
- Batch output records source paths, copied paths, SHA-256 digests, adapter
  counts, allowed/rejected/fallback/blocked counts, diagnostic codes,
  `appliedToDrafting: false`, `registryAuthority: false`, and
  `adapterExecution: not_run`.
- Preflight `manifest.digest` must match the supplied manifest digest.
- The integration does not load adapters, execute adapters, install
  dependencies, invoke package managers, run AI, publish registry metadata,
  accept packages, accept relations, or remove `preview_only`.

## Commands

```bash
PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q
```

Result: `27 passed`

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
```

Result: `120 passed`

```bash
PYTHONPATH=src pytest -q
```

Result: `791 passed, 1 skipped`

```bash
PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q
```

Result: `791 passed, 1 skipped`, total coverage `91%`

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
