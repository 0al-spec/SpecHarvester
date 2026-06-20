# Next Task: P46-T2 Bounded Popular-Library Pilot Static-Only Run

**Status:** Selected
**Branch:** `feature/P46-T2-bounded-popular-library-pilot-static-only-run`
**Phase:** Phase 46. Bounded Popular-Library Pilot After AI Draft Hardening
**Task:** `P46-T2`
**Depends On:** `P46-T1` Bounded Popular-Library Pilot Manifest

## Goal

Run the bounded popular-library pilot in static-only mode first, using the
P46-T1 manifest as the complete input contract.

## Context

P46-T1 defined a six-repository, pinned, local-first manifest at
`inputs/p46-bounded-popular-library-pilot/repositories.yml`.

The P46-T2 run should record deterministic candidate, relation, preflight,
warning, and quality-gate evidence for:

- Flask
- Gin
- xyflow
- Cupertino
- NavigationSplitView
- docc2context

This task is the static-only gate before any AI-enabled pilot run. It should
also preserve carry-forward triage for Gin `model_evidence_path_unsupported`
and the xyflow fork-origin caveat.

## Expected Deliverables

- Static-only run output or fixture/report for the bounded pilot.
- Batch summary covering processed repositories, failures, candidates,
  relations, warning classes, and quality-gate state.
- Documentation explaining static-only findings and any blockers for P46-T3.
- Docs-contract or fixture coverage for run identity, source manifest digest,
  repository count, no-AI boundary, no-adapter boundary, and no-registry-authority
  boundary.
- Validation report and archive artifacts for P46-T2.

## Boundaries

- Do not run AI.
- Do not enable trusted local adapter execution or run adapter code.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat adapter output as registry truth.
- Do not treat static pilot output as registry truth.

## Recently Archived

- `P46-T1` Bounded Popular-Library Pilot Manifest: PASS on 2026-06-20.
- `P45-T8` Targeted-Hardening Readiness Decision: PASS on 2026-06-20.
- `P45-T7` Operational MVP Corpus Rerun After Targeted AI Draft Policy Fixes:
  PASS on 2026-06-20.
- `P45-T6` Single-Package no_proposal_subjects Policy: PASS on 2026-06-20.

## Validation Expectations

- Run the static-only pilot from
  `inputs/p46-bounded-popular-library-pilot/repositories.yml`.
- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for the P46-T2 run and current next task.
- Run formatting/lint/whitespace checks scaled to touched files.
