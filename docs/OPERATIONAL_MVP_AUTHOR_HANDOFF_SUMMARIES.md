# Operational MVP Author Handoff Summaries

Status: P43-T6 author handoff summaries.

P43-T6 translates the P43-T4 static-only baseline and P43-T5 live
proposal-only AI comparison gate into author-facing handoff summaries. The
summaries show what is valid, what is reviewable, what needs manual
correction, and what should not be promoted.

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
sha256:c3913b1c42546fc4c9864e81731edf21d4798143ad703ce8968600611d3ad9f0

tests/fixtures/operational_mvp_validation/p43-t5-operational-mvp-ai-enabled-comparison.example.json
sha256:cd03f8486a7cb9bd1dcf6efde1c7660ce6f63457a082207b1e81ee62ff5e327a
```

## Handoff Categories

Each repository records four author categories:

- `valid`: generated preview candidates passed static-only preflight, have an
  `author_ready_draft` verdict, and are ready for author review.
- `reviewable`: author must confirm package identity, summary, capabilities,
  intents, constraints, evidence support, and downstream SpecPM validation.
- `needsManualCorrection`: repository-specific caveats that need manual
  inspection before relying on the output.
- `doNotPromote`: preview candidates, AI proposal sidecars, and adapter output
  must not be promoted without explicit SpecPM maintainer review.

## Corpus Handoff

| Repository | Handoff verdict | Valid | Reviewable | Needs manual correction | Do not promote |
| --- | --- | ---: | ---: | ---: | ---: |
| `xyflow` | `ready_for_author_review` | 3 | 3 | 2 | 3 |
| `fastapi` | `ready_for_author_review` | 3 | 3 | 0 | 3 |
| `gin` | `ready_for_author_review` | 3 | 3 | 0 | 3 |

The xyflow manual correction items are
`resolve_or_accept_partial_public_interface_index`, which asks the author to
inspect the partial public-interface index diagnostics before relying on
generated interface evidence, and `review_operator_checkout_origin_fork_mismatch`,
which asks the author to confirm whether evidence from the SoundBlaster fork is
acceptable for canonical xyflow package review.

## AI Comparison State

P43-T5 recorded live local LM Studio proposal-only AI evidence. Each
repository records:

```text
status: completed_with_draft_warnings
aiImprovementAvailable: true
warningCode: ai_draft_warning_enrichment_completed
deltaStatus: ai_proposal_available_for_author_review
```

The static-only handoff remains usable for author review. AI proposal sidecars
are review evidence only and are not registry acceptance.

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

- [`OPERATIONAL_MVP_VALIDATION_PLAN.md`](OPERATIONAL_MVP_VALIDATION_PLAN.md)
- [`OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md`](OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md)
- [`OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md`](OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md)
- [`AUTHOR_READY_DRAFT_QUALITY_REPORT.md`](AUTHOR_READY_DRAFT_QUALITY_REPORT.md)
