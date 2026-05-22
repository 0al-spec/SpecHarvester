# P11-T6 Validation Report

Date: 2026-05-22
Task: `P11-T6` LM Studio JSON Schema Compatibility
Verdict: PASS

## Summary

Captured LM Studio `openai/gpt-oss-20b` compatibility findings in the SpecNode
provider boundary and smoke coverage. The contract now prefers
OpenAI-compatible `response_format.type: json_schema` for structured output and
explicitly avoids assuming `json_object` support for LM Studio.

Added `parse_specnode_model_json_object` as a strict parser fallback for direct
JSON object content and the observed `gpt-oss` text-mode channel wrapper:
`<|channel|>final <|constrain|>JSON<|message|>{...}`.

## Deliverables

- Added strict model JSON object parser for direct JSON and `gpt-oss`
  channel-wrapped content.
- Added parser tests for direct JSON, wrapped JSON, empty content, arrays,
  scalar JSON, multiple objects, malformed wrappers, and trailing non-JSON text.
- Updated GitHub provider adapter and provider smoke coverage docs.
- Updated DocC mirrors and docs contract tests.

## Acceptance Results

- Direct JSON object content parses successfully.
- `gpt-oss` channel-wrapped JSON object content parses successfully.
- `json_schema` is documented as the preferred LM Studio structured-output
  mode.
- `json_object` is documented as unsupported/not assumed for LM Studio.
- Multiple objects, arrays, scalar JSON, empty content, and malformed wrapper
  content are rejected.
- Existing provider smoke validation still passes.

## Quality Gates

- `PYTHONPATH=src python -m pytest tests/test_specnode_refinement_smoke.py tests/test_docs_contracts.py -q`
  - PASS: 30 passed
- `PYTHONPATH=src python -m pytest`
  - PASS: 246 passed
- `ruff check src tests`
  - PASS
- `ruff format --check src tests`
  - PASS: 46 files already formatted
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 246 passed, total coverage 91.21%
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Notes

- No HTTP client, LM Studio runtime call, real model execution, provider
  discovery, or patch application was added to project tests.
- The parser fallback only extracts one JSON object. Structural
  `SpecNodeRefinementResult` validation still runs after parsing.
