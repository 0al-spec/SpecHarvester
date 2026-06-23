# Post-Blocker Follow-Up Exit Decision

Status: P48-T4 result.

P48-T4 records the exit decision after the P48-T3 same-scope bounded rerun
gate. The decision is evidence-only: it does not approve a larger curated
corpus, accept packages, accept relations, or treat AI output as registry
truth.

The durable fixture is:

```text
tests/fixtures/post_blocker_follow_up_exit_decision/p48-t4-post-blocker-follow-up-exit-decision.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.post-blocker-follow-up-exit-decision/v0
kind: SpecHarvesterPostBlockerFollowUpExitDecision
authority: producer_post_blocker_follow_up_exit_decision_only
```

Evidence input:

```text
tests/fixtures/ai_draft_blocker_bounded_rerun_gate/p48-t3-ai-draft-blocker-bounded-rerun-gate.example.json
```

## Decision

Selected outcome:

```text
run_docc2context_ai_draft_targeted_pass_before_larger_curated_corpus
```

P48-T3 proved that the static-only gate still passes for the same
six-repository bounded pilot, but the AI-enabled gate still fails. The
remaining hard blocker is `docc2context.aiDraft`, with:

```text
ai_json_repair_exhausted
ai_json_repair_needed
package_set_subject_metadata_missing
```

That blocker is not safe to accept as a non-blocking pilot caveat because the
proposal is missing subject metadata after JSON repair exhaustion. P48-T4
therefore selects another targeted pass focused on `docc2context.aiDraft`.

## What Improved

The P48-T2 follow-up did move the earlier blockers:

- `gin.aiDraft` no longer hard-fails and is now warning-only.
- `navigation-split-view.aiDraft` no longer hard-fails and is now
  warning-only.

Those warnings remain visible, but they do not block the next targeted pass.

## What Still Blocks Expansion

The larger curated corpus planning remains blocked.

Larger curated corpus planning remains blocked by:

- `docc2context.aiDraft.ai_json_repair_exhausted`;
- `docc2context.aiDraft.package_set_subject_metadata_missing`;
- missing P49 targeted follow-up planning and execution;
- missing post-targeted-pass same-scope bounded rerun gate;
- missing post-targeted-pass exit decision;
- xyflow `partial_public_interface_index`;
- xyflow `operator_checkout_origin_fork_mismatch`.

## Next Task

The selected next task is P49-T1 Plan docc2context AI Draft Targeted Follow-Up
Pass.

The follow-up must preserve static-only-before-AI ordering, proposal-only AI
output, no raw prompt/response/chain-of-thought persistence, and no registry
authority.

## Boundary

P48-T4 does not approve a larger curated corpus, run another bounded rerun, run
AI, run adapters, enable trusted local adapter execution, clone or fetch
repositories, install dependencies, invoke package managers, execute harvested
code, accept packages or relations, publish registry metadata, seed baselines,
or remove `preview_only`.

The exit decision does not persist raw prompts, persist raw provider
responses, persist secrets, or persist chain-of-thought. It does not treat AI
output as registry truth, static output as registry truth, rerun output as
registry truth, exit-decision output as registry truth, or adapter output as
registry truth.
