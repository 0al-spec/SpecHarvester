# Next Task: P27-T2 Author-Ready Draft Quality Report

**Status:** Selected
**Last Archived:** P26-T5 Package-Set AI Draft Proposal Contract
**Archived:** 2026-06-10

## Recently Archived

- `P26-T5` added `SpecHarvesterPackageSetAIDraftProposal`, preserving the
  original `LLM + schema` package-set idea: deterministic workspace inventory is
  evidence, the model proposes selected members, exclusions, and `contains`
  relations, and SpecPM plus maintainers remain the acceptance authority.
- `P26-T4` added proposal-only package-set AI enrichment for local
  OpenAI-compatible providers such as LM Studio, with provider receipts,
  privacy boundaries, unsupported evidence diagnostics, and no generated spec
  mutation.
- `P27-T1` documented the author-ready draft quality bar: SpecHarvester should
  produce a valid starter package for repository authors, not a final accepted
  specification.

## Motivation

- The quality bar is now documented, but operators still need a
  machine-readable report that says whether a generated draft is good enough to
  hand to an author.
- Existing quality reports cover real-repository validation dimensions, but they
  do not yet expose an explicit author-ready verdict, author action items, or a
  stop-policy reason.
- Without this report, reviewers may confuse a valid starter package with a
  fully curated spec, or keep rerunning the model after the remaining work is
  author-reviewable.

## Goal

- Extend quality reporting with an `authorReadyDraft` verdict and author action
  items derived from validation reports, bundle preflight, AI draft diagnostics,
  AI enrichment diagnostics, and viewer metadata.

## Next Step

Start `P27-T2` by defining the machine-readable author-ready draft quality
report shape and the first deterministic derivation rules for:

- `author_ready_draft`;
- `needs_regeneration`;
- `blocked`.
