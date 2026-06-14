# Next-Corpus Live Local-Model Batch

Status: P33-T4 live local-provider producer evidence.

This page records the live LM Studio run over the P33 next bounded corpus. It
compares the local `openai/gpt-oss-20b` draft/enrichment outcome with the
deterministic P33-T3 baseline.

The machine-readable companion fixture is:

```text
tests/fixtures/next_corpus_live_local_model_batch/p33-t4-next-corpus-live-local-model.example.json
```

Its contract identity is:

```json
{
  "apiVersion": "spec-harvester.next-corpus-live-local-model-batch/v0",
  "kind": "SpecHarvesterNextCorpusLiveLocalModelBatch",
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

P33-T3 deterministic baseline:

- repositories: `5`;
- candidates: `5`;
- relation proposals: `0`;
- passed preflights: `5`;
- product verdict: `ready_for_live_local_model_next_corpus`.

P33-T4 live result:

- repositories processed: `5`;
- candidates: `5`;
- relation proposals: `0`;
- passed preflights: `5`;
- AI draft proposals: `5`;
- AI enrichment proposals: `5`;
- JSON repair needed: `0`;
- JSON repair exhausted: `0`;
- provider total tokens: `76291`.

The live run preserved deterministic candidate and relation counts: five
preview candidates, zero relation proposals, and five passing bundle-set
preflights. It also recorded five AI draft proposals, five AI enrichment
proposals, zero JSON repair needs, and zero JSON repair exhaustion. Model
output did not replace generated package files or accepted SpecPM metadata.

## Repository Results

| Repository | Candidates | Relations | AI draft | AI draft diagnostics | AI enrichment | AI enrichment diagnostics | JSON repair |
| --- | ---: | ---: | --- | --- | --- | --- | --- |
| `serena` | `1` | `0` | `completed` | `no_proposal_subjects` | `completed` | - | `not_needed` |
| `transmission` | `1` | `0` | `completed` | `no_proposal_subjects` | `completed` | - | `not_needed` |
| `mcpm-sh` | `1` | `0` | `warning` | `selected_member_role_unknown`, `model_evidence_path_unsupported`, `excluded_package_also_selected` | `completed` | - | `not_needed` |
| `specgraph` | `1` | `0` | `completed` | - | `completed` | - | `not_needed` |
| `specpm` | `1` | `0` | `warning` | `excluded_package_unknown`, `no_proposal_subjects` | `completed` | - | `not_needed` |

## Candidate-Layer Findings

The live run is ready for P33-T5 candidate-layer triage, not SpecPM handoff.

Findings to triage:

- `ai_draft_no_proposal_subjects` for `serena` and `transmission`;
- `ai_draft_warning_diagnostics` for `mcpm-sh` because the model selected
  `mcpm.system` with `selected_member_role_unknown`,
  `model_evidence_path_unsupported`, and `excluded_package_also_selected`;
- `package_id_hint_changed_by_package_set_selection` for `mcpm-sh` because the
  source manifest hints `mcpm.core`, while deterministic package-set drafting
  produced `mcpm.system`;
- `package_id_hint_changed_by_package_set_selection` for `specgraph` because
  the source manifest hints `specgraph.core`, while deterministic package-set
  drafting produced `specgraph.system`;
- `ai_draft_warning_diagnostics` for `specpm` because the AI draft returned
  `excluded_package_unknown` and no proposal subjects.

These are proposal-layer signals. They do not invalidate deterministic
preflight, but they should drive P33-T5 classification before any selected
handoff evidence is prepared.

P33-T5 records that classification in
[`NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md`](NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md).

## Product Verdict

Verdict: `ready_for_candidate_layer_triage`.

The live local-model run completed over the entire P33 corpus and produced AI
proposal evidence without requiring JSON repair. Enrichment proposals were
clean for every repository. The useful next action is triage, not another blind
model loop and not registry intake.

This is not a claim that generated specs are final or accepted. The generated
candidate packages remain valid starter packages for author and maintainer
review. SpecPM remains the validation, acceptance, relation, baseline, and
registry authority.

## Commands

Model availability check:

```bash
curl http://127.0.0.1:1234/v1/models
```

Live local-model gate:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p33-next-corpus \
  --out /tmp/specharvester-p33-t4.yQPfwg/live-lm-studio \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Recorded digests:

```text
inputs/p33-next-corpus/repositories.yml        sha256:51ecc86773bf53d968fec1387dbdddd79c8066c351e704998ff54137b0518133
autonomous-candidate-batch-report.json        sha256:cdf22a5ddec014e49c432925f1b71710140d8667954daba36684f8d9c12a1ff2
reports/batch-validation-report.json          sha256:993c8eb865a8f3aa35d35b84eb49ea06862062f0acca8eeb999fce11c27dec42
```

## Non-Authority Boundary

The live local-model batch cannot:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create a SpecPM pull request;
- replace author or SpecPM maintainer review;
- treat model output as canonical package, spec, relation, or registry truth.

See also:

- [`NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md`](NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md)
- [`NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md`](NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md)
- [`NEXT_CORPUS_SOURCE_MANIFEST.md`](NEXT_CORPUS_SOURCE_MANIFEST.md)
- [`BOUNDED_CORPUS_EXPANSION_PLAN.md`](BOUNDED_CORPUS_EXPANSION_PLAN.md)
- [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md)
- [`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md)
