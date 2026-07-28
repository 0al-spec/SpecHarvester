# P53-T13 Validation Report

**Task:** `P53-T13` Campaign Quality Triage
**Date:** 2026-07-28
**Verdict:** PASS

## Campaign Result

The machine-readable triage accounts for exactly 100 unique frozen Phase 53
repositories across four waves of 25.

| Measure | Result |
| --- | ---: |
| Repositories accounted for | `100 / 100` |
| Selected for author review | `100` |
| Deferred | `0` |
| Do not promote | `0` |
| Static completion | `100%` |
| Codex completion | `100%` |
| Schema valid | `100%` |
| Repository specific | `100%` |
| Unsupported claim rate | `0%` |
| Aggregate recorded duration | `1,856,358 ms` |

Actual token counts are not present in Codex worker receipts. The triage records
this as `not_reported_by_worker_receipts` and preserves the configured
`2,000,000` campaign and `20,000` per-repository token ceilings without
presenting either ceiling as actual usage.

## Evidence Restoration and Corrections

The original P53-T6 and P53-T12 full reports had been retained only under
temporary roots that no longer existed. Both exact pinned waves were rerun with
`gpt-5.3-codex-spark`, concurrency two, read-only ephemeral Codex execution,
and no LM Studio worker.

- Restored wave 4 passed directly with `25 / 25` completed outcomes.
- Restored wave 1 produced `24 / 25` direct completions. The only new terminal
  outcome was `ggml-org-llama-cpp` with `package_set_id_mismatch`.
- One explicit targeted rerun of `ggml-org-llama-cpp` then completed,
  schema-valid and repository-specific, with zero unsupported claims.
- The prior explicit `bitcoin-bitcoin` corrective decision remains part of the
  effective campaign evidence.
- Both original outcomes and both correction records remain visible in the
  aggregate audit trail.

The pre-restoration checkout scan observed `99 / 100` clean checkouts.
`kdn251-interviews` in wave 3 contained a modified `.DS_Store`. T13 did not
modify or rerun that checkout; it consumed the immutable committed
`P53-T10_Wave_3_Report.json` generated when the P53-T10 source gate passed.

## Durable Artifacts

- `SPECS/EVIDENCE/P53-T13/P53-T13_Campaign_Quality_Triage.json`
- `SPECS/EVIDENCE/P53-T13/P53-T6_Wave_1_Restored_Report.json`
- `SPECS/EVIDENCE/P53-T13/P53-T12_Wave_4_Restored_Report.json`
- `SPECS/EVIDENCE/P53-T13/P53-T13_GGML_Corrective_Decision.json`
- `SPECS/EVIDENCE/P53-T13/P53-T13_GGML_Corrective_Outcome.json`
- `SPECS/EVIDENCE/P53-T13/P53-T13_GGML_Corrected_Proposal.json`
- `SPECS/EVIDENCE/P53-T13/P53-T13_GGML_Targeted_Static_Record.json`

All durable artifacts are sanitized proposal-only evidence. Raw prompts,
provider responses, secrets, session state, stdout/stderr, and chain-of-thought
were not persisted.

## Validation

- `PYTHONPATH=src .venv/bin/pytest`: `1038 passed, 1 skipped`.
- `PYTHONPATH=src .venv/bin/pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90`:
  passed at `90.00%`.
- `.venv/bin/ruff check src tests`: passed.
- `.venv/bin/ruff format --check src tests`: passed.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed.
- Live aggregate CLI: `status: passed`, 100 unique dispositions, all quality
  thresholds passed.

## Boundary

P53-T13 provides producer triage evidence only. It does not accept packages or
relations, mutate registry truth, publish registry metadata, remove
`preview_only`, or perform maintainer disposition. P53-T14 remains required for
portable author handoff and SpecPM intake preflight.
