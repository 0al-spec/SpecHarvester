# P25-T2 Validation Report

**Task:** P25-T2 Deterministic Workspace Inventory
**Date:** 2026-06-06
**Verdict:** PASS

## Summary

P25-T2 adds an opt-in deterministic workspace inventory artifact for
`collect-batch`. The implementation writes `workspace-inventory.json` beside
`harvest.json` when `--emit-workspace-inventory` is passed.

The artifact records repository URL, exact revision, workspace manifests,
workspace include/exclude patterns, package manifest paths, package metadata,
source target paths, proposed SpecPM package IDs, package roles, privacy-safe
digest evidence, and producer authority boundaries.

## Validation Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_batch_collection.py` | PASS, 30 passed |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py` | PASS, 35 passed |
| `python -m ruff check src/spec_harvester/workspace_inventory.py src/spec_harvester/batch_collection.py src/spec_harvester/cli.py tests/test_batch_collection.py tests/test_docs_contracts.py` | PASS |
| `python -m ruff format --check src/spec_harvester/workspace_inventory.py src/spec_harvester/batch_collection.py src/spec_harvester/cli.py tests/test_batch_collection.py tests/test_docs_contracts.py` | PASS |
| `PYTHONPATH=src python -m pytest` | PASS, 504 passed, 1 skipped |
| `python -m ruff check src tests` | PASS |
| `python -m ruff format --check src tests` | PASS |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing` | PASS, 504 passed, 1 skipped, total coverage 91% |
| `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` | PASS with pre-existing DocC warnings |

## Acceptance Criteria

- `collect-batch --emit-workspace-inventory` writes
  `workspace-inventory.json` per collected repository.
- The artifact has stable identity fields: `apiVersion`,
  `kind: SpecHarvesterWorkspaceInventory`, and `schemaVersion: 1`.
- The artifact records repository URL and exact revision.
- Source manifests with `revision` use `source_manifest_revision`; source
  manifests with `ref` resolve the checkout `git rev-parse HEAD`.
- Workspace manifests include observed include and exclude patterns where
  supported.
- Package records include manifest path, ecosystem, package manager, name,
  version, source target path, proposed SpecPM package ID, role, and digest
  evidence.
- Repeated runs over the same fixture produce identical rendered JSON bytes.
- Existing `collect-batch` behavior remains unchanged unless
  `--emit-workspace-inventory` is set.
- Package-set candidate drafting remains out of scope for P25-T2.

## Residual Notes

DocC generation still reports unrelated pre-existing warnings around
`AcceptedPackageUpdateProposals` and command text references in quality-report
documentation. The new `WorkspaceInventory` page resolves and builds.
