# P36-T2 Validation Report

**Task:** Python Web-Framework Parser Profile Fixture
**Date:** 2026-06-14
**Verdict:** PASS

## Summary

P36-T2 adds the first machine-readable parser profile fixture for the
repository parsing plugin contract. The fixture describes a Python
web-framework profile that treats package source roots as public interface
evidence and treats documentation/tutorial/example/test paths as semantic or
non-public-interface evidence by default.

## Deliverables

- Added
  `tests/fixtures/repository_parsing_profiles/python-web-framework-v0.example.json`.
- Extended `REPOSITORY_PARSING_PLUGIN_CONTRACT.md` and DocC mirror with the
  fixture identity, purpose, and sample FastAPI-like path decisions.
- Added docs-contract regression coverage for fixture schema, evidence roles,
  path role rules, fallback behavior, non-authority statements, and active
  next-task state.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q` -> `100 passed`
- `PYTHONPATH=src pytest -q` -> `725 passed, 1 skipped`
- `PYTHONPATH=src ruff check .` -> passed
- `PYTHONPATH=src ruff format --check src tests` -> passed
- `git diff --check` -> passed
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` -> `725 passed, 1 skipped`, total coverage `90.96%`
- `swift build --target SpecHarvesterDocs` -> passed
- `swift package dump-package >/dev/null` -> passed
- `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` -> passed

## Boundary

This task adds a fixture and documentation only. It does not execute parser
profiles, change analyzer behavior, rerun FastAPI as acceptance evidence,
publish registry metadata, accept packages or relations, remove
`preview_only`, or treat AI output as registry truth.
