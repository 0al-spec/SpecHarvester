# Next Task: P29-T1 Autonomous Candidate Batch Runner

**Status:** Selected
**Selected:** 2026-06-13
**Task:** P29-T1 Autonomous Candidate Batch Runner
**Phase:** Phase 29. Autonomous Candidate Harvest MVP
**Last Archived:** P28-T5 First-Submission or Seeded-Baseline Workflow

## Recently Archived

- `P28-T5` added `SpecHarvesterBaselineSubmissionHandoff` and the
  `baseline-submission-handoff` CLI. The artifact records
  `first_submission_required` when SpecPM reports
  `refresh_decision_prepare_current_contract_files_missing`, exposes
  maintainer actions `first_submission_review`, `seed_baseline`, and
  `reject_or_request_regeneration`, and preserves `notRefreshDecision: true`.
  A practical TanStack/query run produced `39` candidates, `78` contract files,
  and `39` missing-baseline diagnostics.
- `P28-T4` added package-set role selection profiles. The new
  `--role-profile generic_monorepo` selects `workspace` and `member_package`
  roles without requiring raw `--role workspace --role member_package`
  operator knowledge. A practical TanStack/query run produced `39 candidates`
  and `38 contains relation proposals` through the named profile.
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

Phase 28 SpecPM Refresh Compare Handoff is complete on the SpecHarvester side.
SpecHarvester can now export package-set bundles into SpecPM fresh
generated-root layout, prove no-op refresh decisions on existing generated
baselines, expose missing-baseline cases as first-submission or seeded-baseline
handoff evidence, and keep all producer artifacts outside registry authority.

## Next Step

Implement `P29-T1`: add an autonomous candidate batch runner that orchestrates
the existing safe producer pipeline over a source manifest:

- collect deterministic snapshots with workspace inventory and public
  interface indexes;
- draft package-set preview bundles with the autonomous popular-library role
  profile;
- run bundle-set preflight;
- optionally call a local LM Studio/OpenAI-compatible provider for
  schema-bound AI draft and enrichment proposals;
- write one machine-readable batch report summarizing outputs, stop-policy
  status, and non-authority boundaries.

This task is the first MVP step for autonomous popular-library scraping. It
must not clone repositories, execute harvested code, install dependencies,
publish registry metadata, or treat generated output as accepted SpecPM truth.
