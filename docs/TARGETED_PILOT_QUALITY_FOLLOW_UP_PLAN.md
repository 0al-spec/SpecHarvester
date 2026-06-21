# Targeted Pilot Quality Follow-Up Plan

Status: P47-T1 quality follow-up plan.

P47-T1 turns the P46-T6 exit decision into a concrete targeted quality plan.
It does not rerun the pilot and does not approve a larger curated corpus. It
keeps the remaining blockers visible, defines repair or disposition paths, and
requires a bounded rerun gate before scale.

The durable fixture is:

```text
tests/fixtures/targeted_pilot_quality_follow_up_plan/p47-t1-targeted-pilot-quality-follow-up-plan.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.targeted-pilot-quality-follow-up-plan/v0
kind: SpecHarvesterTargetedPilotQualityFollowUpPlan
authority: producer_quality_follow_up_plan_evidence_only
```

## Source Decision

P47-T1 starts from the P46-T6 exit decision:

```text
run_targeted_quality_pass_before_larger_curated_corpus
```

P47-T1 selects:

```text
targeted_quality_follow_up_before_larger_curated_corpus
```

The source artifact is
`p46-t6-bounded-popular-library-pilot-exit-decision.example.json` with digest
`sha256:213337e4636eed6e0410bbf0066fb376a059d4482d5fcdf0ab71f8a246265ff7`.

## Carry-Forward Blockers

| Blocker | Source | Required disposition | Larger corpus blocker |
| --- | --- | --- | --- |
| `gin.aiDraft` | P46-T6 | Regenerate the AI draft or explicitly accept it as non-blocking with a reason | yes |
| `docc2context.aiDraft` | P46-T6 | Regenerate the AI draft or explicitly accept it as non-blocking with a reason | yes |
| `xyflow.aiEnrichment` | P46-T6 | Resolve the unsupported enrichment path or explicitly exclude the sidecar | yes |
| `partial_public_interface_index` | P46-T6 | Resolve the partial interface scope or accept it with a reason | yes |
| `operator_checkout_origin_fork_mismatch` | P46-T6 | Verify checkout origin or accept the fork-origin caveat | yes |
| `model_evidence_path_unsupported` | P46-T6 | Resolve the unsupported enrichment path or exclude the enrichment with a reason | yes |

These blockers stay visible until a later Phase 47 execution task resolves or
explicitly accepts them. P47-T1 only plans that work.

## Workstreams

| Workstream | Target | P47-T1 action | Exit criteria |
| --- | --- | --- | --- |
| `gin_ai_draft_quality_repair` | `gin.aiDraft` | Preserve blocker visibility and define execution acceptance | Valid subject identity or explicit non-blocking acceptance |
| `docc2context_ai_draft_quality_repair` | `docc2context.aiDraft` | Preserve blocker visibility and define execution acceptance | Valid package-set subject metadata or explicit non-blocking acceptance |
| `xyflow_caveat_disposition` | `xyflow.aiEnrichment` and xyflow caveats | Preserve sidecar and caveat visibility and define review evidence | Resolution, exclusion, or explicit acceptance for the sidecar and all three xyflow caveats |
| `bounded_rerun_gate` | same six pilot repositories | Define rerun gate and stop conditions | Static-only evidence first, AI proposal-only evidence second, then explicit exit decision |

## Bounded Rerun Gate

P47-T1 does not approve a rerun now. It defines the gate that must pass before
any larger curated corpus can be reconsidered:

- use the same six-repository bounded pilot scope;
- require pinned local checkouts from
  `inputs/p46-bounded-popular-library-pilot/repositories.yml`;
- record static-only evidence before AI-enabled evidence;
- keep AI-enabled output proposal-only;
- do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought;
- do not publish registry metadata, accept packages, accept relations, seed
  baselines, or remove `preview_only`;
- finish with an explicit quality follow-up exit decision.

The planned sequence is:

1. `P47-T2` execute the targeted quality pass.
2. `P47-T3` rerun the bounded pilot gate after targeted dispositions.
3. `P47-T4` record the quality follow-up exit decision.

## Larger Corpus Gate

The larger curated corpus remains blocked now. It can be reconsidered only
after:

- targeted quality pass execution;
- bounded rerun gate pass;
- quality follow-up exit decision.

## Boundary

P47-T1 did not rerun the pilot, run AI, run adapters, enable trusted local
adapter execution, clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, persist raw
prompts, persist raw provider responses, persist secrets, or persist
chain-of-thought.

The plan does not treat plan output as registry truth, does not treat
exit-decision output as registry truth, does not treat handoff output as
registry truth, does not treat static output as registry truth, does not treat
AI output as registry truth, and does not treat adapter output as registry
truth.

## Follow-Up

After P47-T1 archives, the selected next task is P47-T2 Execute Targeted Pilot
Quality Pass. A larger curated corpus is still not approved.
