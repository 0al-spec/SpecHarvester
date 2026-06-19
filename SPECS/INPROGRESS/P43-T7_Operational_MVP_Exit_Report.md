# P43-T7 Operational MVP Exit Report

## Status

Planned.

## Motivation

P43-T4 shows the static-only pipeline can produce handoff-ready preview
candidates for xyflow, FastAPI, and Gin. P43-T5 shows the local
OpenAI-compatible provider was unavailable, so the optional AI-enabled
comparison was not measured. P43-T6 translates that state into author-facing
handoff summaries with explicit valid, reviewable, manual-correction, and
do-not-promote categories.

Phase 43 needs a final exit report before broader autonomous popular-library
scraping or any future real adapter execution work. The report must state
whether the current pipeline is ready to expand, needs quality hardening first,
or is blocked until an explicitly approved adapter execution phase.

## Goal

Record a durable operational MVP exit report that selects one Phase 43 exit
decision and explains the rejected alternatives using P43-T4, P43-T5, and
P43-T6 evidence.

The expected decision is `needs_quality_hardening`: static-only output is
useful and author-reviewable, but the AI-enabled comparison was unavailable and
xyflow still has a visible manual-correction caveat. That is not an adapter
execution blocker, but it is also not strong enough evidence to expand directly
to broader autonomous popular-library scraping.

## Deliverables

- Machine-readable operational MVP exit report fixture under the operational
  MVP validation fixture layout.
- Source artifact linkage to P43-T4, P43-T5, and P43-T6 with current SHA-256
  digests.
- Explicit selected decision and rejected alternatives:
  - `needs_quality_hardening`
  - `ready_for_bounded_autonomous_scraping`
  - `blocked_until_adapter_execution`
- Evidence summary covering static-only readiness, provider-unavailable AI
  comparison, author handoff readiness, xyflow manual correction, and
  non-authority boundaries.
- GitHub documentation and DocC mirror for the exit report.
- Index/capability/roadmap/validation-plan links.
- Docs-contract regression coverage for fixture identity, source linkage,
  selected decision, rejected alternatives, and non-authority boundaries.
- Validation report for this task.

## Acceptance Criteria

- The fixture references the committed P43-T4, P43-T5, and P43-T6 fixtures with
  correct digests.
- The fixture records exactly one selected decision and explains why the two
  other decisions were rejected.
- The report clearly separates author-ready preview usefulness from registry
  acceptance or public-index readiness.
- The report records that the current pipeline needs quality hardening before
  broader autonomous popular-library scraping.
- The report records that real adapter execution is not required to explain the
  current Phase 43 result and remains disabled.
- Documentation and tests prove the exit decision and no-authority boundary.
- `SPECS/INPROGRESS/next.md` advances to Phase 43 completion after archive.

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
- Do not treat exit-report output as registry truth.

## Validation Plan

- `python3 -m json.tool` for the exit report fixture.
- Targeted docs-contract regression tests for the exit report fixture.
- Full docs-contract suite.
- `PYTHONPATH=src python -m pytest`.
- `ruff check src tests`.
- `ruff format --check src tests`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`.
- `swift package dump-package`.
- `swift build --target SpecHarvesterDocs`.
- `git diff --check`.
