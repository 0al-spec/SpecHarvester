# P33-T5 Next-Corpus Candidate-Layer Triage

**Status:** Planned
**Selected:** 2026-06-14
**Phase:** Phase 33. Bounded Corpus Expansion Planning

## Motivation

P33-T4 proved that the next bounded corpus can pass through the live
local-model path without JSON repair or producer preflight failures. The next
step is not another model run. The next step is a candidate-layer decision that
separates candidates that are ready for selected handoff review from
candidates that should stay deferred until identity or draft evidence is
resolved.

## Goal

Record P33-T5 candidate-layer triage for the five P33 next-corpus candidates,
using only the already archived P33-T3 deterministic evidence and P33-T4 live
local-model evidence.

The triage must classify every candidate into one of:

- `candidate_layer_review_required`;
- `needs_regeneration`;
- `blocked`;
- `not_for_intake`.

It must identify which candidates are selected for P33-T6 selected handoff
preflight and which candidates remain deferred.

## Proposed Triage Policy

Single-package repositories with deterministic preflight pass, author-ready
status, completed enrichment, and only no-subject or unknown-exclusion AI draft
noise can proceed to selected handoff review. Package-id drift should remain
deferred until the generated id is accepted, regenerated, or corrected.

Expected initial disposition:

- selected for P33-T6: `serena.core`, `transmission.core`, `specpm.core`;
- deferred: `mcpm.system`, `specgraph.system`;
- blocked: none;
- not-for-intake: none.

## Deliverables

- Add a machine-readable P33-T5 triage fixture with:
  - P33-T3/P33-T4 input references;
  - source fixture digests;
  - triage policy;
  - candidate dispositions;
  - selected/deferred/blocked/not-for-intake counts;
  - finding classification;
  - P33-T6 selected handoff readiness;
  - non-authority boundary.
- Add GitHub docs and DocC docs for the candidate-layer triage.
- Link the P33-T5 evidence from P33 docs, roadmap, docs index, Workplan, and
  `next.md`.
- Add docs-contract regression tests covering fixture shape, selected and
  deferred candidates, finding classifications, counts, docs links, and
  non-authority boundary.
- Archive Flow artifacts and leave `next.md` on P33-T6.

## Acceptance Criteria

- Every P33-T4 candidate is classified exactly once.
- Selected candidates are explicit and count-backed.
- Deferred candidates preserve blocker/finding codes and explain what must
  happen before handoff.
- The triage does not rerun collection, LM Studio, drafting, enrichment, or
  SpecPM preflight.
- The result remains producer preview evidence only and does not accept
  packages, accept relations, seed baselines, remove `preview_only`, publish
  registry metadata, or create a SpecPM pull request.
- Project docs-contract tests and configured quality gates pass.

## Non-Goals

- No new scrape.
- No LM Studio rerun.
- No generated candidate mutation.
- No selected handoff proposal helper run.
- No SpecPM-side preflight.
- No SpecPM repository change.
- No registry publication or package acceptance.
- No package or relation acceptance.
- No `preview_only` removal.

## Review Subject

`p33_t5_next_corpus_candidate_layer_triage`

---
**Archived:** 2026-06-14
**Verdict:** PASS
