# Next Task: P45-T5 Selected-Member Role Taxonomy Hardening

**Status:** Selected
**Branch:** `feature/P45-T5-selected-member-role-taxonomy-hardening`
**Phase:** Phase 45. Operational MVP AI Draft Shape Hardening
**Task:** `P45-T5`
**Depends On:** `P45-T4` Post-Fix Readiness Decision for Bounded Popular-Library Scraping

## Goal

Resolve the xyflow `selected_member_role_unknown` AI draft blocker by tightening
the selected-member role taxonomy, normalization, and validation/reporting
contract.

## Context

P45-T4 completed the post-fix readiness decision and did not approve Phase 46.
The old `package_set_id_missing` / `excluded_package_unknown` warning class is
resolved, but P45-T3 still left two readiness blockers:

- xyflow reports `selected_member_role_unknown`;
- FastAPI/Gin expose `no_proposal_subjects`.

P45-T5 should address the xyflow role-taxonomy blocker first. P45-T6 will own
the single-package `no_proposal_subjects` policy, P45-T7 will rerun the bounded
operational MVP corpus, and P45-T8 will record the final Phase 46 readiness
decision.

## Expected Deliverables

- Tightened selected-member role taxonomy and normalization/validation behavior.
- Tests proving known package-set member roles no longer remain ambiguous after
  provider output is normalized.
- Documentation or fixture updates explaining the selected-member role boundary
  and warning semantics.
- Validation report and archive artifacts for P45-T5.

## Boundaries

- Do not broaden the corpus.
- Do not run another corpus rerun; P45-T7 owns the rerun evidence.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not treat AI output as registry truth.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.

## Recently Archived

- `P45-T4` Post-Fix Readiness Decision for Bounded Popular-Library Scraping:
  PASS on 2026-06-20.
- `P45-T3` Operational MVP Corpus Rerun After AI Draft Shape Fix: PASS on
  2026-06-20.
- `P45-T2` AI Draft Proposal Validation Guard: PASS on 2026-06-20.
- `P45-T1` AI Draft Proposal Subject Identity Fix: PASS on 2026-06-20.

## Validation Expectations

- Run focused package-set AI draft proposal tests.
- Run docs-contract tests covering the current next task.
- Run formatting/lint/whitespace checks scaled to touched files.
