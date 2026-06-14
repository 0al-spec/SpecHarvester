# Autonomous Candidate Technical Debt Plan

Status: Current plan for Phase 32 after the P30/P31 limited corpus work.

This plan keeps the autonomous candidate MVP bounded. The goal is not to scrape
every framework into SpecPM. The goal is to turn operator-selected local
checkouts into valid starter package evidence, then stop for author or
maintainer review.

## Completed P29 Debt

The original technical debt came from the first Flask/Gin/xyflow corpus run:

- Flask and Gin collected useful evidence but produced `0` candidates because
  they were single-package repositories rather than workspaces.
- Live LM Studio output could produce malformed JSON on real corpus input.
- The runner needed a mixed-corpus quality gate before expanding beyond three
  repositories.

That debt is now closed:

- `P29-T3` recorded the Flask/Gin/xyflow corpus baseline in
  [`AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`](AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md).
- `P29-T4` added the deterministic single-package fallback documented in
  [`SINGLE_PACKAGE_CANDIDATE_FALLBACK.md`](SINGLE_PACKAGE_CANDIDATE_FALLBACK.md).
- `P29-T5` added bounded LM Studio/OpenAI-compatible JSON repair/retry.
- `P29-T6` recorded the post-mitigation quality gate in
  [`AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md`](AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md)
  with verdict `ready_for_limited_popular_library_scraping`.

## Current P30/P31 Debt

The P30/P31 limited corpus showed a stronger boundary:

- selected candidates `flask.core`, `gin.core`, and `docc2context.core` have
  handoff-ready producer evidence;
- deferred candidates are useful calibration evidence, but should not enter
  SpecPM handoff without targeted regeneration or correction.

Current deferred candidates:

| Candidate | Current blocker | Required direction |
| --- | --- | --- |
| `xyflow.workspace` | `package_set_identity_regeneration` | regenerate package-set AI draft/enrichment evidence with package-set identity |
| `xyflow.react` | `package_set_identity_regeneration` | regenerate member evidence from the package-set identity run |
| `xyflow.svelte` | `package_set_identity_regeneration` | regenerate member evidence from the package-set identity run |
| `xyflow.system` | `package_set_identity_regeneration` | regenerate member evidence from the package-set identity run |
| `cupertino.core` | `warning_bearing_enrichment_regeneration` | regenerate enrichment or attach author-curated summary evidence |
| `navigation_split_view.core` | `identity_drift_resolution` | choose canonical package id and regenerate under that id |

## Boundary

SpecHarvester should improve producer-side preview evidence. It must not:

- clone repositories;
- execute harvested code;
- install dependencies;
- publish SpecPM registry content;
- remove `preview_only`;
- accept packages;
- accept relations;
- seed baselines;
- treat AI output as registry truth;
- replace author or SpecPM maintainer review.

## Phase 32 Work Plan

### P32-T1 Autonomous Deferred Candidate Work Plan

Owner: SpecHarvester.

Motivation:

- The P29 debt plan is complete, but the repository still points operators at
  old Flask/Gin/xyflow issues instead of the current P30/P31 deferred-candidate
  debt.
- Without a current work plan, an operator could either over-promote deferred
  candidates or expand scraping before the limited corpus is clean.

Goal:

- Record the current deferred candidate sequence with repository ownership,
  motivation, goal, acceptance criteria, and non-authority boundaries.

Acceptance:

- The plan distinguishes completed P29 debt from current P30/P31 debt.
- The plan names all six deferred P30 candidates.
- The plan lists the next concrete tasks and keeps broad autonomous scraping
  out of scope.

### P32-T2 Deferred Candidate Regeneration Runbook

Owner: SpecHarvester.

Motivation:

- P31-T5 defines what must be regenerated, but not how an operator should run
  the regeneration safely and repeatably.
- The next run should use pinned local checkouts and bounded local model calls,
  not ad-hoc command chains.

Goal:

- Add a runbook that maps each deferred blocker class to the exact producer
  commands, expected artifacts, and stop conditions.

Acceptance:

- The runbook covers package-set identity regeneration, warning-bearing
  enrichment regeneration, author-curated summary evidence, and identity-drift
  resolution.
- It requires local pinned checkouts and forbids clone/fetch/install/execute
  behavior.
- It defines when a candidate remains deferred versus when it can re-enter
  candidate-layer triage.

Artifact:

- [`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md)
  records the P32-T2 operator runbook before any regeneration run.

### P32-T3 Xyflow Package-Set Identity Regeneration Dry Run

Owner: SpecHarvester.

Motivation:

- `xyflow.*` is the representative package-set case. Its generated package
  topology is useful, but the P30 AI draft evidence had package-set identity
  drift.

Goal:

- Re-run the xyflow package-set path with the regeneration runbook and record
  whether `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and
  `xyflow.system` can become selected-handoff candidates.

Acceptance:

- Regenerated evidence keeps the workspace/member topology and `contains`
  relation proposals.
- Producer preflight passes with zero warnings/errors.
- Static viewer output is present.
- `preview_only` and `registryAcceptanceDecision.status: external_required`
  remain intact.
- If identity drift remains, the report says `needs_regeneration`, not
  selected.

Artifact:

- [`XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md`](XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md)
  records the P32-T3 xyflow-only dry run. The recorded decision is
  `candidate_layer_review_required` with `selectedHandoffEligible: true`.

### P32-T4 Single-Package Deferred Candidate Regeneration Dry Run

Owner: SpecHarvester.

Motivation:

- `cupertino.core` and `navigation_split_view.core` are different failure
  shapes from xyflow: one needs summary/enrichment evidence; the other needs
  identity normalization.

Goal:

- Re-run or repair the single-package deferred candidates and record whether
  they can re-enter selected handoff.

Acceptance:

- `cupertino.core` either has clean regenerated enrichment or explicit
  author-curated summary evidence.
- `navigation_split_view.core` records the canonical package id decision and
  rejects or aliases the non-canonical id.
- Producer preflight and viewer evidence are clean before selection.

Artifact:

- [`SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md`](SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md)
  records the P32-T4 dry run. `navigation_split_view.core` is
  `candidate_layer_review_required` with `selectedHandoffEligible: true`;
  `cupertino.core` remains `needs_regeneration` until
  `refined_summary_missing` is resolved by regenerated enrichment or
  author-curated summary evidence.

### P32-T5 Refreshed Candidate-Layer Triage and Selected Handoff

Owner: SpecHarvester.

Motivation:

- Regeneration is not useful until the limited corpus can be reclassified with
  the same triage vocabulary used by P30-T4/P30-T5.

Goal:

- Produce refreshed triage and selected handoff evidence for any regenerated
  candidates that satisfy the hard gates.

Acceptance:

- Every candidate is classified as `candidate_layer_review_required`,
  `needs_regeneration`, `blocked`, or `not_for_intake`.
- Selected candidates have digest-backed evidence roles, passing producer
  preflight, static viewer output, and external registry acceptance decisions.
- Deferred candidates remain visible and are not silently dropped.

Artifact:

- [`REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md`](REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md)
  records the P32-T5 refreshed selected handoff. The selected set is
  `flask.core`, `gin.core`, `docc2context.core`, `xyflow.workspace`,
  `xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
  `navigation_split_view.core`; `cupertino.core` remains deferred on
  `refined_summary_missing`.

### P32-T6 SpecPM Selected Candidate Handoff Preflight

Owner: SpecPM.

Motivation:

- P31-T4 records what SpecPM should verify, but producer evidence is still only
  producer evidence until SpecPM can consume it with its own preflight gate.

Goal:

- Record the merged SpecPM-side consumer preflight for
  `SpecHarvesterSelectedCandidateHandoffProposal` and
  `SpecHarvesterRefreshedCandidateLayerSelectedHandoff`.

Acceptance:

- SpecPM PR
  [`0al-spec/SpecPM#140`](https://github.com/0al-spec/SpecPM/pull/140) is
  merged.
- The P32-T5 refreshed selected handoff fixture passes
  `specpm producer-bundle preflight-selected-candidate-handoff`.
- SpecPM validates proposal identity, authority, selected/deferred candidate
  consistency, required evidence roles, digests, source fixture digests,
  preflight status, viewer status, privacy boundary, and `external_required`
  registry decisions.
- Passing preflight remains review evidence only and does not accept packages,
  seed baselines, remove `preview_only`, publish registry metadata, or create a
  PR.

Artifact:

- `P32-T6` records the merged SpecPM preflight in
  [`0al-spec/SpecPM#140`](https://github.com/0al-spec/SpecPM/pull/140). The
  P32-T5 fixture passed with eight selected candidates, one deferred candidate
  (`cupertino.core`), and three source digests verified.

### P32-T7 Limited Corpus Intake Readiness Decision

Owner: SpecHarvester + SpecPM.

Motivation:

- The project needs a clear stop point before expanding from a limited corpus
  to more popular repositories.

Goal:

- Run the refreshed selected handoff through the SpecPM preflight gate and
  record a decision: ready for author review, needs more regeneration, or stop
  before broader scraping.

Acceptance:

- The decision is machine-readable and linked from both producer and consumer
  docs.
- No package enters SpecPM without explicit maintainer acceptance.
- The next corpus expansion is allowed only if the limited corpus has clean
  selected handoff evidence or documented deferrals.

Artifact:

- [`LIMITED_CORPUS_INTAKE_READINESS_DECISION.md`](LIMITED_CORPUS_INTAKE_READINESS_DECISION.md)
  records the P32-T7 decision. The limited corpus is
  `ready_for_author_maintainer_review_with_explicit_deferral`: eight selected
  preview candidates are ready for author/maintainer review, `cupertino.core`
  remains deferred on `refined_summary_missing`, and any broader autonomous
  scraping requires a separate follow-up task.

## Suggested Order

1. `P32-T1` record this plan.
2. `P32-T2` write the regeneration runbook.
3. `P32-T3` regenerate xyflow package-set evidence.
4. `P32-T4` regenerate or repair Cupertino and NavigationSplitView evidence.
5. `P32-T5` refresh triage and selected handoff.
6. `P32-T6` record SpecPM-side selected handoff preflight.
7. `P32-T7` record the limited corpus intake readiness decision.

This order keeps the current corpus bounded and reviewable before any broader
autonomous popular-library scrape is attempted.

## Phase 33 Follow-Up

Phase 32 ended with a review-ready limited corpus, not with permission for
unbounded scraping.

The next follow-up is
[`BOUNDED_CORPUS_EXPANSION_PLAN.md`](BOUNDED_CORPUS_EXPANSION_PLAN.md), which
records `P33-T1` and requires the next corpus to define its own source
manifest, five-repository limit, deterministic and live-model validation gates,
candidate-layer triage gate, SpecPM-side preflight gate, stop conditions, and
non-authority boundary before any new scrape runs.
