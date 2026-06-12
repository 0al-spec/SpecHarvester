# Next Task: Phase 27 Complete

**Status:** Phase Complete
**Last Archived:** P27-T5 Real Repository Author-Ready Draft Calibration Matrix
**Archived:** 2026-06-12

## Recently Archived

- `P27-T5` added `SpecHarvesterAuthorReadyCalibrationMatrix` and
  `author-ready-calibration-matrix`, then calibrated six pinned real repository
  checkouts. The observed result was 6/6 `author_ready_draft`,
  `totalEstimatedAuthorEdits` = 2, `generatorFollowUpCount` = 0, and
  `calibrationVerdict` = `author_curation_ready`.
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

## Outcome

Phase 27 Author-Ready Valid Drafts is complete. SpecHarvester now has a
documented author-ready quality bar, a machine-readable quality report,
deterministic stop-policy summaries, author review surfaces, and a
real-repository calibration matrix that measures remaining author work
separately from SpecPM validation.

## Next Step

Pick the next product phase from the roadmap. A likely follow-up is expanding
calibration into a repeatable multi-repository quality suite while keeping
generated candidates as local evidence, not committed registry truth.

The current cross-repository follow-up is P28-T1 Fresh Candidate Refresh Run Contract:
export generated package-set bundles into the SpecPM
`prepare-refresh-decision` fresh generated-root layout so refresh/no-op
decisions can be compared mechanically without treating SpecHarvester as
registry authority.
