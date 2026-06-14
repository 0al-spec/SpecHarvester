# Refreshed Candidate-Layer Selected Handoff

This page mirrors `docs/REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md`.

Status: P32-T5 recorded refreshed handoff evidence.

P32-T5 consolidates the P30 selected dry run and targeted P32 deferred
candidate regeneration evidence into one producer-side review artifact.

The fixture is:

```text
tests/fixtures/refreshed_candidate_layer_selected_handoff/p32-t5-refreshed-candidate-layer-selected-handoff.example.json
```

Its identity is
`SpecHarvesterRefreshedCandidateLayerSelectedHandoff` with
`apiVersion: spec-harvester.refreshed-candidate-layer-selected-handoff/v0`,
`schemaVersion: 1`, and `authority: producer_preview_evidence_only`.

## Inputs

P32-T5 does not run a new harvest, does not call LM Studio, and does not
generate new candidate bundles. It references digest-backed committed
fixtures:

- P30-T5 selected handoff dry run;
- P32-T3 xyflow package-set identity regeneration;
- P32-T4 single-package deferred candidate regeneration.

## Selected Candidates

The refreshed selected handoff contains:

- `flask.core`;
- `gin.core`;
- `docc2context.core`;
- `xyflow.workspace`;
- `xyflow.react`;
- `xyflow.svelte`;
- `xyflow.system`;
- `navigation_split_view.core`.

Every selected candidate has
`candidate_layer_review_required`, `selectedHandoffEligible: true`, producer
preflight `status: passed`, `warningCount: 0`, `errorCount: 0`, static viewer
`status: ok`, `preview_only`, digest-backed evidence roles, and
`registryAcceptanceDecision.status: external_required`.

## Deferred Candidate

`cupertino.core` remains in `needs_regeneration` because
`refined_summary_missing` is still unresolved. It needs regenerated enrichment
or author-curated summary evidence before selected handoff.

## Next Gate

The SpecPM-side selected candidate handoff preflight was merged in
[0al-spec/SpecPM#140](https://github.com/0al-spec/SpecPM/pull/140). It emits
`SpecPMSelectedCandidateHandoffPreflightReport` with
`apiVersion: specpm.selected-candidate-handoff-preflight/v0`.

The P32-T5 fixture passed that gate with eight selected candidates, one
deferred candidate, zero warnings, zero errors, and three source digests
verified. P32-T7 records the resulting intake readiness decision in
<doc:LimitedCorpusIntakeReadinessDecision>. Passing preflight is still review
evidence only. It does not accept packages, accept relations, seed baselines,
remove `preview_only`, publish registry metadata, create a SpecPM pull request,
treat AI output as registry truth, or replace author or maintainer review.

See also <doc:AutonomousCandidateTechDebtPlan>,
<doc:DeferredCandidateRegenerationRunbook>,
<doc:SelectedCandidateHandoffProposal>,
<doc:LimitedCorpusIntakeReadinessDecision>, <doc:SpecPMHandoff>,
<doc:XyflowPackageSetIdentityRegenerationDryRun>, and
<doc:SinglePackageDeferredCandidateRegenerationDryRun>.
