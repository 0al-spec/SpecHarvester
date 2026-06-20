# Operational MVP Exit Report

Status: P43-T7 exit report.

P43-T7 records the Phase 43 exit decision. It uses the P43-T4 static-only
baseline, the P43-T5 live proposal-only AI comparison gate, and the P43-T6
author handoff summaries to decide whether SpecHarvester is ready for broader
autonomous popular-library scraping, needs quality hardening first, or is
blocked until an explicitly approved adapter execution phase.

The durable fixture is:

```text
tests/fixtures/operational_mvp_validation/p43-t7-operational-mvp-exit-report.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.operational-mvp-exit-report/v0
kind: SpecHarvesterOperationalMVPExitReport
authority: producer_operational_mvp_exit_report_only
```

## Source Evidence

The exit report references:

```text
tests/fixtures/operational_mvp_validation/p43-t4-operational-mvp-static-only-baseline.example.json
sha256:39e623bb3eb835ef1e57286bd6d06394c4fe62fd594e3f756e18f96a4c9ea3ab

tests/fixtures/operational_mvp_validation/p43-t5-operational-mvp-ai-enabled-comparison.example.json
sha256:1ad9d2b59bd17dfd50d0abd9fc481883d03dacaf3ebe8f717a064b91be58052d

tests/fixtures/operational_mvp_validation/p43-t6-operational-mvp-author-handoff-summaries.example.json
sha256:7e1ccf38f662529777344f3b82c886572538a55190093ca70170c0a6ee349ca9
```

## Decision

Selected decision:

```text
needs_quality_hardening
```

The static-only pipeline produced useful author-reviewable preview output for
xyflow, FastAPI, and Gin:

- 3 repository results
- 6 preview candidates passing preflight
- 3 relation proposals
- 3 author-ready draft verdicts
- 3 handoff-ready summaries

That is enough to prove the producer loop is useful. It is not enough to
approve broader autonomous popular-library scraping because:

- P43-T5 recorded `completed_with_draft_warnings`; the live AI layer produced
  proposal-only enrichment evidence, but each repository retained
  `ai_draft_warning_enrichment_completed`.
- P43-T6 keeps xyflow's
  `resolve_or_accept_partial_public_interface_index` manual-correction item.
- P43-T6 records `doNotPromote` guidance for every repository.

## Rejected Alternatives

`ready_for_bounded_autonomous_scraping` is rejected for now. The pipeline needs
targeted quality hardening, triage of AI draft warnings and proposal quality,
and a bounded popular-library batch gate.

`blocked_until_adapter_execution` is also rejected. P43-T4 and P43-T6 produced
author-reviewable static-only handoff material, so the current Phase 43 result
does not require trusted local adapter execution.

## Quality Hardening Plan

- `burn_down_xyflow_partial_public_interface_index`
- `triage_ai_draft_warnings_and_proposal_quality`
- `define_bounded_popular_library_batch_gate`

## Non-Authority Boundary

This exit report is producer-side review evidence only. It does not:

- approve broader autonomous scraping;
- accept packages or relations;
- publish registry metadata;
- seed baselines;
- remove `preview_only`;
- run AI;
- enable trusted local adapter execution;
- clone or fetch repositories;
- install dependencies;
- invoke package managers;
- execute harvested code;
- treat AI output as registry truth;
- treat adapter output as registry truth;
- treat exit-report output as registry truth.

## Follow-Up

Phase 43 is complete after this report. The recommended next direction is
quality hardening before bounded popular-library scraping.

## References

- [`OPERATIONAL_MVP_VALIDATION_PLAN.md`](OPERATIONAL_MVP_VALIDATION_PLAN.md)
- [`OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md`](OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md)
- [`OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md`](OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md)
- [`OPERATIONAL_MVP_AUTHOR_HANDOFF_SUMMARIES.md`](OPERATIONAL_MVP_AUTHOR_HANDOFF_SUMMARIES.md)
- [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md)
