# P27-T3 — Author-Ready Stop Policy Summary

## Objective

Add a deterministic stop-policy summary that tells operators whether a generated
draft or package-set should stop for author review, continue generation, or stay
blocked until inputs change.

P27-T2 already emits per-candidate `authorReadyDraft` verdicts. P27-T3 turns
those verdicts into an aggregate, reviewable decision surface:

```text
author_ready_draft -> stop_for_author_review
needs_regeneration -> continue_generation
blocked -> blocked_until_inputs_change
```

## Scope

In scope:

- Define a stable `authorReadyDraftSummary` JSON contract.
- Add deterministic stop-policy decisions:
  - `stop_for_author_review`;
  - `continue_generation`;
  - `blocked_until_inputs_change`.
- Aggregate package-set member quality reports into package-set level counts,
  blocking reasons, reviewable dimensions, and top author action items.
- Expose a single-candidate `authorReadyDraftSummary` in `draft_spec_package`
  results.
- Include `authorReadyDraftSummary` in `package-set-draft.json`.
- Include the summary in package-set handoff evidence and static package-set
  viewer JSON.
- Add `stopPolicySummary` to AI draft and AI enrichment proposal outputs so
  model-loop decisions use the same stop/continue/blocked vocabulary without
  claiming package acceptance.
- Keep per-candidate `author-ready-draft-quality-report.json` unchanged and
  backward-compatible.
- Update GitHub docs, DocC docs, Workplan, next task, and Flow artifacts.

Out of scope:

- Running LLMs or changing prompt/provider behavior.
- Automatically rerunning generation.
- Treating the stop-policy decision as SpecPM acceptance, upstream author
  endorsement, relation acceptance, or registry publication.
- Designing the P27-T4 author-facing card UI beyond exposing stable JSON and
  documenting what the viewer can render next.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| All members ready | Verify aggregate stop decision. | Summary decision is `stop_for_author_review`, all counts are ready, no blocking reasons. |
| Member needs regeneration | Verify non-blocking generator work. | Summary decision is `continue_generation`, action items mention regeneration/review needs. |
| Member blocked | Verify fail-closed behavior. | Summary decision is `blocked_until_inputs_change`, blocking reasons identify the blocked package. |
| Handoff integration | Verify proposal evidence. | `package-set-handoff-proposal.json` contains `authorReadyDraftSummary`. |
| Viewer integration | Verify static JSON surface. | `viewer/package-set.json` exposes the same summary for aggregate rendering. |
| Docs contract | Verify public contract is documented. | GitHub docs, DocC, Workplan, and next task mention the summary and decisions. |

## Implementation Plan

1. Inspect current quality-report, package-set handoff, and renderer payload
   shapes.
2. Add a pure helper that summarizes `authorReadyDraft.status`,
   `hardGateStatus`, dimensions, and author action items from member reports.
3. Wire the helper into package-set handoff and static package-set renderer
   outputs without changing package generation semantics.
4. Add result-level summaries for single drafts, package-set drafts, and AI
   proposal flows.
5. Add tests for ready, needs-regeneration, blocked, handoff, and viewer
   surfaces.
6. Update docs, DocC, Workplan, `next.md`, and archive validation artifacts.
7. Run configured quality gates and open a PR.

## Acceptance Criteria

- Package-set output exposes `authorReadyDraftSummary`.
- Single draft results expose `authorReadyDraftSummary`.
- AI draft and AI enrichment proposals expose `stopPolicySummary`.
- The summary includes:
  - `decision`;
  - `memberCounts`;
  - `blockingReasons`;
  - `topAuthorActionItems`;
  - `reviewableDimensions`.
- `blocked` member reports force `blocked_until_inputs_change`.
- `needs_regeneration` member reports force `continue_generation` unless another
  member is blocked.
- all-ready package sets return `stop_for_author_review`.
- The summary remains proposal-side review evidence and does not accept,
  materialize, or publish specs.
