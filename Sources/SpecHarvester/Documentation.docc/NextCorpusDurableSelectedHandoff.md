# Next-Corpus Durable Selected Handoff

P33-T7 records a durable `SpecHarvesterSelectedCandidateHandoffProposal` for
the P33 next bounded corpus with `apiVersion:
spec-harvester.selected-candidate-handoff-proposal/v0` and authority
`producer_preview_evidence_only`.

The fixture lives at
`tests/fixtures/next_corpus_durable_selected_handoff/p33-t7-next-corpus-selected-handoff.example.json`.

## Scope

The selected candidates are `serena.core`, `transmission.core`, and
`specpm.core`. The deferred candidates are `mcpm.system` and
`specgraph.system`.

The artifact references committed, digest-backed P33 evidence only:
P33-T5 candidate-layer triage, P33-T4 live local-model batch, P33-T3
deterministic batch, and the P33-T2 source manifest.

## SpecPM Result

The current SpecPM selected candidate handoff preflight passes with
`selectedCandidateCount: 3`, `deferredCandidateCount: 2`,
`requiredEvidenceRoleCount: 4`, `digestVerifiedCount: 1`, and zero warnings or
errors.

Counter summary: selectedCandidateCount: 3, deferredCandidateCount: 2,
requiredEvidenceRoleCount: 4, digestVerifiedCount: 1, zero warnings, and zero
errors.

This makes the selected scope machine-preflightable before maintainer intake
review. It does not accept packages, accept relations, publish registry
metadata, create a SpecPM pull request, or remove `preview_only`.

P33-T8 records the resulting intake readiness decision in
<doc:NextCorpusIntakeReadinessDecision>: the selected scope is ready for
author/maintainer review with explicit deferral for `mcpm.system` and
`specgraph.system`.

See the GitHub-facing source page:
`docs/NEXT_CORPUS_DURABLE_SELECTED_HANDOFF.md`.
