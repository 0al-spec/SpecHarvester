# P6-T4 - Add Reproducible Local Smoke-Test Fixture Documentation

Branch: `feature/P6-T4-add-reproducible-local-smoke-test-fixture-documentation`
Review subject: `p6_t4_smoke_test_fixture_docs`

## Problem

Recent local smoke runs used useful real repositories (`Cupertino`, `xyflow`,
`docc2context`, and `Puzzle`), but the input manifest, output directories, and
rerun commands were ad hoc. That makes the feedback hard to reproduce and risks
polluting the repository with generated candidate outputs.

## Goals

- Document a deterministic local smoke fixture layout.
- Provide reproducible command snippets for the four locally validated
  repositories.
- Keep generated smoke input/output outside committed source by default.
- Make review reports reproducible from the same smoke output root.

## Non-Goals

- No new repository cloning, network fetch, or checkout management behavior.
- No generated candidate outputs committed to the repository.
- No acceptance or promotion of smoke-generated candidates.
- No change to collector, drafter, or governance report semantics.

## Deliverables

- Add GitHub-facing smoke fixture documentation under `docs/`.
- Link the new page from the documentation index and root README.
- Update ignore rules for canonical local smoke fixture/output directories.
- Add a documentation contract test covering the new smoke page and key
  reproducibility controls.
- Create a validation report for this task.

## Acceptance Criteria

- Documentation explains smoke fixture directories and command conventions.
- Commands cover `Cupertino`, `xyflow`, `docc2context`, and `Puzzle`.
- Generated smoke output is clearly separated from committed artifacts and
  ignored by version control.
- The documented workflow remains local-only and does not install harvested
  dependencies or execute harvested package scripts.
- Quality gates from `.flow/params.yaml` pass.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
