# Next Task: P28-T4 Package-Set Role Selection Profiles

**Status:** In Progress
**Last Archived:** P28-T3 Second Real Repository Refresh Compare Run
**Archived:** 2026-06-12
**Selected:** 2026-06-13

## Recently Archived

- `P28-T3` ran real `TanStack/query` at
  `feb1efd804c1262106f72c8adc1d82a8ce9cfbb0` through SpecHarvester and local
  SpecPM. Default draft roles produced only `tanstack_query.workspace`; explicit
  `--role workspace --role member_package` produced `39` candidates, `38`
  `contains` relation proposals, `78` fresh contract files, and a structured
  SpecPM missing-baseline result:
  `refresh_decision_prepare_current_contract_files_missing`.
- `P28-T2` ran real `xyflow` at
  `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` through SpecHarvester and local
  SpecPM. SpecPM produced `status: no_update_required`,
  `updateNeeded: false`, `reason: no_contract_delta`, and verified 8 generated
  contract-file digests.
- `P28-T1` added `SpecHarvesterFreshCandidateRefreshRun` and
  `fresh-candidate-refresh-run`, exporting generated package-set bundles into
  the SpecPM `prepare-refresh-decision` fresh generated-root layout without
  publishing packages or replacing SpecPM maintainer review.
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

Run P28-T4 Package-Set Role Selection Profiles: add a named role selection
profile or preset for generic monorepos so a useful workspace/member package-set
does not depend on operator knowledge of `--role member_package`.

The immediate product target is the TanStack/query observation from P28-T3:
default drafting found the workspace root, but the useful package-set required
explicit member-package role selection. P28-T4 should make that intent
declarative, documented, and covered by tests.

Expected P28-T4 output:

- a named role selection profile or preset for generic monorepos;
- CLI/docs that explain the profile without requiring raw role flags;
- regression coverage showing the TanStack/query-style workspace/member set can
  be selected through the profile.

Queued after P28-T4:

- `P28-T5` first-submission or seeded-baseline workflow for repositories without
  current SpecPM generated artifacts.
