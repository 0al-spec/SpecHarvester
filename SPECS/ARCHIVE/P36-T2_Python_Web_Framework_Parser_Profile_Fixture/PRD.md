# P36-T2 Python Web-Framework Parser Profile Fixture

## Motivation

P36-T1 defined the repository parsing plugin contract. The next step is to make
that contract concrete with a machine-readable Python web-framework parser
profile fixture.

The FastAPI rerun showed why this matters: `docs_src/*` tutorial files are
useful semantic usage evidence, but they should not inflate
`public_interface_index` or appear as public API symbols for `fastapi.core`.

## Goal

Add a versioned parser profile fixture for Python web frameworks that:

- classifies package source roots as public interface evidence;
- classifies documentation, tutorials, examples, and tests as semantic usage
  or non-public-interface evidence;
- records rule precedence and fallback behavior;
- provides sample FastAPI-like path decisions;
- remains producer-side review evidence only.

## Deliverables

- Add `tests/fixtures/repository_parsing_profiles/python-web-framework-v0.example.json`.
- Document the fixture in `REPOSITORY_PARSING_PLUGIN_CONTRACT.md` and DocC.
- Add docs-contract regression coverage for the fixture shape and key path
  role decisions.
- Archive the task through Flow.

## Fixture Requirements

The fixture should include:

- `apiVersion: spec-harvester.repository-parsing-profile/v0`;
- `kind: SpecHarvesterRepositoryParsingProfile`;
- `schemaVersion: 1`;
- `authority: producer_path_classification_profile_only`;
- profile id such as `python.web_framework.v0`;
- target ecosystem/language metadata;
- rule precedence;
- path role rules for package roots, `docs_src`, docs, examples, tests,
  generated artifacts, tooling, internal paths, and default fallback;
- sample decisions for FastAPI-like paths.

## Non-Goals

- Do not implement parser profile execution in this task.
- Do not change analyzer path selection in this task.
- Do not rerun FastAPI as acceptance evidence in this task.
- Do not publish registry metadata, accept packages or relations, remove
  `preview_only`, or treat AI output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- coverage gate
- Swift docs build
- DocC static generation
