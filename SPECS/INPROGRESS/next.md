# Next Task: P48-T4 Record Post-Blocker Follow-Up Exit Decision

**Status:** Selected
**Branch:** `feature/P48-T4-record-post-blocker-follow-up-exit-decision`
**Phase:** Phase 48. AI Draft Blocker Follow-Up Before Larger Corpus
**Task:** `P48-T4`
**Last Archived:** `P48-T3` Run Bounded Pilot Rerun Gate After AI Draft Blocker Follow-Up
**Depends On:** `P48-T3` Run Bounded Pilot Rerun Gate After AI Draft Blocker Follow-Up

## Goal

Record the post-blocker follow-up exit decision using the P48-T3 same-scope
bounded rerun gate evidence.

## Context

P48-T3 reran the same six-repository bounded pilot scope after the P48-T2 AI
draft blocker follow-up. The static-only gate passed again, but the
AI-enabled gate failed on `docc2context.aiDraft`.

P48-T3 showed:

- `gin.aiDraft` no longer hard-fails and is warning-only.
- `navigation-split-view.aiDraft` no longer hard-fails and is warning-only.
- `docc2context.aiDraft` remains blocking with `ai_json_repair_exhausted`,
  `ai_json_repair_needed`, and `package_set_subject_metadata_missing`.
- `xyflow` caveats remain visible, including `partial_public_interface_index`
  and `operator_checkout_origin_fork_mismatch`.

The larger curated corpus remains blocked until P48-T4 explicitly decides
whether to proceed, run another targeted pass, or stop larger corpus planning.

## Scope

- Use the P48-T3 bounded rerun gate fixture as decision input.
- Decide whether the remaining `docc2context.aiDraft` blocker requires another
  targeted pass, can be accepted as a non-blocking pilot caveat, or stops
  larger corpus planning.
- Preserve static-only-before-AI and proposal-only AI boundaries.
- Keep all warning and caveat evidence visible for future corpus decisions.

## Expected Deliverables

- Durable P48-T4 exit decision evidence.
- Explicit decision on the remaining `docc2context.aiDraft` blocker.
- Clear larger curated corpus readiness decision.
- Validation report and archive artifacts for P48-T4.

## Boundaries

- Do not approve a larger curated corpus without explicitly resolving the
  P48-T3 `docc2context.aiDraft` blocker.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not execute harvested code.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat static output as registry truth.
- Do not treat rerun output as registry truth.
- Do not treat adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P48-T4 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
