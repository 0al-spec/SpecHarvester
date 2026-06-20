# Next Task: P44-T4 Operational MVP Quality-Hardened Rerun

**Status:** Selected
**Branch:** `feature/P44-T4-operational-mvp-quality-hardened-rerun`
**Phase:** Phase 44. Operational MVP Quality Hardening
**Task:** `P44-T4`
**Depends On:** `P44-T3` Operational MVP Xyflow Interface Caveat Resolution

## Goal

Re-run the bounded operational MVP corpus after the targeted quality-hardening
work and compare static-only and AI-enabled proposal output against the P43
baseline.

## Context

P44-T1 triaged `package_set_id_missing` as an AI proposal shape issue. P44-T2
reviewed proposal-only AI enrichment quality. P44-T3 accepted xyflow's partial
public-interface and fork-origin caveats for bounded rerun evidence while
keeping them registry-promotion blockers.

## Expected Deliverables

- A durable P44-T4 quality-hardened rerun artifact.
- Static-only and AI-enabled result summary for xyflow, FastAPI, and Gin.
- Comparison against the P43 baseline, including warnings, candidate counts,
  proposal-only AI sidecars, and manual-correction caveats.
- Updated docs/test coverage sufficient for the repository docs contract.

## Boundaries

- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not execute harvested repository code.
- Do not install repository dependencies unless an existing command explicitly
  documents that behavior and the validation report records it.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.

## Validation Expectations

- Validate any new machine-readable artifact with `python3 -m json.tool`.
- Run focused docs-contract coverage for the P44-T4 artifact and current
  next-task state.
- Run formatting/lint/test gates scaled to the implementation surface.
