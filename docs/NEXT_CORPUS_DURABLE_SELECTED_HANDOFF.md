# Next-Corpus Durable Selected Handoff

Status: P33-T7 durable selected handoff evidence.

This page records the durable selected handoff artifact for the P33 next
bounded corpus. It closes the P33-T6 gap where the P33-T5 candidate-layer
triage fixture was useful review evidence but not a supported SpecPM selected
handoff payload.

The machine-readable fixture is:

```text
tests/fixtures/next_corpus_durable_selected_handoff/p33-t7-next-corpus-selected-handoff.example.json
```

Its identity is:

```json
{
  "apiVersion": "spec-harvester.selected-candidate-handoff-proposal/v0",
  "kind": "SpecHarvesterSelectedCandidateHandoffProposal",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Selected Candidates

The durable handoff contains three selected candidates:

| Candidate | Repository | Maintainer action |
| --- | --- | --- |
| `serena.core` | `serena` | `review_for_possible_specpm_intake` |
| `transmission.core` | `transmission` | `review_for_possible_specpm_intake` |
| `specpm.core` | `specpm` | `review_for_possible_specpm_intake` |

Every selected candidate remains `previewOnly: true`, carries producer
preflight status `passed`, has static viewer status `ok`, and keeps
`registryAcceptanceDecision.status: external_required`.

## Deferred Candidates

The durable handoff excludes:

| Candidate | Reason |
| --- | --- |
| `mcpm.system` | package identity drift plus warning-bearing AI draft evidence |
| `specgraph.system` | package identity drift |

They remain outside selected handoff until regenerated or explicitly approved.

## Evidence Roles

P33-T7 deliberately uses committed, digest-backed corpus fixtures instead of
per-file generated candidate digests that are not present in the repository:

| Role | Source |
| --- | --- |
| `selected_handoff_dry_run` | P33-T5 candidate-layer triage fixture |
| `source_manifest` | P33-T2 source manifest |
| `deterministic_dry_run` | P33-T3 deterministic fixture |
| `live_local_model_batch` | P33-T4 live local-model fixture |

This avoids fabricating digests for historical generated `specpm.yaml`,
`specs/*.spec.yaml`, receipts, validation reports, diagnostics, quality
reports, preflight reports, or viewer payloads.

## SpecPM Preflight Result

The durable handoff passed the current SpecPM selected handoff preflight:

```bash
PYTHONPATH=src python3 -m specpm.cli producer-bundle \
  preflight-selected-candidate-handoff \
  --body /Users/egor/Development/GitHub/0AL/SpecHarvester/tests/fixtures/next_corpus_durable_selected_handoff/p33-t7-next-corpus-selected-handoff.example.json \
  --root /Users/egor/Development/GitHub/0AL/SpecHarvester \
  --json
```

SpecPM revision:

```text
8a5ce3dece3d18bf8f601a5a599520bd520c7839
```

Summary:

```json
{
  "status": "passed",
  "summary": {
    "selectedCandidateCount": 3,
    "deferredCandidateCount": 2,
    "requiredEvidenceRoleCount": 4,
    "digestVerifiedCount": 1,
    "errorCount": 0,
    "warningCount": 0
  }
}
```

Counter summary: selectedCandidateCount: 3, deferredCandidateCount: 2,
requiredEvidenceRoleCount: 4, digestVerifiedCount: 1, zero warnings, and zero
errors.

## Meaning

P33-T7 makes the selected scope machine-preflightable by SpecPM. It still does
not make any candidate an accepted registry package.

The next bounded follow-up should record the intake readiness decision for the
preflighted selected scope, similar to the earlier limited-corpus readiness
step.

## Non-Authority Boundary

P33-T7 does not:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create a SpecPM pull request;
- treat AI output as registry truth;
- replace author or SpecPM maintainer review.

Short form: the selected handoff is preflightable review evidence, not
registry acceptance.
