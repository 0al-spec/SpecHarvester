# P27-T1 — Author-Ready Draft Quality Bar

## Objective

Document the product quality boundary for generated SpecHarvester output:
SpecHarvester should produce a valid starter package for repository authors,
not a final accepted specification.

## Scope

In scope:

- Define the author-ready draft quality target.
- Document valid starter package hard gates.
- Define when generator/model iteration should stop because the remaining work
  is author-reviewable rather than generator-fixable.
- Record review dimensions for future machine-readable quality reports.
- Define the author handoff boundary.
- Link the quality bar from Package-Set AI Draft Proposal docs, DocC, roadmap,
  and workplan.

Out of scope:

- Implementing the `authorReadyDraft` verdict.
- Changing generator behavior.
- Changing package-set AI draft schemas.
- Publishing to SpecPM or changing registry acceptance behavior.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| Docs contract | Verify GitHub docs and DocC expose the quality bar. | The new quality bar is linked from README, DocC root topics, roadmap, and AI draft docs. |
| Next task contract | Verify workflow handoff. | `SPECS/INPROGRESS/next.md` selects `P27-T2`. |
| Workplan contract | Verify phase planning. | Phase 27 lists `P27-T1` through `P27-T5`. |

## Implementation Plan

1. Add GitHub and DocC documentation for the author-ready draft quality bar.
2. Link the quality bar from package-set AI draft docs, DocC root topics,
   roadmap, and docs index.
3. Add Phase 27 to `SPECS/Workplan.md`.
4. Select `P27-T2 Author-Ready Draft Quality Report` in
   `SPECS/INPROGRESS/next.md`.
5. Add docs-contract regression coverage.

## Acceptance Criteria

- The repository documents that generated output is a valid starter package,
  not a final accepted spec.
- Hard gates mention SpecPM validation, required bundle files, producer receipt
  hashes, diagnostics, safe evidence paths, preview lifecycle markers, and no
  registry acceptance claims.
- Stop policy explains when additional model iteration is no longer useful.
- Future report states are documented as `author_ready_draft`,
  `needs_regeneration`, and `blocked`.
- The next planned task is `P27-T2`.
