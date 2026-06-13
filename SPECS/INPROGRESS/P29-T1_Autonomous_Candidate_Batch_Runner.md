# P29-T1 Autonomous Candidate Batch Runner

## Motivation

SpecHarvester can already collect, draft, preflight, enrich, and hand off a
single package-set candidate, but operator runs across popular libraries still
require manual command chaining. The MVP needs one safe orchestration surface
that can process a source manifest into reviewable SpecPM preview artifacts and
use a local LM Studio/OpenAI-compatible model for cost-controlled schema-bound
suggestions.

## Goal

Add an autonomous candidate batch runner for local public checkouts. The runner
should create valid starter package artifacts and a summary report, while
preserving the boundary that SpecHarvester output is producer evidence only and
SpecPM remains the registry authority.

## Deliverables

- New CLI command for autonomous candidate batch runs.
- New machine-readable `SpecHarvesterAutonomousCandidateBatchReport` artifact.
- Local LM Studio provider wiring for optional AI draft and AI enrichment
  proposals.
- Offline-safe tests that exercise the runner without requiring a live model.
- Operator documentation and DocC mirror.
- Workplan, roadmap, and Flow archive updates.

## Acceptance Criteria

- The command accepts the existing repository source manifest directory and
  local checkout paths.
- The command runs collect-batch behavior with workspace inventory and
  interface indexes enabled by default.
- The command drafts package-set candidates with a configurable role profile,
  defaulting to `generic_monorepo`.
- The command runs bundle-set preflight for each drafted package set and records
  pass/fail status.
- The command can call a local OpenAI-compatible provider such as LM Studio via
  `--lm-studio-base-url` and `--lm-studio-model`; CI can disable model calls.
- The report records output paths, statuses, candidate/relation counts, author
  ready summaries, AI proposal statuses, and explicit non-authority boundaries.
- The runner does not clone repositories, browse the network except for the
  operator-provided local model endpoint, execute harvested code, install
  dependencies, publish registry metadata, or remove `preview_only`.

## Validation Plan

- Targeted pytest for the new runner and CLI.
- Existing package-set/drafting related tests.
- Full Python test suite with coverage gate if practical.
- `ruff check .`
- `ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
