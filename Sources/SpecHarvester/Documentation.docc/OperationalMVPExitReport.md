# Operational MVP Exit Report

Status: P43-T7 exit report.

P43-T7 records the Phase 43 exit decision. It uses the P43-T4 static-only
baseline, the P43-T5 AI comparison gate, and the P43-T6 author handoff
summaries to decide whether SpecHarvester is ready for broader autonomous
popular-library scraping, needs quality hardening first, or is blocked until an
explicitly approved adapter execution phase.

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
sha256:c9934bae637aff8d748e431476d297dc58f81583ab7fdb8fc00db1141889e049

tests/fixtures/operational_mvp_validation/p43-t6-operational-mvp-author-handoff-summaries.example.json
sha256:0cf13f0a4349cefa5f0d5268d7c88d4d519ecfaf944e689005ae3db1a1f2bd96
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

- P43-T5 recorded `provider_unavailable`, so no proposal-only AI deltas were
  measured.
- P43-T6 keeps xyflow's
  `resolve_or_accept_partial_public_interface_index` manual-correction item.
- P43-T6 records `doNotPromote` guidance for every repository.

## Rejected Alternatives

`ready_for_bounded_autonomous_scraping` is rejected for now. The pipeline needs
targeted quality hardening, a rerun of the AI-enabled comparison when a local
provider is available or an explicit static-only acceptance, and a bounded
popular-library batch gate.

`blocked_until_adapter_execution` is also rejected. P43-T4 and P43-T6 produced
author-reviewable static-only handoff material, so the current Phase 43 result
does not require trusted local adapter execution.

## Quality Hardening Plan

- `burn_down_xyflow_partial_public_interface_index`
- `rerun_ai_enabled_comparison_when_provider_available`
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

- <doc:OperationalMVPValidationPlan>
- <doc:OperationalMVPStaticOnlyBaseline>
- <doc:OperationalMVPAIEnabledComparison>
- <doc:OperationalMVPAuthorHandoffSummaries>
- <doc:AutonomousCandidateBatch>
