# P43-T4 Operational MVP Static-Only Quality Baseline

## Status

Planned.

## Motivation

P43-T2 and P43-T3 define the operational MVP validation plan and report
contract. P43-T4 needs to replace placeholder blocked results with real
static-only evidence from operator-provided pinned local checkouts, while still
preserving the producer-side non-authority boundary.

The goal is to answer what the deterministic pipeline can prove before any
AI-enabled comparison, adapter execution, package acceptance, or registry
publishing is considered.

## Goal

Run the operational MVP validation over at least three operator-provided pinned
local repository checkouts from different ecosystems and record a static-only
quality baseline using the P43-T3 report shape.

## Deliverables

- Machine-readable static-only baseline fixture under the operational MVP
  validation fixture layout.
- Recorded local checkout paths, repository URLs, exact revisions, ecosystem
  families, and expected package-family shapes for at least three repositories.
- Per-repository static-only run results with validity, repository specificity,
  evidence precision, package topology, claim conservatism, author
  actionability, and SpecPM handoff readiness ratings.
- GitHub documentation describing the static-only baseline artifact, observed
  corpus, results, and stop-policy outcomes.
- DocC mirror and index/capability/roadmap links.
- Docs-contract regression coverage for fixture identity, pinned corpus,
  static-only result status, quality dimensions, non-authority boundaries, and
  next-task handoff.
- Validation report for this task.

## Corpus Boundary

The corpus must be operator-provided and already present on disk. SpecHarvester
must not discover it by cloning, fetching, package-manager invocation, or
network repository search.

Each selected repository record should include:

- repository id and URL;
- local checkout path;
- exact 40-hex revision;
- clean or dirty checkout state;
- ecosystem family;
- expected package-family shape;
- static-only validation status;
- any downgrade or stop-policy condition.

## Static-Only Baseline Shape

The fixture should include:

- `apiVersion`, `kind`, `schemaVersion`, and producer-side authority metadata.
- Linkage to the P43-T2 plan fixture and the P43-T3 report fixture.
- Summary counts for selected repositories, verified pinned checkouts,
  static-only runs, author-ready drafts, quality-hardening needs, blocked
  repositories, and SpecPM handoff readiness.
- Per-repository result records with pinned checkout state, static-only result,
  AI-enabled placeholder result, quality dimension ratings, evidence precision
  notes, stop-policy outcome, and SpecPM handoff readiness.
- Non-authority fields proving that the baseline does not accept packages,
  accept relations, publish registry metadata, seed baselines, remove
  `preview_only`, run AI, enable trusted local adapter execution, or treat
  generated output as registry truth.

## Acceptance Criteria

- At least three repositories from different ecosystem families are recorded.
- Every selected repository uses an operator-provided local checkout and exact
  revision.
- Static-only results are recorded without AI invocation, adapter execution,
  dependency installation, package-manager invocation, clone/fetch, or
  harvested-code execution.
- The baseline fixture is machine-readable and compatible with the P43-T3
  report vocabulary.
- Quality dimension ratings and stop-policy outcomes are explicit for every
  repository.
- Documentation and tests prove the producer-side non-authority boundary.
- `SPECS/INPROGRESS/next.md` advances to P43-T5 after archive.

## Non-Goals

- Do not run AI in P43-T4.
- Do not enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested repository code.
- Do not publish registry metadata.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat generated output as registry truth.

## Validation Plan

- `python3 -m json.tool` for the baseline fixture.
- Targeted docs-contract regression tests for the static-only baseline fixture.
- Full docs-contract suite.
- `PYTHONPATH=src python -m pytest`.
- `ruff check src tests`.
- `ruff format --check src tests`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`.
- `swift package dump-package`.
- `swift build --target SpecHarvesterDocs`.
- `git diff --check`.

---
**Archived:** 2026-06-20
**Verdict:** PASS
