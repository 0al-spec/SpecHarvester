# Limited Popular-Library Candidate-Layer Triage

Status: P30-T4 candidate-layer review evidence.

This page classifies the generated P30 limited popular-library preview
packages and model findings after the deterministic P30-T2 run and live
LM Studio P30-T3 run.

The machine-readable companion fixture is:

```text
tests/fixtures/limited_popular_library_candidate_layer_triage/p30-t4-limited-popular-libraries.example.json
```

Its contract identity is:

```json
{
  "apiVersion": "spec-harvester.limited-popular-library-candidate-layer-triage/v0",
  "kind": "SpecHarvesterLimitedPopularLibraryCandidateLayerTriage",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Inputs

P30-T4 consumes already-recorded evidence only:

- P30-T2 deterministic fixture:
  `tests/fixtures/limited_popular_library_deterministic_batch/p30-t2-limited-popular-libraries.example.json`;
- P30-T3 live LM Studio fixture:
  `tests/fixtures/limited_popular_library_live_lm_studio_batch/p30-t3-limited-popular-libraries.example.json`.

It does not run another scrape, call LM Studio, clone repositories, install
dependencies, or generate SpecPM handoff artifacts.

## Triage States

- `candidate_layer_review_required`: valid starter package can proceed to
  author or maintainer review without becoming accepted registry truth.
- `needs_regeneration`: producer output should be regenerated or corrected
  before selected handoff.
- `blocked`: required local input is missing or a hard gate failed.
- `not_for_intake`: useful calibration evidence that should not be handed to
  SpecPM.

## Candidate Classification

| Candidate | Repository | Classification | P30-T5 selected | Reason |
| --- | --- | --- | --- | --- |
| `flask.core` | Flask | `candidate_layer_review_required` | yes | deterministic candidate and enrichment are usable; `excluded_package_unknown` is non-blocking AI draft noise |
| `gin.core` | Gin | `candidate_layer_review_required` | yes | deterministic candidate and enrichment are usable; `excluded_package_unknown` is non-blocking AI draft noise |
| `xyflow.workspace` | xyflow | `needs_regeneration` | no | package-set AI draft evidence needs package-set identity regeneration |
| `xyflow.react` | xyflow | `needs_regeneration` | no | member candidate is tied to package-set AI draft identity drift |
| `xyflow.svelte` | xyflow | `needs_regeneration` | no | member candidate is tied to package-set AI draft identity drift |
| `xyflow.system` | xyflow | `needs_regeneration` | no | member candidate is tied to package-set AI draft identity drift |
| `cupertino.core` | Cupertino | `needs_regeneration` | no | enrichment warning `refined_summary_missing` should be fixed before selected handoff |
| `navigation_split_view.core` | NavigationSplitView | `needs_regeneration` | no | generated id differs from `navigation-split-view.core`, and draft evidence has identity drift |
| `docc2context.core` | docc2context | `candidate_layer_review_required` | yes | deterministic candidate, AI draft, and enrichment are clean enough for selected dry-run handoff |

Aggregate counts:

- preview candidates: `9`;
- `candidate_layer_review_required`: `3`;
- `needs_regeneration`: `6`;
- `blocked`: `0`;
- `not_for_intake`: `0`;
- selected for P30-T5 dry-run handoff: `3`.

## Finding Classification

| Finding | Origin | Classification | Count | Action |
| --- | --- | --- | ---: | --- |
| `excluded_package_unknown` | AI draft | `candidate_layer_review_required` | `2` | treat as bounded model-output noise; ignore the unknown exclusion field during handoff review |
| `package_set_id_missing` | AI draft | `needs_regeneration` | `2` | regenerate AI draft evidence before package-set or affected package handoff |
| `refined_summary_missing` | AI enrichment | `needs_regeneration` | `1` | regenerate enrichment or provide author-curated summary |
| `package_id_hint_mismatch` | deterministic draft | `needs_regeneration` | `1` | resolve package id normalization before handoff |

## Product Verdict

Verdict: `ready_for_selected_handoff_dry_run`.

P30 should proceed to P30-T5 only for:

- `flask.core`;
- `gin.core`;
- `docc2context.core`.

The other generated preview packages remain useful calibration evidence, but
they should not be included in selected handoff until the relevant identity,
AI draft, or enrichment issue is resolved.

This is still not registry intake. P30-T5 may prepare dry-run handoff evidence
for selected candidates, but SpecPM remains the validation, acceptance,
relation, baseline, and registry authority.

## Non-Authority Boundary

The triage report cannot:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- replace author or SpecPM maintainer review;
- treat model output as canonical package, spec, relation, or registry truth.

See also:

- [`LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md`](LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md)
- [`LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md`](LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md)
- [`LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md`](LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md)
- [`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md)
