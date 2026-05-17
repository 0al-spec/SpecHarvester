# FLOW

Status: Active

Run this workflow when delivering a SpecHarvester task end to end.

Required sequence:

```text
BRANCH -> SELECT -> PLAN -> EXECUTE -> ARCHIVE -> REVIEW -> FOLLOW-UP -> ARCHIVE-REVIEW
```

`FOLLOW-UP` may be skipped only when `REVIEW` records no actionable findings.

## Required Inputs

- Task identifier, for example `P1-T1`.
- Short task description.
- Current branch and whether a feature branch already exists.
- Review subject name for `SPECS/INPROGRESS/REVIEW_{subject}.md`.

If the task identifier is unknown, select the first unchecked task from
`SPECS/Workplan.md`, using `SPECS/INPROGRESS/next.md` as the current hint.

## BRANCH

1. Verify the working tree:

```bash
git status --short --branch
```

2. Update `main`:

```bash
git fetch origin
git switch main
git pull --ff-only
```

3. Create or switch to the feature branch:

```bash
git switch -c feature/{TASK_ID}-{short-description}
```

4. Create the branch checkpoint:

```bash
git commit --allow-empty -m "Branch for {TASK_ID}: {short description}"
```

## SELECT

1. Select the task from `SPECS/Workplan.md`.
2. Update `SPECS/INPROGRESS/next.md` with:
   - task ID;
   - task name;
   - branch;
   - status;
   - selected date;
   - expected artifacts.
3. Commit:

```bash
git add SPECS/INPROGRESS/next.md
git commit -m "Select task {TASK_ID}: {TASK_NAME}"
```

## PLAN

1. Create `SPECS/INPROGRESS/{TASK_ID}_{TASK_NAME}.md`.
2. Include:
   - problem;
   - goals;
   - non-goals;
   - deliverables;
   - acceptance criteria;
   - trust boundary;
   - validation plan.
3. Commit:

```bash
git add SPECS/INPROGRESS/{TASK_ID}_{TASK_NAME}.md
git commit -m "Plan task {TASK_ID}: {TASK_NAME}"
```

## EXECUTE

1. Implement the task against the PRD.
2. Keep edits scoped to the task boundary.
3. Run relevant quality gates.
4. Create `SPECS/INPROGRESS/{TASK_ID}_Validation_Report.md`.
5. Commit:

```bash
git add .
git commit -m "Implement {TASK_ID}: {brief description of changes}"
```

### Baseline Quality Gates

Run from the repository root after installing dev dependencies:

```bash
python -m pip install -e ".[dev]"
ruff check src tests
ruff format --check src tests
pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
```

If the local package is not installed, prefix Python gates with:

```bash
PYTHONPATH=src
```

For tasks that affect candidate generation, promotion, SpecPM integration, CI,
or proposal automation, also run the narrowest relevant integration check and
record the command in the validation report.

`mypy` is not configured in this repository. Do not invent a type-check gate
until a task explicitly adds configuration.

## ARCHIVE

Run `SPECS/COMMANDS/ARCHIVE.md`.

Commit:

```bash
git add SPECS/Workplan.md SPECS/INPROGRESS SPECS/ARCHIVE
git commit -m "Archive task {TASK_ID}: {TASK_NAME} ({VERDICT})"
```

## REVIEW

Run `SPECS/COMMANDS/REVIEW.md`.

Save the report at:

```text
SPECS/INPROGRESS/REVIEW_{subject}.md
```

Commit:

```bash
git add SPECS/INPROGRESS/REVIEW_{subject}.md
git commit -m "Review {TASK_ID}: {short subject}"
```

## FOLLOW-UP

If review has actionable findings, run:

```text
SPECS/COMMANDS/PRIMITIVES/FOLLOW_UP.md
```

Commit:

```bash
git add SPECS/Workplan.md SPECS/INPROGRESS
git commit -m "Follow-up {TASK_ID}: {short subject}"
```

If review has no actionable findings, record `FOLLOW-UP skipped: no actionable
findings` in the review archive note.

## ARCHIVE-REVIEW

Move `SPECS/INPROGRESS/REVIEW_{subject}.md` to the task archive folder or to
`SPECS/ARCHIVE/_Historical/` when it is cross-cutting.

Update `SPECS/ARCHIVE/INDEX.md`.

Commit:

```bash
git add SPECS/ARCHIVE SPECS/INPROGRESS
git commit -m "Archive REVIEW_{subject} report"
```

## Completion Criteria

- All required Flow steps completed in order.
- Optional `FOLLOW-UP` either completed or formally skipped.
- Task PRD, validation report, review report, and archive index are present.
- Quality gates ran and outcomes are recorded.
- Commit checkpoints follow the message patterns above.
