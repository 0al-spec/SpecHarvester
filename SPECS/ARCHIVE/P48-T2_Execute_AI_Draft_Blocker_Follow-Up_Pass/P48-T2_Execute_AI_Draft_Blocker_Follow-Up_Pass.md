# P48-T2 Execute AI Draft Blocker Follow-Up Pass

Task: `P48-T2`
Phase: Phase 48. AI Draft Blocker Follow-Up Before Larger Corpus
Status: Planned
Branch: `feature/P48-T2-execute-ai-draft-blocker-follow-up-pass`
Depends on: `P48-T1` Plan AI Draft Blocker Follow-Up Pass

## Problem

P48-T1 selected an AI draft blocker follow-up before any larger curated corpus
planning. The P47-T3 rerun gate still had blocking AI draft failures for
`gin.aiDraft` and `navigation-split-view.aiDraft`, while `docc2context.aiDraft`
and `xyflow.aiEnrichment` remained warning/caveat evidence that must stay
visible.

P48-T2 must execute that follow-up as durable evidence without changing the
registry authority boundary.

## Goal

Record the targeted blocker follow-up result for the same six-repository
bounded pilot scope, making the disposition of the two blocking AI draft
sidecars explicit and preserving the warning/caveat context needed for the
P48-T3 bounded rerun gate.

## Deliverables

- A machine-readable P48-T2 follow-up result fixture under
  `tests/fixtures/ai_draft_blocker_follow_up_pass/`.
- Human-readable docs and DocC docs describing the P48-T2 result, target
  sidecars, warning/caveat dispositions, preserved boundaries, and P48-T3
  preconditions.
- Docs-contract tests covering the fixture, documentation, Workplan, and
  `SPECS/INPROGRESS/next.md` transition.
- Validation report for P48-T2.

## Acceptance Criteria

- The fixture references the P48-T1 plan fixture with a checked digest.
- The fixture keeps the same six-repository bounded pilot scope and the
  `inputs/p46-bounded-popular-library-pilot/repositories.yml` manifest.
- The follow-up records explicit dispositions for:
  - `gin.aiDraft`;
  - `navigation-split-view.aiDraft`;
  - `docc2context.aiDraft`;
  - `xyflow.aiEnrichment`;
  - xyflow `partial_public_interface_index`;
  - xyflow `operator_checkout_origin_fork_mismatch`;
  - xyflow `ai_json_repair_needed`.
- `gin.aiDraft` and `navigation-split-view.aiDraft` no longer carry
  `ai_json_repair_exhausted` or `package_set_subject_metadata_missing` as
  active P48-T3 blockers in the P48-T2 evidence.
- Remaining warnings/caveats are explicitly retained as visible evidence for
  the P48-T3 gate and P48-T4 exit decision.
- Larger curated corpus planning remains blocked until P48-T3 and P48-T4
  complete.
- Proposal-only AI output and raw prompt/response/CoT non-persistence are
  preserved.

## Boundaries

- Do not approve a larger curated corpus.
- Do not expand beyond the same six-repository bounded pilot scope.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not install dependencies or execute harvested code.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output, static output, adapter output, or follow-up output as
  registry truth.

## Validation Plan

- Validate the durable JSON fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for P48-T2 and the current next task.
- Run `ruff check`, `ruff format --check`, full pytest, Swift manifest/doc
  checks, coverage, and `git diff --check` as required by Flow.

---

**Archived:** 2026-06-23
**Verdict:** PASS
