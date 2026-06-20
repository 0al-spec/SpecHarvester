# Next Task: P45-T1 AI Draft Proposal Subject Identity Fix

**Status:** Selected
**Branch:** `feature/P45-T1-ai-draft-proposal-subject-identity-fix`
**Phase:** Phase 45. Operational MVP AI Draft Shape Hardening
**Task:** `P45-T1`
**Depends On:** `P44-T5` Operational MVP Post-Hardening Readiness Decision

## Goal

Fix AI draft proposal subject identity so single-package and package-set
repositories no longer produce `package_set_id_missing` or
`excluded_package_unknown` warnings when deterministic package-set draft evidence
already has stable candidate identity.

## Context

P44-T5 selected `needs_another_quality_pass` before bounded popular-library
scraping. P44-T4 passed, but resolved zero AI draft warnings: xyflow and FastAPI
still reported `package_set_id_missing`, and Gin changed to
`excluded_package_unknown`.

## Expected Deliverables

- A narrow producer-side fix for AI draft proposal subject identity.
- Regression coverage for package-set and single-package bounded corpus shapes.
- Documentation or fixture updates needed to preserve the operational MVP
  warning lineage.

## Boundaries

- Do not broaden the corpus.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not treat AI output as registry truth.

## Validation Expectations

- Run focused tests for AI draft proposal subject identity.
- Run docs-contract tests if documentation or fixtures change.
- Run formatting/lint/test gates scaled to the implementation surface.
