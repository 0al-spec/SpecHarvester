# Autonomous Candidate Technical Debt Plan

This page mirrors `docs/AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`.

Status: current plan for Phase 32 after the P30/P31 limited corpus work.

The plan keeps the autonomous candidate MVP bounded. SpecHarvester should turn
operator-selected local checkouts into valid starter package evidence, then
stop for author or maintainer review. It should not scrape every framework into
SpecPM.

## Completed P29 Debt

P29 closed the original autonomous candidate technical debt:

- `P29-T3` recorded the Flask/Gin/xyflow corpus baseline in
  <doc:AutonomousCandidateCorpusBaseline>.
- `P29-T4` added the deterministic single-package fallback documented in
  <doc:SinglePackageCandidateFallback>.
- `P29-T5` added bounded LM Studio/OpenAI-compatible JSON repair/retry.
- `P29-T6` recorded the post-mitigation quality gate in
  <doc:AutonomousCandidateCorpusQualityGate> with verdict
  `ready_for_limited_popular_library_scraping`.

## Current P30/P31 Debt

Selected candidates `flask.core`, `gin.core`, and `docc2context.core` have
handoff-ready producer evidence. Deferred candidates remain useful calibration
evidence, but should not enter SpecPM handoff without targeted regeneration or
correction.

Current deferred candidates:

- `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and `xyflow.system`
  require `package_set_identity_regeneration`;
- `cupertino.core` requires `warning_bearing_enrichment_regeneration` or
  author-curated summary evidence;
- `navigation_split_view.core` requires `identity_drift_resolution`.

## Boundary

SpecHarvester must not clone repositories, execute harvested code, install
dependencies, publish SpecPM registry content, remove `preview_only`, accept
packages, accept relations, seed baselines, treat AI output as registry truth,
or replace author or SpecPM maintainer review.

## Phase 32 Work Plan

`P32-T1 Autonomous Deferred Candidate Work Plan`

- Owner: SpecHarvester.
- Motivation: P29 debt is complete, but P30/P31 deferred-candidate debt needs a
  current bounded plan.
- Goal: record the deferred candidate sequence with repository ownership,
  motivation, goal, acceptance criteria, and non-authority boundaries.

`P32-T2 Deferred Candidate Regeneration Runbook`

- Owner: SpecHarvester.
- Motivation: P31-T5 defines what must be regenerated, but not how an operator
  should run it safely.
- Goal: map each blocker class to producer commands, expected artifacts, and
  stop conditions.
- Artifact: <doc:DeferredCandidateRegenerationRunbook> records the P32-T2
  operator runbook before any regeneration run.

`P32-T3 Xyflow Package-Set Identity Regeneration Dry Run`

- Owner: SpecHarvester.
- Motivation: `xyflow.*` is the representative package-set case with
  package-set identity drift.
- Goal: regenerate package-set identity evidence and decide whether
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and `xyflow.system` can
  enter selected handoff.
- Artifact: <doc:XyflowPackageSetIdentityRegenerationDryRun> records the
  P32-T3 xyflow-only dry run with `candidate_layer_review_required` and
  `selectedHandoffEligible: true`.

`P32-T4 Single-Package Deferred Candidate Regeneration Dry Run`

- Owner: SpecHarvester.
- Motivation: `cupertino.core` and `navigation_split_view.core` represent
  summary/enrichment and identity-normalization failures.
- Goal: regenerate or repair those single-package candidates and record whether
  they can re-enter selected handoff.

`P32-T5 Refreshed Candidate-Layer Triage and Selected Handoff`

- Owner: SpecHarvester.
- Motivation: regenerated evidence needs the same triage vocabulary used by
  P30-T4/P30-T5.
- Goal: produce refreshed triage and selected handoff evidence for any
  regenerated candidates that satisfy hard gates.

`P32-T6 SpecPM Selected Candidate Handoff Preflight`

- Owner: SpecPM.
- Motivation: P31-T4 records expected checks, but SpecPM still needs the
  consumer-side gate.
- Goal: add SpecPM preflight for
  `SpecHarvesterSelectedCandidateHandoffProposal` while keeping passing
  preflight as review evidence only.

`P32-T7 Limited Corpus Intake Readiness Decision`

- Owner: SpecHarvester + SpecPM.
- Motivation: the project needs a stop point before expanding beyond the
  limited corpus.
- Goal: run refreshed selected handoff through SpecPM preflight and record
  whether the corpus is ready for author review, needs more regeneration, or
  should stop before broader scraping.

## Suggested Order

Run P32-T1 through P32-T7 in order. This keeps the current corpus bounded and
reviewable before any broader autonomous popular-library scrape is attempted.
