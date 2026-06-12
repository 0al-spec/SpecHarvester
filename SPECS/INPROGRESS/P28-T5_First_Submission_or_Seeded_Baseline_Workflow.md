# P28-T5 — First-Submission or Seeded-Baseline Workflow

## Objective

Define a producer-side handoff for repositories that do not yet have current
SpecPM generated artifacts, so missing-baseline cases are treated as
first-submission or seeded-baseline review evidence rather than failed refresh
decisions.

## Motivation

P28-T3 proved the correct trust boundary for `TanStack/query`: SpecPM returned
`refresh_decision_prepare_current_contract_files_missing` because no current
generated baseline existed. That is not a generator failure and should not be
papered over as a refresh decision.

Operators need a clear artifact that says:

- the producer created candidate evidence;
- SpecPM could not compare because no baseline exists;
- maintainers must choose first submission, seeded baseline, or rejection;
- the artifact does not write registry truth or imply acceptance.

## Scope

In scope:

- Add a small machine-readable missing-baseline handoff artifact.
- Include source/fresh-run identity, package-set member counts, missing baseline
  diagnostic, recommended maintainer actions, and authority boundaries.
- Add CLI support for emitting the artifact from a fresh candidate refresh run
  and optional SpecPM prepare report.
- Update docs, DocC, roadmap, workplan, and Flow artifacts.
- Add regression tests covering the
  `refresh_decision_prepare_current_contract_files_missing` boundary.

Out of scope:

- SpecPM registry mutation.
- Creating accepted-source PRs automatically.
- Seeding a SpecPM baseline automatically.
- Treating generated candidates as accepted packages.
- Running upstream package scripts, package managers, builds, or tests.

## Acceptance Criteria

- A new CLI path emits a JSON artifact for missing-baseline repositories.
- The artifact distinguishes `first_submission_required` from ordinary refresh
  decisions and carries `producerEvidenceAuthority: evidence_only`.
- The artifact exposes maintainer action options such as `seed_baseline`,
  `first_submission_review`, and `reject_or_request_regeneration`.
- The artifact preserves source revision and package-set counts from
  `SpecHarvesterFreshCandidateRefreshRun`.
- Tests prove the missing-baseline diagnostic is recognized and that non-missing
  prepare reports do not produce a misleading first-submission artifact.
- Documentation explains how the artifact fits before SpecPM acceptance.

## Dependencies

- P28-T1 `SpecHarvesterFreshCandidateRefreshRun`.
- P28-T3 missing-baseline observation.
- P28-T4 role selection profiles for generic monorepo package-set production.

## Validation Plan

- Targeted tests for the new handoff artifact.
- CLI smoke for the new command.
- Full Python test suite.
- Ruff lint and format checks.
- Diff whitespace check.
- Swift docs build and DocC static generation.
