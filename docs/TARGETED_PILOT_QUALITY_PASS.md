# Targeted Pilot Quality Pass

Status: P47-T2 targeted quality pass.

P47-T2 executes the targeted quality pass planned by P47-T1. This is an
explicit disposition pass over the current P46 blockers, not a pilot rerun and
not an AI run. The pass decides that the bounded rerun gate can proceed in
P47-T3, while the larger curated corpus remains blocked until P47-T3 and P47-T4
complete.

The durable fixture is:

```text
tests/fixtures/targeted_pilot_quality_pass/p47-t2-targeted-pilot-quality-pass.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.targeted-pilot-quality-pass/v0
kind: SpecHarvesterTargetedPilotQualityPass
authority: producer_quality_pass_evidence_only
```

## Source Plan

P47-T2 starts from the P47-T1 quality follow-up plan:

```text
tests/fixtures/targeted_pilot_quality_follow_up_plan/p47-t1-targeted-pilot-quality-follow-up-plan.example.json
```

Source digest:

```text
sha256:158f717aac9c5a92df9197a4624b08e82d1bad4963a71c35ca1e9d105439c5a2
```

## Selected Outcome

```text
ready_for_bounded_rerun_gate_with_explicit_exclusions
```

The bounded rerun gate is ready for P47-T3 because each current P46 blocker has
an explicit bounded-rerun disposition. The larger curated corpus is not
approved.

## Sidecar Dispositions

| Sidecar | Class | Disposition | Blocks P47-T3 gate | Registry truth |
| --- | --- | --- | --- | --- |
| `gin.aiDraft` | do-not-promote AI draft | Exclude current sidecar from bounded rerun gate | no | no |
| `docc2context.aiDraft` | do-not-promote AI draft | Exclude current sidecar from bounded rerun gate | no | no |
| `xyflow.aiEnrichment` | unsupported AI enrichment | Exclude current unsupported enrichment sidecar | no | no |

The excluded sidecars remain visible. They must not be reused as truth in the
P47-T3 rerun. P47-T3 may emit new proposal-only sidecars, but any new AI output
must stay proposal-only and must not persist raw prompts, raw provider
responses, secrets, or chain-of-thought.

## xyflow Caveat Dispositions

| Caveat | Disposition | Blocks P47-T3 gate | Larger corpus state |
| --- | --- | --- | --- |
| `partial_public_interface_index` | Accepted for bounded rerun with author review visibility | no | blocked until P47-T4 |
| `operator_checkout_origin_fork_mismatch` | Accepted for bounded rerun as an operator checkout caveat | no | blocked until P47-T4 |
| `model_evidence_path_unsupported` | Covered by `xyflow.aiEnrichment` exclusion | no | blocked until P47-T4 |

These dispositions do not make xyflow claims final. They only allow the same
six-repository bounded gate to run while preserving caveats.

## Bounded Rerun Gate

P47-T3 is approved to run the bounded rerun gate under these constraints:

- use the same six-repository bounded pilot scope;
- use `inputs/p46-bounded-popular-library-pilot/repositories.yml`;
- verify pinned local checkouts without clone or fetch;
- run static-only evidence before AI-enabled evidence;
- keep AI-enabled output proposal-only;
- keep excluded current sidecars out of promotion;
- record new or remaining caveats in P47-T3;
- do not approve a larger curated corpus.

## Larger Corpus Gate

The larger curated corpus remains blocked now by:

- `p47_t3_bounded_rerun_gate_not_run`;
- `p47_t4_quality_follow_up_exit_decision_not_recorded`.

The original P46 blockers are disposed only for the bounded rerun gate:

- `gin.aiDraft`;
- `docc2context.aiDraft`;
- `xyflow.aiEnrichment`;
- `partial_public_interface_index`;
- `operator_checkout_origin_fork_mismatch`;
- `model_evidence_path_unsupported`.

## Boundary

P47-T2 did not rerun the pilot, run AI, run adapters, enable trusted local
adapter execution, clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, persist raw
prompts, persist raw provider responses, persist secrets, or persist
chain-of-thought.

The quality pass does not treat quality-pass output as registry truth, does
not treat plan output as registry truth, does not treat static output as
registry truth, does not treat AI output as registry truth, and does not treat
adapter output as registry truth.

## Follow-Up

After P47-T2 archives, the selected next task is P47-T3 Run Bounded Pilot Rerun
Gate. A larger curated corpus is still not approved.
