# Next-Corpus SpecPM Preflight and Intake Decision

Status: P33-T6 consumer preflight coordination evidence.

This page records the SpecPM-side selected candidate handoff preflight result
for the P33 next bounded corpus after P33-T5 selected the next handoff scope.

The machine-readable fixture is:

```text
tests/fixtures/next_corpus_specpm_preflight_intake_decision/p33-t6-next-corpus-specpm-preflight-intake-decision.example.json
```

Its identity is:

```json
{
  "apiVersion": "spec-harvester.next-corpus-specpm-preflight-intake-decision/v0",
  "kind": "SpecHarvesterNextCorpusSpecPMPreflightIntakeDecision",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Inputs

P33-T6 does not run a new scrape, does not rerun LM Studio, and does not
regenerate candidate bundles. It consumes committed P33 evidence only:

- P33-T5 candidate-layer triage:
  `tests/fixtures/next_corpus_candidate_layer_triage/p33-t5-next-corpus-candidate-layer-triage.example.json`;
- P33-T4 live local-model batch:
  `tests/fixtures/next_corpus_live_local_model_batch/p33-t4-next-corpus-live-local-model.example.json`;
- P33-T3 deterministic batch:
  `tests/fixtures/next_corpus_deterministic_dry_run/p33-t3-next-corpus-deterministic-dry-run.example.json`;
- P33-T2 source manifest:
  `inputs/p33-next-corpus/repositories.yml`.

Each input is digest-backed in the fixture.

## Selected Scope

P33-T5 selected three candidates for the next handoff boundary:

| Candidate | Repository | P33-T6 result |
| --- | --- | --- |
| `serena.core` | `serena` | needs durable selected handoff payload |
| `transmission.core` | `transmission` | needs durable selected handoff payload |
| `specpm.core` | `specpm` | needs durable selected handoff payload |

The selected candidates remain useful producer evidence, but they are not yet
ready for SpecPM maintainer intake review because the committed P33-T5 triage
fixture is not itself a supported SpecPM handoff payload.

## Deferred Scope

P33-T6 keeps two candidates outside the selected handoff preflight:

| Candidate | Repository | Reason |
| --- | --- | --- |
| `mcpm.system` | `mcpm-sh` | package identity drift and warning-bearing AI draft evidence |
| `specgraph.system` | `specgraph` | package identity drift |

## SpecPM Gate Result

The current SpecPM selected candidate handoff preflight was run against the
committed P33-T5 triage fixture:

```bash
PYTHONPATH=src python3 -m specpm.cli producer-bundle \
  preflight-selected-candidate-handoff \
  --body /Users/egor/Development/GitHub/0AL/SpecHarvester/tests/fixtures/next_corpus_candidate_layer_triage/p33-t5-next-corpus-candidate-layer-triage.example.json \
  --root /Users/egor/Development/GitHub/0AL/SpecHarvester \
  --json
```

SpecPM revision:

```text
8a5ce3dece3d18bf8f601a5a599520bd520c7839
```

The report failed with:

```json
{
  "status": "failed",
  "summary": {
    "selectedCandidateCount": 0,
    "deferredCandidateCount": 0,
    "digestVerifiedCount": 0,
    "errorCount": 1,
    "warningCount": 0
  },
  "errors": [
    {
      "code": "selected_handoff_payload_missing"
    }
  ]
}
```

This is the expected consumer boundary. P33-T5 is a candidate-layer triage
artifact. SpecPM correctly requires a supported
`SpecHarvesterSelectedCandidateHandoffProposal` or related selected handoff
payload before maintainer intake review.

## Intake Decision

The P33 next corpus is not ready for SpecPM maintainer intake review yet.

Decision:

```text
not_ready_requires_durable_selected_handoff_artifact
```

The next bounded task is P33-T7. It should create durable selected handoff
evidence for `serena.core`, `transmission.core`, and `specpm.core`, or
explicitly extend the SpecPM consumer gate to accept the P33 decision shape.
That task must not invent per-file evidence digests from summary-only fixtures.

## Non-Authority Boundary

P33-T6 does not:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create a SpecPM pull request;
- treat AI output as registry truth;
- replace author or SpecPM maintainer review.

Short form: P33-T6 records a failed consumer preflight and a bounded follow-up,
not a failed product run and not registry acceptance.
