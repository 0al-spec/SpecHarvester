# Next Task: P44-T2 Operational MVP AI Proposal Quality Review

**Status:** Selected
**Branch:** `feature/P44-T2-operational-mvp-ai-proposal-quality-review`
**Phase:** Phase 44. Operational MVP Quality Hardening
**Task:** `P44-T2`
**Depends On:** `P44-T1` Operational MVP Warning Triage

## Goal

Review the P43-T5 proposal-only AI enrichment artifacts for xyflow, FastAPI,
and Gin, then classify useful suggestions, noisy suggestions, unsupported
claims, evidence gaps, and do-not-promote output before any broader scraping
quality baseline uses AI sidecars.

## Context

P44-T1 classified the shared `package_set_id_missing` draft warning as an AI
proposal shape issue, not source checkout identity drift. AI enrichment still
completed for all three repositories and remains available as proposal-only
author review evidence. P44-T2 reviews that proposal quality without applying
the proposals to accepted SpecPM truth.

## Expected Deliverables

- A durable P44-T2 AI proposal quality review artifact or documentation page
  that references P43-T5 and P44-T1.
- Per-repository quality classification for xyflow, FastAPI, and Gin.
- Follow-up guidance for proposal issues that need generator changes,
  evidence tightening, author review, or do-not-promote handling.
- Updated docs/test coverage sufficient for the repository docs contract.

## Boundaries

- Do not clone or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested code.
- Do not call hosted AI services or rerun local AI.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not enable trusted local adapter execution or run adapter code.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat AI output, adapter output, or proposal-quality review output as
  registry truth.

## Validation Expectations

- Validate any new machine-readable artifact with `python3 -m json.tool`.
- Run the focused docs-contract test that covers the new P44-T2 artifact and
  current next-task state.
- Run formatting/lint/test gates scaled to the implementation surface.
