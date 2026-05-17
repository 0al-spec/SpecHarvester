# P4-T2 Add Proposal Preflight Checks for Accepted-Source Diffs

Status: Planned
Selected: 2026-05-18
Branch: `feature/P4-T2-add-proposal-preflight-checks-for-accepted-source-diffs`
Review subject: `p4_t2_add_proposal_preflight_checks`

## Objective

Add deterministic preflight validation gates in SpecHarvester→SpecPM proposal automation so risky or malformed accepted-source proposal inputs fail fast before creating cross-repository proposal diff state.

## Deliverables

- Add a preflight step that validates candidate identity against proposal inputs.
- Enforce `specpm.yaml` is read only from the candidate directory without symlink escape paths.
- Add preflight check for generated SpecPM diff scope (`public-index/generated/...` and `public-index/accepted-packages.yml`).
- Keep promotion/validation flow unchanged when checks pass.
- Record execution and coverage evidence in task validation report.

## Acceptance Criteria

- A candidate with mismatched `metadata.id` or `metadata.version` fails the workflow before promote.
- A candidate with symlink-based `specpm.yaml` is rejected by preflight.
- Proposal diff preflight validates that changed files are limited to:
  - `public-index/generated/<packageId>/<version>/*`
  - `public-index/accepted-packages.yml`
- No cross-repository writes happen before preflight passes.
- Workflow logs actionable failure causes for review.
- Tests and quality gates required by `.flow/params.yaml` pass.

## Dependencies

- `P4-T1`

## Boundaries and Risks

- No candidate content execution is added to the workflow.
- No external network calls or package managers are introduced in preflight.

