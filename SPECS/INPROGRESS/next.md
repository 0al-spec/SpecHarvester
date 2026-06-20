# Next Task: P43-T4 Operational MVP Static-Only Quality Baseline

**Status:** Selected
**Branch:** `feature/P43-T4-operational-mvp-static-only-quality-baseline`
**Phase:** Phase 43. Operational MVP Validation
**Task:** `P43-T4` Run the operational MVP validation over an operator-provided
pinned local corpus and record the static-only quality baseline for at least
three repositories from different ecosystems without accepting packages or
publishing registry metadata.

## Motivation

- P43-T2 and P43-T3 define the plan and report fixture contracts, but the
  product question needs static-only evidence from real pinned local checkouts.
- The task requires an operator-provided pinned local corpus; SpecHarvester must
  not discover it by fetching or cloning repositories.
- The baseline should cover at least three repositories from different ecosystems.
- Record the baseline without accepting packages or publishing registry metadata.
- Static-only baseline results should establish what the current deterministic
  pipeline can produce before any AI-enabled comparison.
- The run must preserve the operator-provided pinned checkout boundary and must
  not silently clone, fetch, install dependencies, invoke package managers, or
  execute harvested code.

## Goal

Run the operational MVP validation over at least three operator-provided pinned
local repository checkouts from different ecosystems and record a static-only
quality baseline that uses the P43-T3 report shape while keeping all output
producer-side evidence.

## Scope

- Identify at least three available operator-provided pinned local checkouts
  from different ecosystems.
- Record repository URL, local checkout path, exact revision, ecosystem family,
  expected package-family shape, and static-only run status.
- Run only deterministic/static SpecHarvester paths that do not require AI,
  adapter execution, dependency installation, package-manager invocation,
  network discovery, or harvested-code execution.
- Record per-repository quality dimensions, evidence precision notes,
  author-ready verdict, stop-policy outcome, and SpecPM handoff readiness.
- Add docs-contract regression coverage for the static-only baseline artifact
  and boundaries.

## Non-Goals

- Do not run AI in P43-T4.
- Do not enable trusted local adapter execution.
- Do not clone or fetch repositories implicitly.
- Do not install dependencies or invoke package managers.
- Do not publish registry metadata, accept packages, accept relations, seed
  baselines, remove `preview_only`, or treat generated output as registry
  truth.

## Recently Archived

- `P43-T3` Operational MVP Validation Report Fixture was archived with PASS
  verdict.
- `P43-T2` Operational MVP Validation Plan Fixture was archived with PASS
  verdict.
- `P43-T1` Operational MVP Validation Plan was archived with PASS verdict.
