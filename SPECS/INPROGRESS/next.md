# Next Task: P45-T3 Operational MVP Corpus Rerun After AI Draft Shape Fix

**Status:** Selected
**Branch:** `feature/P45-T3-operational-mvp-corpus-rerun-after-ai-draft-shape-fix`
**Phase:** Phase 45. Operational MVP AI Draft Shape Hardening
**Task:** `P45-T3`
**Depends On:** `P45-T2` AI Draft Proposal Validation Guard

## Goal

Re-run the bounded operational MVP corpus after the AI draft shape fix and
compare warning counts, proposal counts, and proposal-only boundaries against
P44-T4.

## Context

P45-T1 cleaned safe AI draft subject identity normalization. P45-T2 added a
deterministic pre-normalization validation guard so genuinely ambiguous provider
output still surfaces before proposal evidence is accepted. P45-T3 should now
run the same bounded corpus shape and record whether the AI draft warnings are
resolved without changing registry truth.

## Expected Deliverables

- Bounded operational MVP corpus rerun using the post-P45-T2 AI draft proposal
  shape.
- Comparison against P44-T4 warning counts, proposal counts, and proposal-only
  AI boundaries.
- Archived validation evidence for the rerun and any remaining known warnings.

## Boundaries

- Do not broaden the corpus.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not treat AI output as registry truth.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not add new Workplan tasks.

## Recently Archived

- `P45-T2` AI Draft Proposal Validation Guard: PASS on 2026-06-20.
- `P45-T1` AI Draft Proposal Subject Identity Fix: PASS on 2026-06-20.

## Validation Expectations

- Run the bounded operational MVP corpus rerun commands selected by the task
  PRD.
- Compare resulting diagnostics and proposal counts against P44-T4.
- Run docs-contract tests if report fixtures, docs, or next-task metadata
  change.
