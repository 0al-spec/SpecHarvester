# docc2context AI Draft Same-Scope Bounded Rerun Gate

Status: P49-T3 result.

P49-T3 attempted to run the same six-repository bounded rerun gate after
P49-T2 cleared or explicitly disposed the previous `docc2context.aiDraft`
blockers for the gate. The gate did not run because all six operator-local
checkout paths from the P46 manifest were absent.

The durable fixture is:

```text
tests/fixtures/docc2context_ai_draft_same_scope_bounded_rerun_gate/p49-t3-docc2context-ai-draft-same-scope-bounded-rerun-gate.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.docc2context-ai-draft-same-scope-bounded-rerun-gate/v0
kind: SpecHarvesterDocc2contextAIDraftSameScopeBoundedRerunGate
authority: producer_docc2context_ai_draft_same_scope_bounded_rerun_gate_evidence_only
```

Evidence input:

```text
tests/fixtures/docc2context_ai_draft_targeted_follow_up_pass/p49-t2-docc2context-ai-draft-targeted-follow-up-pass.example.json
inputs/p46-bounded-popular-library-pilot/repositories.yml
```

## Result

Selected outcome:

```text
same_scope_bounded_rerun_gate_blocked_operator_local_checkouts_missing
```

LM Studio was available with `openai/gpt-oss-20b`, but P49-T3 stopped before
the static-only gate because the same-scope source checkouts were absent:

- `flask`: `/Users/egor/Development/GitHub/0AL/flask`
- `gin`: `/Users/egor/Development/GitHub/0AL/gin`
- `xyflow`: `/Users/egor/Development/GitHub/0AL/xyflow`
- `cupertino`: `/Users/egor/Development/GitHub/0AL/cupertino`
- `navigation-split-view`: `/Users/egor/Development/GitHub/0AL/NavigationSplitView`
- `docc2context`: `/Users/egor/Development/GitHub/0AL/docc2context`

P49-T3 did not clone or fetch repositories and did not substitute a smaller
targeted run for the same six-repository gate.

## Carried-Forward Evidence

P49-T2 remains visible as:

```text
docc2context.aiDraft_warning_explicitly_non_blocking_for_p49_t3
excluded_package_also_selected
```

The previous `docc2context.aiDraft` blocking diagnostics remain cleared for the
gate:

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

The xyflow caveats remain larger-corpus blockers until P49-T4:

- `xyflow.partial_public_interface_index`
- `xyflow.operator_checkout_origin_fork_mismatch`

## P49-T4 Input

P49-T4 must record the exit decision. The available decision options are:

- `stop_on_operator_local_checkout_blocker`
- `rerun_p49_t3_after_operator_local_checkouts_are_restored`
- `record_no_larger_corpus_readiness`

Larger curated corpus planning remains blocked.

## Boundary

P49-T3 does not approve a larger curated corpus, expand beyond the same
six-repository bounded pilot scope, accept packages or relations, publish
registry metadata, seed baselines, remove `preview_only`, run adapters, enable
trusted local adapter execution, clone or fetch repositories, install
dependencies, invoke package managers, execute harvested code, run the
static-only gate, or run the AI-enabled gate.

The gate evidence does not persist raw prompts, persist raw provider responses,
persist secrets, or persist chain-of-thought. It does not treat AI output as
registry truth, static output as registry truth, rerun output as registry
truth, targeted follow-up output as registry truth, exit-decision output as
registry truth, or adapter output as registry truth.
