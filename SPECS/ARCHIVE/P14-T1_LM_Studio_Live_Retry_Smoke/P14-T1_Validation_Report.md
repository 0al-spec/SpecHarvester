# P14-T1 Validation Report

Task: `P14-T1` LM Studio Live Retry Smoke
Date: 2026-05-22
Verdict: PASS

## Summary

Implemented an opt-in LM Studio live retry smoke harness for the SpecNode
feedback loop. The harness calls a local OpenAI-compatible `/v1/chat/completions`
endpoint for compact JSON signals, parses direct JSON or `gpt-oss`
channel-wrapped JSON, wraps responses into existing SpecNode protocol objects,
and runs the existing `run_specnode_refinement_retry_orchestration(...)`
controller.

Ordinary CI remains deterministic and does not call LM Studio. The live pytest
path is skipped unless `SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE=1` is set.

## Scope Validated

- Manual script: `scripts/specnode_live_retry_smoke.py`.
- Env-gated pytest: `tests/test_specnode_live_retry_smoke.py`.
- GitHub docs and DocC mirror updates for manual LM Studio live retry smoke.
- OpenAI-compatible response parsing for observed `gpt-oss` wrapper output.
- Two-attempt retry loop with first-pass `needs_revision`, second-pass
  `approve`, retry context propagation, and audit digest validation.

## Quality Gates

| Gate | Command | Result |
| --- | --- | --- |
| Targeted live-smoke tests | `PYTHONPATH=src python -m pytest tests/test_specnode_live_retry_smoke.py -q` | PASS, 3 passed, 1 skipped |
| Targeted docs/live tests | `PYTHONPATH=src python -m pytest tests/test_specnode_live_retry_smoke.py tests/test_docs_contracts.py -q` | PASS, 19 passed, 1 skipped |
| Tests | `PYTHONPATH=src python -m pytest` | PASS, 264 passed, 1 skipped |
| Lint | `ruff check src tests` | PASS |
| Format | `ruff format --check src tests` | PASS, 47 files already formatted |
| Coverage | `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 264 passed, 1 skipped, 90.43% total coverage |
| Swift manifest | `swift package dump-package >/dev/null` | PASS |
| Swift docs target | `swift build --target SpecHarvesterDocs` | PASS |

## Optional Live LM Studio Smoke

Executed locally against LM Studio on `http://127.0.0.1:1234` with
`openai/gpt-oss-20b`.

| Command | Result |
| --- | --- |
| `PYTHONPATH=src SPECHARVESTER_LM_STUDIO_BASE_URL=http://127.0.0.1:1234 SPECHARVESTER_SPECNODE_MODEL=openai/gpt-oss-20b python scripts/specnode_live_retry_smoke.py` | PASS, status `approved`, 2 attempts, retry context seen on attempt 2, token usage 1120 |
| `PYTHONPATH=src SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE=1 SPECHARVESTER_LM_STUDIO_BASE_URL=http://127.0.0.1:1234 SPECHARVESTER_SPECNODE_MODEL=openai/gpt-oss-20b python -m pytest tests/test_specnode_live_retry_smoke.py -q` | PASS, 4 passed |

Live script summary:

```json
{
  "attemptCount": 2,
  "attemptStatuses": ["retry_scheduled", "approved"],
  "model": "openai/gpt-oss-20b",
  "retryContextSeenByProvider": [false, true],
  "reviewVerdicts": ["needs_revision", "approve"],
  "status": "approved"
}
```

## Acceptance Criteria

- PASS: Ordinary `pytest` skips live provider calls unless
  `SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE=1` is set.
- PASS: Missing environment variables fail fast with actionable messages.
- PASS: A successful live run prints compact JSON with model, attempt count,
  statuses, verdict sequence, retry context presence, usage, and final digests.
- PASS: Direct JSON and observed `gpt-oss` channel-wrapped JSON parsing are
  covered without network.
- PASS: Unit tests do not contact the network.
- PASS: Full tests, lint, format, coverage, Swift manifest, and Swift DocC build
  pass.

## Notes

- The harness does not ask the model to author the full SpecNode audit schema.
  It calls the model for compact JSON signals and deterministically wraps those
  signals into existing validated protocol objects.
- The harness does not apply patch proposals, mutate candidate files, commit
  generated artifacts, or treat model output as accepted registry truth.
