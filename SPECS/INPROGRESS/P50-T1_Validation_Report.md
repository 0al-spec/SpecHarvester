# P50-T1 Validation Report

Task: `P50-T1` Record Restored-Checkout Rerun Evidence
Date: 2026-06-25
Verdict: PASS

## Scope

P50-T1 records restored-checkout rerun evidence for the same six-repository
P46 bounded pilot scope after the operator-local checkout paths were restored
through symlinks.

The task adds durable producer evidence, GitHub and DocC documentation, current
planning state updates, and docs-contract coverage. It does not change runtime
batch behavior, accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, clone/fetch repositories, install
dependencies, invoke package managers, execute harvested code, run adapters, or
treat AI/static/rerun/follow-up/exit-decision/adapter output as registry truth.

## Evidence Recorded

- Restored checkout paths: six operator-local symlinks under
  `/Users/egor/Development/GitHub/0AL/`.
- Source scope:
  `inputs/p46-bounded-popular-library-pilot/repositories.yml`.
- Static-only rerun report:
  `sha256:cc1a51ab0e033700ad5813b85bae4d74a79ba1efcd9bbd2eb6237a50bedbd988`.
- AI-enabled rerun report:
  `sha256:30d69b30794886df2753e2549dfff1ef00a05edacd92b3f0040eab4df0d9d3a6`.
- Static-only result: `passed`, processed `6`, failed `0`, passed preflight
  `6`.
- AI-enabled result: `passed`, processed `6`, failed `0`, passed preflight
  `6`, AI draft proposals `6`, AI enrichment proposals `6`.
- Provider: LM Studio `openai/gpt-oss-20b`.
- AI token totals: prompt `107251`, completion `4005`, total `111256`.
- Raw prompts, raw provider responses, secrets, and chain-of-thought were not
  persisted.

## Checks

- `python3 -m json.tool tests/fixtures/restored_checkout_rerun_evidence/p50-t1-restored-checkout-rerun-evidence.example.json`
  - PASS
- `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "restored_checkout_rerun_evidence or docc2context_follow_up_exit_decision"`
  - PASS: `2 passed, 178 deselected`
- `python3 -m ruff format tests/test_docs_contracts.py`
  - PASS: mechanically reformatted the new test after the first format check
    requested reformatting
- `python3 -m ruff format --check src tests`
  - PASS: `131 files already formatted`
- `python3 -m ruff check src tests`
  - PASS: `All checks passed!`
- `PYTHONPATH=src python3 -m pytest`
  - PASS: `911 passed, 1 skipped`
- `PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `911 passed, 1 skipped`, total coverage `90.48%`, required coverage
    `90%`
- `swift package describe`
  - PASS
- `swift package dump-package`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS
- `swift package --allow-writing-to-directory .build/docs generate-documentation --target SpecHarvester --output-path .build/docs`
  - PASS
- `git diff --check`
  - PASS

## Environment Notes

The first coverage attempt failed before tests started because the local Python
environment did not have the `pytest-cov` plugin. `coverage==7.10.7` and
`pytest-cov==6.1.1` were installed in the user Python environment from the
official PyPI index, then the configured coverage gate passed. An attempted
`pytest-cov==5.0.0` install was rejected because pip reported a wheel hash
mismatch; that artifact was not used.

## Result

P50-T1 is complete. The checkout blocker recorded by P49-T4 is resolved by new
post-restore evidence, and the current state is
`larger_corpus_planning_reconsideration_ready_after_restored_checkout_rerun`.
This is planning readiness only, not registry authority or package/relation
acceptance.
