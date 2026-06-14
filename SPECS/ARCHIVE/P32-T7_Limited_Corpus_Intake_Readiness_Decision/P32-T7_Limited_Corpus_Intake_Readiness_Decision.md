# P32-T7 Limited Corpus Intake Readiness Decision

Status: Archived
Phase: Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness
Owner: SpecHarvester + SpecPM coordination

## Motivation

P32-T5 produced refreshed selected handoff evidence for the limited corpus, and
P32-T6 proved that SpecPM can validate that handoff with a consumer-side
preflight gate. The project now needs an explicit stop-point decision before
using this evidence as a reason to broaden autonomous scraping.

Without a decision record, operators could either over-promote preview
evidence into registry acceptance or keep regenerating a corpus that is already
ready for author/maintainer review.

## Goal

Record a machine-readable limited corpus intake readiness decision that:

- marks the selected P32-T5 candidates as ready for author/maintainer review;
- keeps `cupertino.core` deferred on `refined_summary_missing`;
- records the SpecPM P32-T6 preflight result as consumer review evidence;
- allows planning the next bounded corpus expansion only as a separate task;
- preserves the producer-preview and SpecPM-acceptance boundary.

## Deliverables

- Add a fixture under
  `tests/fixtures/limited_corpus_intake_readiness_decision/`.
- Add GitHub docs and a DocC mirror for the decision.
- Link the decision from the autonomous candidate tech-debt plan, SpecPM
  handoff guide, roadmap, docs index, and DocC root.
- Add docs-contract regression coverage for the decision shape and boundary.
- Archive the task and advance `SPECS/INPROGRESS/next.md` to a post-P32
  planning pointer.

## Acceptance Criteria

- The fixture records:
  - `apiVersion: spec-harvester.limited-corpus-intake-readiness-decision/v0`;
  - `kind: SpecHarvesterLimitedCorpusIntakeReadinessDecision`;
  - selected candidates `flask.core`, `gin.core`, `docc2context.core`,
    `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
    `navigation_split_view.core`;
  - deferred candidate `cupertino.core` with `refined_summary_missing`;
  - SpecPM #140 / revision `8a5ce3dece3d18bf8f601a5a599520bd520c7839`;
  - P32-T6 preflight status `passed`, zero warnings, zero errors, and three
    source digests verified.
- The decision says selected candidates are ready for author/maintainer review,
  not accepted into SpecPM.
- The decision states that broader scraping requires a separate follow-up task.
- Tests prove docs, DocC, fixture, Workplan, and next pointer alignment.

## Non-Goals

- Do not regenerate candidates.
- Do not run a new LM Studio or SpecNode pass.
- Do not update SpecPM accepted packages.
- Do not accept packages, accept relations, seed baselines, remove
  `preview_only`, publish registry metadata, or create a SpecPM pull request.
- Do not resolve `cupertino.core`.

## Archive

Archived: 2026-06-13
Verdict: PASS

P32-T7 recorded
`SpecHarvesterLimitedCorpusIntakeReadinessDecision` in
`tests/fixtures/limited_corpus_intake_readiness_decision/p32-t7-limited-corpus-intake-readiness-decision.example.json`.

The decision is `ready_for_author_maintainer_review_with_explicit_deferral`:
eight selected preview candidates are ready for author/maintainer review,
`cupertino.core` remains deferred on `refined_summary_missing`, and broader
autonomous scraping requires a separate follow-up task.

Phase 32 is complete. The limited corpus is review-ready, not
registry-accepted.
