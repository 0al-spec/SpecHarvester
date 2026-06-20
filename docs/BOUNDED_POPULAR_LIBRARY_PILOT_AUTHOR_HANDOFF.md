# Bounded Popular-Library Pilot Author Handoff

Status: P46-T5 author-facing handoff.

P46-T5 turns the P46-T4 triage into author-facing summaries. It separates
reviewable static evidence from noisy AI sidecars, unsupported AI sidecars,
evidence gaps, and do-not-promote AI drafts.

The durable fixture is:

```text
tests/fixtures/bounded_popular_library_pilot_author_handoff/p46-t5-bounded-popular-library-pilot-author-handoff-summaries.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.bounded-popular-library-pilot-author-handoff/v0
kind: SpecHarvesterBoundedPopularLibraryPilotAuthorHandoff
authority: producer_author_handoff_evidence_only
```

## Handoff Summary

| Metric | Count |
| --- | ---: |
| Repositories | 6 |
| Reviewable static members | 9 |
| Relation proposals | 3 |
| Do-not-promote AI sidecars | 2 |
| Unsupported AI sidecars | 1 |
| Noisy AI sidecars | 4 |
| Evidence-gap repositories | 1 |

## Author Summaries

| Repository | Review now | Do not promote | Noisy sidecars | Caveats |
| --- | --- | --- | --- | --- |
| Flask | `flask.core` | none | `flask.aiDraft`, `flask.aiEnrichment` | `excluded_package_also_selected`, `selected_member_role_unknown`, `refined_summary_missing` |
| Gin | `gin.core` | `gin.aiDraft` | none | `ai_json_repair_exhausted`, `package_set_subject_metadata_missing`, carry-forward `model_evidence_path_unsupported` |
| xyflow | `xyflow.react`, `xyflow.svelte`, `xyflow.system`, `xyflow.workspace` | `xyflow.aiEnrichment` | none | `partial_public_interface_index`, `operator_checkout_origin_fork_mismatch`, `model_evidence_path_unsupported` |
| Cupertino | `cupertino.core` | none | `cupertino.aiDraft` | `selected_member_role_unknown` |
| NavigationSplitView | `navigation_split_view.core` | none | `navigation-split-view.aiDraft` | `selected_member_role_unknown` |
| docc2context | `docc2context.core` | `docc2context.aiDraft` | none | `ai_json_repair_exhausted`, `package_set_subject_metadata_missing` |

The reviewable relation proposals are:

- `xyflow.workspace.contains.xyflow.react`
- `xyflow.workspace.contains.xyflow.svelte`
- `xyflow.workspace.contains.xyflow.system`

## Handoff Rules

- Include reviewable static candidates.
- Include relation proposals as review evidence.
- Separate noisy AI sidecars from static evidence.
- Exclude do-not-promote AI sidecars.
- Keep evidence gaps visible.
- Require SpecPM maintainer review before any acceptance.

## Boundary

P46-T5 did not rerun the pilot, run AI, run adapters, enable trusted local
adapter execution, clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, persist raw
prompts, persist raw provider responses, persist secrets, or persist
chain-of-thought.

The handoff does not treat handoff output as registry truth, does not treat
static output as registry truth, does not treat AI output as registry truth,
and does not treat adapter output as registry truth.

## Follow-Up

P46-T6 must record the pilot exit decision: proceed to a larger curated corpus,
run another targeted quality pass, or stop on a documented blocker.
