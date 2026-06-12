## REVIEW REPORT — P28-T5 First-Submission Baseline Workflow

**Scope:** `codex/p28-t4-role-selection-profiles..HEAD`
**Files:** 19

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

- None.

### Secondary Issues

- None.

### Architectural Notes

- `SpecHarvesterBaselineSubmissionHandoff` correctly models missing-baseline
  output as producer evidence, not as a SpecPM refresh decision or registry
  acceptance.
- The command refuses a supplied SpecPM prepare report unless it contains
  `refresh_decision_prepare_current_contract_files_missing`, which avoids
  converting unrelated SpecPM prepare failures into first-submission evidence.
- The next useful step is outside this repository: SpecPM should add
  consumer-side intake policy or preflight for
  `SpecHarvesterBaselineSubmissionHandoff` artifacts.

### Tests

- P28-T5 validation report records targeted tests, full tests, coverage, lint,
  format, diff check, Swift docs build, and DocC static generation.
- The archived practical TanStack/query run proves the intended missing-baseline
  path with `39` candidates, `78` contract files, and `39` missing-baseline
  diagnostics.

### Next Steps

- FOLLOW-UP skipped for SpecHarvester: no actionable repository-local defects
  were found in this review.
- Track the cross-repository SpecPM intake/preflight policy separately in
  SpecPM.
