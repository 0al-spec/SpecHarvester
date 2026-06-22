# AI Draft Blocker Follow-Up Plan

Status: P48-T1 plan.

P48-T1 records the Phase 48 plan selected by P47-T4. It targets the failed AI
draft blockers from the P47-T3 bounded rerun gate and keeps larger curated
corpus planning blocked until P48-T2, P48-T3, and P48-T4 complete.

The durable fixture is:

```text
tests/fixtures/ai_draft_blocker_follow_up_plan/p48-t1-ai-draft-blocker-follow-up-plan.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.ai-draft-blocker-follow-up-plan/v0
kind: SpecHarvesterAIDraftBlockerFollowUpPlan
authority: producer_ai_draft_blocker_follow_up_plan_evidence_only
```

Evidence input:

```text
tests/fixtures/targeted_pilot_quality_follow_up_exit_decision/p47-t4-targeted-pilot-quality-follow-up-exit-decision.example.json
```

## Selected Plan

Selected:

```text
ai_draft_blocker_follow_up_before_larger_curated_corpus
```

Reason:

```text
p47_t4_requires_targeted_pass_for_failed_ai_drafts
```

The plan does not approve larger curated corpus planning. It prepares P48-T2
and P48-T3 while preserving the same six-repository bounded pilot scope.

## Targets

Blocking AI draft sidecars for P48-T2:

| Sidecar | Repository | Current diagnostics | P48-T2 objective |
| --- | --- | --- | --- |
| `gin.aiDraft` | `gin` | `ai_json_repair_exhausted`, `ai_json_repair_needed`, `package_set_subject_metadata_missing` | Regenerate or constrain AI draft until repair exhaustion clears |
| `navigation-split-view.aiDraft` | `navigation-split-view` | `ai_json_repair_exhausted`, `ai_json_repair_needed`, `package_set_subject_metadata_missing` | Regenerate or constrain AI draft until repair exhaustion clears |

Warnings and caveats to keep visible:

- `docc2context.aiDraft` with repaired `ai_json_repair_needed`;
- `xyflow.aiEnrichment` with repaired `ai_json_repair_needed`;
- xyflow `partial_public_interface_index`;
- xyflow `operator_checkout_origin_fork_mismatch`;
- xyflow `ai_json_repair_needed`.

## P48-T2 Success Criteria

P48-T2 must record whether the following are absent or explicitly disposed as
non-blocking:

- `gin.aiDraft` `ai_json_repair_exhausted`;
- `gin.aiDraft` `package_set_subject_metadata_missing`;
- `navigation-split-view.aiDraft` `ai_json_repair_exhausted`;
- `navigation-split-view.aiDraft` `package_set_subject_metadata_missing`;
- `docc2context.aiDraft` warning state;
- `xyflow.aiEnrichment` `ai_json_repair_needed` warning state.

P48-T2 must preserve proposal-only AI output, raw prompt/response/CoT
non-persistence, no package or relation acceptance, no registry publication,
and no adapter execution.

## P48-T3 Rerun Gate

P48-T3 must use the same six-repository bounded pilot scope and
`inputs/p46-bounded-popular-library-pilot/repositories.yml`. It must run the
static-only gate before any AI-enabled gate, keep AI output proposal-only, and
avoid registry promotion.

Larger curated corpus planning can be reconsidered only after:

- P48-T2 records blocker disposition evidence;
- P48-T3 static gate passes;
- P48-T3 AI-enabled gate passes or remaining blockers are explicitly accepted;
- P48-T4 records the post-blocker follow-up exit decision.

## Boundary

P48-T1 did not approve a larger curated corpus, rerun the pilot, run AI, run
adapters, enable trusted local adapter execution, clone or fetch repositories,
install dependencies, invoke package managers inside harvested repositories,
execute harvested code, accept packages or relations, publish registry
metadata, seed baselines, remove `preview_only`, persist raw prompts, persist
raw provider responses, persist secrets, or persist chain-of-thought.

The plan does not treat plan output as registry truth, does not treat
exit-decision output as registry truth, does not treat static output as
registry truth, does not treat AI output as registry truth, and does not treat
adapter output as registry truth.

## Follow-Up

The selected next task is P48-T2 Execute AI Draft Blocker Follow-Up Pass.
The larger curated corpus remains blocked.
