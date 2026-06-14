# P33-T4 Live Local-Model Next-Corpus Dry Run

**Status:** Planned
**Selected:** 2026-06-14
**Phase:** Phase 33. Bounded Corpus Expansion Planning

## Motivation

P33-T3 proved the next bounded corpus can be collected, drafted, preflighted,
and summarized without AI. The next quality question is whether the same five
repositories can pass through the live local-model draft/enrichment path while
preserving the producer preview boundary and exposing model diagnostics before
candidate-layer triage.

## Goal

Run the P33 next-corpus manifest through `autonomous-candidate-batch` with the
operator-provided local LM Studio endpoint and record provider receipts,
bounded JSON repair outcomes, AI draft/enrichment status, candidate counts,
relation counts, package-id review signals, and readiness for P33-T5
candidate-layer triage.

## Deliverables

- Verify LM Studio model availability through `GET /v1/models` before the live
  batch.
- Run `autonomous-candidate-batch inputs/p33-next-corpus` with:
  - `--lm-studio-base-url http://127.0.0.1:1234`;
  - `--lm-studio-model openai/gpt-oss-20b`;
  - `--json-repair-max-attempts 1`.
- Add a machine-readable live local-model fixture that records:
  - deterministic P33-T3 baseline summary;
  - provider identity and privacy boundary;
  - repository outcomes;
  - AI draft/enrichment statuses and diagnostics;
  - JSON repair status;
  - provider token counts when reported;
  - source/report digests;
  - product verdict.
- Add GitHub docs and DocC docs for the P33-T4 live local-model run.
- Link the live-run evidence from P33 docs, roadmap, Workplan, and current
  `next.md`.
- Add regression tests covering the fixture, repository outcome shape,
  provider boundary, JSON repair summary, docs links, and no-authority
  boundary.
- Archive Flow artifacts and leave `next.md` on P33-T5.

## Acceptance Criteria

- The LM Studio endpoint exposes `openai/gpt-oss-20b` before the run starts, or
  the task records a clear provider-unavailable blocker instead of continuing
  silently.
- The live run processes the same five repositories from
  `inputs/p33-next-corpus/repositories.yml`.
- The generated live summary records candidate counts, relation counts,
  preflight status, AI draft status, AI enrichment status, JSON repair status,
  provider receipts, and package-id review signals.
- The live output remains proposal evidence only and does not replace
  deterministic generated package files or accepted SpecPM metadata.
- The result explicitly says whether the corpus can proceed to P33-T5
  candidate-layer triage.
- Project docs-contract tests and configured quality gates pass.

## Non-Goals

- No candidate-layer selected/deferred/blocked/not-for-intake decisions.
- No selected handoff proposal.
- No SpecPM-side preflight.
- No SpecPM repository change.
- No registry publication or package acceptance.
- No package or relation acceptance.
- No `preview_only` removal.

## Review Subject

`p33_t4_live_local_model_next_corpus_dry_run`

---
**Archived:** 2026-06-14
**Verdict:** PASS
