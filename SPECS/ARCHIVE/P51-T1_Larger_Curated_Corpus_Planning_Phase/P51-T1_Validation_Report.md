# P51-T1 Validation Report

Task: `P51-T1` Larger Curated Corpus Planning Phase
Date: 2026-06-25
Verdict: PASS

## Scope

P51-T1 converts P50 restored-checkout rerun evidence into a bounded planning
phase for the larger curated corpus. It adds the planning fixture, GitHub and
DocC documentation, Workplan follow-up tasks, current next-state, and focused
docs-contract coverage.

This task does not run a larger corpus batch, choose the final source manifest,
clone/fetch repositories, install dependencies, invoke package managers,
execute harvested code, run adapters, run AI, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, or treat
AI/static/rerun/planning/adapter output as registry truth.

## Evidence Recorded

- Source evidence:
  `tests/fixtures/restored_checkout_rerun_evidence/p50-t1-restored-checkout-rerun-evidence.example.json`.
- Source digest:
  `sha256:eeb94038127f016d0302c03ae141312c7a8cda6fd286a5ec58e401481fabed07`.
- P50 decision:
  `larger_corpus_planning_reconsideration_ready_after_restored_checkout_rerun`.
- Phase 51 task sequence:
  `P51-T2 -> P51-T3 -> P51-T4 -> P51-T5 -> P51-T6 -> P51-T7`.
- Gate order:
  `source plan -> readiness -> static-only -> AI-enabled -> triage -> exit decision`.
- Next task pointer: `P51-T2`.

## Checks

- `python3 -m json.tool tests/fixtures/larger_curated_corpus_planning_phase/p51-t1-larger-curated-corpus-planning-phase.example.json`
  - PASS
- `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "larger_curated_corpus_planning_phase or restored_checkout_rerun_evidence"`
  - PASS: `2 passed, 179 deselected`
- `python3 -m ruff format tests/test_docs_contracts.py`
  - PASS: mechanically reformatted the new test after the first format check
    requested reformatting
- `python3 -m ruff format --check src tests`
  - PASS: `131 files already formatted`
- `python3 -m ruff check src tests`
  - PASS: `All checks passed!`
- `PYTHONPATH=src python3 -m pytest`
  - PASS: `912 passed, 1 skipped`
- `PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `912 passed, 1 skipped`, total coverage `90.48%`, required coverage
    `90%`
- `swift package describe`
  - PASS
- `swift package dump-package`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS
- `swift package --allow-writing-to-directory .build/docs generate-documentation --target SpecHarvester --output-path .build/docs`
  - PASS
- `git diff --check`
  - PASS

## Result

P51-T1 is complete. The larger curated corpus planning phase is now defined,
but execution is not approved. The next task is `P51-T2`, which must author the
larger curated corpus source plan and manifest criteria before readiness,
static-only, AI-enabled, triage, or exit-decision tasks proceed.
