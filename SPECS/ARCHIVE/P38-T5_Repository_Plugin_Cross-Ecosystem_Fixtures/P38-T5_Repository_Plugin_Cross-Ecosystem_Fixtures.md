# P38-T5 Repository Plugin Cross-Ecosystem Fixtures

## Motivation

P38-T2 through P38-T4 define the repository plugin registry fixture,
applicability report fixture, and autonomous batch sidecar integration. The
current examples still center on one generic workspace shape. That leaves a
risk that later implementation work accidentally overfits plugin applicability
contracts to a single repository layout.

## Goal

Add static cross-ecosystem repository plugin applicability fixtures that cover
several repository shapes while keeping the subsystem language- and
framework-agnostic.

## Deliverables

- Add a fixture directory for cross-ecosystem repository plugin applicability
  examples.
- Cover at least:
  - manifest-backed single-package repository;
  - workspace or multi-package repository;
  - documentation-heavy repository;
  - nested package roots;
  - ambiguous mixed layout.
- Keep fixture decisions producer-side and review-only.
- Add docs and DocC pages describing the fixture matrix and non-authority
  boundary.
- Add regression coverage for fixture identity, summary counts, decision sets,
  non-authority statements, and documentation links.
- Archive the task through Flow.

## Acceptance Criteria

- Each fixture is valid JSON and declares:
  - `apiVersion: spec-harvester.repository-plugin-applicability/v0`;
  - `kind: SpecHarvesterRepositoryPluginApplicabilityReport`;
  - `schemaVersion: 1`;
  - `authority: producer_plugin_applicability_only`.
- Fixtures cover selected, rejected, fallback, and blocked decisions across the
  matrix.
- Each selected plugin has all required declared input evidence kinds available
  in the fixture's `staticEvidence.evidenceKinds[]`.
- Each fixture includes `nonAuthorityStatements[]` that preserve the no
  execution, no network, no package manager, no AI, no acceptance, and no
  registry-truth boundary.
- Docs explain that these are static producer-side fixture examples, not plugin
  execution and not ecosystem-specific normative behavior.

## Non-Goals

- Do not implement plugin execution.
- Do not load third-party plugin code.
- Do not implement runtime plugin discovery or selection.
- Do not clone or fetch repositories.
- Do not run package managers.
- Do not install dependencies.
- Do not execute harvested code.
- Do not invoke AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat plugin decisions as registry truth.

## Dependencies

- P38-T2 `SpecHarvesterRepositoryPluginRegistry` fixture.
- P38-T3 `SpecHarvesterRepositoryPluginApplicabilityReport` fixture.
- P38-T4 autonomous candidate batch sidecar integration.

## Validation Plan

- `python3 -m json.tool` for each new fixture.
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin_cross_ecosystem or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
