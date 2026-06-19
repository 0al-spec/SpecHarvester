# Operational MVP AI-Enabled Comparison

Status: P43-T5 provider-unavailable comparison.

P43-T5 compares the P43-T4 static-only operational MVP baseline with
AI-enabled proposal mode over the same pinned local corpus. The configured
local OpenAI-compatible provider was unavailable, so no AI proposal run was
performed and no deltas were claimed.

The durable fixture is:

```text
tests/fixtures/operational_mvp_validation/p43-t5-operational-mvp-ai-enabled-comparison.example.json
```

## Provider Gate

The comparison probed the local OpenAI-compatible model endpoint:

```bash
curl --silent --show-error --max-time 2 http://127.0.0.1:1234/v1/models
```

The probe returned:

```text
status: provider_unavailable
exitCode: 7
```

Because the provider was unavailable, P43-T5 did not run
`autonomous-candidate-batch` without `--skip-ai`, did not select a model, did
not persist raw prompts or raw provider responses, and did not create AI
proposal artifacts.

## Baseline Linkage

The comparison references the P43-T4 static-only baseline fixture:

```text
tests/fixtures/operational_mvp_validation/p43-t4-operational-mvp-static-only-baseline.example.json
sha256:39e623bb3eb835ef1e57286bd6d06394c4fe62fd594e3f756e18f96a4c9ea3ab
```

The same pinned corpus is preserved:

| Repository | Ecosystem | Static-only baseline | AI-enabled comparison |
| --- | --- | --- | --- |
| `xyflow` | JavaScript/TypeScript | passed, 4 candidates, 3 relations | `provider_unavailable` |
| `fastapi` | Python | passed, 1 candidate | `provider_unavailable` |
| `gin` | Go | passed, 1 candidate | `provider_unavailable` |

## Result Summary

The comparison records:

- `samePinnedCorpusAsStaticBaseline: true`;
- `providerAvailable: false`;
- `aiEnabledRunPerformed: false`;
- `aiProposalArtifactCount: 0`;
- `aiComparisonProviderUnavailableCount: 3`;
- `specpmHandoffChangedByAI: false`;
- `aiOutputAcceptedAsRegistryTruth: false`.

Each repository keeps its static-only handoff-ready preview result from P43-T4.
The AI delta is `not_evaluated_provider_unavailable`, and the warning is
`ai_provider_unavailable_static_baseline_retained`.

## Proposal-Only Boundary

AI-enabled output remains proposal-only even when a future local provider is
available. P43-T5 does not:

- call hosted AI services;
- persist raw prompts;
- persist raw provider responses;
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

Provider-unavailable evidence does not weaken the P43-T4 static-only baseline;
it only records that no AI comparison could be measured in this environment.

## Follow-Up

- `P43-T6`: add author handoff summaries based on the available static-only
  baseline and provider-unavailable comparison state.
- `P43-T7`: record the operational MVP exit decision.

## References

- <doc:OperationalMVPValidationPlan>
- <doc:OperationalMVPValidationPlanFixture>
- <doc:OperationalMVPValidationReportFixture>
- <doc:OperationalMVPStaticOnlyBaseline>
- <doc:AutonomousCandidateBatch>
- <doc:PackageSetAIDraftProposal>
- <doc:PackageSetAIEnrichment>
