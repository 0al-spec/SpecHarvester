# P46-T2 Bounded Popular-Library Pilot Static-Only Run

Status: Planned
Phase: Phase 46. Bounded Popular-Library Pilot After AI Draft Hardening
Task: P46-T2
Branch: `feature/P46-T2-bounded-popular-library-pilot-static-only-run`
Depends on: P46-T1 Bounded Popular-Library Pilot Manifest

## Problem

P46-T1 defined the bounded pilot input contract, but Phase 46 still needs a
real deterministic static-only run before any local model provider can be used.
The static gate must prove that all six pinned local checkouts can be processed
without AI, adapter execution, dependency installation, package-manager
invocation, harvested-code execution, registry publication, or baseline
seeding.

## Goal

Run the P46 bounded popular-library pilot in static-only mode and record durable
evidence for candidates, relations, warnings, preflight state, quality gates,
and non-authority boundaries.

## Deliverables

- Real static-only `autonomous-candidate-batch --skip-ai` output under a
  timestamped `/tmp` run root.
- Machine-readable P46-T2 static-only run fixture under
  `tests/fixtures/bounded_popular_library_pilot_static_only_run/`.
- GitHub Markdown and DocC documentation describing run inputs, results,
  warnings, blockers, and static-only boundaries.
- Docs-contract coverage for run identity, source manifest digest, report
  digest, repository count, candidate/relation counts, no-AI and no-adapter
  boundaries, and current next-task pointer.
- Validation report and archive artifacts for P46-T2.

## Acceptance Criteria

- The run consumes
  `inputs/p46-bounded-popular-library-pilot/repositories.yml`.
- The run uses `autonomous-candidate-batch --skip-ai
  --repository-profile-selection auto`.
- The run records processed, failed, preflight, candidate, relation, warning,
  and quality-gate counts for all six selected repositories.
- AI draft proposals and AI enrichment proposals remain zero.
- No raw prompts, raw provider responses, secrets, or chain-of-thought are
  produced or persisted.
- Trusted local adapter execution remains disabled and no adapter sidecars are
  treated as authority.
- All generated packages and relations remain preview-only review evidence, not
  registry truth.
- P46-T2 updates `SPECS/INPROGRESS/next.md` for P46-T3 after archival.

## Boundaries

- Do not run AI.
- Do not enable trusted local adapter execution.
- Do not run adapter code.
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
- Do not treat static output, AI output, adapter output, or readiness output as
  registry truth.

## Validation Plan

- Parse the source manifest through `spec_harvester source-manifests`.
- Run static-only `autonomous-candidate-batch` with
  `--repository-profile-selection auto`.
- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the P46-T2 run and current next task.
- Run lint, format, and whitespace checks for touched files.
