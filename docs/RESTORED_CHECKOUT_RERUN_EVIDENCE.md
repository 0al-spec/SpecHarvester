# Restored-Checkout Rerun Evidence

Status: P50-T1 result.

P50-T1 records the same-scope bounded rerun after the operator-local checkout
paths expected by the P46 manifest were restored. It does not rewrite P49-T4:
P49-T4 correctly recorded no larger corpus readiness when all six checkouts
were missing. P50-T1 adds new evidence after the local environment was fixed.

The durable fixture is:

```text
tests/fixtures/restored_checkout_rerun_evidence/p50-t1-restored-checkout-rerun-evidence.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.restored-checkout-rerun-evidence/v0
kind: SpecHarvesterRestoredCheckoutRerunEvidence
authority: producer_restored_checkout_rerun_evidence_only
```

Evidence inputs:

```text
tests/fixtures/docc2context_follow_up_exit_decision/p49-t4-docc2context-follow-up-exit-decision.example.json
inputs/p46-bounded-popular-library-pilot/repositories.yml
/tmp/specharvester-p49-t3-rerun-after-checkout-restore-20260625T004309/output-static/autonomous-candidate-batch-report.json
/tmp/specharvester-p49-t3-rerun-after-checkout-restore-20260625T004309/output-ai/autonomous-candidate-batch-report.json
```

## Restored Checkout Paths

The P46 manifest still points to sibling paths under
`/Users/egor/Development/GitHub/0AL/`. P50-T1 restored those paths through
operator-local symlinks to the pinned checkouts under
`/Users/egor/Development/GitHub/`.

| Repository | Expected path | Target path | Revision |
| --- | --- | --- | --- |
| `flask` | `/Users/egor/Development/GitHub/0AL/flask` | `/Users/egor/Development/GitHub/flask` | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` |
| `gin` | `/Users/egor/Development/GitHub/0AL/gin` | `/Users/egor/Development/GitHub/gin` | `5f4f9643258dc2a65e684b63f12c8d543c936c67` |
| `xyflow` | `/Users/egor/Development/GitHub/0AL/xyflow` | `/Users/egor/Development/GitHub/xyflow` | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` |
| `cupertino` | `/Users/egor/Development/GitHub/0AL/cupertino` | `/Users/egor/Development/GitHub/cupertino` | `65dcae238d30cfbd0d9d15ae10f7b8c67575c19b` |
| `navigation-split-view` | `/Users/egor/Development/GitHub/0AL/NavigationSplitView` | `/Users/egor/Development/GitHub/NavigationSplitView` | `2c88df50b8f587560b91f6027e9ea275aee17060` |
| `docc2context` | `/Users/egor/Development/GitHub/0AL/docc2context` | `/Users/egor/Development/GitHub/docc2context` | `a2babcc4910c87bbd1b65f9a4221097f5ae4b753` |

All six restored checkouts matched the manifest revisions. The xyflow origin
caveat remains visible because the local origin is the operator fork
`git@github.com:SoundBlaster/xyflow.git`.

## Rerun Result

P50-T1 preserved static-only-before-AI ordering:

1. static-only gate;
2. AI-enabled gate through local LM Studio `openai/gpt-oss-20b`.

| Gate | Status | Processed | Failed | Passed preflight |
| --- | --- | ---: | ---: | ---: |
| static-only | `passed` | 6 | 0 | 6 |
| AI-enabled | `passed` | 6 | 0 | 6 |

AI-enabled proposal counts:

| Proposal type | Count |
| --- | ---: |
| AI draft proposals | 6 |
| AI enrichment proposals | 6 |

Provider token counts recorded by the AI enrichment summaries:

| Token class | Count |
| --- | ---: |
| Prompt tokens | 107,251 |
| Completion tokens | 4,005 |
| Total tokens | 111,256 |

Raw prompts, raw provider responses, secrets, and chain-of-thought were not
persisted.

## Remaining Warnings

The restored rerun passed, but warnings and caveats remain review evidence:

- Flask: `excluded_package_also_selected`,
  `selected_member_role_unknown`, `refined_summary_missing`.
- Gin: `selected_member_role_unknown`.
- xyflow: `partial_public_interface_index`,
  `operator_checkout_origin_fork_mismatch`, `refined_summary_missing`.
- Cupertino: `excluded_package_also_selected`,
  `selected_member_role_unknown`.
- NavigationSplitView: `selected_member_role_unknown`,
  `ai_json_repair_needed`.
- docc2context: `excluded_package_also_selected`,
  `selected_member_role_unknown`.

These warnings do not make the rerun a failure, but they are not registry
acceptance.

## Current Decision

Selected outcome:

```text
larger_corpus_planning_reconsideration_ready_after_restored_checkout_rerun
```

The checkout blocker is resolved, and both same-scope gates passed. Larger
curated corpus planning can now be authored from the restored-checkout rerun
evidence. That means planning readiness, not package acceptance, relation
acceptance, registry publication, or maintainer approval.

## Boundary

P50-T1 does not accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, clone or fetch repositories, install
dependencies, invoke package managers, execute harvested code, run adapters, or
enable trusted local adapter execution.

The restored rerun evidence does not treat AI output as registry truth, static
output as registry truth, rerun output as registry truth, targeted follow-up
output as registry truth, exit-decision output as registry truth, or adapter
output as registry truth.
