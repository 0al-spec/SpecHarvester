# P32-T6 Validation Report

Task: `P32-T6 SpecPM Selected Candidate Handoff Preflight`

## Scope

P32-T6 records the SpecPM-side consumer gate for the P32-T5 refreshed selected
candidate handoff artifact. The gate lives in SpecPM and was merged through
[`0al-spec/SpecPM#140`](https://github.com/0al-spec/SpecPM/pull/140).

## SpecPM Revision

```text
8a5ce3dece3d18bf8f601a5a599520bd520c7839
Merge pull request #140 from 0al-spec/codex/selected-candidate-handoff-preflight
```

## Command

```bash
PYTHONPATH=src python3 -m specpm.cli producer-bundle \
  preflight-selected-candidate-handoff \
  --body /Users/egor/Development/GitHub/0AL/SpecHarvester/tests/fixtures/refreshed_candidate_layer_selected_handoff/p32-t5-refreshed-candidate-layer-selected-handoff.example.json \
  --root /Users/egor/Development/GitHub/0AL/SpecHarvester \
  --json
```

## Result

```json
{
  "status": "passed",
  "summary": {
    "selectedCandidateCount": 8,
    "deferredCandidateCount": 1,
    "requiredEvidenceRoleCount": 6,
    "digestVerifiedCount": 3,
    "errorCount": 0,
    "warningCount": 0
  }
}
```

Selected candidates:

- `flask.core`
- `gin.core`
- `docc2context.core`
- `xyflow.workspace`
- `xyflow.react`
- `xyflow.svelte`
- `xyflow.system`
- `navigation_split_view.core`

Deferred candidate:

- `cupertino.core` remains deferred on `refined_summary_missing`.

## Boundary Check

The SpecPM report keeps the handoff as review evidence only:

- `preflightOnly: true`
- `acceptsPackages: false`
- `acceptsRelations: false`
- `seedsBaselines: false`
- `removesPreviewOnly: false`
- `publishesRegistryMetadata: false`
- `createsSpecPMPullRequest: false`

## Verdict

PASS. P32-T6 is complete. The P32-T5 refreshed handoff is now
machine-checkable by SpecPM before maintainers make the P32-T7 intake readiness
decision.
