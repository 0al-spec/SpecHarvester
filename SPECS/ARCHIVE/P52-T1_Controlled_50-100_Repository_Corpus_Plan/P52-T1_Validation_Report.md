# P52-T1 Validation Report

**Task:** `P52-T1` Controlled 50-100 Repository Corpus Plan
**Date:** 2026-07-22
**Verdict:** PASS

## Scope

P52-T1 defines the planning contract for a controlled 50-100 repository
corpus. It adds the durable plan fixture, GitHub and DocC documentation, Phase
52 follow-up tasks, a P52-T2 next-state, and documentation-contract coverage.

The task did not create or restore checkouts, clone/fetch repositories, install
dependencies, invoke package managers, execute harvested code, run adapters,
run Codex, run AI, accept packages or relations, publish registry metadata,
seed baselines, remove `preview_only`, or treat any output as registry truth.

## Evidence Recorded

- Source evidence:
  `tests/fixtures/larger_curated_corpus_exit_decision/p51-t8-larger-curated-corpus-exit-decision.example.json`.
- Source digest:
  `sha256:9c080b5f8f17d021894a3b2755177fefc56ac4d836aebd450098fbb09ee06ec9`.
- New fixture:
  `tests/fixtures/controlled_repository_corpus_plan/p52-t1-controlled-repository-corpus-plan.example.json`.
- Target corpus range: 50-100 operator-curated repositories with pinned local
  checkouts.
- Rollout: Codex Spark adapter contract -> 5 repository calibration -> 20
  repository pilot -> source/readiness -> static-only -> proposal-only Spark ->
  triage/handoff -> exit decision.
- Next task pointer: `P52-T2` Codex Spark External-Model Adapter Contract.

## Checks

- `python -m json.tool tests/fixtures/controlled_repository_corpus_plan/p52-t1-controlled-repository-corpus-plan.example.json >/dev/null`
  - PASS
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -k controlled_repository_corpus_plan -q`
  - PASS: `1 passed, 188 deselected`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
  - PASS: `189 passed`
- `PYTHONPATH=src python -m pytest`
  - PASS: `921 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `921 passed, 1 skipped`, total coverage `90.53%`, threshold `90%`
- `ruff format --check src tests`
  - PASS: `131 files already formatted`
- `ruff check src tests`
  - PASS: `All checks passed!`
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS, with one existing SwiftPM warning that the `.docc` directory is an
    unhandled resource.
- `git diff --check`
  - PASS

## Post-Review Correction

PR #303 review identified that the initial source-policy vocabulary could be
read as keys for the existing repository manifest. P52-T1 now distinguishes:

- the existing ingestible manifest keys: `id`, `repository`, `revision` or
  `ref`, and `checkout`, with the existing optional keys retained; and
- a separate `spec-harvester.controlled-repository-selection-metadata/v0`
  companion schema for ecosystem, repository shape, importance, license
  provenance, and size budget.

Focused revalidation after the correction:

- `python -m json.tool tests/fixtures/controlled_repository_corpus_plan/p52-t1-controlled-repository-corpus-plan.example.json >/dev/null`
  - PASS
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -k controlled_repository_corpus_plan -q`
  - PASS: `1 passed, 188 deselected`
- `ruff format --check tests/test_docs_contracts.py && ruff check tests/test_docs_contracts.py`
  - PASS
- `git diff --check`
  - PASS

## Result

P52-T1 passes. Phase 52 is now defined as a controlled rollout rather than a
single 50-100 repository batch. P52-T2 must define the schema-validated
`codex exec` external-model contract before any five-repository calibration or
live Codex Spark execution can occur.
