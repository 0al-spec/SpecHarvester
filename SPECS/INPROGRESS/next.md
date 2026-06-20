# Next Task: P44-T3 Operational MVP Xyflow Interface Caveat Resolution

**Status:** Selected
**Branch:** `feature/P44-T3-operational-mvp-xyflow-interface-caveat-resolution`
**Phase:** Phase 44. Operational MVP Quality Hardening
**Task:** `P44-T3`
**Depends On:** `P44-T2` Operational MVP AI Proposal Quality Review

## Goal

Resolve or explicitly accept the xyflow partial `PublicInterfaceIndex` and
fork-origin caveats from P43-T4/P43-T6 so package-set handoff can distinguish
real interface gaps from acceptable parser coverage limits.

## Context

P44-T1 classified the shared AI draft warning as an AI proposal shape issue.
P44-T2 reviewed AI enrichment quality and kept `xyflow.workspace`
do-not-promote until author review. The remaining xyflow-specific blocker is
manual-correction context around partial public-interface evidence and operator
checkout fork origin.

## Expected Deliverables

- A durable P44-T3 xyflow caveat resolution artifact or documentation page.
- Explicit decision for partial `PublicInterfaceIndex`: resolved, accepted, or
  deferred with reason.
- Explicit decision for fork-origin caveat: acceptable review input, blocker,
  or deferred with reason.
- Updated docs/test coverage sufficient for the repository docs contract.

## Boundaries

- Do not clone or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested code.
- Do not call hosted AI services or rerun local AI.
- Do not enable trusted local adapter execution or run adapter code.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat caveat-resolution output as registry truth.

## Validation Expectations

- Validate any new machine-readable artifact with `python3 -m json.tool`.
- Run the focused docs-contract test that covers the new P44-T3 artifact and
  current next-task state.
- Run formatting/lint/test gates scaled to the implementation surface.
