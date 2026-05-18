# P8-T1 - Document Accepted Package Update Lifecycle and Immutability Policy

Branch: `feature/P8-T1-accepted-update-lifecycle-docs`
Review subject: `p8_t1_accepted_update_lifecycle_docs`

## Problem

SpecHarvester can now generate, validate, and promote deterministic candidate
metadata, but there is no explicit policy documenting how accepted package sources
should evolve after publication.

Without a lifecycle definition, teams risk mutating accepted package content or
changing accepted versioned paths without preserving review evidence and auditable
reasoning.

## Goals

- Define the immutability expectation for accepted package versions.
- Distinguish update triggers for upstream source changes versus metadata corrections.
- Define a minimal audit trail schema for accepted version updates and errata.
- Keep the acceptance boundary clear: SpecHarvester prepares updates, SpecPM
  review/merge accepts them.

## Non-Goals

- Changing any promotion or proposal implementation behavior.
- Automating version bump decisions.
- Implementing update proposal tooling for `0al-spec/SpecPM`.
- Changing SpecPM contracts or registry schema in this task.

## Deliverables

- Add a dedicated documentation page describing accepted package lifecycle,
  immutability, and update triggers.
- Document required fields for future update audit automation.
- Reference the policy from key operator/runbook docs (`HOW_IT_WORKS.md`,
  `SPECPM_PROPOSAL_AUTOMATION.md`, and `ARCHITECTURE.md`).
- Add corresponding DocC mirror documentation page.

## Acceptance Criteria

- The docs define accepted package immutability expectations unambiguously.
- The docs separate upstream-driven updates from metadata correction paths.
- The docs list required audit trail fields:
  source revision, evidence digests, old/new package version, changed claims,
  validation status, and reviewer notes.
- The docs preserve SpecPM review/merge as the acceptance boundary.
- `SPECS/Workplan.md` advances P8-T1 to done after archive.

## Validation Plan

- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
