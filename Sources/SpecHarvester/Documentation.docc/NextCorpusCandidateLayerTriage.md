# Next-Corpus Candidate-Layer Triage

Status: P33-T5 candidate-layer review evidence.

P33-T5 records `SpecHarvesterNextCorpusCandidateLayerTriage` with
`apiVersion: spec-harvester.next-corpus-candidate-layer-triage/v0`.
Authority is `producer_preview_evidence_only`.

The source manifest is `inputs/p33-next-corpus/repositories.yml`, and the
companion fixture is
`tests/fixtures/next_corpus_candidate_layer_triage/p33-t5-next-corpus-candidate-layer-triage.example.json`.

## Inputs

P33-T5 consumes already recorded P33-T3 deterministic evidence and P33-T4 live
local-model evidence. It does not run another scrape, rerun LM Studio, clone
repositories, install dependencies, mutate generated candidates, or run SpecPM
preflight.

## Triage Result

The triage covers five preview candidates and zero relation proposals.

Selected for P33-T6 selected handoff preflight:

- `serena.core`;
- `specpm.core`.

Deferred from P33-T6:

- `transmission.core`;
- `mcpm.system`;
- `specgraph.system`.

The selected candidates are classified as
`candidate_layer_review_required`. The deferred candidates are classified as
`needs_regeneration`. The run has zero `blocked` candidates and zero
`not_for_intake` candidates.

## Finding Classification

P33-T5 treats `ai_draft_no_proposal_subjects` for `serena.core` as
non-blocking single-package model noise.

P33-T5 defers `transmission.core` because Transmission is a multi-component
C/C++ application candidate and the AI draft did not identify proposal
subjects.

P33-T5 treats `ai_draft_warning_diagnostics` for `specpm.core` as
candidate-layer review evidence because the warning is limited to
`excluded_package_unknown` plus no proposal subjects for a single-package
candidate.

P33-T5 defers `mcpm.system` because `ai_draft_warning_diagnostics` includes
`selected_member_role_unknown`, `model_evidence_path_unsupported`, and
`excluded_package_also_selected`. It also defers `mcpm.system` and
`specgraph.system` on `package_id_hint_changed_by_package_set_selection` until
package identity drift is resolved, regenerated, or explicitly approved.

## Product Verdict

Verdict: `ready_for_p33_t6_selected_handoff_preflight`.

P33-T6 records the consumer preflight outcome in
<doc:NextCorpusSpecPMPreflightIntakeDecision>. The selected scope is valid as
triage evidence, but it still needs a durable selected handoff payload before
SpecPM maintainer intake review. This does not accept packages, accept
relations, seed baselines, remove `preview_only`, publish registry metadata,
create a SpecPM pull request, or treat model output as registry truth.

## Source

Canonical source:
`docs/NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md`
