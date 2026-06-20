# Next Task: P45-T7 Operational MVP Corpus Rerun After Targeted AI Draft Policy Fixes

**Status:** Selected
**Branch:** `feature/P45-T7-operational-mvp-rerun-after-targeted-ai-draft-policy-fixes`
**Phase:** Phase 45. Operational MVP AI Draft Shape Hardening
**Task:** `P45-T7`
**Depends On:** `P45-T6` Single-Package no_proposal_subjects Policy

## Goal

Re-run the bounded operational MVP corpus after P45-T5 and P45-T6, comparing
warning codes, diagnostic counts, stop-policy reasons, proposal-only
boundaries, and raw prompt/response/chain-of-thought non-persistence against
P45-T3.

## Context

P45-T5 resolved the xyflow selected-member role ambiguity by normalizing known
role aliases while preserving true unknown-role diagnostics. P45-T6 made
diagnostic-clean zero-subject AI draft output non-blocking only for stable
single-package inventories, while keeping `no_proposal_subjects` blocking for
multi-package and diagnostic-bearing outputs.

P45-T7 should now run the same bounded operational MVP corpus used by P45-T3:

- xyflow;
- FastAPI;
- Gin.

The rerun should verify whether xyflow no longer reports
`selected_member_role_unknown` and FastAPI/Gin no longer block on
`no_proposal_subjects` when their single-package inventory evidence is clean.
P45-T8 will use the P45-T7 evidence to record the final Phase 46 readiness
decision.

## Expected Deliverables

- Bounded operational MVP rerun evidence after P45-T5/P45-T6.
- Comparison fixture or report against P45-T3 warning codes, diagnostic counts,
  stop-policy reasons, proposal counts, proposal-only authority, and privacy
  persistence boundaries.
- Documentation or DocC updates explaining the rerun result.
- Validation report and archive artifacts for P45-T7.

## Boundaries

- Do not broaden the corpus beyond xyflow, FastAPI, and Gin.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not treat AI output as registry truth.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.

## Recently Archived

- `P45-T6` Single-Package no_proposal_subjects Policy: PASS on 2026-06-20.
- `P45-T5` Selected-Member Role Taxonomy Hardening: PASS on 2026-06-20.
- `P45-T4` Post-Fix Readiness Decision for Bounded Popular-Library Scraping:
  PASS on 2026-06-20.
- `P45-T3` Operational MVP Corpus Rerun After AI Draft Shape Fix: PASS on
  2026-06-20.

## Validation Expectations

- Run the bounded operational MVP corpus with the same three repositories.
- Compare P45-T7 outputs against P45-T3 recorded evidence.
- Run docs-contract tests for the rerun report and current next task.
- Run formatting/lint/whitespace checks scaled to touched files.
