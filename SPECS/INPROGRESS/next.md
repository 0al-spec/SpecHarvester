# Next Task: P33-T1 Bounded Corpus Expansion Plan

**Status:** Selected
**Selected:** 2026-06-13
**Task:** P33-T1 Bounded Corpus Expansion Plan
**Phase:** Phase 33. Bounded Corpus Expansion Planning
**Last Archived:** P32-T7 Limited Corpus Intake Readiness Decision

## Recently Archived

- `P32-T5` recorded the refreshed selected handoff in
  `docs/REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md`,
  `<doc:RefreshedCandidateLayerSelectedHandoff>`, and
  `tests/fixtures/refreshed_candidate_layer_selected_handoff/p32-t5-refreshed-candidate-layer-selected-handoff.example.json`.
  The selected set is `flask.core`, `gin.core`, `docc2context.core`,
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
  `navigation_split_view.core`; `cupertino.core` remains deferred on
  `refined_summary_missing`.
- `P32-T6` recorded the merged SpecPM selected candidate handoff preflight in
  [`0al-spec/SpecPM#140`](https://github.com/0al-spec/SpecPM/pull/140). The
  P32-T5 fixture passed with eight selected candidates, one deferred candidate,
  and three source digests verified. The preflight remains review evidence
  only.
- `P32-T7` recorded the limited corpus intake readiness decision in
  `docs/LIMITED_CORPUS_INTAKE_READINESS_DECISION.md`,
  `<doc:LimitedCorpusIntakeReadinessDecision>`, and
  `tests/fixtures/limited_corpus_intake_readiness_decision/p32-t7-limited-corpus-intake-readiness-decision.example.json`.
  The fixture identity is
  `SpecHarvesterLimitedCorpusIntakeReadinessDecision`, and the decision is
  `ready_for_author_maintainer_review_with_explicit_deferral`.

## Current Selection

Implement `P33-T1`: record the bounded corpus expansion plan.

The plan must define:

- source manifest requirements for the next corpus;
- repository count limits;
- repository selection rationale;
- deterministic and live-model validation gates;
- stop conditions;
- author/maintainer review handoff;
- non-authority boundaries.

## Boundaries

This task must not run a new scrape, clone repositories, fetch remote state,
install dependencies, execute harvested code, publish registry metadata, accept
packages, accept relations, seed baselines, remove `preview_only`, or treat AI
output as registry truth.
