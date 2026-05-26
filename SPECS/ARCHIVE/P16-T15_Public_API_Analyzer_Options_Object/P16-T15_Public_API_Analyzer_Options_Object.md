# P16-T15 — Public API Analyzer Options Object

Branch: `feature/P16-T15-public-api-analyzer-options`
Review subject: `p16_t15_public_api_analyzer_options_object`

## Context

After P16-T14, the trusted `pylint` duplicate-code backend reports zero
duplicate blocks. The builtin advisory backend still reports one public API
analyzer option-shape cluster across:

- `src/spec_harvester/python_public_api.py`
- `src/spec_harvester/go_public_api.py`
- `src/spec_harvester/js_ts_public_api.py`

The repeated shape is not language behavior; it is the common analyzer request
context: source root, optional package ID, source revision, and cache directory.

## Scope

- Add a shared `PublicApiAnalyzerOptions` object for analyzer request context.
- Keep existing public analyzer function call signatures compatible for current
  callers and tests.
- Move common source-root validation, package ID fallback, and cache construction
  behind behavior on the shared object.
- Refactor Python, Go, and JS/TS analyzers to use the shared object internally.
- Re-run duplicate-code, architecture-lint, and analyzer behavior tests.

## Non-Goals

- Do not change analyzer output schemas.
- Do not change analyzer IDs, versions, confidence values, or execution policy.
- Do not change language-specific public symbol extraction behavior.
- Do not execute harvested repository code.
- Do not require callers to instantiate the new object.

## Acceptance Criteria

- Existing analyzer tests pass for Python, Go, and JS/TS.
- Public analyzer functions remain source-compatible for current callers.
- Builtin duplicate-code report no longer contains the analyzer option-shape
  cluster, or any remaining cluster is justified as below practical minimum.
- `pylint` duplicate-code remains at zero duplicate blocks.
- Full Flow validation passes.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_python_public_api.py tests/test_go_public_api.py tests/test_js_ts_public_api.py tests/test_analyzer_orchestration.py -q`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t15-dup-builtin.json`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t15-dup-pylint.json`
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t15-architecture-lint.json`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
