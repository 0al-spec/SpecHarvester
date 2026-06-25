# P51-T2 Larger Curated Corpus Source Plan and Manifest Criteria

**Status:** Planned
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T2`
**Created:** 2026-06-25T12:28:06+03:00
**Depends On:** `P51-T1` Larger Curated Corpus Planning Phase
**Reasoning Effort:** medium

## Goal

Author the larger curated corpus source plan and manifest criteria that must
exist before the checkout readiness gate in `P51-T3`.

## Context

`P51-T1` created the Phase 51 planning phase from `P50-T1` restored-checkout
rerun evidence. The P50 evidence showed that the previous operator-local
checkout blocker was resolved for the same six-repository bounded pilot and
that both static-only and AI-enabled proposal-only gates passed.

`P51-T2` is the first expansion-specific task. It may choose sources and write
criteria, but it must not execute a larger corpus batch.

## Deliverables

- A machine-readable source plan fixture for the larger curated corpus.
- A durable source manifest under `inputs/` that `P51-T3` can check.
- GitHub and DocC documentation explaining the source plan, manifest criteria,
  inclusion signals, exclusions, and boundaries.
- Contract tests proving that the plan is bounded, curated, pinned, local
  checkout based, and not registry authority.
- A validation report recording the exact checks that were run.

## Source Plan Requirements

- Select a bounded corpus within the `P51-T1` range of 10 to 16 repositories.
- Preserve the original six restored-checkout pilot repositories.
- Add curated sources that improve ecosystem and repository-shape coverage.
- Include Python, Go, Swift, JavaScript/TypeScript, and documentation-heavy
  repository families.
- Record importance signals, repository shape, expected package subject,
  pinned revision, checkout path, and exclusion evidence.
- Carry P50 warnings and xyflow caveats forward as visible review evidence.

## Manifest Criteria

Each selected source must include:

- stable repository id;
- canonical repository URL;
- exact 40-character pinned revision;
- operator-local checkout path;
- expected package id;
- ecosystem family labels;
- repository shape labels;
- importance signals;
- stop conditions for missing checkout, revision mismatch, clone/fetch
  requirement, dependency installation requirement, harvested code execution
  requirement, or unclear license/source boundary.

## Acceptance Criteria

- `P51-T2` marks the source plan as authored but keeps execution readiness
  false until `P51-T3`.
- `P51-T2` does not run the larger corpus batch, static gate, AI gate, adapter
  execution, dependency installation, package managers, clone, or fetch.
- The source manifest is deterministic data only and is safe for `P51-T3`
  readiness verification.
- `SPECS/INPROGRESS/next.md` selects `P51-T3` after archive.
- Contract tests cover the fixture, manifest, docs, Workplan, and next task
  state.

## Non-Goals

- Do not run `autonomous-candidate-batch`.
- Do not verify checkout existence or revisions beyond gathering current
  operator-provided metadata for the manifest.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat source-plan output as registry truth.
