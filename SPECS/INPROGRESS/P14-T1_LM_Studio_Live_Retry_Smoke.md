# P14-T1 LM Studio Live Retry Smoke

Status: Planned
Task: `P14-T1`
Phase: Phase 14. Live SpecNode Provider Smoke
Priority: P1
Effort: 8 hours
Dependencies: `P13-T3`

## Problem

P13-T3 proves the SpecNode feedback loop with deterministic scripted providers,
but it does not prove that a local OpenAI-compatible provider such as LM Studio
can be driven through the same orchestration boundary. We need a manual live
smoke path that exercises the loop against a local model without introducing a
CI dependency on developer-local infrastructure.

## Goals

- Add a manual live smoke harness for LM Studio-compatible
  `/v1/chat/completions`.
- Keep the harness disabled by default and controlled by explicit environment
  variables.
- Adapt model responses into the existing `SpecNodeCompatibleProvider` and
  `SpecNodeSemanticReviewer` protocols.
- Reuse the existing `run_specnode_refinement_retry_orchestration(...)`
  controller instead of creating a parallel loop.
- Prove retry feedback mechanically: first review emits `needs_revision`, retry
  directives are passed into attempt 2, and the final run is approved or capped
  with a deterministic audit trail.
- Parse direct JSON and observed `gpt-oss` channel-wrapped JSON through the
  repository parser.
- Add unit tests for adapter behavior and skip behavior without requiring LM
  Studio.
- Add documentation explaining how to run the smoke manually.

## Non-Goals

- Do not enable live LM Studio calls in ordinary CI.
- Do not apply generated patch proposals or mutate candidate files.
- Do not commit generated smoke output.
- Do not send raw repository source, secrets, provider logs, or arbitrary
  prompts to the model.
- Do not implement a production SpecNode HTTP runtime.

## Deliverables

- `scripts/specnode_live_retry_smoke.py`
- Env-gated pytest coverage for the manual live path.
- Unit tests for OpenAI-compatible response parsing, request construction,
  provider/reviewer adapter behavior, and skip behavior.
- Documentation in `docs/SPECNODE_PROVIDER_SMOKE_COVERAGE.md` or a dedicated
  live-smoke doc.
- Flow validation report for local deterministic gates and optional live smoke
  outcome when LM Studio is available.

## Environment Contract

- `SPECHARVESTER_LM_STUDIO_BASE_URL`, default example:
  `http://127.0.0.1:1234`
- `SPECHARVESTER_SPECNODE_MODEL`, default example:
  `openai/gpt-oss-20b`
- `SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE=1` to enable live pytest execution.
- Optional `SPECHARVESTER_LIVE_SMOKE_TIMEOUT_SECONDS`.

## Acceptance Criteria

- Running ordinary `pytest` skips live provider calls unless
  `SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE=1` is set.
- The script fails fast with an actionable message when required environment
  variables are missing or the provider endpoint is unavailable.
- A successful live run prints a compact JSON summary with model ID, attempt
  count, run status, review verdict sequence, retry context presence, and token
  usage summary.
- The adapter accepts direct JSON and `gpt-oss` channel-wrapped JSON model
  content using `parse_specnode_model_json_object(...)`.
- Unit tests do not contact the network.
- Full tests, lint, format, coverage, Swift manifest, and Swift DocC build pass.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_specnode_live_retry_smoke.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- Optional live smoke:
  `SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE=1 SPECHARVESTER_LM_STUDIO_BASE_URL=http://127.0.0.1:1234 SPECHARVESTER_SPECNODE_MODEL=openai/gpt-oss-20b PYTHONPATH=src python -m pytest tests/test_specnode_live_retry_smoke.py -q`
