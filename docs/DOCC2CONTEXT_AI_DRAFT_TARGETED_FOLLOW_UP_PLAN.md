# docc2context AI Draft Targeted Follow-Up Plan

Status: P49-T1 plan.

P49-T1 plans the targeted follow-up pass selected by P48-T4 for the remaining
`docc2context.aiDraft` blocker. It is planning evidence only: it does not run
AI, run another bounded rerun, accept packages, accept relations, or approve a
larger curated corpus.

The durable fixture is:

```text
tests/fixtures/docc2context_ai_draft_targeted_follow_up_plan/p49-t1-docc2context-ai-draft-targeted-follow-up-plan.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.docc2context-ai-draft-targeted-follow-up-plan/v0
kind: SpecHarvesterDocc2contextAIDraftTargetedFollowUpPlan
authority: producer_docc2context_ai_draft_targeted_follow_up_plan_evidence_only
```

Evidence input:

```text
tests/fixtures/post_blocker_follow_up_exit_decision/p48-t4-post-blocker-follow-up-exit-decision.example.json
```

## Decision

Selected outcome:

```text
docc2context_ai_draft_targeted_follow_up_before_larger_curated_corpus
```

P49-T1 targets only `docc2context.aiDraft`. The previous AI-enabled gate
failed with:

```text
ai_json_repair_exhausted
ai_json_repair_needed
package_set_subject_metadata_missing
```

P49-T2 must constrain subject/member metadata so the proposal cannot omit
`docc2context.core`, and it must clear or explicitly dispose JSON repair
exhaustion before the same-scope P49-T3 bounded rerun gate.

## Carried-Forward Evidence

The P49 plan keeps P48-T3/P48-T4 warning and caveat IDs correlatable:

- `flask.aiDraft`
- `flask.aiEnrichment`
- `gin.aiDraft`
- `cupertino.aiDraft`
- `navigation-split-view.aiDraft`
- `xyflow.partial_public_interface_index`
- `xyflow.operator_checkout_origin_fork_mismatch`

`gin.aiDraft` and `navigation-split-view.aiDraft` are resolved hard failures
that remain warning-only. xyflow caveats remain larger-corpus blockers for the
next exit review.

## P49-T2 Success Criteria

Before P49-T3 can rerun the bounded gate, P49-T2 must record that:

- `docc2context.aiDraft` no longer has unresolved `ai_json_repair_exhausted`;
- `docc2context.aiDraft` no longer has unresolved
  `package_set_subject_metadata_missing`;
- subject metadata includes `docc2context.core`;
- the sidecar status is `completed` or explicitly non-blocking `warning`;
- P48 warning IDs are carried forward unchanged.

## P49-T3 Rerun Gate

P49-T3 must rerun the same six-repository bounded pilot scope:

```text
inputs/p46-bounded-popular-library-pilot/repositories.yml
```

It must preserve static-only-before-AI ordering, proposal-only AI output, no
raw prompt/response/chain-of-thought persistence, and no registry promotion.
P49-T4 remains the later exit decision task that decides whether the larger
curated corpus can be reconsidered.

## Boundary

P49-T1 does not execute the targeted pass, run another bounded rerun, run AI,
run adapters, enable trusted local adapter execution, clone or fetch
repositories, install dependencies, invoke package managers, execute harvested
code, accept packages or relations, publish registry metadata, seed baselines,
remove `preview_only`, or approve a larger curated corpus.

The plan does not persist raw prompts, persist raw provider responses, persist
secrets, or persist chain-of-thought. It does not treat AI output as registry
truth, static output as registry truth, exit-decision output as registry truth,
plan output as registry truth, or adapter output as registry truth.
