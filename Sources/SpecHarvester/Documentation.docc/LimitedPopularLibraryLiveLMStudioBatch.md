# Limited Popular-Library Live LM Studio Batch

This page records the P30-T3 live LM Studio run over the limited
popular-library corpus.

The machine-readable companion fixture is:

```text
tests/fixtures/limited_popular_library_live_lm_studio_batch/p30-t3-limited-popular-libraries.example.json
```

Its identity is `SpecHarvesterLimitedPopularLibraryLiveLMStudioBatch` with
`apiVersion: spec-harvester.limited-popular-library-live-lm-studio-batch/v0`,
`schemaVersion: 1`, and `authority: producer_preview_evidence_only`.

## Provider

Provider: `lm_studio`

Model: `openai/gpt-oss-20b`

Endpoint: `http://127.0.0.1:1234`

JSON repair cap: `jsonRepairMaxAttempts: 1`

The run records `rawPromptPersisted: false`, `rawResponsePersisted: false`, and
`chainOfThoughtPersisted: false`.

## Baseline Comparison

P30-T2 deterministic baseline:

- repositories: `6`;
- candidates: `9`;
- relation proposals: `3`;
- passed preflights: `6`;
- product verdict: `ready_for_live_lm_studio_limited_corpus`.

P30-T3 live result:

- repositories processed: `6`;
- candidates: `9`;
- relation proposals: `3`;
- passed preflights: `6`;
- AI draft proposals: `6`;
- AI enrichment proposals: `6`;
- JSON repair needed: `0`;
- JSON repair exhausted: `0`;
- provider total tokens: `138700`.

## Repository Results

| Repository | Candidates | Relations | AI draft | AI draft diagnostics | AI enrichment | AI enrichment diagnostics | JSON repair |
| --- | ---: | ---: | --- | --- | --- | --- | --- |
| Flask | `1` | `0` | `warning` | `excluded_package_unknown` | `completed` | - | `not_needed` |
| Gin | `1` | `0` | `warning` | `excluded_package_unknown` | `completed` | - | `not_needed` |
| xyflow | `4` | `3` | `warning` | `package_set_id_missing` | `completed` | - | `not_needed` |
| Cupertino | `1` | `0` | `completed` | - | `warning` | `refined_summary_missing` | `not_needed` |
| NavigationSplitView | `1` | `0` | `warning` | `package_set_id_missing` | `completed` | - | `not_needed` |
| docc2context | `1` | `0` | `completed` | - | `completed` | - | `not_needed` |

## Product Verdict

Verdict: `ready_for_candidate_layer_triage`.

The live run completed over the entire P30 corpus and produced AI proposal
evidence without requiring JSON repair. The useful next action is P30-T4
candidate-layer triage.

Findings to triage include `excluded_package_unknown`,
`package_set_id_missing`, `refined_summary_missing`, and the carried-forward
`package_id_hint_mismatch` where `navigation-split-view.core` normalizes to
`navigation_split_view.core`.

The generated output remains producer preview evidence. SpecPM remains the
validation, acceptance, relation, baseline, and registry authority.
The live run does not remove `preview_only` from generated candidates.

P30-T5 selected handoff dry-run evidence is recorded separately in
<doc:LimitedPopularLibrarySelectedHandoffDryRun> after the P30-T4 triage
narrows the handoff set to `flask.core`, `gin.core`, and `docc2context.core`.

## Command

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --out /tmp/specharvester-p30-t3.f7iGn0/live-lm-studio \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

See also <doc:LimitedPopularLibraryCandidateLayerTriage>,
<doc:LimitedPopularLibrarySelectedHandoffDryRun>,
<doc:LimitedPopularLibraryDeterministicBatch>,
<doc:LimitedPopularLibraryCorpusPlan>, and
<doc:AutonomousCandidateIntakePolicy>.
