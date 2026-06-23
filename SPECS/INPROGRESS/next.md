# Next Task: P49-T1 Plan docc2context AI Draft Targeted Follow-Up Pass

**Status:** Selected
**Branch:** `feature/P49-T1-plan-docc2context-ai-draft-targeted-follow-up-pass`
**Phase:** Phase 49. docc2context AI Draft Targeted Follow-Up
**Task:** `P49-T1`
**Last Archived:** `P48-T4` Record Post-Blocker Follow-Up Exit Decision
**Depends On:** `P48-T4` Record Post-Blocker Follow-Up Exit Decision

## Goal

Plan the targeted follow-up pass for the remaining `docc2context.aiDraft`
blocker recorded by P48-T4.

## Context

P48-T4 selected:

```text
run_docc2context_ai_draft_targeted_pass_before_larger_curated_corpus
```

P48-T3 showed that the static-only same-scope bounded gate passed, but the
AI-enabled gate failed on `docc2context.aiDraft` with:

- `ai_json_repair_exhausted`
- `ai_json_repair_needed`
- `package_set_subject_metadata_missing`

`gin.aiDraft` and `navigation-split-view.aiDraft` no longer hard-fail and are
warning-only. xyflow caveats remain visible for later exit review.

The larger curated corpus remains blocked until the docc2context targeted pass,
same-scope bounded rerun gate, and follow-up exit decision complete.

## Scope

- Plan a targeted follow-up for `docc2context.aiDraft`.
- Preserve the same six-repository bounded pilot scope for the later rerun.
- Define constraints for subject metadata and JSON repair exhaustion.
- Keep all AI output proposal-only.
- Preserve no raw prompt, raw provider response, secrets, or chain-of-thought
  persistence.

## Expected Deliverables

- Durable P49-T1 plan evidence.
- Explicit success criteria for P49-T2 and P49-T3.
- Clear statement that larger curated corpus planning remains blocked.
- Validation report and archive artifacts for P49-T1.

## Boundaries

- Do not approve a larger curated corpus.
- Do not run the targeted pass in P49-T1.
- Do not run another bounded rerun in P49-T1.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not execute harvested code.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat static output as registry truth.
- Do not treat exit-decision output as registry truth.
- Do not treat adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P49-T1 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
