# docc2context Follow-Up Exit Decision

Status: P49-T4 result.

P49-T4 records the exit decision after the P49-T3 same-scope bounded rerun
gate stopped at operator-local checkout preflight. The decision is
evidence-only: it does not approve a larger curated corpus, accept packages,
accept relations, or treat exit-decision output as registry truth.

The durable fixture is:

```text
tests/fixtures/docc2context_follow_up_exit_decision/p49-t4-docc2context-follow-up-exit-decision.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.docc2context-follow-up-exit-decision/v0
kind: SpecHarvesterDocc2contextFollowUpExitDecision
authority: producer_docc2context_follow_up_exit_decision_only
```

Evidence input:

```text
tests/fixtures/docc2context_ai_draft_same_scope_bounded_rerun_gate/p49-t3-docc2context-ai-draft-same-scope-bounded-rerun-gate.example.json
```

## Decision

Selected outcome:

```text
record_no_larger_corpus_readiness_due_to_operator_local_checkout_blocker
```

P49-T3 did not reach the static-only gate or the AI-enabled gate because all
six operator-local checkouts from the P46 manifest were missing:

- `flask`
- `gin`
- `xyflow`
- `cupertino`
- `navigation-split-view`
- `docc2context`

LM Studio was available with `openai/gpt-oss-20b`, but AI execution was not
reached because static-only-before-AI ordering stopped at checkout preflight.
P49-T4 therefore records no larger curated corpus readiness.

## Carried-Forward Evidence

P49-T4 carries the P49-T2 and P49-T3 evidence forward unchanged:

```text
same_scope_bounded_rerun_gate_blocked_operator_local_checkouts_missing
docc2context.aiDraft_warning_explicitly_non_blocking_for_p49_t3
excluded_package_also_selected
```

The previous `docc2context.aiDraft` blocking diagnostics remain cleared for
the gate:

```text
ai_json_repair_exhausted
ai_json_repair_needed
package_set_subject_metadata_missing
```

The P48 warning IDs remain visible:

- `flask.aiDraft`
- `flask.aiEnrichment`
- `gin.aiDraft`
- `cupertino.aiDraft`
- `navigation-split-view.aiDraft`

The xyflow caveats remain larger-corpus blockers:

- `xyflow.partial_public_interface_index`
- `xyflow.operator_checkout_origin_fork_mismatch`

## What Still Blocks Expansion

Larger curated corpus planning remains blocked by:

- the P49-T3 same-scope bounded rerun gate being blocked;
- missing operator-local checkouts;
- static-only gate not run;
- AI-enabled gate not run;
- xyflow `partial_public_interface_index`;
- xyflow `operator_checkout_origin_fork_mismatch`.

Readiness can be reconsidered only after the same six operator-local checkouts
are restored, P49-T3 is rerun over the same six-repository scope, and the exit
decision is revisited after a successful rerun.

## Next State

There is no next task selected by P49-T4. Phase 49 is complete as a bounded
evidence and decision record, but larger curated corpus planning remains
blocked.

The practical follow-up is operator action: restore the same six
operator-local checkouts before rerunning P49-T3, or author a new follow-up
phase if the project wants a different path.

## Boundary

P49-T4 does not approve a larger curated corpus, run another bounded rerun, run
the static-only gate, run the AI-enabled gate, run AI, run adapters, enable
trusted local adapter execution, clone or fetch repositories, install
dependencies, invoke package managers, execute harvested code, accept packages
or relations, publish registry metadata, seed baselines, or remove
`preview_only`.

The exit decision does not persist raw prompts, persist raw provider
responses, persist secrets, or persist chain-of-thought. It does not treat AI
output as registry truth, static output as registry truth, rerun output as
registry truth, targeted follow-up output as registry truth, exit-decision
output as registry truth, or adapter output as registry truth.
