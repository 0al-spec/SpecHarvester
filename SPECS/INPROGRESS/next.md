# Next Task: P33-T8 Next-Corpus Intake Readiness Decision

**Status:** Selected
**Selected:** 2026-06-14
**Task:** P33-T8 Next-Corpus Intake Readiness Decision
**Phase:** Phase 33. Bounded Corpus Expansion Planning
**Last Archived:** P33-T7 Durable Next-Corpus Selected Handoff Artifact

## Recently Archived

- `P33-T6` recorded the next-corpus SpecPM preflight intake decision in
  `docs/NEXT_CORPUS_SPECPM_PREFLIGHT_INTAKE_DECISION.md`,
  `<doc:NextCorpusSpecPMPreflightIntakeDecision>`, and
  `tests/fixtures/next_corpus_specpm_preflight_intake_decision/p33-t6-next-corpus-specpm-preflight-intake-decision.example.json`.
  The fixture identity is
  `SpecHarvesterNextCorpusSpecPMPreflightIntakeDecision` with
  `apiVersion: spec-harvester.next-corpus-specpm-preflight-intake-decision/v0`.
  The current SpecPM selected handoff preflight returned
  `selected_handoff_payload_missing` against the P33-T5 triage fixture,
  proving the selected scope needed a durable selected handoff payload before
  maintainer intake review. The decision status was
  `not_ready_requires_durable_selected_handoff_artifact`. It preserved
  selected candidates `serena.core`, `transmission.core`, and `specpm.core`,
  kept `mcpm.system` and `specgraph.system` deferred, and remained review
  evidence only with no package acceptance, relation acceptance, baseline
  seeding, `preview_only` removal, registry publication, or SpecPM pull request
  creation.
- `P33-T7` recorded the durable selected handoff in
  `docs/NEXT_CORPUS_DURABLE_SELECTED_HANDOFF.md`,
  `<doc:NextCorpusDurableSelectedHandoff>`, and
  `tests/fixtures/next_corpus_durable_selected_handoff/p33-t7-next-corpus-selected-handoff.example.json`.
  The fixture identity is `SpecHarvesterSelectedCandidateHandoffProposal` with
  `apiVersion: spec-harvester.selected-candidate-handoff-proposal/v0` and
  `authority: producer_preview_evidence_only`. It selected `serena.core`,
  `transmission.core`, and `specpm.core`, deferred `mcpm.system` and
  `specgraph.system`, referenced four committed evidence roles, and passed
  SpecPM selected handoff preflight with selectedCandidateCount: 3,
  deferredCandidateCount: 2, requiredEvidenceRoleCount: 4,
  digestVerifiedCount: 1, zero warnings, and zero errors. It does not accept
  packages, does not accept relations, does not remove `preview_only`, does
  not publish registry metadata, and does not create a SpecPM pull request.

## Current Selection

Implement `P33-T8`: record the next-corpus intake readiness decision using the
passing P33-T7 durable selected handoff preflight result.

The selected handoff scope remains:

- `serena.core`;
- `transmission.core`;
- `specpm.core`.

Deferred candidates remain outside intake readiness:

- `mcpm.system`;
- `specgraph.system`.

The decision should state whether the selected scope is ready for
author/maintainer review, while keeping registry acceptance in a separate
SpecPM maintainer flow.

## Boundaries

This task must not run a new scrape, must not rerun LM Studio, must not clone
repositories, must not fetch remote state, must not install dependencies, must
not execute harvested code, must not run package scripts, must not publish
registry metadata, must not accept packages, must not accept relations, must
not seed baselines, must not remove `preview_only`, or treat AI output as
registry truth.
