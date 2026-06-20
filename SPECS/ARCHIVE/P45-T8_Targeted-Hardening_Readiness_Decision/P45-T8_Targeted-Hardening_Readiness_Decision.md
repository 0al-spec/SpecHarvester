# P45-T8 Targeted-Hardening Readiness Decision

Status: Planned
Phase: Phase 45. Operational MVP AI Draft Shape Hardening
Task: P45-T8
Branch: `feature/P45-T8-targeted-hardening-readiness-decision`
Depends on: P45-T7 Operational MVP Corpus Rerun After Targeted AI Draft Policy Fixes

## Problem

P45-T7 records that the bounded operational MVP AI draft blockers are resolved,
but it intentionally does not decide whether Phase 46 can start. Phase 45 still
needs a final readiness record that either approves the bounded popular-library
pilot or blocks it with explicit follow-up work.

## Goal

Record the final targeted-hardening readiness decision for Phase 46 using
P45-T7 evidence, while preserving proposal-only authority and no-execution
boundaries.

## Deliverables

- Machine-readable readiness decision fixture under
  `tests/fixtures/operational_mvp_quality_hardening/`.
- GitHub Markdown and DocC documentation for the readiness decision.
- Docs-contract coverage for fixture identity, source artifact digests,
  decision fields, rejected alternatives, remaining warning treatment, and
  authority boundaries.
- Validation report and archive artifacts for P45-T8.

## Acceptance Criteria

- P45-T8 does not run AI and does not rerun the corpus.
- Fixture links to the P45-T7 targeted rerun fixture by digest.
- Decision explicitly states whether Phase 46 bounded popular-library pilot can
  start.
- Decision records why `selected_member_role_unknown` and
  `no_proposal_subjects` no longer block Phase 46.
- Decision records how the remaining Gin `model_evidence_path_unsupported` AI
  enrichment warning is treated.
- Decision preserves proposal-only output, raw prompt/response/
  chain-of-thought non-persistence, and no registry truth mutation.

## Boundaries

- Do not run AI.
- Do not broaden the corpus or begin Phase 46 pilot work.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not treat AI output as registry truth.

## Validation Plan

- Validate the readiness fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the readiness decision and current next
  task.
- Run lint, format, and whitespace checks for touched files.
