# P39-T2 Static Plugin Evidence Envelope Fixture

## Motivation

P39-T1 documented the static repository plugin applicability evaluator plan.
Before evaluator logic or CLI surfaces exist, SpecHarvester needs a stable
machine-readable input artifact that describes the bounded static evidence
available for plugin applicability decisions.

The envelope makes evidence availability explicit before any future
`SpecHarvesterRepositoryPluginApplicabilityReport` is derived.

## Goal

Add a machine-readable static plugin evidence envelope fixture and document the
contract.

The fixture should link the P38 plugin registry to the future P39 evaluator by
declaring source identity, evidence paths, SHA-256 digests, evidence kinds,
advisory signals, and authority boundaries.

## Deliverables

- Add `tests/fixtures/repository_plugins/static-evidence-envelope.example.json`.
- Add GitHub-facing documentation for the fixture.
- Add a DocC mirror for the fixture.
- Link the fixture from:
  - static evaluator plan docs;
  - repository plugin subsystem docs;
  - repository plugin applicability report docs;
  - capabilities docs;
  - roadmap docs;
  - DocC root.
- Add regression tests for:
  - fixture identity;
  - registry reference;
  - repository/source identity;
  - safe relative evidence paths;
  - SHA-256 digest format;
  - `evidenceKinds[]`;
  - advisory signals;
  - authority and non-authority statements;
  - current `next.md` state.

## Acceptance Criteria

- The fixture uses a versioned identity such as
  `apiVersion: spec-harvester.repository-plugin-static-evidence/v0`.
- The fixture kind is `SpecHarvesterRepositoryPluginStaticEvidenceEnvelope`.
- The fixture references `SpecHarvesterRepositoryPluginRegistry`.
- The fixture is producer-side evidence only.
- The fixture includes static evidence from:
  - source manifest metadata;
  - `harvest.json`;
  - `workspace-inventory.json`;
  - `repository-profile-detection.json`;
  - public-interface indexes;
  - parser profile decisions;
  - operator labels.
- Every evidence path is relative, normalized, and safe for review.
- Every digest uses `sha256:<64 hex chars>`.
- The fixture describes how it feeds a future
  `SpecHarvesterRepositoryPluginApplicabilityReport`.
- The docs state that this is not plugin execution, not evaluator execution,
  not accepted package truth, and not registry authority.

## Non-Goals

- Do not implement evaluator logic.
- Do not add `repository-plugin-applicability-detect`.
- Do not change `autonomous-candidate-batch`.
- Do not load third-party plugin code.
- Do not execute plugins.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat plugin decisions or evidence envelopes as registry truth.

## Dependencies

- P38-T2 `SpecHarvesterRepositoryPluginRegistry` fixture.
- P38-T3 `SpecHarvesterRepositoryPluginApplicabilityReport` fixture.
- P39-T1 static repository plugin applicability evaluator plan.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'static_plugin_evidence_envelope or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
