# Next Task: P49-T2 Execute docc2context AI Draft Targeted Follow-Up Pass

**Status:** Selected
**Branch:** `feature/P49-T2-execute-docc2context-ai-draft-targeted-follow-up-pass`
**Phase:** Phase 49. docc2context AI Draft Targeted Follow-Up
**Task:** `P49-T2`
**Last Archived:** `P49-T1` Plan docc2context AI Draft Targeted Follow-Up Pass
**Depends On:** `P49-T1` Plan docc2context AI Draft Targeted Follow-Up Pass

## Goal

Execute the targeted follow-up pass for `docc2context.aiDraft`, constraining
subject metadata and JSON repair exhaustion before the next same-scope bounded
rerun gate.

## Context

P49-T1 selected:

```text
docc2context_ai_draft_targeted_follow_up_before_larger_curated_corpus
```

The target blocker remains:

- `docc2context.aiDraft`
- `ai_json_repair_exhausted`
- `ai_json_repair_needed`
- `package_set_subject_metadata_missing`

P49-T2 must keep `docc2context.core` subject metadata present and must record
whether the sidecar becomes `completed` or explicitly non-blocking `warning`.

The larger curated corpus remains blocked until P49-T2 executes the targeted
pass, P49-T3 reruns the same six-repository bounded gate, and P49-T4 records
the exit decision.

## Scope

- Target only `docc2context.aiDraft`.
- Preserve P48-T3/P48-T4 warning IDs unchanged:
  `flask.aiDraft`, `flask.aiEnrichment`, `gin.aiDraft`,
  `cupertino.aiDraft`, and `navigation-split-view.aiDraft`.
- Preserve xyflow caveats for the next exit review; xyflow caveats remain
  visible until P49-T4 records their exit disposition.
- Keep all AI output proposal-only.
- Preserve no raw prompt, raw provider response, secrets, or chain-of-thought
  persistence.

## Expected Deliverables

- Durable P49-T2 execution evidence.
- Explicit status for `docc2context.aiDraft`.
- Clear disposition for `ai_json_repair_exhausted` and
  `package_set_subject_metadata_missing`.
- Validation report and archive artifacts for P49-T2.

## Boundaries

- Do not approve a larger curated corpus.
- Do not run the same-scope bounded rerun in P49-T2.
- Do not expand beyond `docc2context.aiDraft`.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not execute harvested code.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat static output as registry truth.
- Do not treat targeted follow-up output as registry truth.
- Do not treat exit-decision output as registry truth.
- Do not treat plan output as registry truth.
- Do not treat adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P49-T2 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
