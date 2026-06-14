# P36-T1 Validation Report

**Task:** Repository Parsing Plugin Contract
**Date:** 2026-06-14
**Verdict:** PASS

## Summary

P36-T1 documents the repository parsing plugin contract. The contract uses the
FastAPI `docs_src/*` over-capture as the motivating case and defines a reusable
language/framework parser profile boundary instead of a repository-specific
exception.

## Deliverables

- Added `docs/REPOSITORY_PARSING_PLUGIN_CONTRACT.md`.
- Added DocC mirror `RepositoryParsingPluginContract`.
- Linked the contract from documentation entrypoints, capabilities, and
  roadmap.
- Added docs-contract regression coverage for contract content, entrypoint
  links, workplan tasks, and active next-task state.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q` -> `99 passed`
- `PYTHONPATH=src pytest -q` -> `724 passed, 1 skipped`
- `PYTHONPATH=src ruff check .` -> passed
- `PYTHONPATH=src ruff format --check src tests` -> passed
- `git diff --check` -> passed
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` -> `724 passed, 1 skipped`, total coverage `90.96%`
- `swift build --target SpecHarvesterDocs` -> passed
- `swift package dump-package >/dev/null` -> passed
- `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` -> passed

## Boundary

This task is documentation and contract planning only. It does not implement
parser plugins, change analyzer behavior, publish registry metadata, accept
packages or relations, remove `preview_only`, or treat AI output as registry
truth.
