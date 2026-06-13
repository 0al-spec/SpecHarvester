# Next-Corpus Candidate-Layer Triage

Status: P33-T5 candidate-layer review evidence.

This page classifies the generated P33 next-corpus preview packages after the
P33-T3 deterministic run and P33-T4 live local-model run. It decides which
candidates can proceed to P33-T6 selected handoff preflight and which
candidates must remain deferred.

The machine-readable companion fixture is:

```text
tests/fixtures/next_corpus_candidate_layer_triage/p33-t5-next-corpus-candidate-layer-triage.example.json
```

Its contract identity is:

```json
{
  "apiVersion": "spec-harvester.next-corpus-candidate-layer-triage/v0",
  "kind": "SpecHarvesterNextCorpusCandidateLayerTriage",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Inputs

P33-T5 consumes already-recorded evidence only:

- P33-T3 deterministic fixture:
  `tests/fixtures/next_corpus_deterministic_dry_run/p33-t3-next-corpus-deterministic-dry-run.example.json`;
- P33-T4 live local-model fixture:
  `tests/fixtures/next_corpus_live_local_model_batch/p33-t4-next-corpus-live-local-model.example.json`;
- P33 source manifest:
  `inputs/p33-next-corpus/repositories.yml`.

It does not run another scrape, call LM Studio, clone repositories, install
dependencies, mutate generated candidates, or run SpecPM preflight.

## Triage States

- `candidate_layer_review_required`: valid starter package can proceed to
  author or maintainer review without becoming accepted registry truth.
- `needs_regeneration`: producer output should be regenerated, corrected, or
  explicitly approved before selected handoff.
- `blocked`: required local input is missing or a hard gate failed.
- `not_for_intake`: useful calibration evidence that should not be handed to
  SpecPM.

## Candidate Classification

| Candidate | Repository | Classification | P33-T6 selected | Reason |
| --- | --- | --- | --- | --- |
| `serena.core` | `serena` | `candidate_layer_review_required` | yes | deterministic preflight and enrichment are usable; empty AI draft subject list is non-blocking single-package model noise |
| `transmission.core` | `transmission` | `candidate_layer_review_required` | yes | deterministic preflight and enrichment are usable; empty AI draft subject list is non-blocking single-package model noise |
| `mcpm.system` | `mcpm-sh` | `needs_regeneration` | no | manifest hint is `mcpm.core`, generated id is `mcpm.system`, and AI draft has warning-level role, evidence path, and exclusion diagnostics |
| `specgraph.system` | `specgraph` | `needs_regeneration` | no | manifest hint is `specgraph.core`, while generated id is `specgraph.system` |
| `specpm.core` | `specpm` | `candidate_layer_review_required` | yes | deterministic preflight and enrichment are usable; `excluded_package_unknown` plus no proposal subjects is bounded single-package AI draft noise |

Aggregate counts:

- preview candidates: `5`;
- relation proposals: `0`;
- `candidate_layer_review_required`: `3`;
- `needs_regeneration`: `2`;
- `blocked`: `0`;
- `not_for_intake`: `0`;
- selected for P33-T6 selected handoff preflight: `3`;
- deferred from P33-T6: `2`.

## Finding Classification

| Finding | Origin | Classification | Count | Action |
| --- | --- | --- | ---: | --- |
| `ai_draft_no_proposal_subjects` | AI draft | `candidate_layer_review_required` | `2` | treat as non-blocking single-package model noise for `serena.core` and `transmission.core` |
| `ai_draft_warning_diagnostics` | AI draft | `candidate_layer_review_required` | `1` | treat `specpm.core` unknown exclusion/no-subject warning as bounded single-package model noise |
| `ai_draft_warning_diagnostics` | AI draft | `needs_regeneration` | `1` | regenerate or manually review `mcpm.system` AI draft evidence before selected handoff |
| `package_id_hint_changed_by_package_set_selection` | deterministic draft | `needs_regeneration` | `2` | resolve package identity before selecting `mcpm.system` or `specgraph.system` |

## Product Verdict

Verdict: `ready_for_p33_t6_selected_handoff_preflight`.

P33 should proceed to P33-T6 only for:

- `serena.core`;
- `transmission.core`;
- `specpm.core`.

The deferred candidates remain useful review evidence:

- `mcpm.system`;
- `specgraph.system`.

They should not be included in selected handoff preflight until package
identity drift is resolved, regenerated, or explicitly approved. `mcpm.system`
also needs regenerated or manually reviewed AI draft evidence because the model
returned `selected_member_role_unknown`, `model_evidence_path_unsupported`, and
`excluded_package_also_selected`.

This is still not registry intake. P33-T6 may run or coordinate a selected
handoff preflight for the selected candidates, but SpecPM remains the
validation, acceptance, relation, baseline, and registry authority.

## Non-Authority Boundary

The triage report cannot:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create a SpecPM pull request;
- replace author or SpecPM maintainer review;
- treat model output as canonical package, spec, relation, or registry truth.

See also:

- [`NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md`](NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md)
- [`NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md`](NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md)
- [`NEXT_CORPUS_SOURCE_MANIFEST.md`](NEXT_CORPUS_SOURCE_MANIFEST.md)
- [`BOUNDED_CORPUS_EXPANSION_PLAN.md`](BOUNDED_CORPUS_EXPANSION_PLAN.md)
- [`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md)
