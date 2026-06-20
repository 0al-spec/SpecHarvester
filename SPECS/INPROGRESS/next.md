# Next Task: P43-T5 Operational MVP AI-Enabled Comparison

**Status:** Selected
**Branch:** `feature/P43-T5-operational-mvp-ai-enabled-comparison`
**Phase:** Phase 43. Operational MVP Validation
**Task:** `P43-T5` Run the AI-enabled comparison over the same pinned corpus
when a local OpenAI-compatible provider is available, recording deltas and
warning when AI output stays proposal-only.

## Motivation

- P43-T4 records the static-only quality baseline over the operator-provided
  pinned local corpus.
- The AI-enabled comparison should use the same pinned corpus so deltas are
  attributable to proposal-only AI assistance rather than corpus drift.
- AI output must remain proposal-only and must not become registry truth,
  package acceptance, relation acceptance, or baseline seeding.
- If no local OpenAI-compatible provider is available, the task should record a
  clear skipped or unavailable comparison instead of silently changing provider
  policy.

## Goal

Run or explicitly gate the AI-enabled operational MVP comparison over the same
xyflow, FastAPI, and Gin pinned local corpus used by P43-T4, then record
per-repository deltas against the static-only baseline while preserving the
proposal-only and non-authority boundary.

## Scope

- Reuse the P43-T4 pinned corpus and static-only baseline artifact.
- Detect whether a local OpenAI-compatible provider is available for the
  configured comparison.
- When available, run AI-enabled proposal mode without accepting packages,
  publishing registry metadata, seeding baselines, removing `preview_only`, or
  treating AI output as registry truth.
- When unavailable, record provider-unavailable evidence and keep comparison
  output explicit rather than pretending that AI ran.
- Record per-repository deltas, warnings, proposal-only authority, stop-policy
  outcomes, and SpecPM handoff implications.
- Add docs-contract regression coverage for the comparison artifact and
  boundaries.

## Non-Goals

- Do not enable trusted local adapter execution.
- Do not run adapter code.
- Do not clone or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested repository code.
- Do not publish registry metadata.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat AI output as registry truth.

## Recently Archived

- `P43-T4` Operational MVP Static-Only Quality Baseline was archived with PASS
  verdict.
- `P43-T3` Operational MVP Validation Report Fixture was archived with PASS
  verdict.
- `P43-T2` Operational MVP Validation Plan Fixture was archived with PASS
  verdict.
