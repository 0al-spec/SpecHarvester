# Bounded Popular-Library Pilot Exit Decision

Status: P46-T6 exit decision.

P46-T6 records the Phase 46 bounded popular-library pilot decision. The pilot
proved that the static candidate layer can produce reviewable evidence for all
six repositories, but the AI proposal layer is not ready to scale to a larger
curated corpus.

The durable fixture is:

```text
tests/fixtures/bounded_popular_library_pilot_exit_decision/p46-t6-bounded-popular-library-pilot-exit-decision.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.bounded-popular-library-pilot-exit-decision/v0
kind: SpecHarvesterBoundedPopularLibraryPilotExitDecision
authority: producer_exit_decision_evidence_only
```

## Selected Decision

Selected:

```text
run_targeted_quality_pass_before_larger_curated_corpus
```

Reason:

```text
static_pilot_reviewable_but_ai_sidecar_quality_blocks_larger_corpus
```

The decision is not `proceed_to_larger_curated_corpus` because
`gin.aiDraft` and `docc2context.aiDraft` remain do-not-promote AI sidecars,
and xyflow still has `partial_public_interface_index`,
`operator_checkout_origin_fork_mismatch`, and
`model_evidence_path_unsupported` caveats.

The decision is not `stop_on_documented_blocker` because the static candidate
layer is reviewable for all six repositories and the remaining blockers are
targeted enough for a quality pass.

## Evidence Summary

| Metric | Count |
| --- | ---: |
| Repositories | 6 |
| Reviewable static members | 9 |
| Relation proposals | 3 |
| Reviewable repositories | 6 |
| Do-not-promote AI sidecars | 2 |
| Unsupported AI sidecars | 1 |
| Noisy AI sidecars | 4 |
| Evidence-gap repositories | 1 |

## Repository Treatment

| Repository | Reviewable static evidence | Blocking sidecars or caveats | Follow-up |
| --- | --- | --- | --- |
| Flask | `flask.core` | noisy AI sidecars | Author review before AI use |
| Gin | `gin.core` | `gin.aiDraft` | Regenerate AI draft |
| xyflow | `xyflow.react`, `xyflow.svelte`, `xyflow.system`, `xyflow.workspace` | `xyflow.aiEnrichment`, `partial_public_interface_index`, `operator_checkout_origin_fork_mismatch`, `model_evidence_path_unsupported` | Resolve or explicitly accept caveats |
| Cupertino | `cupertino.core` | noisy AI draft | Author review before AI use |
| NavigationSplitView | `navigation_split_view.core` | noisy AI draft | Author review before AI use |
| docc2context | `docc2context.core` | `docc2context.aiDraft` | Regenerate AI draft |

The reviewable xyflow relation proposals are:

- `xyflow.workspace.contains.xyflow.react`
- `xyflow.workspace.contains.xyflow.svelte`
- `xyflow.workspace.contains.xyflow.system`

## Larger Corpus Gate

The larger curated corpus is not approved now. Required before reconsidering:

- clear do-not-promote AI drafts;
- triage unsupported xyflow enrichment;
- document the xyflow evidence-gap disposition;
- rerun the small bounded pilot before expanding.

The recommended next work is `targeted_quality_pass`.

## Boundary

P46-T6 did not rerun the pilot, run AI, run adapters, enable trusted local
adapter execution, clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, persist raw
prompts, persist raw provider responses, persist secrets, or persist
chain-of-thought.

The exit decision does not treat exit-decision output as registry truth, does
not treat handoff output as registry truth, does not treat static output as
registry truth, does not treat AI output as registry truth, and does not treat
adapter output as registry truth.

## Follow-Up

Phase 46 is complete. The selected next task is P47-T1 Targeted Pilot Quality
Follow-Up Plan under Phase 47 Targeted Pilot Quality Follow-Up Planning before
any larger curated corpus approval.
