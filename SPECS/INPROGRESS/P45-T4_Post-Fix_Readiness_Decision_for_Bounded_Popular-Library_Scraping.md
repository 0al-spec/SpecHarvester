# P45-T4 Post-Fix Readiness Decision for Bounded Popular-Library Scraping

**Status:** Planned
**Phase:** Phase 45. Operational MVP AI Draft Shape Hardening
**Task:** `P45-T4`
**Branch:** `feature/P45-T4-post-fix-readiness-decision`
**Depends On:** `P45-T3` Operational MVP Corpus Rerun After AI Draft Shape Fix

## Problem

P44-T5 selected `needs_another_quality_pass` because the bounded operational
MVP rerun passed but resolved zero AI draft warning diagnostics. P45-T1 and
P45-T2 then fixed AI draft proposal subject identity and added a validation
guard, and P45-T3 reran the same pinned xyflow, FastAPI, and Gin corpus.

P45-T3 improved the evidence: the old `package_set_id_missing` and
`excluded_package_unknown` warning class is gone, FastAPI and Gin now have no
AI draft diagnostics, and the AI sidecars remain proposal-only. The result is
still not fully clean: xyflow reports `selected_member_role_unknown`, and the
single-package FastAPI/Gin proposals complete with stop-policy reason
`no_proposal_subjects`.

P45-T4 must record whether that post-fix state is sufficient to start bounded
popular-library scraping, still needs another targeted quality pass, or should
defer on a different blocker.

## Goal

Record a durable, machine-readable readiness decision for the P45 post-fix
state, backed by P44-T5 and P45-T3 evidence, without broadening the corpus or
mutating registry truth.

## Deliverables

- Add a machine-readable readiness fixture:
  `tests/fixtures/operational_mvp_quality_hardening/p45-t4-operational-mvp-post-fix-readiness-decision.example.json`.
- Add GitHub Markdown documentation:
  `docs/OPERATIONAL_MVP_POST_FIX_READINESS_DECISION.md`.
- Add DocC mirror documentation:
  `Sources/SpecHarvester/Documentation.docc/OperationalMVPPostFixReadinessDecision.md`.
- Update documentation indexes/capability/roadmap references.
- Add a docs-contract test proving the fixture, documentation, and boundaries
  stay aligned.
- Write a validation report under `SPECS/INPROGRESS/P45-T4_Validation_Report.md`.

## Decision Criteria

The decision must compare P44-T5 and P45-T3 on these concrete signals:

- Same pinned operational MVP corpus was used.
- Static-only candidate/relation counts still match the P44 baseline.
- P45-T3 AI-enabled run passed with zero repository failures.
- Old identity/unknown-exclusion warning class is resolved across all three
  repositories.
- AI draft warning repository count changed from three repositories to one.
- AI draft warning diagnostic count remains three because xyflow now reports
  `selected_member_role_unknown`.
- FastAPI and Gin are diagnostic-clean but still stop with
  `no_proposal_subjects`.
- AI output remains proposal-only and does not mutate registry truth.
- Raw prompts, raw provider responses, and chain-of-thought are not persisted.

## Expected Decision

Unless implementation evidence contradicts the PRD, P45-T4 should select:

`needs_targeted_ai_draft_quality_pass_before_bounded_popular_library_scraping`

This means bounded popular-library scraping is not approved yet. The blocker is
not adapter execution, registry publication, or baseline seeding; it is the
remaining AI draft quality ambiguity after the shape fix.

## Boundaries

- Do not broaden the corpus.
- Do not run another corpus rerun.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI for this task.
- Do not treat AI output as registry truth.
- Do not treat adapter output as registry truth.
- Do not treat readiness output as registry truth.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not add new Workplan tasks.

## Acceptance Criteria

- The readiness fixture validates as JSON and identifies:
  `SpecHarvesterOperationalMVPPostFixReadinessDecision`,
  `spec-harvester.operational-mvp-post-fix-readiness-decision/v0`, and
  `producer_operational_mvp_post_fix_readiness_decision_only`.
- Source artifact digests for P44-T5 and P45-T3 are checked by tests against
  the current repository files.
- The fixture rejects `ready_for_bounded_popular_library_scraping` and rejects
  `blocked_until_adapter_execution`.
- The fixture records that P45-T3 improved identity warning quality but did not
  make the AI draft layer fully clean.
- Documentation and DocC mirror mention `selected_member_role_unknown`,
  `no_proposal_subjects`, proposal-only AI output, and the registry-authority
  boundaries.
- Docs indexes, capabilities, and roadmap references include the new decision.
- `SPECS/Workplan.md` marks `P45-T4` complete only during ARCHIVE.
- `SPECS/INPROGRESS/next.md` must not invent a new task; if no unfinished task
  exists in this branch, it should state that no next task is selected.

## Validation Plan

- `python3 -m json.tool tests/fixtures/operational_mvp_quality_hardening/p45-t4-operational-mvp-post-fix-readiness-decision.example.json >/dev/null`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'operational_mvp_post_fix_readiness_decision or current_next_task'`
- `ruff check tests/test_docs_contracts.py`
- `ruff format --check tests/test_docs_contracts.py`
- `git diff --check`
