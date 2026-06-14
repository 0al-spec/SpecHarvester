# Next-Corpus SpecPM Preflight and Intake Decision

P33-T6 records `SpecHarvesterNextCorpusSpecPMPreflightIntakeDecision` with
`apiVersion: spec-harvester.next-corpus-specpm-preflight-intake-decision/v0`.
The authority is `producer_preview_evidence_only`.
The fixture lives at
`tests/fixtures/next_corpus_specpm_preflight_intake_decision/p33-t6-next-corpus-specpm-preflight-intake-decision.example.json`.

## Result

P33-T5 selected `serena.core`, `transmission.core`, and `specpm.core` for the
next handoff boundary. P33-T6 ran the current SpecPM selected candidate handoff
preflight against the committed P33-T5 triage fixture and received
`selected_handoff_payload_missing`.

This is a boundary finding, not registry failure: P33-T5 is a candidate-layer
triage artifact, not a supported `SpecHarvesterSelectedCandidateHandoffProposal`
payload.

## Decision

The intake decision is
`not_ready_requires_durable_selected_handoff_artifact`.

`mcpm.system` and `specgraph.system` remain deferred. The selected candidates
need a durable selected handoff payload before SpecPM maintainer intake review.
P33-T7 is the next bounded follow-up for that durable selected handoff
artifact. The completed artifact is recorded in
<doc:NextCorpusDurableSelectedHandoff>.

See the GitHub-facing source page:
`docs/NEXT_CORPUS_SPECPM_PREFLIGHT_INTAKE_DECISION.md`.
