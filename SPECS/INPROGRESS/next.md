# Next Task: P45-T8 Targeted-Hardening Readiness Decision

**Status:** Selected
**Branch:** `feature/P45-T8-targeted-hardening-readiness-decision`
**Phase:** Phase 45. Operational MVP AI Draft Shape Hardening
**Task:** `P45-T8`
**Depends On:** `P45-T7` Operational MVP Corpus Rerun After Targeted AI Draft Policy Fixes

## Goal

Record the final targeted-hardening readiness decision for Phase 46 using the
P45-T7 bounded corpus rerun evidence.

## Context

P45-T7 reran the same bounded operational MVP corpus as P45-T3:

- xyflow;
- FastAPI;
- Gin.

The P45-T7 AI-enabled batch passed with 3 processed repositories and 0 failed
repositories. The previously blocking AI draft signals are resolved:

- xyflow no longer reports `selected_member_role_unknown`;
- FastAPI no longer blocks on `no_proposal_subjects`; its only draft warning is
  `ai_json_repair_needed`, and successful repair is non-blocking;
- Gin no longer blocks on `no_proposal_subjects`.

The remaining warning is outside AI draft selection: Gin AI enrichment reports
`model_evidence_path_unsupported`. P45-T8 must decide whether that warning is
non-blocking for starting Phase 46 bounded popular-library pilot work or whether
another targeted hardening task is required.

## Expected Deliverables

- A machine-readable targeted-hardening readiness decision fixture.
- GitHub Markdown and DocC documentation explaining the decision.
- Docs-contract coverage for the fixture identity, P45-T7 evidence linkage,
  decision fields, rejected alternatives, and authority boundaries.
- Validation report and archive artifacts for P45-T8.

## Boundaries

- Do not run AI for P45-T8; use P45-T7 evidence.
- Do not broaden the corpus or start Phase 46 work inside P45-T8.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not treat AI output as registry truth.
- Preserve proposal-only output boundaries and raw prompt/response/
  chain-of-thought non-persistence.

## Recently Archived

- `P45-T7` Operational MVP Corpus Rerun After Targeted AI Draft Policy Fixes:
  PASS on 2026-06-20.
- `P45-T6` Single-Package no_proposal_subjects Policy: PASS on 2026-06-20.
- `P45-T5` Selected-Member Role Taxonomy Hardening: PASS on 2026-06-20.
- `P45-T4` Post-Fix Readiness Decision for Bounded Popular-Library Scraping:
  PASS on 2026-06-20.

## Validation Expectations

- Validate the readiness fixture with `python3 -m json.tool`.
- Run docs-contract tests for the readiness decision and current next task.
- Run formatting/lint/whitespace checks scaled to touched files.
