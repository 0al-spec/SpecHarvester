# Next Task: P48-T2 Execute AI Draft Blocker Follow-Up Pass

**Status:** Selected
**Branch:** `feature/P48-T2-execute-ai-draft-blocker-follow-up-pass`
**Phase:** Phase 48. AI Draft Blocker Follow-Up Before Larger Corpus
**Task:** `P48-T2`
**Last Archived:** `P48-T1` Plan AI Draft Blocker Follow-Up Pass
**Depends On:** `P48-T1` Plan AI Draft Blocker Follow-Up Pass

## Goal

Execute the P48-T1 blocker follow-up plan for the same six-repository bounded
pilot scope, clearing or explicitly disposing the AI draft blockers before any
larger curated corpus approval.

## Context

P48-T1 selected
`ai_draft_blocker_follow_up_before_larger_curated_corpus`. The plan keeps the
same six-repository bounded pilot scope and targets the failed AI draft
sidecars from the P47-T3 rerun gate:

- `gin.aiDraft`
- `navigation-split-view.aiDraft`

It also keeps the warning and caveat evidence visible for:

- `docc2context.aiDraft`
- `xyflow`

The larger curated corpus remains blocked until P48-T2 executes the targeted
pass, P48-T3 completes the static-only-before-AI bounded rerun gate, and P48-T4
records the exit decision.

## Scope

- Read the P48-T1 plan fixture and documentation.
- Execute the targeted blocker follow-up for `gin.aiDraft` and
  `navigation-split-view.aiDraft`.
- Preserve `docc2context.aiDraft` warning disposition evidence.
- Preserve `xyflow` partial-interface, fork-origin, and AI repair caveat
  visibility.
- Keep all AI sidecars proposal-only.
- Keep the same six-repository bounded pilot scope.
- Prepare evidence needed for the P48-T3 same-scope bounded rerun gate.

## Expected Deliverables

- Durable P48-T2 evidence describing the targeted blocker follow-up results.
- Explicit disposition for `gin.aiDraft`.
- Explicit disposition for `navigation-split-view.aiDraft`.
- Preserved warning disposition for `docc2context.aiDraft`.
- Preserved caveat visibility for `xyflow`.
- Clear statement that larger curated corpus planning remains blocked.
- Validation report and archive artifacts for P48-T2.

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
- Do not treat follow-up output as registry truth.
- Do not treat adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P48-T2 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
