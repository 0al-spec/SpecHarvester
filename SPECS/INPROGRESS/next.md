# Next Task: P27-T5 Real Repository Author-Ready Draft Calibration Matrix

**Status:** In Progress
**Started:** 2026-06-12
**Last Archived:** P27-T4 Author Review Viewer and Handoff Checklist
**Archived:** 2026-06-12

## Recently Archived

- `P27-T4` added author review checklists through `authorReview`, making
  package-set viewer and handoff Markdown show weak claims, evidence gaps,
  recommended edits, and member action summaries without implying SpecPM
  acceptance.
- `P27-T3` added a deterministic stop-policy summary across single draft,
  package-set draft, AI draft, AI enrichment, package-set handoff, and static
  package-set viewer outputs. The summary is exposed as
  `authorReadyDraftSummary` and `stopPolicySummary`. Clean output maps to
  `stop_for_author_review`, warning-level gaps map to `continue_generation`,
  and blocked inputs map to `blocked_until_inputs_change`.
- `P27-T2` added `author-ready-draft-quality-report.json` with an
  `authorReadyDraft` verdict, hard gates, advisory dimensions, author action
  items, receipt `quality_report` output digests, package-set member evidence
  links, and static renderer JSON exposure.
- `P27-T1` documented the author-ready draft quality bar: SpecHarvester should
  produce a valid starter package for repository authors, not a final accepted
  specification.
- `P26-T5` added `SpecHarvesterPackageSetAIDraftProposal`, preserving the
  original `LLM + schema` package-set idea: deterministic workspace inventory is
  evidence, the model proposes selected members, exclusions, and `contains`
  relations, and SpecPM plus maintainers remain the acceptance authority.

## Motivation

- P27-T1 through P27-T4 define and expose author-ready valid starter packages,
  but the quality bar needs calibration across real repositories.
- A single `xyflow` reference run is useful plumbing evidence, not enough
  product evidence for how many author edits are usually needed.
- The next decision should be evidence-driven: which draft gaps repeat across
  repositories and should become deterministic fixes, and which gaps should
  remain author curation.

## Goal

- Run a real-repository author-ready draft calibration matrix and record how
  many author edits are needed to move valid starter packages toward curated
  specs.

## Next Step

Start `P27-T5` by defining the calibration matrix shape: repository selection,
quality dimensions, author edit categories, expected artifacts, and the
criteria for turning repeated gaps into follow-up generator work.
