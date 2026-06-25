# P51-T2 Validation Report

**Task:** `P51-T2` Larger Curated Corpus Source Plan and Manifest Criteria
**Date:** 2026-06-25
**Verdict:** PASS

## Summary

P51-T2 authored the larger curated corpus source plan and manifest criteria.
The task added a 12-repository operator-curated source manifest, a
machine-readable source-plan fixture, GitHub docs, DocC docs, and contract
tests. It did not run a larger corpus batch, readiness gate, static gate,
AI-enabled gate, adapter execution, clone/fetch, dependency installation, or
package-manager command.

## Validation Commands

- `python3 -m json.tool tests/fixtures/larger_curated_corpus_source_plan/p51-t2-larger-curated-corpus-source-plan.example.json`
  - PASS
- `PYTHONPATH=src python3 -c 'from pathlib import Path; from spec_harvester.source_manifest import read_repository_source_manifests; records=read_repository_source_manifests(Path("inputs/p51-larger-curated-corpus")); assert len(records)==12; print("manifest records", len(records))'`
  - PASS: `manifest records 12`
- `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "larger_curated_corpus_source_plan or larger_curated_corpus_planning_phase"`
  - PASS: `2 passed, 180 deselected`
- `python3 -m ruff format tests/test_docs_contracts.py`
  - PASS: `1 file reformatted`
- `python3 -m ruff format --check src tests`
  - PASS: `131 files already formatted`
- `python3 -m ruff check src tests`
  - PASS: `All checks passed!`
- `PYTHONPATH=src python3 -m pytest`
  - PASS: `913 passed, 1 skipped`
- `PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `913 passed, 1 skipped`; total coverage `90.48%`
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
- No checkout readiness gate was run in P51-T2.
- No clone/fetch, dependency installation, package-manager invocation,
  harvested-code execution, adapter execution, trusted local adapter execution,
  or AI execution was performed.
- No packages or relations were accepted.
- No registry metadata was published, no baselines were seeded, and
  `preview_only` was not removed.
- Source-plan output remains producer evidence only and is not registry truth.
