# P37-T6 Cross-Ecosystem Profile Fixtures

## Motivation

P37-T5 defines a generic repository profile hint vocabulary, but the current
fixture coverage still looks like one generic package-set example. Before
adding ecosystem-specific plugins, SpecHarvester needs cross-ecosystem fixtures
that prove repository profile selection is driven by static repository shape,
not by a hardcoded language or framework rule.

## Goal

Add a small, replayable fixture set for repository profile detection across
multiple repository shapes:

- workspace-shaped repository;
- single-package repository;
- nested-package repository;
- ambiguous multi-signal repository.

The fixtures should remain language- and framework-agnostic at the contract
level while using varied manifest filenames to exercise current generic static
evidence handling.

## Deliverables

- Add four machine-readable repository profile detection fixtures.
- Ensure each fixture is generated from `build_repository_profile_detection`
  expectations and covered by regression tests.
- Document the fixture set in GitHub docs and DocC.
- Link the fixture set from repository profile selection docs, capabilities,
  roadmap, docs index, and DocC root.
- Keep profile decisions and hints producer-side evidence only.
- Archive the task through Flow.

## Acceptance Criteria

- Fixtures exist under `tests/fixtures/repository_profile_detection/`.
- The fixture set includes:
  - `cross-ecosystem-workspace.example.json`;
  - `cross-ecosystem-single-package.example.json`;
  - `cross-ecosystem-nested-package.example.json`;
  - `cross-ecosystem-ambiguous-multi-signal.example.json`.
- Each fixture uses:
  - `apiVersion: spec-harvester.repository-profile-detection/v0`;
  - `kind: SpecHarvesterRepositoryProfileDetection`;
  - `schemaVersion: 1`;
  - `authority: producer_profile_selection_only`.
- Workspace-shaped fixture selects `generic.package_set.v0` with high
  confidence and emits package-set/member/documentation hints.
- Single-package fixture selects `generic.single_package.v0` with high
  confidence.
- Nested-package fixture records nested manifest evidence without selecting a
  high-confidence profile.
- Ambiguous multi-signal fixture falls back to `generic.repository.v0` because
  no single high-confidence profile is selected.
- Documentation explicitly states that these fixtures do not implement
  ecosystem-specific plugins and do not accept packages, accept relations,
  publish registry metadata, remove `preview_only`, or treat profile decisions
  as registry truth.

## Non-Goals

- Do not implement parser/profile plugins for a specific language or framework.
- Do not change repository profile scoring semantics.
- Do not change autonomous candidate batch behavior.
- Do not collect source files, install dependencies, execute harvested code,
  invoke package managers, or run AI.
- Do not treat fixture outcomes as registry acceptance.

## Dependencies

- P37-T1 repository profile selection contract.
- P37-T2 detection fixture format.
- P37-T3 detection CLI/report surface.
- P37-T4 autonomous batch sidecar evidence integration.
- P37-T5 generic profile discovery hints.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_repository_profile_detection.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
