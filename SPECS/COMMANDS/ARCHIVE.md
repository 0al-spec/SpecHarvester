# ARCHIVE

Status: Active

Archive completed task artifacts after `EXECUTE`.

## Inputs

- `TASK_ID`
- `TASK_NAME`
- `VERDICT`: `PASS`, `PASS_WITH_NOTES`, or `FAIL`
- Task PRD path under `SPECS/INPROGRESS/`
- Validation report path under `SPECS/INPROGRESS/`

## Procedure

1. Create the task archive directory:

```text
SPECS/ARCHIVE/{TASK_ID}_{TASK_NAME}/
```

2. Move or copy task artifacts into the archive directory:

```text
SPECS/INPROGRESS/{TASK_ID}_{TASK_NAME}.md
SPECS/INPROGRESS/{TASK_ID}_Validation_Report.md
```

3. Add `SUMMARY.md` with:
   - task ID and name;
   - branch;
   - implementation summary;
   - validation commands and outcomes;
   - final verdict;
   - follow-up requirement.

4. Update `SPECS/Workplan.md`:
   - mark the task complete when `VERDICT` is `PASS` or `PASS_WITH_NOTES`;
   - leave it incomplete and add a note when `VERDICT` is `FAIL`.

5. Update `SPECS/INPROGRESS/next.md`:
   - clear the active task;
   - point to the next unchecked task from `SPECS/Workplan.md`.

6. Update `SPECS/ARCHIVE/INDEX.md` with the archive path and verdict.

## Completion Criteria

- Task archive directory exists.
- Validation report is archived.
- Workplan reflects the task verdict.
- `next.md` no longer points to completed work as active.
- Archive index links the task archive.
