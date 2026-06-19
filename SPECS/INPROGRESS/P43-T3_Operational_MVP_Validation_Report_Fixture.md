# P43-T3 Operational MVP Validation Report Fixture

## Status

Planned.

## Motivation

P43-T2 defines the operational MVP validation plan as a machine-readable
fixture. P43-T3 needs to define the companion report fixture before any real
corpus run starts, so static-only and AI-enabled results can be captured with a
shared vocabulary and without expanding producer authority.

The report shape must make per-repository quality and handoff readiness
reviewable. It should record the same quality dimensions and stop-policy
outcomes as the plan fixture, while preserving that generated output remains
producer-side evidence.

## Goal

Add a versioned operational MVP validation report fixture that records
per-repository draft status, static-only result, optional AI-enabled result,
author-ready verdict, evidence precision notes, quality dimension ratings,
stop-policy outcome, and SpecPM handoff readiness.

## Deliverables

- Machine-readable fixture under the existing operational MVP validation
  fixture layout.
- Linkage to the P43-T2
  `SpecHarvesterOperationalMVPValidationPlan` fixture with a pinned digest.
- GitHub documentation describing the report fixture contract.
- DocC mirror and index/capability/roadmap links.
- Docs-contract regression coverage for fixture identity, plan linkage,
  per-repository result shape, quality dimensions, stop policy, handoff
  readiness, and non-authority boundaries.
- Validation report for this task.

## Fixture Shape

The fixture should include:

- `apiVersion`, `kind`, `schemaVersion`, and producer-side authority metadata.
- `plan` reference to the P43-T2 plan fixture path, digest, kind, and authority.
- Summary counts for repository results, static-only results, AI-enabled
  proposal results, author-ready drafts, quality-hardening needs, and blocked
  repositories.
- Per-repository result records with repository id, ecosystem family,
  expected package-family shape, pinned checkout state, draft status,
  `staticOnlyResult`, optional `aiEnabledResult`, quality dimension ratings,
  author-ready verdict, evidence precision notes, stop-policy outcome, and
  SpecPM handoff readiness.
- Non-authority fields proving that the report fixture is not package
  acceptance, relation acceptance, registry publishing, baseline seeding, AI
  truth, adapter truth, or adapter execution permission.

## Acceptance Criteria

- The report fixture is synthetic or placeholder-based and does not require
  real local checkouts.
- The report fixture references the P43-T2 plan fixture with a pinned digest.
- Per-repository records cover at least the same repository ids as the P43-T2
  plan fixture.
- Static-only and AI-enabled result fields remain distinguishable, and
  AI-enabled output remains proposal-only.
- Quality dimension ids match the P43-T2 plan fixture vocabulary.
- Stop-policy outcomes are machine-readable and compatible with the P43-T2
  shared stop policy.
- Documentation and tests prove the non-authority boundary.

## Non-Goals

- Do not run the real corpus in P43-T3.
- Do not clone, fetch, or inspect external repositories.
- Do not run AI as part of this task.
- Do not enable trusted local adapter execution.
- Do not publish registry metadata.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat AI or adapter output as registry truth.

## Validation Plan

- `python3 -m json.tool` for the report fixture.
- Targeted docs-contract regression tests for the new report fixture.
- Full docs-contract suite.
- `PYTHONPATH=src python -m pytest`.
- `ruff check src tests`.
- `ruff format --check src tests`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`.
- `swift package dump-package`.
- `swift build --target SpecHarvesterDocs`.
- `git diff --check`.
