## REVIEW REPORT — P14-T1 LM Studio Live Retry Smoke

**Scope:** `origin/main..HEAD`
**Files:** 10
**Date:** 2026-05-22

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

- None.

### Secondary Issues

- None.

### Architectural Notes

- The live smoke remains opt-in and outside ordinary CI. Default test execution
  skips the LM Studio path unless `SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE=1`
  is set.
- The script uses LM Studio only for compact JSON signals, then deterministically
  wraps those signals into existing SpecNode protocol objects. This avoids
  letting a weak model author the full audit schema directly.
- The provider base URL is restricted to local hosts (`localhost`, `127.0.0.1`,
  `::1`) and rejects paths, query strings, and fragments to avoid turning a
  manual smoke helper into an arbitrary network client.
- The two-attempt smoke proves feedback-loop plumbing: first review schedules a
  retry, the second provider call sees `SpecNodeRetryContext`, and the final run
  validates as `approved`.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_specnode_live_retry_smoke.py -q` — PASS, 6 passed, 1 skipped.
- `PYTHONPATH=src python -m pytest tests/test_specnode_live_retry_smoke.py tests/test_docs_contracts.py -q` — PASS, 22 passed, 1 skipped.
- `PYTHONPATH=src python -m pytest` — PASS, 267 passed, 1 skipped.
- `ruff check src tests` — PASS.
- `ruff format --check src tests` — PASS.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` — PASS, 267 passed, 1 skipped, 90.43% total coverage.
- `swift package dump-package >/dev/null` — PASS.
- `swift build --target SpecHarvesterDocs` — PASS.
- Manual LM Studio script against `http://127.0.0.1:1234` / `openai/gpt-oss-20b` — PASS, status `approved`, 2 attempts.
- Env-gated live pytest against LM Studio — PASS, 7 passed.

### Next Steps

- FOLLOW-UP skipped: no actionable findings were found.
- Keep this live path manual unless a future task introduces a dedicated
  provider-runtime test environment.
