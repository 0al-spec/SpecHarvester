# Next Task: P53-T4 Mass Corpus Checkout Readiness Gate

**Priority:** P0
**Phase:** Phase 53. Mass Popular Repository Parsing and Candidate Production
**Dependencies:** `P53-T3` Mass Corpus Source Manifest
**Status:** Selected

## Objective

Verify all 100 operator-provided local checkouts against the immutable P53-T3
source manifest. Require presence, clean revision match, safe size, and
resolved local provenance and license evidence before P53-T5 static parsing can
be unlocked.

## Next Step

Run the PLAN command to generate the implementation-ready PRD. This selection
does not create, restore, clone, or fetch repositories; run static parsing;
invoke Codex or another model; or mutate registry truth.

## Recently Archived

- `P53-T1` Mass Corpus Operating Plan: PASS. Structured review found no
  actionable findings, so FOLLOW-UP created no new tasks.
- `P53-T3` Mass Corpus Source Manifest: PASS. It froze 100 new source
  identities and public discovery evidence; all checkout-dependent evidence is
  pending P53-T4 verification.
- `P53-T3` review: no actionable follow-up tasks. The case-insensitive P52
  source-identity check was corrected during review and is covered by tests.
