# P29-T3 Validation Report

Task: `P29-T3 Corpus Baseline and Gap Report`
Verdict: PASS
Date: 2026-06-13

## Scope

Implemented the Flask/Gin/xyflow autonomous candidate corpus baseline as
producer-side evidence only:

- added
  `tests/fixtures/autonomous_candidate_corpus_baseline/flask-gin-xyflow.example.json`;
- added GitHub docs page
  `docs/AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`;
- added DocC mirror
  `Sources/SpecHarvester/Documentation.docc/AutonomousCandidateCorpusBaseline.md`;
- linked the baseline from docs index, roadmap, intake policy, and tech debt
  plan;
- added regression coverage for fixture identity, deterministic counts, live
  LM Studio statuses, gap codes, and non-authority boundary.

The task intentionally did not implement single-package fallback or LM Studio
JSON repair/retry. Those remain `P29-T4` and `P29-T5`.

## Baseline Result

Deterministic `--skip-ai` baseline:

- Flask: `0` candidates, `0` relations, preflight `passed`,
  `single_package_fallback_needed`.
- Gin: `0` candidates, `0` relations, preflight `passed`,
  `single_package_fallback_needed`.
- xyflow: `4` candidates, `3` relations, preflight `passed`,
  `stop_for_author_review`.

Live LM Studio baseline:

- Flask: AI draft `completed`, AI enrichment `completed`, but no proposal
  subjects because deterministic drafting produced `0` candidates.
- Gin: AI draft `completed`, AI enrichment `completed`, but no proposal
  subjects because deterministic drafting produced `0` candidates.
- xyflow: AI draft `failed` with `model_output_invalid_json`; AI enrichment was
  not run after the draft failure.

Product verdict:

- `pipelineHealth: deterministic_pipeline_passed`
- `candidateQuality: needs_follow_up`

## Gates

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
  - PASS: `53 passed`
- `PYTHONPATH=src python -m pytest -q`
  - PASS: `615 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `615 passed, 1 skipped`
  - Coverage: `90.11%`
- `PYTHONPATH=src ruff check src tests`
  - PASS
- `PYTHONPATH=src ruff format --check src tests`
  - PASS after applying `ruff format tests/test_docs_contracts.py`
- `git diff --check`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Boundary

This baseline is `producer_preview_evidence_only`.

It does not:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- replace SpecPM validation;
- replace maintainer review.
