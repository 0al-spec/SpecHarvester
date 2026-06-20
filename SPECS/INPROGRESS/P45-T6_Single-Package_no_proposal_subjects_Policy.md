# P45-T6 Single-Package no_proposal_subjects Policy

Status: Planned
Phase: Phase 45. Operational MVP AI Draft Shape Hardening
Task: P45-T6
Branch: `feature/P45-T6-single-package-no-proposal-subjects-policy`
Depends on: P45-T5 Selected-Member Role Taxonomy Hardening

## Problem

P45-T4 left FastAPI and Gin as diagnostic-clean AI draft proposals that still
stop with `no_proposal_subjects`. The generic stop-policy helper treats a clean
proposal with zero subjects as `needs_regeneration`, which is appropriate for
most proposal surfaces but ambiguous for a stable single-package repository
where the deterministic inventory already identifies the package subject.

## Goal

Define and implement a bounded package-set AI draft policy that treats
diagnostic-clean zero-subject proposals as non-blocking only for stable
single-package inventories, while preserving `no_proposal_subjects` for
multi-package package sets, warning/failed proposals, and other producer
surfaces.

## Deliverables

- Package-set AI draft stop-policy context for single-package inventories.
- Focused tests proving:
  - diagnostic-clean zero-subject single-package output stops for author review;
  - multi-package zero-subject output still continues generation with
    `no_proposal_subjects`;
  - warning/error proposals are not accepted solely because they are
    single-package.
- Documentation and DocC updates explaining the single-package exception.
- Validation report and archive artifacts for P45-T6.

## Acceptance Criteria

- The default `stop_policy_summary_from_diagnostics` behavior remains unchanged.
- Package-set AI draft proposals expose a machine-readable zero-subject policy
  decision.
- FastAPI/Gin-style stable single-package proposals no longer block Phase 45
  solely on `no_proposal_subjects` when diagnostics are clean.
- AI output remains proposal-only and does not become registry truth.
- P45-T7 remains responsible for rerun evidence on xyflow, FastAPI, and Gin.

## Boundaries

- Do not broaden the corpus.
- Do not run the P45 bounded corpus rerun in this task.
- Do not change package-set role normalization from P45-T5.
- Do not change package acceptance, relation acceptance, registry publication,
  baseline seeding, or `preview_only`.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not run trusted local adapters or execute package code.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_package_set_ai_draft_proposal.py -q`
- `PYTHONPATH=src python -m pytest tests/test_author_ready_quality_report.py -q -k no_subjects`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py::test_docc_and_github_docs_cover_specpm_shared_fixture_policy -q`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py::test_docc_and_github_docs_cover_author_ready_draft_quality_bar -q`
- `ruff check src/spec_harvester/package_set_ai_draft_proposal.py src/spec_harvester/producer_reports.py tests/test_package_set_ai_draft_proposal.py tests/test_author_ready_quality_report.py tests/test_docs_contracts.py`
- `ruff format --check src/spec_harvester/package_set_ai_draft_proposal.py src/spec_harvester/producer_reports.py tests/test_package_set_ai_draft_proposal.py tests/test_author_ready_quality_report.py tests/test_docs_contracts.py`
- `git diff --check`
