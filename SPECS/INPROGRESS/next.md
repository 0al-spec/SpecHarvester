# Next Task: P48-T3 Run Bounded Pilot Rerun Gate After AI Draft Blocker Follow-Up

**Status:** Selected
**Branch:** `feature/P48-T3-run-bounded-pilot-rerun-gate-after-ai-draft-blocker-follow-up`
**Phase:** Phase 48. AI Draft Blocker Follow-Up Before Larger Corpus
**Task:** `P48-T3`
**Last Archived:** `P48-T2` Execute AI Draft Blocker Follow-Up Pass
**Depends On:** `P48-T2` Execute AI Draft Blocker Follow-Up Pass

## Goal

Run the same six-repository bounded pilot rerun gate after the P48-T2 blocker
follow-up, preserving static-only-before-AI ordering and recording whether the
AI-enabled gate now passes.

## Context

P48-T2 recorded
`ready_for_p48_t3_bounded_rerun_gate_with_explicit_ai_draft_dispositions`.
The current `gin.aiDraft` and `navigation-split-view.aiDraft` failed sidecars
were explicitly disposed as non-blocking for this rerun gate, while remaining
non-promotable and not accepted as registry truth.

P48-T3 must use the same six-repository bounded pilot scope and manifest:

```text
inputs/p46-bounded-popular-library-pilot/repositories.yml
```

The rerun gate must keep visible evidence for:

- `gin.aiDraft`
- `navigation-split-view.aiDraft`
- `docc2context.aiDraft`
- `xyflow`

The larger curated corpus remains blocked until P48-T3 records the same-scope
bounded rerun result and P48-T4 records the post-blocker follow-up exit
decision.

## Scope

- Verify the same six-repository bounded pilot scope.
- Run or record the static-only gate before any AI-enabled evidence.
- Run or record the proposal-only AI-enabled gate after static evidence.
- Preserve warning and caveat visibility for `docc2context.aiDraft` and
  `xyflow`.
- Keep current disposed `gin.aiDraft` and `navigation-split-view.aiDraft`
  sidecars out of registry truth.
- Record whether the AI-enabled gate now passes.

## Expected Deliverables

- Durable P48-T3 bounded rerun gate evidence.
- Explicit static-only-before-AI ordering evidence.
- Per-repository gate status for the same six repositories.
- Proposal-only AI sidecar status for `gin.aiDraft`,
  `navigation-split-view.aiDraft`, `docc2context.aiDraft`, and `xyflow`.
- Clear statement that larger curated corpus planning remains blocked until
  P48-T4.
- Validation report and archive artifacts for P48-T3.

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
- Do not treat adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P48-T3 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
