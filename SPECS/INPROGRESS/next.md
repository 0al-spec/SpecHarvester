# Next Task: P44-T5 Operational MVP Post-Hardening Readiness Decision

**Status:** Selected
**Branch:** `feature/P44-T5-operational-mvp-post-hardening-readiness-decision`
**Phase:** Phase 44. Operational MVP Quality Hardening
**Task:** `P44-T5`
**Depends On:** `P44-T4` Operational MVP Quality-Hardened Rerun

## Goal

Record the post-hardening readiness decision: proceed to bounded popular-library
scraping, run another targeted quality pass, or defer until adapter execution is
separately approved and implemented.

The decision must explicitly consider bounded popular-library scraping.
It must also decide whether SpecHarvester needs another quality pass or should
defer until adapter execution is separately approved.

## Context

P44-T4 reran the bounded operational MVP corpus after P44-T1 through P44-T3.
Both static-only and AI-enabled reruns passed, but AI draft warning ambiguity
was not fully resolved: xyflow and FastAPI still report `package_set_id_missing`,
and Gin now reports `excluded_package_unknown`.

## Expected Deliverables

- A durable P44-T5 readiness-decision artifact.
- Explicit decision among proceed, another quality pass, or defer.
- Evidence references to P43-T7 and P44-T1 through P44-T4.
- Clear handling of xyflow caveats, AI proposal-only status, unresolved draft
  warnings, and adapter-execution absence.
- Updated docs/test coverage sufficient for the repository docs contract.

## Boundaries

- Do not run another corpus batch.
- Do not call hosted AI services or rerun local AI.
- Do not clone or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested code.
- Do not enable trusted local adapter execution or run adapter code.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat readiness output as registry truth.

## Validation Expectations

- Validate any new machine-readable artifact with `python3 -m json.tool`.
- Run focused docs-contract coverage for the P44-T5 artifact and current
  next-task state.
- Run formatting/lint/test gates scaled to the implementation surface.
