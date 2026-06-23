# P48-T3 Run Bounded Pilot Rerun Gate After AI Draft Blocker Follow-Up

Task: `P48-T3`
Phase: Phase 48. AI Draft Blocker Follow-Up Before Larger Corpus
Status: Planned
Branch: `feature/P48-T3-run-bounded-pilot-rerun-gate-after-ai-draft-blocker-follow-up`
Depends on: `P48-T2` Execute AI Draft Blocker Follow-Up Pass

## Problem

P48-T2 explicitly disposed the current failed `gin.aiDraft` and
`navigation-split-view.aiDraft` sidecars as non-blocking for another bounded
rerun gate. The next required step is to run or record the same six-repository
bounded pilot rerun gate with static-only evidence before AI-enabled evidence.

The gate must determine whether the AI-enabled path now passes or whether
remaining blockers must be carried to P48-T4.

## Goal

Record durable P48-T3 same-scope bounded rerun gate evidence after the P48-T2
dispositions, preserving proposal-only AI output, no raw prompt/response/CoT
persistence, and no registry authority.

## Deliverables

- A durable P48-T3 rerun gate fixture under
  `tests/fixtures/ai_draft_blocker_bounded_rerun_gate/`.
- Documentation and DocC documentation describing the rerun gate result,
  static-only-before-AI ordering, per-repository outcome, warnings, caveats,
  and P48-T4 exit-decision input.
- Docs-contract coverage for the P48-T3 fixture, docs, and current next task.
- Validation report for P48-T3.

## Acceptance Criteria

- The fixture references the P48-T2 follow-up pass fixture with a checked
  digest.
- The fixture uses the same six-repository bounded pilot scope and
  `inputs/p46-bounded-popular-library-pilot/repositories.yml`.
- Static-only evidence is recorded before AI-enabled evidence.
- AI output remains proposal-only and is not accepted as registry truth.
- Raw prompts, raw provider responses, secrets, and chain-of-thought are not
  persisted.
- Per-repository static and AI statuses are recorded for:
  - `flask`
  - `gin`
  - `xyflow`
  - `cupertino`
  - `navigation-split-view`
  - `docc2context`
- The result records whether the AI-enabled gate passes, and why larger
  curated corpus planning remains blocked or can be reconsidered by P48-T4.
- The next task is P48-T4 post-blocker follow-up exit decision.

## Boundaries

- Do not approve a larger curated corpus.
- Do not expand beyond the same six-repository bounded pilot scope.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories outside existing bounded pilot inputs.
- Do not execute harvested code.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output, static output, adapter output, or rerun output as
  registry truth.

## Validation Plan

- Validate durable JSON fixtures with `python3 -m json.tool`.
- Run focused docs-contract tests for P48-T3 and the current next task.
- Run `ruff check`, `ruff format --check`, full pytest, Swift manifest/doc
  checks, coverage, and `git diff --check` as required by Flow.
