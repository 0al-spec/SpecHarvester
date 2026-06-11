# Next Task: P27-T3 Author-Ready Stop Policy Summary

**Status:** Selected
**Last Archived:** P27-T2 Author-Ready Draft Quality Report
**Archived:** 2026-06-11

## Recently Archived

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

- P27-T2 tells operators whether a draft is `author_ready_draft`,
  `needs_regeneration`, or `blocked`, but it does not yet explain why the
  generator should stop or continue.
- Draft, package-set draft, AI draft, and AI enrichment flows should expose a
  common stop-policy summary so operators do not keep rerunning the model after
  remaining work is author-reviewable.
- A shared stop-policy surface will make the static viewer and handoff Markdown
  easier to build in P27-T4.

## Goal

- Add a deterministic stop-policy summary to draft, package-set draft, AI draft,
  and AI enrichment outputs that distinguishes generator-fixable work from
  author-reviewable work.

## Next Step

Start `P27-T3` by defining the stop-policy summary contract and mapping current
statuses to:

- `continue_generation`;
- `stop_for_author_review`;
- `blocked_until_inputs_change`.
