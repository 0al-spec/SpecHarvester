# P52-T3 Validation Report

**Task:** `P52-T3` Five-Repository Controlled Calibration
**Date:** 2026-07-22
**Verdict:** PASS

## Scope

P52-T3 runs the first live Phase 52 calibration over exactly five
operator-provided pinned local checkouts: Flask, Gin, xyflow, FastAPI, and
FastMCP. It records a static-only baseline before two proposal-only controls:
LM Studio `openai/gpt-oss-20b` using request-side JSON Schema output, and
`gpt-5.3-codex-spark` through the P52-T2 read-only external-model handoff.

The task did not clone, fetch, restore, or modify repositories; install
dependencies; invoke package managers; execute harvested code or adapters;
accept packages or relations; publish registry metadata; seed baselines; remove
`preview_only`; or make static or model output registry truth.

## Live Evidence

- Input manifest:
  `inputs/p52-five-repository-calibration/repositories.yml`.
- Durable report:
  `tests/fixtures/controlled_calibration/p52-t3-five-repository-controlled-calibration.example.json`.
- Report digest:
  `sha256:9d33c7fec360f131eb564d83815ee6c2ba628fec9a16e1801ea6f990250b85bf`.
- Static-only baseline: passed for all five repositories before either model
  control was invoked.
- LM Studio control: completed 13 proposal calls with
  `response_format.type: json_schema`; 122,284 prompt tokens, 5,076 completion
  tokens, and 127,360 total tokens. Flask, Gin, and FastAPI retain
  proposal-level warning diagnostics for review; no warning changed registry
  state.
- Codex Spark control: all five calls returned exit code `0`, schema-valid
  final messages, repository-specific proposals, and zero unsupported claims.
  Recorded total duration: 144,923 ms.
- Quality result: static completion `5/5`, Codex completion `5/5`, schema
  validity `5/5`, repository specificity `5/5`, unsupported claims `0/5`.
  All Phase 52 thresholds passed and P52-T4 is unlocked.

The first bounded Codex attempt returned schema-valid but empty selections for
Flask and Gin. The runner was hardened to require one selected inventory package
for a non-empty P52 inventory, then the entire five-repository calibration was
rerun. The durable report contains the final passing rerun only.

## Privacy And Authority

SpecHarvester durable artifacts contain no raw prompts, raw model responses,
Codex stdout/stderr, session state, secrets, or chain-of-thought. The runner
deletes its temporary Codex evidence stage, final message, and handoff files.

This is not a claim about an external provider's own logs. LM Studio server
logging is operator-managed and must be disabled separately before treating a
future live run as provider-log-clean. The P52 report explicitly scopes its
privacy fields to SpecHarvester durable artifacts.

## Checks

- `python -m json.tool tests/fixtures/controlled_calibration/p52-t3-five-repository-controlled-calibration.example.json >/dev/null`
  - PASS
- `PYTHONPATH=src python -m pytest tests/test_controlled_calibration.py tests/test_package_set_ai_draft_proposal.py tests/test_package_set_ai_enrichment.py tests/test_docs_contracts.py -q`
  - PASS: `240 passed`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `931 passed, 1 skipped`, total coverage `90.16%`, threshold `90%`
- `ruff check src tests`
  - PASS
- `ruff format --check src tests`
  - PASS: `133 files already formatted`
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS; Swift emits its existing unhandled DocC-directory warning.
- `git diff --check`
  - PASS

## Result

P52-T3 passes. The live Phase 52 integration now has five-repository evidence
that the static baseline, LM Studio JSON Schema control, and schema-validated
Codex proposal-only handoff work together without granting registry authority.
The next task is P52-T4, the twenty-repository controlled pilot, subject to the
same external provider logging precondition.

## Post-Review Correction

External PR review added two source-integrity corrections before merge:

- `--skip-codex` no longer loads or validates the Codex final-message schema;
  an offline diagnostic run can write its blocked report without a Codex schema.
- Every P52 checkout must now be clean under `git status --porcelain`, including
  staged, unstaged, and untracked paths, before static collection begins.

The correction passed focused coverage and documentation checks, then
`PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
`933 passed, 1 skipped`, total coverage `90.09%`.
