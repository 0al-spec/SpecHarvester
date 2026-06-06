# P25-T4 Validation Report

**Task:** P25-T4 Package Relation Proposal Output
**Date:** 2026-06-06
**Verdict:** PASS

## Summary

P25-T4 adds deterministic package relation proposal output to
`draft-package-set`. The command now writes `package-relation-proposals.json`
beside `package-set-draft.json`, starting with producer-observed `contains`
relations from aggregate workspace candidates to selected scoped member
candidates.

For an `xyflow`-like workspace inventory, the output proposes:

- `xyflow.workspace contains xyflow.system`
- `xyflow.workspace contains xyflow.react`
- `xyflow.workspace contains xyflow.svelte`

The relation artifact references `workspace-inventory.json` and
`package-set-draft.json` with digests, records workspace/package manifest
evidence, and remains review evidence rather than accepted registry metadata.

## Validation Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_package_set_drafter.py` | PASS, 4 passed |
| `PYTHONPATH=src python -m pytest tests/test_package_set_drafter.py tests/test_docs_contracts.py` | PASS, 41 passed |
| `python -m ruff check src/spec_harvester/package_set_drafter.py tests/test_package_set_drafter.py tests/test_docs_contracts.py` | PASS |
| `python -m ruff format --check src/spec_harvester/package_set_drafter.py tests/test_package_set_drafter.py tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |
| `PYTHONPATH=src python -m pytest` | PASS, 511 passed, 1 skipped |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 511 passed, 1 skipped, total coverage 91.18% |
| `python -m ruff check src tests` | PASS |
| `python -m ruff format --check src tests` | PASS, 86 files already formatted |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` | PASS with pre-existing DocC warnings |

## Acceptance Criteria

- `draft-package-set <workspace-inventory.json> --out <dir>` writes
  `package-relation-proposals.json` beside `package-set-draft.json`.
- The relation artifact has stable identity fields:
  `apiVersion: spec-harvester.package-relation-proposals/v0` and
  `kind: SpecHarvesterPackageRelationProposals`.
- For an `xyflow`-like fixture, generated relations include
  `xyflow.workspace contains xyflow.system`,
  `xyflow.workspace contains xyflow.react`, and
  `xyflow.workspace contains xyflow.svelte`.
- Each relation has `reviewStatus: producer_observed`.
- Evidence includes workspace manifests and source/target package manifest
  paths with digest records where present.
- Relation source and target package IDs match generated candidate subjects.
- Relation output remains producer review evidence, not accepted registry
  metadata.

## Residual Notes

DocC generation still reports unrelated pre-existing warnings around
`AcceptedPackageUpdateProposals` and inline command text references in
quality-report documentation. The new `PackageRelationProposals` DocC page
builds and is covered by docs contract tests.
