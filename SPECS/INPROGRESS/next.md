# Next Task: P49-T4 Record docc2context Follow-Up Exit Decision

**Status:** Selected
**Branch:** `feature/P49-T4-record-docc2context-follow-up-exit-decision`
**Phase:** Phase 49. docc2context AI Draft Targeted Follow-Up
**Task:** `P49-T4`
**Last Archived:** `P49-T3` Run Same-Scope Bounded Rerun Gate
**Depends On:** `P49-T3` Run Same-Scope Bounded Rerun Gate

## Goal

Record the docc2context follow-up exit decision after P49-T3 documented that
the same-scope bounded rerun gate is blocked by missing operator-local
checkouts.

## Context

P49-T3 selected:

```text
same_scope_bounded_rerun_gate_blocked_operator_local_checkouts_missing
```

P49-T3 did not run the static-only gate or the AI-enabled gate because all six
P46 operator-local checkout paths were absent:

- `flask`
- `gin`
- `xyflow`
- `cupertino`
- `navigation-split-view`
- `docc2context`

LM Studio was available with `openai/gpt-oss-20b`, but AI execution was not
reached because static-only-before-AI ordering stopped at checkout preflight.

P49-T2 remains carried forward as:

```text
docc2context.aiDraft_warning_explicitly_non_blocking_for_p49_t3
excluded_package_also_selected
```

The larger curated corpus remains blocked until P49-T4 records the exit
decision.

## Scope

- Decide whether Phase 49 should stop on the operator-local checkout blocker,
  request a P49-T3 rerun after checkouts are restored, or record no larger
  corpus readiness.
- Preserve P48 warning IDs and xyflow caveats.
- Preserve proposal-only and non-registry-authority boundaries.

## Expected Deliverables

- Durable P49-T4 exit decision evidence.
- GitHub and DocC documentation for the exit decision.
- Workplan/next update to the selected follow-up state.
- Validation report and archive artifacts for P49-T4.

## Boundaries

- Do not approve a larger curated corpus unless the P49-T3 blocker is
  explicitly resolved by evidence.
- Do not run another bounded rerun in P49-T4.
- Do not run AI.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat AI output, static output, rerun output, targeted follow-up
  output, exit-decision output, or adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P49-T4 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
