# P46-T5 Bounded Popular-Library Pilot Author Handoff Summaries

Status: Planned
Phase: Phase 46. Bounded Popular-Library Pilot After AI Draft Hardening
Task: P46-T5
Branch: `feature/P46-T5-bounded-popular-library-pilot-author-handoff-summaries`
Depends on: P46-T4 Bounded Popular-Library Pilot Output Triage

## Problem

P46-T4 classified the pilot outputs, but authors need a concise handoff that
separates reviewable static evidence from unresolved warnings, caveats,
unsupported AI sidecars, and do-not-promote AI drafts.

## Goal

Produce author-facing handoff summaries for all six bounded pilot repositories
without changing registry truth.

## Deliverables

- Machine-readable P46-T5 handoff fixture under
  `tests/fixtures/bounded_popular_library_pilot_author_handoff/`.
- GitHub Markdown and DocC documentation with per-repository author summaries.
- Docs-contract coverage for handoff identity, P46-T4 source artifact linkage,
  per-repository outcomes, separated sidecar classes, no-authority boundaries,
  and current next-task pointer.
- Validation report and archive artifacts for P46-T5.

## Acceptance Criteria

- The handoff references P46-T4 by digest.
- Reviewable static candidates and relation proposals are listed separately
  from AI sidecars.
- Gin and docc2context AI draft sidecars remain do-not-promote.
- xyflow evidence gaps and unsupported enrichment remain visible.
- Authors can see what is reviewable now, what needs manual correction, and
  what must be excluded from promotion.
- P46-T5 does not accept packages or relations, publish registry metadata, seed
  baselines, or remove `preview_only`.
- P46-T5 updates `SPECS/INPROGRESS/next.md` for P46-T6 after archival.

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
- Do not treat handoff output, static output, AI output, or adapter output as
  registry truth.

## Validation Plan

- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the P46-T5 handoff and current next task.
- Run lint, format, and whitespace checks for touched files.
