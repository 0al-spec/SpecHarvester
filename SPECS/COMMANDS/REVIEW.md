# REVIEW

Status: Active

Review completed task work before final archive closure.

## Inputs

- `TASK_ID`
- Review subject name for `REVIEW_{subject}.md`
- Task archive path
- Diff range or branch name

## Review Focus

Prioritize findings in this order:

- correctness bugs;
- trust-boundary regressions;
- unsafe repository-content handling;
- deterministic output regressions;
- missing validation;
- CI, DocC, or SpecPM integration risks;
- documentation drift.

## Procedure

1. Inspect the task PRD, validation report, and relevant diff.
2. Verify that the implemented behavior matches acceptance criteria.
3. Check whether quality gates were appropriate for the change.
4. Save `SPECS/INPROGRESS/REVIEW_{subject}.md`.

## Report Template

```markdown
# REVIEW {subject}

Status: PASS | PASS_WITH_FINDINGS | FAIL
Task: {TASK_ID}
Date: YYYY-MM-DD

## Findings

- None.

## Required Follow-Up

- None.

## Validation Review

- Command: `...`
- Outcome: pass/fail/not run with reason

## Notes

- ...
```

## Completion Criteria

- Review report exists under `SPECS/INPROGRESS/`.
- Findings are ordered by severity.
- Each actionable finding has a required follow-up or an explicit decision to
  address it immediately.
- No actionable findings means `FOLLOW-UP` may be skipped.
