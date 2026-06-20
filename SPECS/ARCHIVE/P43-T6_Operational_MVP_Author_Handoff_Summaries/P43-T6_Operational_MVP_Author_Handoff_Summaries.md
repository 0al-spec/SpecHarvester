# P43-T6 Operational MVP Author Handoff Summaries

## Status

Planned.

## Motivation

P43-T4 proves that the static-only pipeline can produce handoff-ready preview
candidates for xyflow, FastAPI, and Gin. P43-T5 proves that live local
LM Studio AI draft/enrichment sidecars are available, but they remain
proposal-only and must not be treated as registry truth.

Package authors need a concise handoff layer that explains what is valid, what
is reviewable, what needs manual correction, and what should not be promoted.
The handoff must be clear enough for author review while remaining
machine-readable and non-authoritative.

## Goal

Add operational MVP author handoff summaries that translate the P43-T4
static-only baseline and P43-T5 AI comparison state into per-repository author
actions without accepting packages, publishing registry metadata, or treating
the summary as registry truth.

## Deliverables

- Machine-readable author handoff summary fixture under the operational MVP
  validation fixture layout.
- Linkage to the P43-T4 static-only baseline and P43-T5 AI comparison fixtures
  with pinned digests.
- Per-repository handoff records for xyflow, FastAPI, and Gin.
- Handoff categories for `valid`, `reviewable`, `needsManualCorrection`, and
  `doNotPromote`.
- Explicit handling of xyflow's partial public-interface-index caveat and the
  P43-T5 live proposal-only AI state.
- GitHub documentation describing the author handoff summary artifact.
- DocC mirror and index/capability/roadmap links.
- Docs-contract regression coverage for fixture identity, source linkage,
  author categories, per-repository handoff actions, and non-authority
  boundaries.
- Validation report for this task.

## Acceptance Criteria

- The handoff fixture covers the same three repositories as P43-T4/P43-T5.
- The fixture references P43-T4 and P43-T5 with current SHA-256 digests.
- Every repository records what is valid, what is reviewable, what needs manual
  correction, and what should not be promoted.
- The handoff distinguishes static-only readiness from proposal-only AI
  comparison evidence.
- The handoff remains producer-side review evidence and not package acceptance,
  relation acceptance, registry authority, baseline seeding, or `preview_only`
  removal.
- Documentation and tests prove the author-facing categories and no-authority
  boundary.
- `SPECS/INPROGRESS/next.md` advances to P43-T7 after archive.

## Non-Goals

- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not run AI.
- Do not enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested repository code.
- Do not treat handoff output as registry truth.

## Validation Plan

- `python3 -m json.tool` for the handoff summary fixture.
- Targeted docs-contract regression tests for the handoff summary fixture.
- Full docs-contract suite.
- `PYTHONPATH=src python -m pytest`.
- `ruff check src tests`.
- `ruff format --check src tests`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`.
- `swift package dump-package`.
- `swift build --target SpecHarvesterDocs`.
- `git diff --check`.
