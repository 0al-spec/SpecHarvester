# REVIEW — P25-T7 Xyflow Package-Set Smoke Scenario

## Subject

Review of P25-T7 local `xyflow` package-set smoke implementation, CLI command,
docs, tests, Flow archive updates, and Phase 25 completion state.

## Findings

No actionable findings.

## Checks Reviewed

- `xyflow-package-set-smoke` creates a deterministic local synthetic `xyflow`
  checkout and source manifest without fetching the network.
- The smoke path runs workspace inventory collection, package-set drafting,
  bundle-set preflight, and package-set static viewer rendering.
- The smoke summary has stable identity:
  `spec-harvester.xyflow-package-set-smoke/v0` and
  `SpecHarvesterXyflowPackageSetSmokeReport`.
- The generated package set includes `xyflow.workspace`, `xyflow.system`,
  `xyflow.react`, and `xyflow.svelte`.
- The generated relation proposals include producer-observed `contains`
  relations from `xyflow.workspace` to system, React, and Svelte member
  packages.
- The package-set role hardening was verified against the existing real local
  `xyflow` checkout at `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`: root
  aggregate package `xyflow.workspace`, primary members, three relations,
  skipped examples/tooling/tests, passing preflight, and viewer output.
- The summary explicitly records that networks, package scripts, package
  managers, builds, tests, and prompts are not run.
- GitHub docs, DocC, workflow docs, and package-set alignment docs expose the
  smoke command and output artifacts.
- `next.md` marks Phase 25 complete and names package-set handoff/proposal
  automation as the next planning direction.

## Validation Reviewed

- `PYTHONPATH=src pytest tests/test_batch_collection.py::test_collect_batch_snapshots_emits_deterministic_workspace_inventory tests/test_package_set_drafter.py tests/test_xyflow_package_set_smoke.py tests/test_docs_contracts.py -q`
  — PASS, 62 passed.
- `PYTHONPATH=src python -m spec_harvester.cli xyflow-package-set-smoke --output /tmp/spec-harvester-xyflow-package-set-smoke`
  — PASS, `status: passed`.
- Real local `xyflow` package-set pipeline at
  `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` — PASS, 4 candidates, 3
  relations, preflight passed, viewer ok.
- `PYTHONPATH=src ruff check .` — PASS.
- `ruff format --check src tests` — PASS, 89 files already formatted.
- `PYTHONPATH=src pytest -q` — PASS, 537 passed, 1 skipped.
- `git diff --check` — PASS.
- `swift build --target SpecHarvesterDocs` — PASS.
- DocC static generation — PASS with unrelated pre-existing warnings.

## Follow-Up

FOLLOW-UP selected: define the next phase for package-set handoff/proposal
automation between SpecHarvester and SpecPM.
