# P52-T4 Validation Report

**Task:** `P52-T4` Twenty-Repository Controlled Pilot
**Date:** 2026-07-22
**Verdict:** PASS

## Live Result

- Static-only baseline completed for 20/20 clean pinned public checkouts.
- LM Studio `openai/gpt-oss-20b` completed 20/20 proposal-only controls after
  the operator set `logSensitiveData` to `false`.
- Codex `gpt-5.3-codex-spark` completed 20/20 calls with exit code `0` and
  schema-valid final messages.
- Static completion, Codex completion, schema validity, and repository
  specificity were each 100%; unsupported claim rate was 0%.
- Ten digest-bound author-review records were supported; the finalized decision
  is `unlock_p52_t5`.

## Boundaries

No repositories were cloned, fetched, restored, or modified. No dependencies,
package managers, harvested code, or adapters were executed. All model output
remains proposal-only. Durable artifacts contain no raw prompts, raw model
responses, Codex stdout/stderr, session state, secrets, or chain-of-thought.

## Checks

- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `937 passed, 1 skipped`, coverage `90.12%`.
- `ruff check src tests` - PASS.
- `ruff format --check src tests` - PASS.
- `swift package dump-package >/dev/null` - PASS.
- `swift build --target SpecHarvesterDocs` - PASS with the existing DocC
  directory warning.
- `python -m json.tool tests/fixtures/twenty_repository_controlled_pilot/p52-t4-twenty-repository-controlled-pilot.example.json >/dev/null` - PASS.
- `git diff --check` - PASS.
