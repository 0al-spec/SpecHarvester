# AI Draft Blocker Bounded Rerun Gate

Status: P48-T3 result.

P48-T3 reran the same six-repository bounded pilot gate after the P48-T2 AI
draft blocker follow-up. It preserved static-only-before-AI ordering and kept
all local model output proposal-only.

The durable fixture is:

```text
tests/fixtures/ai_draft_blocker_bounded_rerun_gate/p48-t3-ai-draft-blocker-bounded-rerun-gate.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.ai-draft-blocker-bounded-rerun-gate/v0
kind: SpecHarvesterAIDraftBlockerBoundedRerunGate
authority: producer_ai_draft_blocker_bounded_rerun_gate_evidence_only
```

Evidence input:

```text
tests/fixtures/ai_draft_blocker_follow_up_pass/p48-t2-ai-draft-blocker-follow-up-pass.example.json
```

## Result

Selected outcome:

```text
bounded_rerun_executed_static_passed_ai_failed_on_docc2context_ai_draft
```

Static-only gate:

```text
status: passed
processed: 6
failed repositories: 0
passed preflight: 6
```

AI-enabled gate:

```text
status: failed
exit code: 1
processed: 6
failed repositories: 1
passed preflight: 6
AI draft proposals: 5
AI enrichment proposals: 6
```

The P48-T2 dispositions worked for the specific hard failures they targeted:
`gin.aiDraft` and `navigation-split-view.aiDraft` no longer hard-failed. The
rerun exposed one remaining blocker: `docc2context.aiDraft` failed JSON repair
and emitted `package_set_subject_metadata_missing`.

## Repository Outcomes

| Repository | Static gate | AI draft | AI enrichment | Notes |
| --- | --- | --- | --- | --- |
| `flask` | passed | warning | warning | non-blocking proposal gaps remain |
| `gin` | passed | warning | completed | previous hard failure resolved to warning |
| `xyflow` | passed | completed | completed | partial interface and fork-origin caveats remain visible |
| `cupertino` | passed | warning | completed | non-blocking proposal gaps remain |
| `navigation-split-view` | passed | warning | completed | previous hard failure resolved to warning |
| `docc2context` | passed | failed | completed | remaining blocker: `ai_json_repair_exhausted` and `package_set_subject_metadata_missing` |

## Gate Decision

P48-T3 is complete as a bounded rerun gate, but it does not approve a larger
curated corpus.

The selected next task is P48-T4 Record Post-Blocker Follow-Up Exit Decision.
P48-T4 must decide whether the remaining `docc2context.aiDraft` blocker
requires another targeted pass, can be accepted as a non-blocking pilot caveat,
or stops larger corpus planning.

## Boundary

P48-T3 does not approve a larger curated corpus, expand beyond the same
six-repository bounded pilot scope, accept packages or relations, publish
registry metadata, seed baselines, remove `preview_only`, run adapters, enable
trusted local adapter execution, clone or fetch repositories, install
dependencies, invoke package managers inside harvested repositories, or execute
harvested code.

The rerun does not persist raw prompts, persist raw provider responses,
persist secrets, or persist chain-of-thought. The rerun does not treat AI
output as registry truth, static output as registry truth, rerun output as
registry truth, follow-up output as registry truth, or adapter output as
registry truth.
