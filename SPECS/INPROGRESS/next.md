# Next Task: P53-T8 Codex Spark Wave 2

**Priority:** P0
**Phase:** Phase 53. Mass Popular Repository Parsing and Candidate Production
**Dependencies:** `P53-T7` Wave-1 Quality Review and Scale-Out Decision (`unlock_p53_t8`)
**Status:** In Progress
**Started:** 2026-07-28
**Branch:** feature/p53-t8-codex-spark-wave-2

## Objective

Run Codex 5.3 Spark only for the 25 manifest-pinned repositories at positions
26-50 after revalidating their static evidence and revisions.

## Next Step

Persist proposal-only receipts, checkpoint state, and aggregate metrics for
P53-T9. Do not process positions 1-25 or 51-100, accept packages, or modify
registry truth.

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
