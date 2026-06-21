# Targeted Pilot Quality Follow-Up Exit Decision

Status: P47-T4 exit decision.

P47-T4 records the Phase 47 targeted quality follow-up decision after the
P47-T3 bounded rerun gate. The same six-repository scope passed the static-only
gate, but the AI-enabled gate failed. The larger curated corpus remains
blocked.

The durable fixture is:

```text
tests/fixtures/targeted_pilot_quality_follow_up_exit_decision/p47-t4-targeted-pilot-quality-follow-up-exit-decision.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.targeted-pilot-quality-follow-up-exit-decision/v0
kind: SpecHarvesterTargetedPilotQualityFollowUpExitDecision
authority: producer_quality_follow_up_exit_decision_evidence_only
```

Evidence input:

```text
tests/fixtures/targeted_pilot_bounded_rerun_gate/p47-t3-targeted-pilot-bounded-rerun-gate.example.json
```

## Selected Decision

Selected:

```text
run_another_targeted_quality_pass_before_larger_curated_corpus
```

Reason:

```text
p47_t3_static_passed_but_ai_enabled_gate_failed
```

The decision is not `proceed_to_larger_curated_corpus_planning` because the
P47-T3 AI-enabled gate failed. `gin.aiDraft` and
`navigation-split-view.aiDraft` both ended with `ai_json_repair_exhausted` and
`package_set_subject_metadata_missing`.

The decision is not `stop_on_documented_blocker` because the static gate
passed for all six repositories, `docc2context.aiDraft` improved to a repaired
non-blocking warning, and the remaining blockers are targeted AI draft shape
failures.

## Evidence Summary

| Signal | Result |
| --- | --- |
| Source gate | same six-repository bounded pilot scope |
| Static-only gate | passed |
| AI-enabled gate | failed |
| Failed AI draft repositories | 2 |
| Blocking AI sidecars | `gin.aiDraft`, `navigation-split-view.aiDraft` |
| Repaired warning | `docc2context.aiDraft` |
| xyflow remaining caveats | `partial_public_interface_index`, `operator_checkout_origin_fork_mismatch`, `ai_json_repair_needed` |
| Larger curated corpus | not approved |

## Blocker Treatment

`gin.aiDraft` remains a blocking AI draft sidecar. It must be regenerated or
constrained until `ai_json_repair_exhausted` and
`package_set_subject_metadata_missing` clear.

`navigation-split-view.aiDraft` is a new blocking AI draft sidecar from P47-T3.
It must be handled with the same targeted pass before any larger curated
corpus planning.

`docc2context.aiDraft` is no longer a do-not-promote failure in this evidence
set. It is a repaired `ai_json_repair_needed` warning and stays visible for the
next rerun.

xyflow did not repeat `model_evidence_path_unsupported`, but it still carries
`partial_public_interface_index`, `operator_checkout_origin_fork_mismatch`,
and `xyflow.aiEnrichment` `ai_json_repair_needed` caveats. Those caveats stay
visible into P48.

## Next Work

P47-T4 adds Phase 48. AI Draft Blocker Follow-Up Before Larger Corpus.

The selected next task is P48-T1 Plan AI Draft Blocker Follow-Up Pass.

The Phase 48 path is:

1. `P48-T1` plan the blocker follow-up pass.
2. `P48-T2` execute the AI draft blocker follow-up pass.
3. `P48-T3` rerun the same six-repository bounded gate.
4. `P48-T4` record the post-blocker follow-up exit decision.

The larger curated corpus can be reconsidered only after the P48 bounded rerun
gate passes or the remaining blockers are explicitly accepted with review
authority.

## Boundary

P47-T4 did not rerun the pilot, run AI, run adapters, enable trusted local
adapter execution, clone or fetch repositories, install dependencies, invoke
package managers inside harvested repositories, execute harvested code, accept
packages or relations, publish registry metadata, seed baselines, remove
`preview_only`, approve a larger curated corpus, persist raw prompts, persist
raw provider responses, persist secrets, or persist chain-of-thought.

The exit decision does not treat exit-decision output as registry truth, does
not treat bounded rerun gate output as registry truth, does not treat static
output as registry truth, does not treat AI output as registry truth, and does
not treat adapter output as registry truth.
