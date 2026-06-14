# P36-T3 Plugin-Aware Source Classification Hook

## Motivation

P36-T1 defined the repository parsing plugin contract and P36-T2 added the
first Python web-framework parser profile fixture. The fixture is useful only
as documentation until the collection/analyzer path can consume it in a
bounded, opt-in way.

The immediate motivating case is FastAPI: tutorial files under `docs_src/*`
are valuable semantic usage evidence, but they should not inflate the Python
public interface index. The hook must make that distinction without hardcoding
FastAPI-specific exclusions into the core analyzer.

## Goal

Implement the first plugin-aware source classification hook so an operator can
select `python.web_framework.v0` and have Python analyzer path selection honor
the profile's `publicInterfaceEligible` decisions.

## Deliverables

- Add a parser profile loader/decision helper for the P36-T2 fixture shape.
- Extend public API analyzer options with an optional parser profile id.
- Wire `collect-batch` to accept an explicit parser profile for interface
  index generation.
- Keep default behavior unchanged when no parser profile is selected.
- Add regression coverage for FastAPI-like paths, including `docs_src`, docs,
  examples, tests, generated, tooling, internal, fallback, and package-root
  paths.
- Update repository parsing plugin docs and DocC with the executable hook.

## Acceptance Criteria

- No parser profile selected means the current Python public API analyzer still
  includes ordinary Python files according to existing behavior.
- Selecting `python.web_framework.v0` excludes `docs_src/*`, docs, examples,
  tests, generated, tooling, internal, and fallback paths from public interface
  entrypoints.
- Selecting `python.web_framework.v0` keeps package-root Python files such as
  `fastapi/applications.py` in the public interface index.
- The generated analyzer result records parser profile metadata and decisions
  enough for reviewers to understand why paths were included or excluded.
- Unsupported parser profile ids fail closed with a clear `ValueError`.

## Non-Goals

- Do not build a dynamic plugin runtime.
- Do not clone or fetch repositories.
- Do not install harvested dependencies or execute harvested code.
- Do not publish registry metadata, accept packages or relations, remove
  `preview_only`, or treat AI output as registry truth.
- Do not run the FastAPI comparison in this task; that is P36-T4.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_python_public_api.py tests/test_analyzer_orchestration.py tests/test_batch_collection.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- coverage gate
- Swift docs build
- DocC static generation
