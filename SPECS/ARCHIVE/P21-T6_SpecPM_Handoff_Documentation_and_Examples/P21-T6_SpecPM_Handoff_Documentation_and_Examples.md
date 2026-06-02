# P21-T6 — SpecPM Handoff Documentation and Examples

**Status:** In Progress
**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Date:** 2026-06-02
**Stack Base:** `feature/P21-T5-static-viewer-producer-receipt-panels`

## Problem

SpecHarvester can now emit, preflight, and display an evidence-rich generated
candidate bundle. Maintainers still need a single practical handoff guide that
explains the expected bundle shape, review steps, example commands, rejection
signals, and the trust boundary between SpecHarvester and SpecPM.

Without this documentation, generated bundles can be mistaken for accepted
registry sources or reviewers can miss required evidence such as receipt hashes,
validation reports, diagnostics, privacy notes, and human review status.

## Goals

- Add SpecHarvester-facing handoff documentation for generated candidate
  bundles.
- Include example commands for draft generation, preflight, static rendering,
  and review preparation.
- Include compact example snippets for `producer-receipt.json`,
  `validation-report.json`, and `diagnostics.json`.
- Explain the boundary: SpecHarvester produces a candidate, SpecPM validates
  package shape, maintainers approve acceptance, and the public index publishes
  only reviewed sources.
- Link the handoff guide from existing docs indexes.

## Non-Goals

- Do not implement SpecPM-side enforcement or registry acceptance.
- Do not add networked proposal automation.
- Do not change the producer receipt schema or generated bundle layout.
- Do not make generated evidence authoritative without maintainer review.

## Deliverables

- Handoff documentation page under `docs/`.
- Example bundle snippets or fixtures that are safe, compact, and deterministic.
- Updates to docs index/contract tests if required.
- Validation report with exact quality gate results.

## Acceptance Criteria

- Documentation names the required bundle files:
  `specpm.yaml`, `specs/*.spec.yaml`, `producer-receipt.json`,
  `validation-report.json`, and `diagnostics.json`.
- Documentation includes commands for `draft`, `preflight-candidate-bundle`, and
  `render-spec-site`.
- Documentation explicitly states that generated evidence is not automatic
  SpecPM acceptance.
- Documentation describes maintainer review and public index publication
  boundary.
- Existing docs contract tests, lint, format, coverage, Swift manifest, and
  DocC build pass.
