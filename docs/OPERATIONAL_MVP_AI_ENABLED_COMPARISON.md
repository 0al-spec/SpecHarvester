# Operational MVP AI-Enabled Comparison

Status: P43-T5 live AI-enabled comparison.

P43-T5 compares the P43-T4 static-only operational MVP baseline with local
LM Studio proposal mode over the same pinned local corpus. The provider was
available, the selected model was `openai/gpt-oss-20b`, and
`autonomous-candidate-batch` produced proposal-only AI draft and enrichment
sidecars for xyflow, FastAPI, and Gin.

The durable fixture is:

```text
tests/fixtures/operational_mvp_validation/p43-t5-operational-mvp-ai-enabled-comparison.example.json
```

## Provider Gate

The comparison probed the local OpenAI-compatible model endpoint:

```bash
curl --silent --show-error --max-time 5 http://127.0.0.1:1234/v1/models
```

The probe returned:

```text
status: provider_available
exitCode: 0
provider: lm_studio
model: openai/gpt-oss-20b
```

The live batch command was:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p43-t5-operational-mvp-ai-enabled-live-20260620T071412Z/inputs --out /tmp/specharvester-p43-t5-operational-mvp-ai-enabled-live-20260620T071412Z/output --repository-profile-selection auto --lm-studio-base-url http://127.0.0.1:1234 --lm-studio-model openai/gpt-oss-20b --json-repair-max-attempts 1
```

Batch report:

```text
/tmp/specharvester-p43-t5-operational-mvp-ai-enabled-live-20260620T071412Z/output/autonomous-candidate-batch-report.json
sha256:3a677f471c18bdbabd7c80d6edcbb5af4ec80ec36ff7d325a483c87f672a8016
```

Raw prompts, raw provider responses, secrets, and chain-of-thought were not
persisted.

## Baseline Linkage

The comparison references the P43-T4 static-only baseline fixture:

```text
tests/fixtures/operational_mvp_validation/p43-t4-operational-mvp-static-only-baseline.example.json
sha256:c3913b1c42546fc4c9864e81731edf21d4798143ad703ce8968600611d3ad9f0
```

The same pinned corpus is preserved:

| Repository | Ecosystem | Static-only baseline | AI-enabled comparison |
| --- | --- | --- | --- |
| `xyflow` | JavaScript/TypeScript | passed, 4 candidates, 3 relations | draft warning, 4 enrichment proposals |
| `fastapi` | Python | passed, 1 candidate | draft warning, 1 enrichment proposal |
| `gin` | Go | passed, 1 candidate | draft warning, 1 enrichment proposal |

## Result Summary

The comparison records:

- `samePinnedCorpusAsStaticBaseline: true`;
- `providerAvailable: true`;
- `aiEnabledRunPerformed: true`;
- `aiProposalArtifactCount: 6`;
- `aiEnrichmentProposalMemberCount: 6`;
- `aiComparisonProviderUnavailableCount: 0`;
- `aiEnrichedPreviewAppliedCount: 0`;
- `providerTotalTokens: 81003`;
- `specpmHandoffChangedByAI: false`;
- `aiOutputAcceptedAsRegistryTruth: false`.

Each repository keeps its static-only handoff-ready preview result from P43-T4.
The AI delta is `ai_proposal_available_for_author_review`: AI enrichment
sidecars are available for author review, but they are not applied to accepted
SpecPM truth. The draft warning is
`ai_draft_warning_enrichment_completed`, caused by `package_set_id_missing` in
the draft proposal layer while enrichment completed cleanly.

## Proposal-Only Boundary

AI-enabled output remains proposal-only. P43-T5 does not:

- call hosted AI services;
- persist raw prompts;
- persist raw provider responses;
- persist chain-of-thought;
- clone or fetch repositories;
- accept mutable repository state;
- execute harvested code;
- install dependencies;
- invoke package managers;
- enable trusted local adapter execution;
- run adapter code;
- accept packages or relations;
- publish registry metadata;
- seed baselines;
- remove `preview_only`;
- treat AI output as registry truth;
- treat adapter output as registry truth.

Live LM Studio evidence strengthens the comparison result but does not weaken
the P43-T4 static-only baseline. Since `--apply-ai-enrichment` was not used,
AI sidecars do not change static handoff truth or SpecPM acceptance state.

## Follow-Up

- `P43-T6`: add author handoff summaries based on the static-only baseline and
  live proposal-only AI comparison state.
- `P43-T7`: record the operational MVP exit decision.

## References

- [`OPERATIONAL_MVP_VALIDATION_PLAN.md`](OPERATIONAL_MVP_VALIDATION_PLAN.md)
- [`OPERATIONAL_MVP_VALIDATION_PLAN_FIXTURE.md`](OPERATIONAL_MVP_VALIDATION_PLAN_FIXTURE.md)
- [`OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md`](OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md)
- [`OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md`](OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md)
- [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md)
- [`PACKAGE_SET_AI_DRAFT_PROPOSAL.md`](PACKAGE_SET_AI_DRAFT_PROPOSAL.md)
- [`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md)
