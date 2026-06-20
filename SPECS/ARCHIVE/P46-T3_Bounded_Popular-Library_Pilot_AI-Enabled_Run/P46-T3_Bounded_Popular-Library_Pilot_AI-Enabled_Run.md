# P46-T3 Bounded Popular-Library Pilot AI-Enabled Run

Status: Planned
Phase: Phase 46. Bounded Popular-Library Pilot After AI Draft Hardening
Task: P46-T3
Branch: `feature/P46-T3-bounded-popular-library-pilot-ai-enabled-run`
Depends on: P46-T2 Bounded Popular-Library Pilot Static-Only Run

## Problem

P46-T2 proved the static-only gate over the six-repository bounded pilot. The
next question is whether the same pinned corpus can run with the local
OpenAI-compatible provider while preserving proposal-only AI output, zero raw
prompt/response persistence, and no registry authority.

## Goal

Run the P46 bounded popular-library pilot with the local OpenAI-compatible
provider and record comparison evidence against the P46-T2 static-only gate.

## Deliverables

- Real AI-enabled `autonomous-candidate-batch` output under a timestamped
  `/tmp` run root.
- Machine-readable P46-T3 AI-enabled run fixture under
  `tests/fixtures/bounded_popular_library_pilot_ai_enabled_run/`.
- GitHub Markdown and DocC documentation describing run inputs, AI proposal
  counts, token usage, warning classes, comparison with P46-T2, and authority
  boundaries.
- Docs-contract coverage for run identity, source manifest digest, P46-T2
  baseline linkage, no raw prompt/response/chain-of-thought persistence,
  proposal-only AI boundary, no-adapter boundary, and no-registry-authority
  boundary.
- Validation report and archive artifacts for P46-T3.

## Acceptance Criteria

- The run consumes
  `inputs/p46-bounded-popular-library-pilot/repositories.yml`.
- The run uses the local OpenAI-compatible provider and records provider/model
  identity.
- Static candidate and relation counts remain comparable to P46-T2.
- AI draft and enrichment proposal counts, token totals, repair outcomes, and
  warning classes are recorded.
- Raw prompts, raw provider responses, secrets, and chain-of-thought are not
  persisted.
- AI sidecars remain proposal-only and do not update registry truth.
- Trusted local adapter execution remains disabled and no adapter output is
  treated as authority.
- P46-T3 updates `SPECS/INPROGRESS/next.md` for P46-T4 after archival.

## Boundaries

- Do not change the source manifest.
- Do not run outside the six pinned local checkouts.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not enable trusted local adapter execution.
- Do not run adapter code.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output, adapter output, static output, or readiness output as
  registry truth.

## Validation Plan

- Parse the source manifest through `spec_harvester source-manifests`.
- Run AI-enabled `autonomous-candidate-batch` with
  `--repository-profile-selection auto`, the local LM Studio base URL, the
  selected model, and bounded JSON repair.
- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the P46-T3 run/comparison and current
  next task.
- Run lint, format, and whitespace checks for touched files.
