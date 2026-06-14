# P33-T3 Deterministic Next-Corpus Dry Run

**Status:** Planned
**Selected:** 2026-06-13
**Phase:** Phase 33. Bounded Corpus Expansion Planning

## Motivation

P33-T2 added the next-corpus source manifest. Before any live local-model work,
SpecHarvester needs a deterministic no-AI run over that manifest to prove the
local checkout set can be collected, drafted, preflighted, and summarized as
review evidence.

## Goal

Run the P33 next-corpus manifest through `autonomous-candidate-batch --skip-ai`
and record deterministic collection, candidate, relation, preflight, blocker,
and live-model readiness outcomes.

## Deliverables

- Run `autonomous-candidate-batch inputs/p33-next-corpus --skip-ai` against a
  temporary output directory.
- Add a machine-readable deterministic dry-run fixture that records repository
  outcomes, aggregate counts, report digests, source manifest digest, and
  non-authority boundaries.
- Add GitHub docs and DocC docs for the P33-T3 deterministic run.
- Link the dry-run evidence from P33 docs, roadmap, Workplan, and current
  `next.md`.
- Add regression tests covering the fixture, repository outcome shape, parsed
  source manifest alignment, report digest references, docs links, and
  no-AI/no-authority boundary.
- Archive Flow artifacts and leave `next.md` on P33-T4.

## Acceptance Criteria

- The source manifest parser reports exactly five repositories.
- The deterministic run processes every selected repository without clone,
  fetch, dependency install, package script, harvested code execution, or AI
  provider calls.
- Every repository outcome records collection status, candidate count, relation
  count, preflight status, blocker classes, and whether it can proceed to
  live-model review.
- Aggregate counts and report digests are recorded.
- The result is explicit review evidence only and does not accept packages,
  accept relations, seed baselines, remove `preview_only`, publish registry
  metadata, create a SpecPM pull request, or treat AI output as registry truth.
- Project docs-contract tests pass.

## Non-Goals

- No live local-model draft or enrichment run.
- No candidate-layer triage.
- No selected handoff proposal.
- No SpecPM-side preflight.
- No SpecPM repository change.
- No registry publication or package acceptance.

## Review Subject

`p33_t3_deterministic_next_corpus_dry_run`
