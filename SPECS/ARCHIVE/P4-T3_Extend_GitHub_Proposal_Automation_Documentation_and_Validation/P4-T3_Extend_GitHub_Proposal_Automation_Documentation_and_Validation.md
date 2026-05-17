# P4-T3 Extend GitHub Proposal Automation Documentation and Validation

Status: Planned
Selected: 2026-05-18
Branch: `feature/P4-T3-extend-github-proposal-automation-documentation-and-validation`
Review subject: `p4_t3_extend_proposal_automation_docs`

## Objective

Improve proposal automation operator documentation and trust-boundary guidance for
cross-repository accepted-source proposal automation so trusted maintainers can
quickly validate safety and scope of each proposal before creating a SpecPM PR.

## Deliverables

- Update `docs/SPECPM_PROPOSAL_AUTOMATION.md` with explicit preflight validation
  semantics for proposal candidate identity and diff scope.
- Update the DocC page `Sources/SpecHarvester/Documentation.docc/ProposalAutomation.md`
  to mirror the proposal trust and preflight guidance.
- Clarify where proposal evidence comes from in CI and what to include in PR review.
- Ensure `docs/README.md` and cross-references remain current and complete.
- Keep all edits documentation-only and deterministic.

## Proposal Preflight Documentation Scope

- Candidate identity validation (`metadata.id`, `metadata.version`) against
  workflow inputs (`package_id`, `package_version`).
- Symlink rejection for candidate manifest reads.
- SpecPM diff scope check after `specpm public-index generate`.
- Failure-mode map from preflight output to operator action.
- Explicit trust boundary and review checklist updates.

## Acceptance Criteria

- Documentation clearly explains what is validated by workflow preflight before
  cross-repository write.
- Operators can determine from docs how to set `candidate_dir`, `package_id`, and
  `package_version` deterministically.
- Reviewer evidence list includes both candidate validation and generated public
  index checks.
- No behavior change in automation logic; only documentation and mirrored DocC
  content are required for this task.
- Existing Flow quality gates and docs contracts continue to pass.
