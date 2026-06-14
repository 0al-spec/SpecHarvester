# Limited Popular-Library Candidate-Layer Triage

This page records the P30-T4 candidate-layer triage report for the limited
popular-library corpus.

The machine-readable companion fixture is:

```text
tests/fixtures/limited_popular_library_candidate_layer_triage/p30-t4-limited-popular-libraries.example.json
```

Its identity is `SpecHarvesterLimitedPopularLibraryCandidateLayerTriage` with
`apiVersion: spec-harvester.limited-popular-library-candidate-layer-triage/v0`,
`schemaVersion: 1`, and `authority: producer_preview_evidence_only`.

## Inputs

The report consumes the deterministic P30-T2 fixture and the live LM Studio
P30-T3 fixture. It does not run another scrape, call LM Studio, clone
repositories, install dependencies, or generate SpecPM handoff artifacts.

## Triage States

- `candidate_layer_review_required`: valid starter package can proceed to
  author or maintainer review without becoming accepted registry truth.
- `needs_regeneration`: producer output should be regenerated or corrected
  before selected handoff.
- `blocked`: required local input is missing or a hard gate failed.
- `not_for_intake`: useful calibration evidence that should not be handed to
  SpecPM.

## Candidate Classification

| Candidate | Classification | P30-T5 selected |
| --- | --- | --- |
| `flask.core` | `candidate_layer_review_required` | yes |
| `gin.core` | `candidate_layer_review_required` | yes |
| `xyflow.workspace` | `needs_regeneration` | no |
| `xyflow.react` | `needs_regeneration` | no |
| `xyflow.svelte` | `needs_regeneration` | no |
| `xyflow.system` | `needs_regeneration` | no |
| `cupertino.core` | `needs_regeneration` | no |
| `navigation_split_view.core` | `needs_regeneration` | no |
| `docc2context.core` | `candidate_layer_review_required` | yes |

Finding classifications include `excluded_package_unknown` as non-blocking
model-output noise, plus `package_set_id_missing`,
`refined_summary_missing`, and `package_id_hint_mismatch` as
`needs_regeneration` signals.

## Product Verdict

Verdict: `ready_for_selected_handoff_dry_run`.

P30-T5 should prepare dry-run handoff evidence only for `flask.core`,
`gin.core`, and `docc2context.core`. All output remains producer preview
evidence. The triage report does not accept packages, accept relations, seed
baselines, remove `preview_only`, publish registry metadata, or replace author
or SpecPM maintainer review.

See also <doc:LimitedPopularLibraryLiveLMStudioBatch>,
<doc:LimitedPopularLibraryDeterministicBatch>,
<doc:LimitedPopularLibraryCorpusPlan>, and
<doc:AutonomousCandidateIntakePolicy>.
