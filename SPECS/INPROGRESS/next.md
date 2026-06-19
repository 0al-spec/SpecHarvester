# Next Task: P43-T2 Operational MVP Validation Plan Fixture

**Status:** Selected
**Branch:** `feature/P43-T2-operational-mvp-validation-plan-fixture`
**Phase:** Phase 43. Operational MVP Validation
**Task:** `P43-T2` Add a machine-readable
`SpecHarvesterOperationalMVPValidationPlan` fixture that records selected
corpus requirements, pinned local checkout policy, run modes, quality
dimensions, stop policy, and non-authority boundaries.

## Motivation

- P43-T1 documented the operational MVP validation plan, but the next step needs
  a stable machine-readable contract that later tasks can validate and consume.
- The validation loop must keep pinned local checkout inputs explicit rather
  than silently cloning, fetching, or treating a mutable repository state as
  trusted evidence.
- Static-only and AI-enabled runs need the same declared quality dimensions and
  stop policy so comparison results are reviewable instead of anecdotal.

## Goal

Add a versioned fixture for `SpecHarvesterOperationalMVPValidationPlan` that can
act as producer-side evidence for the operational MVP validation phase without
accepting packages, publishing registry metadata, or granting AI or adapter
output authority.

## Scope

- Add a fixture under the existing test fixture layout for
  `SpecHarvesterOperationalMVPValidationPlan`.
- Include corpus item fields for repository URL, local checkout path placeholder,
  exact revision placeholder, ecosystem family, expected package-family shape,
  allowed run modes, and stop conditions.
- Include run mode declarations for static-only and AI-enabled validation.
- Include quality dimensions for validity, repository specificity, evidence
  precision, package topology, claim conservatism, author actionability, and
  SpecPM handoff readiness.
- State that the fixture is producer-side evidence and does not create registry
  authority.
- Add docs-contract regression coverage for the fixture shape and boundaries.
- Keep the fixture synthetic or placeholder-based; do not run a real corpus in
  P43-T2.

## Non-Goals

- Do not run the real corpus in P43-T2.
- Do not enable trusted local adapter execution.
- Do not clone or fetch repositories implicitly.
- Do not publish registry metadata, accept packages, accept relations, seed
  baselines, remove `preview_only`, or treat AI output as registry truth.

## Recently Archived

- `P43-T1` Operational MVP Validation Plan was archived with PASS verdict.
