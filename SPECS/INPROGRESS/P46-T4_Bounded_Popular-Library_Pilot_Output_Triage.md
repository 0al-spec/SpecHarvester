# P46-T4 Bounded Popular-Library Pilot Output Triage

Status: Planned
Phase: Phase 46. Bounded Popular-Library Pilot After AI Draft Hardening
Task: P46-T4
Branch: `feature/P46-T4-bounded-popular-library-pilot-output-triage`
Depends on: P46-T3 Bounded Popular-Library Pilot AI-Enabled Run

## Problem

P46-T2 produced a clean static-only candidate layer, while P46-T3 produced a
failed AI proposal layer with mixed warnings and blockers. Before author-facing
handoff summaries can be created, the pilot outputs need explicit triage by
repository and package-set member.

## Goal

Classify static candidates, relation proposals, AI draft sidecars, AI
enrichment sidecars, warnings, blockers, and do-not-promote outputs across the
bounded pilot.

## Deliverables

- Machine-readable P46-T4 output triage fixture under
  `tests/fixtures/bounded_popular_library_pilot_output_triage/`.
- GitHub Markdown and DocC documentation describing valid, reviewable, noisy,
  unsupported, evidence-gap, and do-not-promote classifications.
- Docs-contract coverage for triage identity, source artifact linkage,
  classification counts, repository/member outcomes, no-authority boundaries,
  and current next-task pointer.
- Validation report and archive artifacts for P46-T4.

## Acceptance Criteria

- The triage references P46-T2 and P46-T3 fixtures by digest.
- Static candidate and relation layers remain reviewable producer evidence.
- Failed Gin and docc2context AI draft outputs are classified as
  do-not-promote proposal sidecars.
- xyflow `model_evidence_path_unsupported`, `partial_public_interface_index`,
  and fork-origin caveat remain visible as evidence gaps or promotion blockers.
- Flask, Cupertino, and NavigationSplitView AI draft warnings are classified as
  noisy/reviewable and not registry-promotable without author review.
- The triage does not rerun the pilot, run AI, run adapters, or change registry
  truth.
- P46-T4 updates `SPECS/INPROGRESS/next.md` for P46-T5 after archival.

## Boundaries

- Do not rerun the pilot.
- Do not run AI.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output, static output, adapter output, or triage output as
  registry truth.

## Validation Plan

- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the P46-T4 triage and current next task.
- Run lint, format, and whitespace checks for touched files.
