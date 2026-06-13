# Next-Corpus Intake Readiness Decision

Status: P33-T8 intake readiness decision.

This page records the Phase 33 stop point after the durable selected handoff
passed the SpecPM selected candidate handoff preflight.

The machine-readable fixture is:

```text
tests/fixtures/next_corpus_intake_readiness_decision/p33-t8-next-corpus-intake-readiness-decision.example.json
```

Its identity is:

```json
{
  "apiVersion": "spec-harvester.next-corpus-intake-readiness-decision/v0",
  "kind": "SpecHarvesterNextCorpusIntakeReadinessDecision",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Decision

Decision status:

```text
ready_for_author_maintainer_review_with_explicit_deferral
```

The selected scope is ready for author/maintainer review because the P33-T7
durable selected handoff passed SpecPM selected handoff preflight. This means
maintainers can review the selected preview candidates as intake evidence. It
does not mean any package is accepted into the SpecPM public registry.

## Inputs

P33-T8 references committed P33 evidence:

| Input | Path | Status |
| --- | --- | --- |
| P33-T7 durable selected handoff | `tests/fixtures/next_corpus_durable_selected_handoff/p33-t7-next-corpus-selected-handoff.example.json` | `specpm_preflight_passed` |
| P33-T5 candidate-layer triage | `tests/fixtures/next_corpus_candidate_layer_triage/p33-t5-next-corpus-candidate-layer-triage.example.json` | `selected_candidates_triaged` |
| P33 source manifest | `inputs/p33-next-corpus/repositories.yml` | committed local manifest |
| SpecPM selected handoff preflight | `SpecPMSelectedCandidateHandoffPreflightReport` | `passed` |

SpecPM revision:

```text
8a5ce3dece3d18bf8f601a5a599520bd520c7839
```

Preflight summary:

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

## Selected Candidates

The selected review scope contains:

| Candidate | Repository | Status |
| --- | --- | --- |
| `serena.core` | `serena` | `ready_for_author_maintainer_review` |
| `transmission.core` | `transmission` | `ready_for_author_maintainer_review` |
| `specpm.core` | `specpm` | `ready_for_author_maintainer_review` |

All selected candidates remain `previewOnly: true` and keep
`registryAcceptanceDecision.status: external_required`.

## Deferred Candidates

The decision explicitly keeps these candidates outside intake readiness:

| Candidate | Repository | Reason |
| --- | --- | --- |
| `mcpm.system` | `mcpm-sh` | package identity drift plus warning-bearing AI draft evidence |
| `specgraph.system` | `specgraph` | package identity drift |

They remain deferred until the package identity and AI draft evidence findings
are resolved or explicitly reviewed in a later task.

## Meaning

P33-T8 closes the Phase 33 bounded corpus expansion loop. The selected scope is
now reviewable by authors and SpecPM maintainers, and the deferred scope is
visible with required follow-up.

The next step, if maintainers want to publish anything, is a separate SpecPM
maintainer flow. That flow may accept, reject, or request regeneration for each
candidate independently.

## Non-Authority Boundary

P33-T8 does not:

- run a new scrape;
- rerun LM Studio or any model provider;
- clone repositories;
- fetch remote state;
- install dependencies;
- execute harvested repository code;
- mutate generated candidate bundles;
- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create a SpecPM pull request;
- replace author review;
- replace SpecPM maintainer review;
- treat AI output as registry truth.

Short form: the selected scope is ready for author/maintainer review, not
accepted into the registry.
