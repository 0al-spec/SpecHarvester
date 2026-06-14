# Next-Corpus Live Local-Model Batch

Status: P33-T4 live local-provider producer evidence.

P33-T4 records `SpecHarvesterNextCorpusLiveLocalModelBatch` with
`apiVersion: spec-harvester.next-corpus-live-local-model-batch/v0`.

The source manifest is `inputs/p33-next-corpus/repositories.yml`, and the
companion fixture is
`tests/fixtures/next_corpus_live_local_model_batch/p33-t4-next-corpus-live-local-model.example.json`.

## Provider

The run used provider `lm_studio`, local LM Studio at `http://127.0.0.1:1234`
with `openai/gpt-oss-20b` and `jsonRepairMaxAttempts: 1`. It records
`rawPromptPersisted: false`, `rawResponsePersisted: false`, and
`chainOfThoughtPersisted: false`.

## Live Result

The live local-model batch processed all five repositories from the P33 next
bounded corpus. It produced five preview candidates, zero relation proposals,
five passing bundle-set preflights, five AI draft proposals, five AI enrichment
proposals, zero JSON repair needs, zero JSON repair exhaustion, and `76291`
provider tokens.

AI enrichment completed cleanly for all repositories. AI draft output still
needs candidate-layer triage:

- `serena` and `transmission` completed with `no_proposal_subjects`;
- `mcpm-sh` returned `selected_member_role_unknown`,
  `model_evidence_path_unsupported`, and `excluded_package_also_selected`;
- `specpm` returned `excluded_package_unknown` and no proposal subjects;
- `mcpm-sh` and `specgraph` carry forward
  `package_id_hint_changed_by_package_set_selection` from P33-T3.

## Product Verdict

Verdict: `ready_for_candidate_layer_triage`.

The live run preserved deterministic candidate and relation counts and produced
proposal evidence without requiring JSON repair. The useful next action is
P33-T5 candidate-layer triage.

P33-T5 classification is recorded in
<doc:NextCorpusCandidateLayerTriage>.

## Non-Authority Boundary

P33-T4 did not clone repositories, fetch remote state, install dependencies,
execute harvested repository code, run package scripts, accept packages, accept
relations, seed baselines, remove `preview_only`, publish registry metadata,
create a SpecPM pull request, or treat model output as canonical package,
specification, relation, or registry truth.

See `docs/NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md` for the full GitHub-facing
record and digest list.
