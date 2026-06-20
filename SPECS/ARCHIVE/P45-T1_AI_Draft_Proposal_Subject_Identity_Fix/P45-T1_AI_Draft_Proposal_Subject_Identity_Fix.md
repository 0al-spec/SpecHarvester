# P45-T1 AI Draft Proposal Subject Identity Fix

## Status

Archived as PASS on 2026-06-20.

## Motivation

P44-T5 selected `needs_another_quality_pass` before bounded popular-library
scraping because P44-T4 resolved zero AI draft warnings. xyflow and FastAPI
still reported `package_set_id_missing`, while Gin changed to
`excluded_package_unknown`.

The next fix should target producer-side AI draft proposal shape handling, not
adapter execution, registry acceptance, or broader corpus expansion.

## Goal

Fix AI draft proposal subject identity so single-package and package-set
repositories can use deterministic candidate/package-set identity when provider
output omits a stable package-set id or references an unknown excluded package.

## Deliverables

- Narrow producer-side code fix for AI draft proposal subject identity.
- Regression coverage for package-set and single-package proposal shapes.
- Documentation or fixture updates needed to preserve the operational MVP
  warning lineage.
- Validation report for the task.

## Acceptance Criteria

- Package-set AI draft proposal output can resolve the deterministic package-set
  id when the provider omits the package-set id but selected package members are
  known.
- Single-package AI draft proposal output does not report
  `excluded_package_unknown` when the exclusion is only model-side noise and the
  deterministic candidate identity is stable.
- Existing warning diagnostics remain available for genuinely ambiguous or
  unsupported proposal subjects.
- AI output remains proposal-only and is not promoted to registry truth.
- The fix does not broaden the corpus, accept packages or relations, publish
  registry metadata, seed baselines, remove `preview_only`, enable trusted local
  adapter execution, execute harvested code, install dependencies, or invoke
  package managers.

## Validation Plan

- Run focused AI draft proposal tests.
- Run focused autonomous batch or docs-contract tests if fixtures or report
  shapes change.
- Run formatting and lint checks for touched Python files.

## Non-Goals

- Do not run the full bounded operational MVP rerun; that belongs to P45-T3.
- Do not add new Workplan tasks.
- Do not call hosted AI services.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
