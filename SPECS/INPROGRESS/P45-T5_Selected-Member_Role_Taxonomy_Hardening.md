# P45-T5 Selected-Member Role Taxonomy Hardening

Status: Planned
Phase: Phase 45. Operational MVP AI Draft Shape Hardening
Task: P45-T5
Branch: `feature/P45-T5-selected-member-role-taxonomy-hardening`
Depends on: P45-T4 Post-Fix Readiness Decision for Bounded Popular-Library Scraping

## Problem

P45-T4 kept Phase 46 blocked because the P45-T3 bounded corpus rerun still had
one package-set warning class: xyflow emitted `selected_member_role_unknown`.
The old package-set identity warning class is gone, so the remaining xyflow
issue is specifically role taxonomy ambiguity after provider output is
normalized into proposal evidence.

## Goal

Make selected-member roles deterministic and reviewable by normalizing known
model role aliases into the documented package-set role taxonomy while keeping
unknown roles visible as warning-level diagnostics.

## Deliverables

- Add a selected-member role normalization helper and canonical alias map.
- Preserve `selected_member_role_unknown` for genuinely unsupported model role
  labels.
- Cover both accepted aliases and unsupported roles in focused tests.
- Document canonical roles, accepted aliases, and warning semantics in the AI
  draft proposal contract.
- Record validation evidence for the focused implementation.

## Acceptance Criteria

- Known package-set member-role aliases no longer produce
  `selected_member_role_unknown` after normalization.
- Normalized selected-member records expose only canonical role strings.
- Unsupported role labels still produce `selected_member_role_unknown` and keep
  enough diagnostic detail for author review.
- Existing AI draft proposal behavior remains proposal-only and does not accept
  packages, relations, or registry truth.
- P45-T7 remains responsible for the bounded operational MVP rerun evidence.

## Boundaries

- Do not broaden the corpus.
- Do not run the P45 bounded corpus rerun in this task.
- Do not change author-ready package acceptance rules.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not run trusted local adapters or execute package code.
- Do not suppress unrelated diagnostics such as unsupported evidence paths or
  relation endpoint errors.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_package_set_ai_draft_proposal.py -q`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k current_next_task`
- `ruff check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py`
- `ruff format --check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py`
- `git diff --check`
