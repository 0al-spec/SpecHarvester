# P25-T3 Validation Report

**Task:** P25-T3 Package-Set and Scoped Member Candidate Drafting
**Date:** 2026-06-06
**Verdict:** PASS

## Summary

P25-T3 adds `draft-package-set`, a preview-only producer command that consumes a
deterministic `workspace-inventory.json` and writes a package-set draft summary
plus independently reviewable candidate bundles for selected package roles.

For an `xyflow`-like workspace inventory, the command drafts
`xyflow.workspace`, `xyflow.system`, `xyflow.react`, and `xyflow.svelte` without
collapsing all repository intent into one package subject. Skipped packages are
recorded with explicit reasons for later relation and bundle-set review work.

## Validation Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_package_set_drafter.py` | PASS, 3 passed |
| `PYTHONPATH=src python -m pytest tests/test_package_set_drafter.py tests/test_docs_contracts.py` | PASS, 39 passed |
| `python -m ruff check src/spec_harvester/package_set_drafter.py src/spec_harvester/cli.py tests/test_package_set_drafter.py tests/test_docs_contracts.py` | PASS |
| `python -m ruff format --check src/spec_harvester/package_set_drafter.py src/spec_harvester/cli.py tests/test_package_set_drafter.py tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |
| `PYTHONPATH=src python -m pytest` | PASS, 509 passed, 1 skipped |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 509 passed, 1 skipped, total coverage 91.24% |
| `python -m ruff check src tests` | PASS |
| `python -m ruff format --check src tests` | PASS, 86 files already formatted |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` | PASS with pre-existing DocC warnings |

## Acceptance Criteria

- `draft-package-set <workspace-inventory.json> --out <dir>` writes a
  deterministic `package-set-draft.json` summary.
- The summary has stable identity fields:
  `apiVersion: spec-harvester.package-set-draft/v0` and
  `kind: SpecHarvesterPackageSetDraft`.
- The command creates separate candidate bundle directories for the aggregate
  workspace package and selected scoped member packages.
- For an `xyflow`-like fixture, generated package IDs include
  `xyflow.workspace`, `xyflow.system`, `xyflow.react`, and `xyflow.svelte`.
- Generated candidate manifests remain `preview_only`.
- Each generated candidate passes existing producer-side candidate bundle
  preflight.
- Skipped inventory packages are recorded in `skipped[]` with explicit reasons.
- Relation proposals remain absent until P25-T4.
- Existing single-package `draft` behavior remains unchanged.

## Residual Notes

DocC generation still reports unrelated pre-existing warnings around
`AcceptedPackageUpdateProposals` and inline command text references in
quality-report documentation. The new package-set drafting documentation builds
and is covered by docs contract tests.
