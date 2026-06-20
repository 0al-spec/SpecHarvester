# P43-T7 Validation Report

Task: Operational MVP Exit Report

Status: PASS

## Scope

P43-T7 records the Phase 43 exit decision using P43-T4 static-only baseline
evidence, P43-T5 live proposal-only AI comparison evidence, and P43-T6 author
handoff evidence.

Selected decision:

```text
needs_quality_hardening
```

The report rejects immediate `ready_for_bounded_autonomous_scraping` because
the live AI-enabled comparison still has draft warnings, AI sidecars remain
proposal-only and unapplied, and xyflow retains manual-correction caveats. It
rejects `blocked_until_adapter_execution` because useful author-reviewable
static-only handoff material exists and the current Phase 43 result does not
require trusted local adapter execution.

## Artifacts

- `tests/fixtures/operational_mvp_validation/p43-t7-operational-mvp-exit-report.example.json`
- `docs/OPERATIONAL_MVP_EXIT_REPORT.md`
- `Sources/SpecHarvester/Documentation.docc/OperationalMVPExitReport.md`
- Documentation and DocC navigation links in capabilities, roadmap,
  validation plan, and author handoff summary docs.
- Contract coverage in `tests/test_docs_contracts.py`.

## Fixture Evidence

- Fixture API: `spec-harvester.operational-mvp-exit-report/v0`
- Fixture kind: `SpecHarvesterOperationalMVPExitReport`
- Fixture authority: `producer_operational_mvp_exit_report_only`
- Fixture digest:
  `sha256:8630da1e0ad387e37d2133441bfba39de1328868ed53fcaffbf509ce74f5e384`
- Source static baseline digest:
  `sha256:c3913b1c42546fc4c9864e81731edf21d4798143ad703ce8968600611d3ad9f0`
- Source AI comparison digest:
  `sha256:cd03f8486a7cb9bd1dcf6efde1c7660ce6f63457a082207b1e81ee62ff5e327a`
- Source author handoff digest:
  `sha256:53daf55c0afd5721d773cb3e0126dd2467f0cbfe247d0f429844845085fba6bd`

## Decision Evidence

- Static-only author-reviewable output exists for 3 repositories.
- Static-only preflight passed for 6 preview candidates.
- P43-T5 recorded live local LM Studio proposal-only AI evidence with
  `completed_with_draft_warnings`.
- P43-T6 kept xyflow's `resolve_or_accept_partial_public_interface_index` and
  `review_operator_checkout_origin_fork_mismatch` manual-correction items
  visible.
- Adapter execution remains disabled and is not required for the current exit
  decision.
- The report does not approve broader autonomous scraping or grant registry
  authority.

## Validation Commands

```bash
python3 -m json.tool tests/fixtures/operational_mvp_validation/p43-t7-operational-mvp-exit-report.example.json >/dev/null
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'operational_mvp_exit_report or current_next_task'
ruff format src tests
PYTHONPATH=src python -m pytest
ruff check src tests
ruff format --check src tests
swift package dump-package >/dev/null
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
swift build --target SpecHarvesterDocs
git diff --check
```

## Validation Outcomes

- JSON fixture validation: PASS
- Targeted docs contract test: PASS (`1 passed, 151 deselected`)
- Full pytest: PASS (`865 passed, 1 skipped`)
- Ruff lint: PASS
- Ruff format check: PASS (`131 files already formatted`)
- Swift package manifest: PASS
- Coverage gate: PASS (`90.49%`, required `90%`)
- Swift DocC target build: PASS
- Whitespace diff check: PASS

## Decision

P43-T7 is complete and ready to archive. Phase 43 should be marked complete
after archive, with the recommended next direction recorded as quality
hardening before bounded popular-library scraping.
