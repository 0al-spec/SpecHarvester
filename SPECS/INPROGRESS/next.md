# Next Task: P45-T4 Post-Fix Readiness Decision for Bounded Popular-Library Scraping

**Status:** Selected
**Branch:** `feature/P45-T4-post-fix-readiness-decision`
**Phase:** Phase 45. Operational MVP AI Draft Shape Hardening
**Task:** `P45-T4`
**Depends On:** `P45-T3` Operational MVP Corpus Rerun After AI Draft Shape Fix

## Goal

Record the post-fix readiness decision for bounded popular-library scraping
after the P45-T3 corpus rerun.

## Context

P45-T3 reran the same bounded operational MVP corpus after P45-T1/P45-T2 AI
draft shape hardening. The old identity/unknown-exclusion warning class is
resolved across xyflow, FastAPI, and Gin, but the AI draft layer is not fully
clean: xyflow now reports `selected_member_role_unknown`, and FastAPI/Gin
diagnostic-clean draft proposals still have stop-policy reason
`no_proposal_subjects`.

P45-T4 should decide whether this post-fix state is sufficient for bounded
popular-library scraping, still needs another quality pass, or should defer
until a different blocker is resolved.

## Expected Deliverables

- Machine-readable readiness decision fixture for the post-fix P45 state.
- Documentation and DocC mirror for the readiness decision.
- Comparison against P44-T5 and P45-T3 evidence.
- Explicit registry-authority, AI-output, and adapter-execution boundaries.

## Boundaries

- Do not broaden the corpus.
- Do not run another corpus rerun; P45-T3 owns the rerun evidence.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not treat AI output as registry truth.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not add new Workplan tasks.

## Recently Archived

- `P45-T3` Operational MVP Corpus Rerun After AI Draft Shape Fix: PASS on
  2026-06-20.
- `P45-T2` AI Draft Proposal Validation Guard: PASS on 2026-06-20.
- `P45-T1` AI Draft Proposal Subject Identity Fix: PASS on 2026-06-20.

## Validation Expectations

- Validate the readiness fixture with `python3 -m json.tool`.
- Run docs-contract tests covering the readiness decision and current next task.
- Run formatting/lint/whitespace checks scaled to touched files.
