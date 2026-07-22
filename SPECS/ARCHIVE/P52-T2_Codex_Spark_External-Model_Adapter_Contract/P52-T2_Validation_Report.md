# P52-T2 Validation Report

**Task:** `P52-T2` Codex Spark External-Model Adapter Contract
**Date:** 2026-07-22
**Verdict:** PASS

## Scope

P52-T2 defines the future external `gpt-5.3-codex-spark` proposal-worker
contract. It adds a durable contract fixture, strict final-message JSON Schema,
GitHub and DocC documentation, and regression coverage for the existing
external `package-set-ai-draft-proposal --model-output` handoff.

No `codex exec` or AI request was run. The task did not create, restore, clone,
or fetch repositories; install dependencies; invoke package managers; execute
harvested code or adapters; accept packages or relations; publish registry
metadata; seed baselines; remove `preview_only`; or treat output as registry
truth.

## Evidence Recorded

- Planning authority: P52-T1 fixture, digest
  `sha256:2455aa8b9c6441b17c38481e10e4c9e2fa5ecace2779e90fed686734eaa5799f`.
- Contract fixture:
  `tests/fixtures/codex_spark_external_model_adapter_contract/p52-t2-codex-spark-external-model-adapter-contract.example.json`.
- Final-message schema:
  `tests/fixtures/codex_spark_external_model_adapter_contract/package-set-ai-draft-final-message.schema.json`, digest
  `sha256:d40b941f03b95c63c0dd241f78631706b96daee9885bc571c7d628c134493128`.
- Future invocation policy: `codex exec`, selected Spark model, read-only
  sandbox, ephemeral state, ignored user configuration, generated evidence
  stage, JSON Schema output, and a last-message file.
- Rejection policy: no repair or automatic retry after non-zero exit, timeout,
  missing/invalid final message, policy drift, receipt mismatch, or handoff
  failure.
- Privacy policy: raw prompts, raw provider responses, secrets, session state,
  and chain-of-thought are not persisted.

## Checks

- `python -m json.tool tests/fixtures/codex_spark_external_model_adapter_contract/package-set-ai-draft-final-message.schema.json >/dev/null`
  - PASS
- `python -m json.tool tests/fixtures/codex_spark_external_model_adapter_contract/p52-t2-codex-spark-external-model-adapter-contract.example.json >/dev/null`
  - PASS
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -k 'codex_spark_external_model_adapter_contract or controlled_repository_corpus_plan' -q`
  - PASS: `2 passed, 188 deselected`
- `PYTHONPATH=src python -m pytest`
  - PASS: `922 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `922 passed, 1 skipped`, total coverage `90.53%`, threshold `90%`
- `ruff check src tests`
  - PASS
- `ruff format --check src tests`
  - PASS: `131 files already formatted`
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS
- `git diff --check`
  - PASS

## Result

P52-T2 passes. The external-model boundary is now concrete and testable, but
remains inactive. P52-T3 is the next task: it must acquire five
operator-provided pinned local checkouts and run the bounded static-versus-Spark
calibration under this contract.
