# Next-Corpus Intake Readiness Decision

P33-T8 records `SpecHarvesterNextCorpusIntakeReadinessDecision` with
`apiVersion: spec-harvester.next-corpus-intake-readiness-decision/v0` and
authority `producer_preview_evidence_only`.

The fixture lives at
`tests/fixtures/next_corpus_intake_readiness_decision/p33-t8-next-corpus-intake-readiness-decision.example.json`.

## Decision

The decision status is
`ready_for_author_maintainer_review_with_explicit_deferral`.

The selected candidates `serena.core` and `specpm.core` are ready for
author/maintainer review because the P33-T7 durable selected handoff passed
SpecPM selected handoff preflight.

The deferred candidates remain `transmission.core`, `mcpm.system`, and
`specgraph.system`.

## SpecPM Result

The current SpecPM selected candidate handoff preflight passes with
`selectedCandidateCount: 2`, `deferredCandidateCount: 3`,
`requiredEvidenceRoleCount: 4`, `digestVerifiedCount: 1`, and zero warnings or
errors.

SpecPM revision:
`8a5ce3dece3d18bf8f601a5a599520bd520c7839`.

Counter summary: selectedCandidateCount: 2, deferredCandidateCount: 3,
requiredEvidenceRoleCount: 4, digestVerifiedCount: 1, zero warnings, and zero
errors.

## Boundary

P33-T8 is review evidence only. It does not accept packages, accept relations,
seed baselines, remove `preview_only`, publish registry metadata, create a
SpecPM pull request, replace author review, replace SpecPM maintainer review,
or treat AI output as registry truth.

See the GitHub-facing source page:
`docs/NEXT_CORPUS_INTAKE_READINESS_DECISION.md`.
