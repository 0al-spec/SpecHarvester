# P36-T3 Validation Report

**Task:** Plugin-Aware Source Classification Hook
**Date:** 2026-06-14
**Verdict:** PASS

## Summary

P36-T3 implements the first opt-in repository parsing profile hook. Operators
can pass `python.web_framework.v0` to collection or autonomous candidate batch
runs, and the Python public API analyzer will use the profile to keep
documentation/tutorial/example/test/tooling/internal paths out of
`public-interface-index.json` entrypoints.

Default behavior remains unchanged when no parser profile is selected.

## Deliverables

- Added `spec_harvester.repository_parsing_profile`.
- Added optional `parser_profile_id` public analyzer option.
- Wired parser profile selection through analyzer orchestration,
  `collect-batch`, and `autonomous-candidate-batch`.
- Added `--parser-profile` CLI support.
- Added Python analyzer path classification metadata:
  `repositoryParsingProfile` and `pathClassification`.
- Added regression coverage for default behavior, FastAPI-like profile
  decisions, unknown profile failure before analyzer dispatch, analyzer
  orchestration, and batch collection.
- Updated GitHub docs and DocC mirror.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_python_public_api.py tests/test_analyzer_orchestration.py tests/test_batch_collection.py -q` -> `58 passed`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_parsing_plugin_contract or python_web_framework_parser_profile'` -> `2 passed, 98 deselected`
- `PYTHONPATH=src pytest tests/test_python_public_api.py tests/test_analyzer_orchestration.py tests/test_batch_collection.py tests/test_docs_contracts.py -q` -> `158 passed`
- `PYTHONPATH=src pytest -q` -> `731 passed, 1 skipped`
- `PYTHONPATH=src ruff check .` -> passed
- `PYTHONPATH=src ruff format --check src tests` -> passed
- `git diff --check` -> passed
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` -> `731 passed, 1 skipped`, total coverage `91.02%`
- `swift build --target SpecHarvesterDocs` -> passed
- `swift package dump-package >/dev/null` -> passed
- `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` -> passed

## Boundary

The hook is producer-side path classification only. It does not clone or fetch
repositories, install dependencies, execute harvested code, publish registry
metadata, accept packages or relations, remove `preview_only`, or treat AI
output as registry truth.
