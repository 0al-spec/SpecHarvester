# P46-T1 Bounded Popular-Library Pilot Manifest

Status: Planned
Phase: Phase 46. Bounded Popular-Library Pilot After AI Draft Hardening
Task: P46-T1
Branch: `feature/P46-T1-bounded-popular-library-pilot-manifest`
Depends on: P45-T8 Targeted-Hardening Readiness Decision

## Problem

P45-T8 approved starting Phase 46 only as a bounded popular-library pilot. The
pilot cannot start from a broad corpus idea or from older dry-run success. It
needs a concrete, pinned, local-first manifest that P46-T2 can run in
static-only mode without clone, fetch, dependency installation, package-manager
invocation, harvested-code execution, or adapter execution.

## Goal

Define the first post-hardening bounded popular-library pilot manifest and
companion fixture from existing corpus-selection policy and available pinned
local checkouts.

## Deliverables

- `inputs/p46-bounded-popular-library-pilot/repositories.yml`.
- Machine-readable manifest fixture under
  `tests/fixtures/bounded_popular_library_pilot_manifest/`.
- GitHub Markdown and DocC documentation describing selected repositories,
  local checkout requirements, ecosystem coverage, exclusion rules, stop
  conditions, and authority boundaries.
- Docs-contract coverage for manifest identity, digest linkage, repository
  count, checkout requirements, stop conditions, and next-task pointer.
- Validation report and archive artifacts for P46-T1.

## Acceptance Criteria

- The manifest is bounded, pinned, local-first, and reproducible.
- Every selected repository has a stable id, repository URL, pinned revision,
  operator-local checkout path, package id, ecosystem labels, selection
  rationale, expected package shape, and stop conditions.
- The manifest requires existing local checkouts and records that missing or
  revision-mismatched checkouts block P46-T2.
- The manifest carries forward Gin `model_evidence_path_unsupported` as Phase
  46 triage context.
- P46-T1 does not run the pilot, run AI, run adapters, accept packages or
  relations, publish registry metadata, seed baselines, or remove
  `preview_only`.
- P46-T1 updates `SPECS/INPROGRESS/next.md` for P46-T2 after archival.

## Boundaries

- Do not run `autonomous-candidate-batch`.
- Do not run AI.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not enable trusted local adapter execution.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output, adapter output, manifest output, or readiness output
  as registry truth.

## Validation Plan

- Parse the source manifest through `spec_harvester source-manifests`.
- Validate the fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the P46-T1 manifest and current next
  task.
- Run lint, format, and whitespace checks for touched files.
