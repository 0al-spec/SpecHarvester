# Limited Popular-Library Live LM Studio Batch

Status: P30-T3 live local-provider producer evidence.

This page records the live LM Studio run over the P30 limited popular-library
corpus. It compares the local `openai/gpt-oss-20b` AI draft/enrichment outcome
with the deterministic P30-T2 baseline.

The machine-readable companion fixture is:

```text
tests/fixtures/limited_popular_library_live_lm_studio_batch/p30-t3-limited-popular-libraries.example.json
```

Its contract identity is:

```json
{
  "apiVersion": "spec-harvester.limited-popular-library-live-lm-studio-batch/v0",
  "kind": "SpecHarvesterLimitedPopularLibraryLiveLMStudioBatch",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Provider

Provider: `lm_studio`

Model: `openai/gpt-oss-20b`

Endpoint: `http://127.0.0.1:1234`

JSON repair cap: `jsonRepairMaxAttempts: 1`

Privacy boundary:

- `rawPromptPersisted: false`;
- `rawResponsePersisted: false`;
- `chainOfThoughtPersisted: false`.

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

The live run preserved deterministic candidate and relation counts. Model
output did not replace generated package files or accepted SpecPM metadata.

## Repository Results

| Repository | Candidates | Relations | AI draft | AI draft diagnostics | AI enrichment | AI enrichment diagnostics | JSON repair |
| --- | ---: | ---: | --- | --- | --- | --- | --- |
| Flask | `1` | `0` | `warning` | `excluded_package_unknown` | `completed` | - | `not_needed` |
| Gin | `1` | `0` | `warning` | `excluded_package_unknown` | `completed` | - | `not_needed` |
| xyflow | `4` | `3` | `warning` | `package_set_id_missing` | `completed` | - | `not_needed` |
| Cupertino | `1` | `0` | `completed` | - | `warning` | `refined_summary_missing` | `not_needed` |
| NavigationSplitView | `1` | `0` | `warning` | `package_set_id_missing` | `completed` | - | `not_needed` |
| docc2context | `1` | `0` | `completed` | - | `completed` | - | `not_needed` |

## Candidate-Layer Findings

The live run is ready for P30-T4 candidate-layer triage, not SpecPM handoff.

Findings to triage:

- `excluded_package_unknown` for Flask and Gin AI draft output;
- `package_set_id_missing` for xyflow and NavigationSplitView AI draft output;
- `refined_summary_missing` for Cupertino AI enrichment output;
- `package_id_hint_mismatch`: `navigation-split-view.core` in the source
  manifest remained normalized to `navigation_split_view.core` in generated
  candidate output.

These are proposal-layer signals. They do not invalidate deterministic
preflight, but they should drive P30-T4 classification before any P30-T5
handoff evidence is prepared.

## Product Verdict

Verdict: `ready_for_candidate_layer_triage`.

The live LM Studio run completed over the entire P30 corpus and produced AI
proposal evidence without requiring JSON repair. The useful next action is
triage, not another blind model loop and not registry intake.

This is not a claim that generated specs are final or accepted. The generated
candidate packages remain valid starter packages for author and maintainer
review. SpecPM remains the validation, acceptance, relation, baseline, and
registry authority.

## Commands

Model availability check:

```bash
curl http://127.0.0.1:1234/v1/models
```

Live LM Studio gate:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --out /tmp/specharvester-p30-t3.f7iGn0/live-lm-studio \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Recorded report digests:

```text
autonomous-candidate-batch-report.json sha256:901e1fd2e81b03975fa7cd46d8a5a75b35b16a34512a41f264952a72909cd2c1
batch-validation-report.json           sha256:f21e068bd63f8fb413578541989ee4fbd6d78a21ecb9483c31ee3dc15fa5da69
```

## Non-Authority Boundary

The live batch cannot:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- replace author or SpecPM maintainer review;
- treat model output as canonical package, spec, relation, or registry truth.

See also:

- [`LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`](LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md)
- [`LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md`](LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md)
- [`LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md`](LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md)
- [`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md)
