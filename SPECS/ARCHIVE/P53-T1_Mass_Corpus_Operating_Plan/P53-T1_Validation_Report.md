# P53-T1 Validation Report

**Task:** `P53-T1` Mass Corpus Operating Plan
**Date:** 2026-07-27
**Verdict:** PASS

## Result

P53-T1 adds a digest-bound `SpecHarvesterMassRepositoryCampaignPlan` contract
for exactly 100 new operator-curated repositories. The corpus is divided into
four immutable waves of 25. `gpt-5.3-codex-spark` is the sole campaign AI
worker; it remains a future, operator-opt-in `codex exec`, schema-validated,
proposal-only worker. LM Studio and alternate AI workers are excluded from this
campaign contract.

The contract fixes initial concurrency at two, one classified retry per source,
20,000 tokens and 300 seconds per repository, 500,000 tokens per wave, and
2,000,000 tokens and 28,800 seconds for the campaign. It requires deterministic
run identity, immutable inputs, atomic checkpoints, and idempotent resume.
P53-T7, P53-T9, and P53-T11 each unlock only the immediately following wave
after the required human-review sample and quality thresholds pass.

Post-review, the fixture also encodes the complete stop policy: quality failure,
three consecutive Codex/schema/transport failures, budget limit, input
revision/digest drift, and authority-boundary breach all stop the current wave
and block later waves.

## Evidence

- Source decision:
  `tests/fixtures/phase_52_exit_decision/p52-t9-phase-52-exit-decision.example.json`
  at `sha256:e4917bcacbc4ff7dfca45627cc01f599cf6fd0c7d4f5a9be167cd8c11018ad56`.
- New contract:
  `tests/fixtures/mass_repository_campaign_plan/p53-t1-mass-repository-campaign-plan.example.json`.
- Operator documentation:
  `docs/MASS_REPOSITORY_CAMPAIGN_PLAN.md` and its DocC counterpart.

## Checks

```text
python -m json.tool tests/fixtures/mass_repository_campaign_plan/
  p53-t1-mass-repository-campaign-plan.example.json >/dev/null
PASS

PYTHONPATH=src python -m pytest -q tests/test_docs_contracts.py -k mass_repository_campaign_plan -x
1 passed, 195 deselected

PYTHONPATH=src python -m pytest -q tests/test_docs_contracts.py -x
196 passed

PYTHONPATH=src python -m pytest
969 passed, 1 skipped

PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
969 passed, 1 skipped; total coverage 90.01%

ruff check src tests
PASS

ruff format --check src tests
141 files already formatted

swift package dump-package >/dev/null
PASS

swift build --target SpecHarvesterDocs
PASS; existing unhandled DocC-directory warning only

git diff --check
PASS
```

`make check-workplan-summary` was not run because this repository has no
`Makefile` or such target; the same absence is recorded in the P52-T10
historical review artifact.

## Boundaries

P53-T1 did not create or restore checkouts, clone or fetch repositories,
install dependencies, invoke package managers, execute harvested code, run
adapters, run Codex, or run AI. It did not accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, or treat
planning, static, or AI output as registry truth.

Raw prompts, raw provider responses, secrets, session state, stdout/stderr,
and chain-of-thought were not persisted.
