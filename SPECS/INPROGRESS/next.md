# Next Task: P27-T4 Author Review Viewer and Handoff Checklist

**Status:** In Progress
**Started:** 2026-06-12
**Last Archived:** P27-T3 Author-Ready Stop Policy Summary
**Archived:** 2026-06-11

## Recently Archived

- `P27-T3` added a deterministic stop-policy summary across single draft,
  package-set draft, AI draft, AI enrichment, package-set handoff, and static
  package-set viewer outputs. Clean output maps to `stop_for_author_review`,
  warning-level gaps map to `continue_generation`, and blocked inputs map to
  `blocked_until_inputs_change`.
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

- P27-T3 exposes machine-readable `authorReadyDraftSummary` and
  `stopPolicySummary`, but the human-facing package-set viewer and handoff
  Markdown still need author review checklists.
- Authors should see what to keep, edit, reject, or investigate without reading
  raw JSON first.
- The UI and Markdown must preserve the boundary: these are recommended edits
  and weak-claim/evidence-gap prompts, not SpecPM acceptance.

## Goal

- Extend the static viewer and handoff Markdown with author review checklists,
  weak claim/evidence-gap summaries, and recommended edits derived from existing
  quality reports and stop-policy summaries.

## Next Step

Start `P27-T4` by defining the author-review checklist payload and deciding how
the package-set viewer should render aggregate stop decision, member action
items, weak claims, evidence gaps, and recommended edits without becoming a
registry acceptance UI.
