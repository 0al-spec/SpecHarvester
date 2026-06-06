# P25-T5 Validation Report

**Task:** P25-T5 Bundle-Set Preflight
**Date:** 2026-06-06
**Verdict:** PASS

## Summary

P25-T5 adds producer-side bundle-set preflight for generated package-set output.
The new `preflight-bundle-set` command verifies `package-set-draft.json`,
`package-relation-proposals.json`, candidate bundle directories, relation
endpoints, digest references, and producer review boundaries as one
multi-package review unit.

The verifier reuses ordinary candidate bundle preflight for each member bundle.
It fails on duplicate candidate package IDs, missing candidate directories,
non-passing candidate preflight reports, dangling relation endpoints, mismatched
package-set draft digests, workspace inventory input mismatches, and invalid
candidate diagnostics status or producer review boundaries.

## Validation Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_package_set_drafter.py` | PASS, 14 passed |
| `PYTHONPATH=src python -m pytest tests/test_package_set_drafter.py tests/test_docs_contracts.py` | PASS, 51 passed |
| `python -m ruff check src/spec_harvester/bundle_set_preflight.py src/spec_harvester/cli.py tests/test_package_set_drafter.py tests/test_docs_contracts.py` | PASS |
| `python -m ruff format --check src/spec_harvester/bundle_set_preflight.py src/spec_harvester/cli.py tests/test_package_set_drafter.py tests/test_docs_contracts.py` | PASS |
| `PYTHONPATH=src python -m pytest` | PASS, 524 passed, 1 skipped |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 524 passed, 1 skipped, total coverage 90.82% |
| `python -m ruff check src tests` | PASS |
| `python -m ruff format --check src tests` | PASS, 87 files already formatted |
| `git diff --check` | PASS |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` | PASS with pre-existing DocC warnings |

## Acceptance Criteria

- `python -m spec_harvester preflight-bundle-set <package-set-dir>` prints a
  deterministic JSON report.
- The report has stable identity:
  `apiVersion: spec-harvester.bundle-set-preflight/v0` and
  `kind: SpecHarvesterBundleSetPreflightReport`.
- A generated `xyflow`-like package set passes bundle-set preflight.
- Missing candidate bundles, duplicate package IDs, dangling relations, digest
  mismatches, and non-passing candidate preflight reports fail the bundle-set
  preflight.
- The verifier does not execute package code, package managers, build tools, or
  generated prompts.
- The verifier remains producer-side evidence and does not accept packages or
  relations automatically.

## Residual Notes

DocC generation still reports unrelated pre-existing warnings around
`AcceptedPackageUpdateProposals` and inline command text references in
quality-report documentation. The new `BundleSetPreflight` DocC page builds and
is covered by docs contract tests.
