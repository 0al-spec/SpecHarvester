# Mass Popular Repository Campaign Plan

Status: P53-T1 plan.

P53-T1 defines the operating contract for a 100-repository campaign. It is a
planning artifact, not a scrape, checkout acquisition, static run, Codex run,
AI run, or registry decision.

The durable contract is:

```text
tests/fixtures/mass_repository_campaign_plan/
  p53-t1-mass-repository-campaign-plan.example.json
```

Its identity is `SpecHarvesterMassRepositoryCampaignPlan` at
`spec-harvester.mass-repository-campaign-plan/v0` with authority
`producer_planning_evidence_only`.

## Starting Point

The contract binds to the digest of the P52-T9 exit decision. That decision
selected `go_with_guardrails_for_maintainer_disposition`; it made prior evidence
available for maintainer review, but did not approve corpus expansion, registry
promotion, package acceptance, or relation acceptance.

P52 remains reference/canary evidence and is not counted among the 100 new
repositories. Each future source must be an operator-provided pinned local
checkout selected through the later P53-T3 manifest task.

## Worker And Waves

`gpt-5.3-codex-spark` is the sole campaign AI worker. It is invoked through
`codex exec` using the existing schema-validated external-model-output boundary
and produces proposal-only results. LM Studio is not a campaign worker, and no
alternative AI worker is permitted by this plan.

The campaign has four sequential waves of 25:

```text
1-25   P53-T6 wave 1
26-50  P53-T8 wave 2, only after P53-T7
51-75  P53-T10 wave 3, only after P53-T9
76-100 P53-T12 wave 4, only after P53-T11
```

P53-T7 requires five reviewed candidates. P53-T9 and P53-T11 each require
three. Each decision unlocks only the immediately following range, rather than
the rest of the campaign.

## Operating Limits

The initial runtime limit is at most 2 workers. The future P53-T2 orchestrator
must use deterministic run identities, immutable input digests, atomic
checkpoints, and idempotent resume; completed repositories are never rerun.
It may make at most one classified retry per repository.

| Budget | Maximum |
| --- | ---: |
| Per repository | 20,000 tokens and 300 seconds |
| Per wave | 500,000 tokens |
| Campaign | 2,000,000 tokens and 28,800 seconds |

The campaign stops before its total budget is exceeded. It also stops the
current wave and blocks later waves on a quality failure, three consecutive
Codex/schema/transport failures, input drift, or an authority-boundary breach.

Quality thresholds are static completion at least 98%, Codex completion at
least 95%, schema validity at least 99%, repository specificity at least 90%,
and unsupported claims at most 2%. The aggregate manual review minimum is 15
candidates.

## Boundaries

P53-T1 did not create or restore checkouts, clone or fetch repositories,
install dependencies, invoke package managers, execute harvested code, run
adapters, run Codex, or run AI. It did not accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, or treat
planning, static, or AI output as registry truth.

Raw prompts, raw provider responses, secrets, session state, stdout/stderr,
and chain-of-thought are not persisted. The only durable model-related
artifacts allowed in later tasks are sanitized final proposals, validation
diagnostics, digests, and bounded usage receipts.
