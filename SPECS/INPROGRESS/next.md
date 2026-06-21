# Next Task: P47-T4 Record Targeted Quality Follow-Up Exit Decision

**Status:** Selected
**Branch:** `feature/P47-T4-record-targeted-quality-follow-up-exit-decision`
**Phase:** Phase 47. Targeted Pilot Quality Follow-Up
**Task:** `P47-T4`
**Last Archived:** `P47-T3` Run Bounded Pilot Rerun Gate
**Depends On:** `P47-T3` Run Bounded Pilot Rerun Gate

## Goal

Record the targeted quality follow-up exit decision after the P47-T3 bounded
pilot rerun gate, deciding whether the project needs another targeted pass or
must stop on a documented blocker before larger curated corpus planning.

## Context

P47-T3 used the same six-repository bounded pilot scope. The static-only gate
passed. The AI-enabled gate failed because `gin.aiDraft` and
`navigation-split-view.aiDraft` failed after one JSON repair attempt.

`docc2context.aiDraft` improved to a repaired warning. `xyflow` did not repeat
`model_evidence_path_unsupported`, but still carries partial interface and AI
repair caveats. The larger curated corpus remains blocked until P47-T4 records
an explicit exit decision.

## Scope

- Read the P47-T3 validation report and durable fixture.
- Decide one of:
  - another targeted quality pass,
  - stop on documented blocker,
  - proceed only if the evidence explicitly supports readiness.
- Name the blocking sidecars and caveats:
  - `gin.aiDraft`
  - `navigation-split-view.aiDraft`
  - `docc2context.aiDraft`
  - `xyflow`
- Preserve proposal-only AI output and registry authority boundaries.

## Expected Deliverables

- Exit decision document for the targeted quality follow-up.
- Durable fixture or documentation recording the selected decision and evidence
  basis.
- Workplan/next-task update reflecting the selected path.
- Validation report and archive artifacts for P47-T4.

## Boundaries

- Do not approve a larger curated corpus unless P47-T4 explicitly chooses
  readiness from recorded evidence.
- Do not approve a larger curated corpus if the P47-T3 failed AI-enabled gate
  remains the controlling result.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not expand beyond the same six-repository bounded pilot scope during the
  decision task.
- Do not clone or fetch repositories.
- Do not execute harvested code.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat static output as registry truth.
- Do not treat plan output as registry truth.
- Do not treat adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P47-T4 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
