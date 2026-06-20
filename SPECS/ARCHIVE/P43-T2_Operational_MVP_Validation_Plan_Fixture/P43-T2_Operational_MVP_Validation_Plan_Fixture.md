# P43-T2 Operational MVP Validation Plan Fixture

## Status

Planned.

## Motivation

P43-T1 defines the operational MVP validation loop in prose. P43-T2 turns that
plan into a stable machine-readable producer-side fixture so later tasks can
generate validation reports, compare static-only and AI-enabled runs, and
preserve no-authority boundaries without inferring them from documentation text.

The fixture must make operator-provided pinned local checkouts explicit. It must
not clone, fetch, or treat mutable repository state as trusted evidence. It also
must keep AI-enabled output and future adapter output as proposal evidence only.

## Goal

Add a versioned `SpecHarvesterOperationalMVPValidationPlan` fixture that records
the selected corpus requirements, pinned local checkout policy, run modes,
quality dimensions, stop policy, and non-authority boundaries for Phase 43.

## Deliverables

- Machine-readable fixture under the existing test fixture layout.
- Docs-contract regression coverage for fixture identity, selected corpus item
  fields, pinned checkout policy, run modes, quality dimensions, stop policy,
  and non-authority boundary.
- GitHub documentation describing the fixture contract.
- DocC mirror and index/capability/roadmap links where the project normally
  exposes new contracts.
- Validation report for this task.

## Fixture Shape

The fixture should include:

- `apiVersion` and `kind` for
  `SpecHarvesterOperationalMVPValidationPlan`.
- `schemaVersion` and producer-side authority metadata.
- Corpus items with repository URL, local checkout path placeholder, exact
  revision placeholder, ecosystem family, expected package-family shape,
  allowed run modes, and stop conditions.
- Run mode declarations for static-only and AI-enabled validation.
- Quality dimensions for validity, repository specificity, evidence precision,
  package topology, claim conservatism, author actionability, and SpecPM handoff
  readiness.
- Stop policy entries for missing pinned checkouts, generation failures,
  validation/preflight failures, authority-confused AI output, evidence
  over-capture, and disabled adapter requirements.
- Explicit booleans or policy fields proving the fixture does not accept
  packages, publish registry metadata, grant AI authority, enable adapter
  execution, or remove `preview_only`.

## Acceptance Criteria

- The fixture is synthetic or placeholder-based and does not require a real
  corpus checkout.
- The fixture records at least three ecosystem families and requires pinned
  local checkouts before any future validation run.
- The static-only and AI-enabled run modes share the declared quality
  dimensions and stop policy.
- The non-authority boundary is machine-readable and covered by tests.
- Documentation and DocC expose the fixture without claiming registry
  acceptance, baseline seeding, or adapter execution.
- Regression tests prove the fixture shape and required boundary vocabulary.

## Non-Goals

- Do not run the real corpus in P43-T2.
- Do not clone, fetch, or inspect external repositories.
- Do not enable trusted local adapter execution.
- Do not run AI as part of this task.
- Do not publish registry metadata.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat AI or adapter output as registry truth.

## Validation Plan

- `python3 -m json.tool` for the fixture.
- Targeted docs-contract regression tests for the new fixture.
- Full docs-contract suite.
- `PYTHONPATH=src python -m pytest`.
- `ruff check src tests`.
- `ruff format --check src tests`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`.
- `swift package dump-package`.
- `swift build --target SpecHarvesterDocs`.
- `git diff --check`.

---
**Archived:** 2026-06-19
**Verdict:** PASS
