# AI Draft Blocker Follow-Up Pass

Status: P48-T2 result.

P48-T2 records the targeted follow-up pass selected by P48-T1. It disposes the
remaining blocking AI draft sidecars for the same six-repository bounded pilot
rerun gate while preserving proposal-only and registry authority boundaries.

The durable fixture is:

```text
tests/fixtures/ai_draft_blocker_follow_up_pass/p48-t2-ai-draft-blocker-follow-up-pass.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.ai-draft-blocker-follow-up-pass/v0
kind: SpecHarvesterAIDraftBlockerFollowUpPass
authority: producer_ai_draft_blocker_follow_up_pass_evidence_only
```

Evidence input:

```text
tests/fixtures/ai_draft_blocker_follow_up_plan/p48-t1-ai-draft-blocker-follow-up-plan.example.json
```

## Result

Selected outcome:

```text
ready_for_p48_t3_bounded_rerun_gate_with_explicit_ai_draft_dispositions
```

Mode:

```text
explicit_disposition_evidence_only
```

P48-T2 does not approve larger curated corpus planning. It only clears the
immediate P48-T3 rerun precondition by recording explicit dispositions for the
failed AI draft sidecars.

## Dispositions

| Evidence | P48-T2 disposition | Blocks P48-T3 gate | Blocks larger corpus until P48-T4 |
| --- | --- | --- | --- |
| `gin.aiDraft` | `explicitly_disposed_non_blocking_for_p48_t3_rerun_gate` | no | yes |
| `navigation-split-view.aiDraft` | `explicitly_disposed_non_blocking_for_p48_t3_rerun_gate` | no | yes |
| `docc2context.aiDraft` | `kept_visible_as_non_blocking_warning_for_p48_t3` | no | no |
| `xyflow.aiEnrichment` | `kept_visible_as_larger_corpus_blocking_caveat_until_p48_t4` | no | yes |
| `partial_public_interface_index` | kept visible | no | yes |
| `operator_checkout_origin_fork_mismatch` | kept visible | no | yes |
| `ai_json_repair_needed` | covered by xyflow warning visibility | no | yes |

For `gin.aiDraft` and `navigation-split-view.aiDraft`, the active P48-T3
blockers `ai_json_repair_exhausted` and
`package_set_subject_metadata_missing` are explicitly disposed as non-blocking
for the rerun gate. The current failed sidecars remain non-promotable and must
not be reused as registry truth.

## P48-T3 Preconditions

P48-T3 is approved to run the same six-repository bounded pilot gate using:

```text
inputs/p46-bounded-popular-library-pilot/repositories.yml
```

P48-T3 must:

- verify the same six-repository bounded pilot scope;
- run the static-only gate before any AI-enabled gate;
- keep all AI output proposal-only;
- avoid raw prompt, response, and chain-of-thought persistence;
- keep current disposed AI sidecars out of registry truth;
- record any new or remaining warning and caveat evidence.

## Boundary

P48-T2 does not approve a larger curated corpus, rerun the pilot, run AI, run
adapters, enable trusted local adapter execution, clone or fetch repositories,
install dependencies, invoke package managers inside harvested repositories,
execute harvested code, accept packages or relations, publish registry
metadata, seed baselines, remove `preview_only`, persist raw prompts, persist
raw provider responses, persist secrets, or persist chain-of-thought.

The follow-up pass does not treat follow-up output as registry truth, does not
treat plan output as registry truth, does not treat static output as registry
truth, does not treat AI output as registry truth, and does not treat adapter
output as registry truth.

## Follow-Up

The selected next task is P48-T3 Run Bounded Pilot Rerun Gate After AI Draft
Blocker Follow-Up.

The larger curated corpus remains blocked until P48-T3 records the same-scope
bounded rerun gate and P48-T4 records the post-blocker follow-up exit decision.
