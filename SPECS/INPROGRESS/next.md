# Next Task: P49-T3 Run Same-Scope Bounded Rerun Gate

**Status:** Selected
**Branch:** `feature/P49-T3-run-same-scope-bounded-rerun-gate`
**Phase:** Phase 49. docc2context AI Draft Targeted Follow-Up
**Task:** `P49-T3`
**Last Archived:** `P49-T2` Execute docc2context AI Draft Targeted Follow-Up Pass
**Depends On:** `P49-T2` Execute docc2context AI Draft Targeted Follow-Up Pass

## Goal

Run the same six-repository bounded rerun gate after the `docc2context.aiDraft`
targeted follow-up pass, preserving static-only-before-AI ordering.

## Context

P49-T2 selected:

```text
docc2context.aiDraft_warning_explicitly_non_blocking_for_p49_t3
```

The previous `docc2context.aiDraft` blockers are cleared or explicitly disposed
for P49-T3:

- `ai_json_repair_exhausted`
- `ai_json_repair_needed`
- `package_set_subject_metadata_missing`

P49-T2 still carries a non-blocking warning:

- `excluded_package_also_selected`

The larger curated corpus remains blocked until P49-T3 runs the same-scope
bounded gate and P49-T4 records the exit decision.

## Scope

- Use the same six-repository bounded pilot manifest:
  `inputs/p46-bounded-popular-library-pilot/repositories.yml`.
- Run the static-only gate before the AI-enabled gate.
- Preserve P48-T3/P48-T4 warning IDs unchanged:
  `flask.aiDraft`, `flask.aiEnrichment`, `gin.aiDraft`,
  `cupertino.aiDraft`, and `navigation-split-view.aiDraft`.
- Preserve xyflow caveats for the P49-T4 exit review:
  `xyflow.partial_public_interface_index` and
  `xyflow.operator_checkout_origin_fork_mismatch`.
- Keep all AI output proposal-only.
- Preserve no raw prompt, raw provider response, secrets, or chain-of-thought
  persistence.

## Expected Deliverables

- Durable P49-T3 bounded rerun gate evidence.
- Static-only gate result for the same six repositories.
- AI-enabled gate result for the same six repositories if local model execution
  is available.
- Explicit disposition for any remaining `docc2context.aiDraft` warnings.
- Validation report and archive artifacts for P49-T3.

## Boundaries

- Do not approve a larger curated corpus.
- Do not expand beyond the same six-repository bounded pilot scope.
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
- Do not treat targeted follow-up output as registry truth.
- Do not treat exit-decision output as registry truth.
- Do not treat adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P49-T3 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
