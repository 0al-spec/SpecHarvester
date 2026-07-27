# Next Task: P53-T6 Codex Spark Wave 1

**Priority:** P0
**Phase:** Phase 53. Mass Popular Repository Parsing and Candidate Production
**Dependencies:** `P53-T5` Mass Corpus Static-Only Gate
**Status:** In Progress
**Started:** 2026-07-27
**Branch:** feature/p53-t6-codex-spark-wave-1

## Objective

Run only repositories 1-25 through the existing P53 Codex Spark campaign path.
Enforce two-worker concurrency, per-source and campaign budgets, checkpointed
resume, schema validation, bounded retries, and the wave stop policy.

## Next Step

After wave 1 completes, manually review at least five candidates and record the
P53-T7 scale-out decision before any wave-2 work begins.

## Recently Archived

- `P53-T5` Mass Corpus Static-Only Gate: PASS. All 100 pinned local checkouts
  produced deterministic preview evidence with zero failures; AI and execution
  surfaces remained disabled.

- `P53-T1` Mass Corpus Operating Plan: PASS. Structured review found no
  actionable findings, so FOLLOW-UP created no new tasks.
- `P53-T3` Mass Corpus Source Manifest: PASS. It froze 100 new source
  identities and public discovery evidence; all checkout-dependent evidence is
  pending P53-T4 verification.
- `P53-T3` review: no actionable follow-up tasks. The case-insensitive P52
  source-identity check was corrected during review and is covered by tests.
