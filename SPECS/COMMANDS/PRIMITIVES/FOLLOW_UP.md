# FOLLOW_UP

Status: Active

Create follow-up work from actionable review findings.

## Inputs

- Review report path.
- `TASK_ID` of the reviewed task.
- List of actionable findings.

## Procedure

1. For each actionable finding, decide whether it must be fixed immediately or
   converted into a future task.
2. If fixing immediately, update the implementation and validation report
   before archiving review.
3. If creating future work, append a task to `SPECS/Workplan.md` with:
   - task ID;
   - short title;
   - source review report;
   - acceptance criteria;
   - trust-boundary notes.
4. Update the review report with the follow-up decision.

## Completion Criteria

- Every actionable finding has a recorded disposition.
- Future work appears in `SPECS/Workplan.md`.
- Immediate fixes have validation evidence.
