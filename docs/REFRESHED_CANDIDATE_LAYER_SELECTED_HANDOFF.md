# Refreshed Candidate-Layer Selected Handoff

Status: P32-T5 recorded refreshed handoff evidence.

This page records the refreshed selected handoff after the P30 selected dry run
and the targeted P32 deferred-candidate regeneration work.

The machine-readable fixture is:

```text
tests/fixtures/refreshed_candidate_layer_selected_handoff/p32-t5-refreshed-candidate-layer-selected-handoff.example.json
```

Its identity is:

```json
{
  "apiVersion": "spec-harvester.refreshed-candidate-layer-selected-handoff/v0",
  "kind": "SpecHarvesterRefreshedCandidateLayerSelectedHandoff",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Inputs

P32-T5 does not run a new harvest, does not call LM Studio, and does not
generate new candidate bundles. It consolidates already recorded evidence:

- P30-T5 selected handoff dry run:
  `tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json`;
- P32-T3 xyflow package-set identity regeneration:
  `tests/fixtures/xyflow_package_set_identity_regeneration/p32-t3-xyflow-package-set-identity-regeneration.example.json`;
- P32-T4 single-package deferred candidate regeneration:
  `tests/fixtures/single_package_deferred_candidate_regeneration/p32-t4-single-package-deferred-candidate-regeneration.example.json`.

Each source fixture is digest-backed in the refreshed handoff artifact.

## Selected Candidates

The refreshed selected handoff contains eight preview candidates:

| Candidate | Source | Decision |
| --- | --- | --- |
| `flask.core` | P30-T5 | `candidate_layer_review_required` |
| `gin.core` | P30-T5 | `candidate_layer_review_required` |
| `docc2context.core` | P30-T5 | `candidate_layer_review_required` |
| `xyflow.workspace` | P32-T3 | `candidate_layer_review_required` |
| `xyflow.react` | P32-T3 | `candidate_layer_review_required` |
| `xyflow.svelte` | P32-T3 | `candidate_layer_review_required` |
| `xyflow.system` | P32-T3 | `candidate_layer_review_required` |
| `navigation_split_view.core` | P32-T4 | `candidate_layer_review_required` |

Every selected candidate keeps:

- `selectedHandoffEligible: true`;
- producer preflight `status: passed`;
- producer preflight `warningCount: 0`;
- producer preflight `errorCount: 0`;
- static viewer `status: ok`;
- `preview_only`;
- `registryAcceptanceDecision.status: external_required`;
- digest-backed evidence roles.

## Deferred Candidate

`cupertino.core` remains deferred:

```text
status: needs_regeneration
blocker: refined_summary_missing
selectedHandoffEligible: false
```

The generated candidate has valid preview evidence, producer preflight, and
viewer output, but AI enrichment still reports `refined_summary_missing`.
It should not enter selected handoff until regenerated enrichment or
author-curated summary evidence resolves that blocker.

## Next Gate

The next gate is SpecPM-side selected candidate handoff preflight:

```text
SpecPMSelectedCandidateHandoffPreflightReport
apiVersion: specpm.selected-candidate-handoff-preflight/v0
```

That future gate should consume the refreshed handoff fixture as review
evidence, validate candidate identity and evidence roles, and preserve the
external registry acceptance boundary.

## Non-Authority Boundary

This artifact cannot:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create a SpecPM pull request;
- treat AI output as registry truth;
- replace author or SpecPM maintainer review.

See also:

- [`AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`](AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md)
- [`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md)
- [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md)
- [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md)
- [`XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md`](XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md)
- [`SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md`](SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md)

