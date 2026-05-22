# P11-T6 LM Studio JSON Schema Compatibility

Status: Archived
Created: 2026-05-22
Task: `P11-T6` Capture LM Studio `gpt-oss` response compatibility by requiring
OpenAI-compatible `json_schema` response format for structured output and a safe
parser fallback for `gpt-oss` channel-wrapped JSON in text mode.

## Problem

Local runtime probing against LM Studio on `127.0.0.1:1234` showed that
`openai/gpt-oss-20b` is available and can answer `/v1/chat/completions`.
However, two compatibility details matter for future SpecNode provider
integration:

- LM Studio rejects `response_format.type: json_object` and accepts
  `response_format.type: json_schema`.
- In plain text mode, `openai/gpt-oss-20b` may return JSON wrapped as
  `<|channel|>final <|constrain|>JSON<|message|>{...}`.

The current contract says OpenAI-compatible provider output must be
schema-validated, but it does not pin this LM Studio behavior. Without this
clarification, a future provider adapter could choose `json_object`, fail
against LM Studio, or reject recoverable channel-wrapped JSON that is otherwise
valid structured data.

## Goals

- Document `json_schema` as the preferred structured-output request mode for
  LM Studio `openai/gpt-oss-20b`.
- Document that `json_object` must not be assumed for LM Studio compatibility.
- Add a deterministic parser helper for extracting JSON payloads from direct
  JSON text and `gpt-oss` channel-wrapped text mode responses.
- Keep parser fallback strict: return a parsed JSON object only when exactly one
  object payload can be extracted and parsed.
- Add tests for direct JSON, channel-wrapped JSON, invalid wrappers, arrays,
  multiple JSON objects, and non-object payloads.
- Mirror the contract in GitHub docs and DocC.

## Non-Goals

- Do not implement a real HTTP client for LM Studio.
- Do not call LM Studio from CI tests.
- Do not execute models in project tests.
- Do not apply generated patches.
- Do not relax `SpecNodeRefinementResult` validation.
- Do not make SpecHarvester own provider discovery or model execution.

## Design

- Add a small parser helper in `spec_harvester.specnode_refinement`:
  `parse_specnode_model_json_object`.
- The helper accepts provider message content and returns a JSON object for:
  direct JSON object text and the observed `gpt-oss` wrapper shape.
- The helper rejects arrays, scalar JSON, empty text, multiple candidate object
  payloads, and malformed wrappers.
- Update provider adapter and smoke coverage docs with LM Studio
  `json_schema` request guidance and text-mode fallback rules.
- Update DocC mirrors and docs contract tests.

## Deliverables

- Parser helper for direct and channel-wrapped JSON object content.
- Unit tests for parser success and rejection cases.
- GitHub and DocC documentation updates for LM Studio `json_schema`
  compatibility.
- Flow validation report.

## Acceptance Criteria

- Direct JSON object content parses successfully.
- `<|channel|>final <|constrain|>JSON<|message|>{...}` content parses
  successfully when the payload is a single object.
- `json_object` is documented as unsupported/not assumed for LM Studio.
- `json_schema` is documented as preferred structured-output mode for
  `openai/gpt-oss-20b`.
- Multiple objects, arrays, scalar JSON, empty content, and malformed wrapper
  content are rejected.
- Existing provider smoke validation still passes.
- Configured Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_specnode_refinement_smoke.py -q`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`

Archived: 2026-05-22
Verdict: PASS
