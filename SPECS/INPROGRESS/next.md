# Next Task: P44-T1 Operational MVP Warning Triage

**Status:** Selected
**Branch:** `feature/P44-T1-operational-mvp-warning-triage`
**Phase:** Phase 44. Operational MVP Quality Hardening
**Task:** `P44-T1`
**Depends On:** `P43-T7` Operational MVP Exit Report

## Goal

Triage the P43-T5 `package_set_id_missing` draft warnings for xyflow, FastAPI,
and Gin, then record whether each warning is caused by missing draft context,
package-set identity drift, AI proposal shape, or an expected producer-side
boundary.

## Context

Phase 43 closed with `needs_quality_hardening`. The live LM Studio run proved
that proposal-only AI enrichment works over the pinned operational MVP corpus,
but all three repositories still reported `package_set_id_missing` draft
warnings. Before broader bounded popular-library scraping, the warning cause
needs to be explicit and reviewable.

## Expected Deliverables

- A durable P44-T1 warning triage artifact or documentation page that references
  the P43-T5 AI-enabled comparison and P43-T7 exit report.
- Per-repository classification for xyflow, FastAPI, and Gin.
- Clear follow-up guidance for warnings that require generator changes,
  proposal-quality review, package-set identity repair, or no code change.
- Updated docs/test coverage sufficient for the repository docs contract.

## Boundaries

- Do not clone or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested code.
- Do not call hosted AI services.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not enable trusted local adapter execution or run adapter code.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat AI output, adapter output, or warning triage output as registry
  truth.

## Validation Expectations

- Validate any new machine-readable artifact with `python3 -m json.tool`.
- Run the focused docs-contract test that covers the new P44-T1 artifact and
  current next-task state.
- Run formatting/lint/test gates scaled to the implementation surface.
