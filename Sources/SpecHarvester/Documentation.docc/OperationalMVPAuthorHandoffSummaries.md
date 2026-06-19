# Operational MVP Author Handoff Summaries

Status: P43-T6 author handoff summaries.

P43-T6 translates the P43-T4 static-only baseline and P43-T5 AI comparison gate
into author-facing handoff summaries. The summaries show what is valid, what
is reviewable, what needs manual correction, and what should not be promoted.

The durable fixture is:

```text
tests/fixtures/operational_mvp_validation/p43-t6-operational-mvp-author-handoff-summaries.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.operational-mvp-author-handoff/v0
kind: SpecHarvesterOperationalMVPAuthorHandoffSummaries
authority: producer_operational_mvp_author_handoff_only
```

## Source Evidence

The handoff summary references:

```text
tests/fixtures/operational_mvp_validation/p43-t4-operational-mvp-static-only-baseline.example.json
sha256:39e623bb3eb835ef1e57286bd6d06394c4fe62fd594e3f756e18f96a4c9ea3ab

tests/fixtures/operational_mvp_validation/p43-t5-operational-mvp-ai-enabled-comparison.example.json
sha256:c9934bae637aff8d748e431476d297dc58f81583ab7fdb8fc00db1141889e049
```

## Handoff Categories

Each repository records four author categories:

- `valid`: generated preview candidates passed static-only preflight, have an
  `author_ready_draft` verdict, and are ready for author review.
- `reviewable`: author must confirm package identity, summary, capabilities,
  intents, constraints, evidence support, and downstream SpecPM validation.
- `needsManualCorrection`: repository-specific caveats that need manual
  inspection before relying on the output.
- `doNotPromote`: preview candidates, AI deltas, and adapter output must not be
  promoted without explicit SpecPM maintainer review.

## Corpus Handoff

| Repository | Handoff verdict | Valid | Reviewable | Needs manual correction | Do not promote |
| --- | --- | ---: | ---: | ---: | ---: |
| `xyflow` | `ready_for_author_review` | 3 | 3 | 1 | 3 |
| `fastapi` | `ready_for_author_review` | 3 | 3 | 0 | 3 |
| `gin` | `ready_for_author_review` | 3 | 3 | 0 | 3 |

The xyflow manual correction item is
`resolve_or_accept_partial_public_interface_index`, which asks the author to
inspect the partial public-interface index diagnostics before relying on
generated interface evidence.

## AI Comparison State

P43-T5 recorded `provider_unavailable`, so no AI improvement is available in
this handoff. Each repository records:

```text
aiImprovementAvailable: false
warningCode: ai_provider_unavailable_static_baseline_retained
deltaStatus: not_evaluated_provider_unavailable
```

The static-only handoff remains usable for author review; it is not upgraded by
AI and is not registry acceptance.

## Non-Authority Boundary

This handoff is producer-side review evidence only. It does not:

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
- treat handoff output as registry truth.

## Follow-Up

- `P43-T7`: record the operational MVP exit decision.

## References

- <doc:OperationalMVPValidationPlan>
- <doc:OperationalMVPStaticOnlyBaseline>
- <doc:OperationalMVPAIEnabledComparison>
- <doc:AuthorReadyDraftQualityReport>
