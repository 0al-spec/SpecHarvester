# P36-T4 Validation Report

**Task:** FastAPI AI-Enabled Parser Profile Rerun
**Date:** 2026-06-14
**Verdict:** PASS

## Summary

P36-T4 reran FastAPI through deterministic collection and the AI-enabled
autonomous candidate pipeline using `--parser-profile python.web_framework.v0`.

The parser profile fixed the motivating evidence boundary problem:
`docs_src/*` public interface entrypoints dropped from `454` to `0`, while
FastAPI package entrypoints stayed at `48`.

The autonomous candidate batch passed and produced an `author_ready_draft`
starter package. AI proposal artifacts still had warning-level gaps, so the
result is closer to registry-review quality on public API evidence but is not
a clean registry handoff.

## Run Inputs

- Local checkout: `/Users/egor/Development/GitHub/fastapi`
- Revision: `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263`
- Parser profile: `python.web_framework.v0`
- LM Studio base URL: `http://127.0.0.1:1234`
- Model: `openai/gpt-oss-20b`
- Run root: `/tmp/specharvester-p36-t4-fastapi-20260614T190747Z`

## Evidence Comparison

| Run | Entrypoints | Symbols | `docs_src/*` entrypoints | `fastapi/*` entrypoints |
| --- | ---: | ---: | ---: | ---: |
| Baseline | 1121 | 6009 | 454 | 48 |
| Profiled | 48 | 298 | 0 | 48 |

## AI Batch Result

- Batch status: `passed`
- Candidate count: `1`
- Bundle-set preflight: `passed`
- Author-ready draft status: `author_ready_draft`
- AI draft status: `warning`
- AI enrichment status: `warning`
- AI enriched preview status: `skipped`

## Deliverables

- Added durable fixture:
  `tests/fixtures/fastapi_parser_profile_rerun/p36-t4-fastapi-parser-profile-rerun.example.json`.
- Added GitHub docs:
  `docs/FASTAPI_PARSER_PROFILE_RERUN.md`.
- Added DocC mirror:
  `Sources/SpecHarvester/Documentation.docc/FastAPIParserProfileRerun.md`.
- Updated docs index, capabilities, roadmap, DocC root, and docs-contract
  regression coverage.

## Validation Commands

- `collect-batch` baseline without parser profile -> `status: ok`
- `collect-batch --parser-profile python.web_framework.v0` -> `status: ok`
- `autonomous-candidate-batch --lm-studio-model openai/gpt-oss-20b --parser-profile python.web_framework.v0 --apply-ai-enrichment` -> `status: passed`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'fastapi_parser_profile_rerun or current_next_task or repository_parsing_plugin_contract'` -> `2 passed, 99 deselected`
- `PYTHONPATH=src pytest -q` -> `732 passed, 1 skipped`
- `PYTHONPATH=src ruff check .` -> passed
- `PYTHONPATH=src ruff format --check src tests` -> passed
- `git diff --check` -> passed
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` -> `732 passed, 1 skipped`, total coverage `91.02%`
- `swift build --target SpecHarvesterDocs` -> passed
- `swift package dump-package >/dev/null` -> passed
- `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` -> passed

## Boundary

The rerun report is producer-side evidence only. It is not SpecPM registry
acceptance, maintainer approval, or upstream FastAPI endorsement. It does not
publish registry metadata, remove `preview_only`, or treat AI output as
registry truth.
