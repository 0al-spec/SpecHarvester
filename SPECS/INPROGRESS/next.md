# Next Task: P33-T7 Durable Next-Corpus Selected Handoff Artifact

**Status:** Selected
**Selected:** 2026-06-14
**Task:** P33-T7 Durable Next-Corpus Selected Handoff Artifact
**Phase:** Phase 33. Bounded Corpus Expansion Planning
**Last Archived:** P33-T6 Next-Corpus SpecPM Preflight and Intake Decision

## Recently Archived

- `P33-T5` recorded the next-corpus candidate-layer triage in
  `docs/NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md`,
  `<doc:NextCorpusCandidateLayerTriage>`, and
  `tests/fixtures/next_corpus_candidate_layer_triage/p33-t5-next-corpus-candidate-layer-triage.example.json`.
  The fixture identity is `SpecHarvesterNextCorpusCandidateLayerTriage` with
  `apiVersion: spec-harvester.next-corpus-candidate-layer-triage/v0`. It
  selected three candidates for P33-T6: `serena.core`, `transmission.core`,
  and `specpm.core`. It kept two deferred candidates: `mcpm.system` and
  `specgraph.system`. It recorded zero blocked candidates and zero
  not-for-intake candidates while reaching
  `ready_for_p33_t6_selected_handoff_preflight`. It remains review evidence
  only, does not accept packages, does not accept relations, does not remove
  `preview_only`, does not publish registry metadata, and does not create a
  SpecPM pull request. Short form: three selected, two deferred, zero blocked,
  and zero not-for-intake candidates. The carried findings are
  `ai_draft_no_proposal_subjects`, `ai_draft_warning_diagnostics`, and
  `package_id_hint_changed_by_package_set_selection`.
- `P33-T6` recorded the next-corpus SpecPM preflight intake decision in
  `docs/NEXT_CORPUS_SPECPM_PREFLIGHT_INTAKE_DECISION.md`,
  `<doc:NextCorpusSpecPMPreflightIntakeDecision>`, and
  `tests/fixtures/next_corpus_specpm_preflight_intake_decision/p33-t6-next-corpus-specpm-preflight-intake-decision.example.json`.
  The fixture identity is
  `SpecHarvesterNextCorpusSpecPMPreflightIntakeDecision` with `apiVersion:
  spec-harvester.next-corpus-specpm-preflight-intake-decision/v0`. The current
  SpecPM selected handoff preflight returned `selected_handoff_payload_missing`
  against the P33-T5 triage fixture, proving the selected scope needs a
  durable selected handoff payload before maintainer intake review. The intake
  decision is `not_ready_requires_durable_selected_handoff_artifact`. It
  preserves selected candidates `serena.core`, `transmission.core`, and
  `specpm.core`, keeps `mcpm.system` and `specgraph.system` deferred, and
  remains review evidence only with no package acceptance, relation
  acceptance, baseline seeding, `preview_only` removal, registry publication,
  or SpecPM pull request creation.

## Current Selection

Implement `P33-T7`: create durable selected handoff evidence for the P33 next
corpus selected scope, or explicitly extend the SpecPM selected handoff
consumer gate so the selected scope can be machine-preflighted before
maintainer intake review.

The selected handoff scope remains limited to:

- `serena.core`;
- `transmission.core`;
- `specpm.core`.

Deferred candidates stay outside selected handoff:

- `mcpm.system`;
- `specgraph.system`.

The task should produce or enable a supported SpecPM input such as
`SpecHarvesterSelectedCandidateHandoffProposal` without fabricating per-file
evidence digests from summary-only fixtures.

## Boundaries

This task must not run a new scrape, must not rerun LM Studio, must not clone
repositories, must not fetch remote state, must not install dependencies, must
not execute harvested code, must not run package scripts, must not publish
registry metadata, must not accept packages, must not accept relations, must
not seed baselines, must not remove `preview_only`, or treat AI output as
registry truth.
