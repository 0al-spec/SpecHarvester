# Next Task: P46-T1 Bounded Popular-Library Pilot Manifest

**Status:** Selected
**Branch:** `feature/P46-T1-bounded-popular-library-pilot-manifest`
**Phase:** Phase 46. Bounded Popular-Library Pilot After AI Draft Hardening
**Task:** `P46-T1`
**Depends On:** `P45-T8` Targeted-Hardening Readiness Decision

## Goal

Define the first post-hardening bounded popular-library pilot manifest from the
existing corpus-selection policy and the P45-T8 readiness decision.

## Context

P45-T8 selected `ready_for_phase46_bounded_popular_library_pilot`. This means
Phase 46 can start, but only as a bounded popular-library pilot. It does not
approve unbounded scraping, package acceptance, relation acceptance, registry
publication, baseline seeding, or trusted local adapter execution.

P46-T1 should define the pilot input contract before any run:

- pinned local checkout requirements;
- multi-ecosystem coverage;
- repository exclusion rules;
- pilot stop conditions;
- static-only evidence gate before any AI-enabled pilot;
- proposal-only AI output boundary;
- carry-forward triage for Gin `model_evidence_path_unsupported`.

## Expected Deliverables

- A bounded pilot source manifest or manifest fixture that names the selected
  repositories, local checkout requirements, revisions, ecosystem coverage, and
  exclusions.
- Documentation explaining pilot scope, stop conditions, static-only-first
  ordering, and no-execution boundaries.
- Docs-contract or fixture coverage for manifest identity, repository bounds,
  checkout requirements, and authority boundaries.
- Validation report and archive artifacts for P46-T1.

## Boundaries

- Do not run the pilot in P46-T1.
- Do not run AI in P46-T1.
- Do not install dependencies, invoke package managers, or execute harvested
  code.
- Do not clone or fetch repositories as part of the manifest task.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat adapter output as registry truth.

## Recently Archived

- `P45-T8` Targeted-Hardening Readiness Decision: PASS on 2026-06-20.
- `P45-T7` Operational MVP Corpus Rerun After Targeted AI Draft Policy Fixes:
  PASS on 2026-06-20.
- `P45-T6` Single-Package no_proposal_subjects Policy: PASS on 2026-06-20.
- `P45-T5` Selected-Member Role Taxonomy Hardening: PASS on 2026-06-20.

## Validation Expectations

- Validate any manifest fixture with `python3 -m json.tool` or an equivalent
  parser for its format.
- Run docs-contract tests for the P46-T1 manifest and current next task.
- Run formatting/lint/whitespace checks scaled to touched files.
