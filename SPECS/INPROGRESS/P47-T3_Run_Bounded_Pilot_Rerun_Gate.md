# P47-T3 Run Bounded Pilot Rerun Gate

Status: Planned
Phase: Phase 47. Targeted Pilot Quality Follow-Up
Task: P47-T3
Branch: `feature/P47-T3-run-bounded-pilot-rerun-gate`
Depends on: P47-T2 Execute Targeted Pilot Quality Pass

## Problem

P47-T2 disposed the P46 blockers only for the bounded rerun gate. The project
still needs a real rerun gate over the same six-repository pilot before P47-T4
can decide whether larger curated corpus planning may proceed.

The rerun must prove the target dispositions are operationally usable without
expanding scope, accepting packages, treating AI output as registry truth, or
hiding remaining sidecar/caveat issues.

## Goal

Run and record a bounded pilot rerun gate that preserves the P46 scope,
executes static-only evidence before AI-enabled evidence, keeps AI output
proposal-only, and records any new or remaining caveats for P47-T4.

## Deliverables

- Verified same-scope source manifest evidence for
  `inputs/p46-bounded-popular-library-pilot/repositories.yml`.
- Static-only rerun evidence over the same six repositories.
- AI-enabled proposal-only rerun evidence over the same six repositories.
- Machine-readable P47-T3 bounded rerun gate fixture under
  `tests/fixtures/targeted_pilot_bounded_rerun_gate/`.
- GitHub Markdown and DocC documentation describing commands, results,
  remaining warnings/caveats, and authority boundaries.
- Docs-contract coverage for fixture identity, source digests, static-before-AI
  ordering, proposal-only AI output, non-authority boundaries, and current
  next-task pointer.
- Validation report and archive artifacts for P47-T3.

## Acceptance Criteria

- The rerun uses the same six repository ids from P46:
  `flask`, `gin`, `xyflow`, `cupertino`, `navigation-split-view`, and
  `docc2context`.
- The source manifest digest is recorded and the rerun does not expand the
  corpus.
- Pinned local checkout revisions are verified before the run without clone or
  fetch.
- Static-only evidence is generated before any AI-enabled evidence.
- AI-enabled evidence remains proposal-only and does not persist raw prompts,
  raw provider responses, secrets, or chain-of-thought.
- Current P47-T2 excluded sidecars are not reused as registry truth:
  `gin.aiDraft`, `docc2context.aiDraft`, and `xyflow.aiEnrichment`.
- The gate records whether P47-T4 can evaluate larger curated corpus readiness,
  without approving that larger corpus in P47-T3.
- P47-T3 does not accept packages or relations, publish registry metadata,
  seed baselines, remove `preview_only`, run adapters, enable trusted local
  adapter execution, install harvested-repository dependencies, invoke
  harvested-repository package managers, execute harvested code, or treat
  static/AI/adapter output as registry truth.
- P47-T3 updates `SPECS/INPROGRESS/next.md` after archival to show P47-T4.

## Boundaries

- Do not approve a larger curated corpus.
- Do not expand the pilot scope beyond the six P46 repositories.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers inside harvested repositories.
- Do not execute harvested code.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat rerun gate output, static output, AI output, or adapter output
  as registry truth.

## Validation Plan

- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the P47-T3 bounded rerun gate and current
  next task.
- Run lint, format, coverage, Swift manifest, Swift docs build, and whitespace
  checks as required by Flow.
