# P27-T4 — Author Review Viewer and Handoff Checklist

## Objective

Turn the P27-T3 stop-policy JSON surfaces into a human-facing author review
surface in the package-set static viewer and handoff Markdown.

P27-T3 tells machines whether to stop, continue, or block generation. P27-T4
should help repository authors and maintainers answer the next practical
question:

```text
What should I review, keep, edit, reject, or investigate next?
```

## Scope

In scope:

- Define a stable `authorReview` payload for package-set viewer JSON.
- Derive author checklist sections from existing `authorReadyDraftSummary`,
  member quality reports, action items, reviewable dimensions, blocking
  reasons, and evidence gaps already present in generated artifacts.
- Render package-set author review summary in the static viewer.
- Add per-member review action items to member cards.
- Add handoff Markdown sections for:
  - stop decision;
  - author checklist;
  - weak claims / reviewable dimensions;
  - evidence gaps;
  - recommended edits.
- Document the review surface in GitHub docs and DocC.
- Keep all review language explicit that this is producer-side review evidence,
  not SpecPM acceptance.

Out of scope:

- Changing generated `specpm.yaml` or `specs/*.spec.yaml`.
- Running LLMs or changing AI prompts/provider behavior.
- Accepting packages, accepting relations, publishing registry metadata, or
  replacing SpecPM maintainer review.
- Designing a full registry review application.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| Author review payload | Verify package-set JSON. | `package-set.json` contains `authorReview` with stop decision, checklist, weak claims, evidence gaps, and recommended edits. |
| Member cards | Verify per-member review data. | Member records expose author action item summaries and reviewable dimensions. |
| Handoff Markdown | Verify human handoff. | Markdown contains author checklist, weak claims, evidence gaps, and recommended edits. |
| Boundary language | Verify non-authority. | Docs and Markdown say review evidence only, not SpecPM acceptance. |
| Docs contract | Verify public docs. | GitHub docs, DocC, Workplan, and `next.md` mention the P27-T4 review surface. |

## Implementation Plan

1. Inspect current package-set renderer payload, viewer assets, and handoff
   Markdown builder.
2. Add deterministic helpers that derive `authorReview` from P27-T3 summaries
   and member quality reports.
3. Wire helpers into package-set viewer JSON and handoff Markdown.
4. Render author review summary/checklists in the static viewer without adding
   registry authority language.
5. Add regression tests for JSON payload, UI asset hooks, Markdown sections,
   and docs coverage.
6. Run quality gates and archive the Flow task.

## Acceptance Criteria

- Package-set viewer JSON exposes `authorReview`.
- The static viewer renders:
  - aggregate stop decision;
  - checklist items;
  - weak claims / reviewable dimensions;
  - evidence gaps;
  - recommended edits;
  - per-member action item summaries.
- Handoff Markdown includes the same review sections.
- The review surface preserves the producer-side boundary and does not imply
  acceptance, publication, or upstream endorsement.
- P27-T5 remains the next selected task after archive.
