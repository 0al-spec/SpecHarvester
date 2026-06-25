# P51-T3 Validation Report

**Task:** `P51-T3` Larger Curated Corpus Checkout Readiness Gate
**Date:** 2026-06-25
**Verdict:** PASS

## Summary

P51-T3 ran the checkout readiness gate for the 12 selected P51-T2 sources. All
12 operator-local checkout paths resolved to git repositories, all 12 observed
`HEAD` revisions matched the pinned manifest revisions, and no blocking
readiness reasons were found.

The gate carries two non-blocking caveats forward:

- `xyflow.operator_checkout_origin_fork_mismatch`;
- `docc2context.source_checkout_had_untracked_doccarchive`.

P51-T4 static-only execution is allowed. P51-T5 AI-enabled execution remains
blocked until P51-T4 records passing static-only evidence.

## Validation Commands

- `PYTHONPATH=src python3 - <<'PY' ... read_repository_source_manifests(Path('inputs/p51-larger-curated-corpus')) ... git rev-parse HEAD ... git status --porcelain ... PY`
  - PASS: `12` selected sources checked, `12` checkouts present, `12`
    revisions matched, `0` blocking reasons.
- `python3 -m json.tool tests/fixtures/larger_curated_corpus_checkout_readiness/p51-t3-larger-curated-corpus-checkout-readiness.example.json`
  - PASS
- `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "larger_curated_corpus_checkout_readiness or larger_curated_corpus_source_plan or larger_curated_corpus_planning_phase"`
  - PASS: `3 passed, 180 deselected`
- `python3 -m ruff format tests/test_docs_contracts.py`
  - PASS: `1 file reformatted`
- `python3 -m ruff format --check src tests`
  - PASS: `131 files already formatted`
- `python3 -m ruff check src tests`
  - PASS: `All checks passed!`
- `PYTHONPATH=src python3 -m pytest`
  - PASS: `914 passed, 1 skipped`
- `PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `914 passed, 1 skipped`; total coverage `90.48%`
- `swift package describe`
  - PASS
- `swift package dump-package`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS
- `swift package --allow-writing-to-directory .build/docs generate-documentation --target SpecHarvester --output-path .build/docs`
  - PASS

## Boundaries Confirmed

- No larger corpus batch was run.
- No static-only gate was run in P51-T3.
- No AI-enabled gate was run.
- No clone/fetch, dependency installation, package-manager invocation,
  harvested-code execution, adapter execution, or trusted local adapter
  execution was performed.
- No packages or relations were accepted.
- No registry metadata was published, no baselines were seeded, and
  `preview_only` was not removed.
- Readiness output remains producer evidence only and is not registry truth.
