# docc2context AI Draft Targeted Follow-Up Pass

Status: P49-T2 result.

P49-T2 executed the targeted follow-up pass selected by P49-T1 for the
remaining `docc2context.aiDraft` blocker. The pass targeted only
`docc2context.aiDraft` and kept local model output proposal-only.

The durable fixture is:

```text
tests/fixtures/docc2context_ai_draft_targeted_follow_up_pass/p49-t2-docc2context-ai-draft-targeted-follow-up-pass.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.docc2context-ai-draft-targeted-follow-up-pass/v0
kind: SpecHarvesterDocc2contextAIDraftTargetedFollowUpPass
authority: producer_docc2context_ai_draft_targeted_follow_up_pass_evidence_only
```

Evidence input:

```text
tests/fixtures/docc2context_ai_draft_targeted_follow_up_plan/p49-t1-docc2context-ai-draft-targeted-follow-up-plan.example.json
inputs/p46-bounded-popular-library-pilot/repositories.yml
```

## Result

Selected outcome:

```text
docc2context.aiDraft_warning_explicitly_non_blocking_for_p49_t3
```

The targeted LM Studio run used `openai/gpt-oss-20b` through
`package-set-ai-draft-proposal`. It emitted a proposal-only warning:

```text
excluded_package_also_selected
```

The previous blocking diagnostics are cleared or explicitly disposed for the
P49-T3 rerun gate:

```text
ai_json_repair_exhausted
ai_json_repair_needed
package_set_subject_metadata_missing
```

JSON repair was `not_needed`, raw prompts and raw provider responses were not
persisted, and chain-of-thought was not persisted. The selected member metadata
contains `docc2context.core` with role `primary_package`.

## Execution Note

The P46 manifest points at the operator-local checkout path
`../../../docc2context`, resolved as:

```text
/Users/egor/Development/GitHub/0AL/docc2context
```

That checkout was absent at execution time. P49-T2 did not clone or fetch.
Instead, it used source-manifest-backed minimal workspace inventory for
`docc2context.core` so the targeted AI draft path could validate the remaining
subject metadata and JSON repair blocker without expanding scope. The recorded
execution caveat is `operator_local_checkout_missing_no_clone_fetch`.

## P49-T3 Readiness

P49-T3 is approved to rerun the same six-repository bounded pilot gate using:

```text
inputs/p46-bounded-popular-library-pilot/repositories.yml
```

P49-T3 must preserve static-only-before-AI ordering, proposal-only AI output,
no raw prompt/response/chain-of-thought persistence, no registry promotion, and
the carried-forward warning IDs:

- `flask.aiDraft`
- `flask.aiEnrichment`
- `gin.aiDraft`
- `cupertino.aiDraft`
- `navigation-split-view.aiDraft`

The xyflow caveats remain visible until the P49-T4 exit decision:

- `xyflow.partial_public_interface_index`
- `xyflow.operator_checkout_origin_fork_mismatch`

## Boundary

P49-T2 does not approve a larger curated corpus, run the same-scope bounded
rerun, expand beyond `docc2context.aiDraft`, run adapters, enable trusted local
adapter execution, clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, accept packages or relations, publish
registry metadata, seed baselines, or remove `preview_only`.

The pass does not persist raw prompts, persist raw provider responses, persist
secrets, or persist chain-of-thought. It does not treat AI output as registry
truth, static output as registry truth, targeted follow-up output as registry
truth, exit-decision output as registry truth, plan output as registry truth,
or adapter output as registry truth.
