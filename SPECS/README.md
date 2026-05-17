# SpecHarvester SPECS

Status: Active

This directory contains the repository-local Flow operating layer for planning,
executing, reviewing, and archiving SpecHarvester tasks.

## Entry Points

- `PRD.md`: product requirements and non-goals for SpecHarvester.
- `Workplan.md`: ordered task backlog and task identifiers.
- `COMMANDS/FLOW.md`: required end-to-end task workflow.
- `COMMANDS/ARCHIVE.md`: archive procedure for completed task artifacts.
- `COMMANDS/REVIEW.md`: review procedure for completed task work.
- `COMMANDS/PRIMITIVES/FOLLOW_UP.md`: follow-up task creation procedure.
- `INPROGRESS/next.md`: currently selected or recommended next task.
- `ARCHIVE/INDEX.md`: historical task archive index.

## Task Identifier Format

Use `P{phase}-T{task}` identifiers, for example `P1-T1`.

Branch names should follow:

```text
feature/{TASK_ID}-{short-description}
```

## Quality Gates

Flow tasks that touch implementation, tests, candidate generation, validation,
promotion, CI, or DocC must record the relevant gates in their validation
report. The baseline local gates are:

```bash
python -m pip install -e ".[dev]"
ruff check src tests
ruff format --check src tests
pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
```

Documentation-only tasks may run a narrower gate set, but the validation report
must state why broader gates were not required.
