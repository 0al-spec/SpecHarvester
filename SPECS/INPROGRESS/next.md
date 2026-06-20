# Next Task: P45-T6 Single-Package no_proposal_subjects Policy

**Status:** Selected
**Branch:** `feature/P45-T6-single-package-no-proposal-subjects-policy`
**Phase:** Phase 45. Operational MVP AI Draft Shape Hardening
**Task:** `P45-T6`
**Depends On:** `P45-T5` Selected-Member Role Taxonomy Hardening

## Goal

Define and implement the single-package `no_proposal_subjects` policy for
FastAPI/Gin-style repositories, deciding when a diagnostic-clean zero-subject AI
draft is acceptable, when it should remain warning-level, and what evidence must
be visible before broader scraping.

## Context

P45-T5 resolved the xyflow `selected_member_role_unknown` blocker by normalizing
selected-member role aliases and preserving true unknown role labels as
diagnostics. The remaining Phase 45 readiness blocker is the single-package
AI-draft stop-policy ambiguity:

- FastAPI and Gin can produce diagnostic-clean AI draft proposals;
- those proposals still expose zero selected proposal subjects;
- the stop-policy reason remains `no_proposal_subjects`;
- P45-T6 must decide and encode whether that state is acceptable for stable
  single-package repositories or should continue to block generation.

P45-T7 will rerun the bounded operational MVP corpus after P45-T6, and P45-T8
will record the final Phase 46 readiness decision.

## Expected Deliverables

- Deterministic policy for diagnostic-clean zero-subject single-package AI
  draft proposals.
- Tests proving FastAPI/Gin-style single-package outputs get the intended
  stop-policy decision and reason.
- Documentation explaining when `no_proposal_subjects` is blocking,
  warning-level, or accepted as non-blocking model-loop evidence.
- Validation report and archive artifacts for P45-T6.

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

- `P45-T5` Selected-Member Role Taxonomy Hardening: PASS on 2026-06-20.
- `P45-T4` Post-Fix Readiness Decision for Bounded Popular-Library Scraping:
  PASS on 2026-06-20.
- `P45-T3` Operational MVP Corpus Rerun After AI Draft Shape Fix: PASS on
  2026-06-20.
- `P45-T2` AI Draft Proposal Validation Guard: PASS on 2026-06-20.
- `P45-T1` AI Draft Proposal Subject Identity Fix: PASS on 2026-06-20.

## Validation Expectations

- Run focused package-set AI draft proposal stop-policy tests.
- Run docs-contract tests covering the current next task.
- Run formatting/lint/whitespace checks scaled to touched files.
