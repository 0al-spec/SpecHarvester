# P25-T7 Validation Report

**Task:** P25-T7 Xyflow Package-Set Smoke Scenario
**Date:** 2026-06-07
**Verdict:** PASS

## Summary

P25-T7 adds `xyflow-package-set-smoke`, a repeatable local synthetic smoke
scenario for the complete package-set producer path. The command writes a
synthetic `xyflow` checkout, source manifest, workspace inventory,
package-set draft, relation proposals, bundle-set preflight report, static
viewer output, and `xyflow-package-set-smoke.json` summary.

The smoke scenario exercises:

1. `collect-batch --emit-workspace-inventory`
2. `draft-package-set`
3. `preflight-bundle-set`
4. `render-package-set-site`

The scenario remains local-only and does not fetch the real repository, run
package scripts, run package managers, execute builds, run tests, execute
prompts, accept packages, accept relations, or publish registry metadata.

The package-set drafting hardening was also checked against the existing local
real `xyflow` checkout at
`/Users/egor/Development/GitHub/xyflow@a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`.
That run now produces `xyflow.workspace`, `xyflow.system`, `xyflow.react`, and
`xyflow.svelte`, records three `contains` relations from `xyflow.workspace`,
skips examples/tooling/tests as non-primary package records, passes
bundle-set preflight, and renders package-set viewer output.

## Validation Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src pytest tests/test_batch_collection.py::test_collect_batch_snapshots_emits_deterministic_workspace_inventory tests/test_package_set_drafter.py tests/test_xyflow_package_set_smoke.py tests/test_docs_contracts.py -q` | PASS, 62 passed |
| `PYTHONPATH=src python -m spec_harvester.cli xyflow-package-set-smoke --output /tmp/spec-harvester-xyflow-package-set-smoke` | PASS, `status: passed` |
| Real local `xyflow` package-set pipeline at `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` | PASS, 4 candidates, 3 relations, preflight passed, viewer ok |
| `PYTHONPATH=src ruff check .` | PASS |
| `ruff format --check src tests` | PASS, 89 files already formatted |
| `PYTHONPATH=src pytest -q` | PASS, 537 passed, 1 skipped |
| `git diff --check` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` | PASS with pre-existing DocC warnings |

## Acceptance Criteria

- The smoke scenario produces `xyflow.workspace`, `xyflow.system`,
  `xyflow.react`, and `xyflow.svelte` as separate candidate subjects.
- The smoke scenario records `xyflow.workspace contains xyflow.system`,
  `xyflow.workspace contains xyflow.react`, and
  `xyflow.workspace contains xyflow.svelte`.
- Bundle-set preflight passes without executing harvested repository code,
  package scripts, package managers, builds, tests, or prompts.
- The static viewer emits `package-set.json` and keeps aggregate/scoped package
  boundaries visible.
- The scenario is deterministic and local-only.

## Residual Notes

DocC generation still reports unrelated pre-existing warnings around
`AcceptedPackageUpdateProposals` and inline command text references in
quality-report documentation. The new `XyflowPackageSetSmoke` DocC page builds
and is covered by docs contract tests.

Phase 25 is complete after P25-T7. A useful next planning step is a new phase
for package-set handoff/proposal automation between SpecHarvester and SpecPM.
