# P37-T2 Repository Profile Detection Fixture

## Motivation

P37-T1 documented the repository profile selection contract, but the next
implementation steps need a concrete, machine-readable artifact before any
runtime detector or CLI surface is added.

The fixture should make profile selection replayable and reviewable: a reviewer
must be able to see which profiles were considered, why one was selected or
rejected, what fallback applies, which diagnostics were emitted, and which
downstream hints are advisory only.

## Goal

Add a versioned
`SpecHarvesterRepositoryProfileDetection` fixture format that records one
repository profile selection decision without implementing runtime profile
detection.

The fixture must follow the P37-T1 model:

```text
detect candidates -> score evidence -> select or fallback -> record decision
```

## Deliverables

- Add
  `tests/fixtures/repository_profile_detection/generic-package-set.example.json`.
- Document the fixture in `docs/REPOSITORY_PROFILE_SELECTION_CONTRACT.md`.
- Add the same fixture documentation to the DocC mirror.
- Add docs-contract regression coverage for the fixture shape and boundary
  statements.
- Archive the task through Flow.

## Fixture Requirements

The fixture should include:

- `apiVersion: spec-harvester.repository-profile-detection/v0`;
- `kind: SpecHarvesterRepositoryProfileDetection`;
- `schemaVersion: 1`;
- `authority: producer_profile_selection_only`;
- repository identity and source manifest metadata;
- selection mode and override source;
- selected profile id or `null`;
- fallback profile id;
- candidate profiles with confidence, score, evidence paths, reason codes,
  conflicts, and recommended actions;
- rejected profiles and reason codes;
- diagnostics with severity, code, message, and evidence paths;
- non-authority statements;
- advisory downstream hints produced by the selected profile.

## Acceptance Criteria

- The fixture is language- and framework-agnostic.
- The fixture records a successful high-confidence auto-selection and at least
  one rejected lower-confidence candidate.
- The fixture demonstrates advisory workspace/member hints without treating
  them as registry truth.
- The fixture includes explicit non-authority statements that it does not
  clone/fetch repositories, run AI, draft packages, publish registry metadata,
  accept packages or relations, remove `preview_only`, or treat plugin
  decisions as registry truth.
- Regression tests validate the required fields, selected/fallback profile
  relationship, candidate/rejection shape, diagnostics shape, and boundary
  statements.

## Non-Goals

- Do not implement runtime repository profile detection.
- Do not add a CLI/report surface.
- Do not connect profile selection to autonomous candidate batch behavior.
- Do not add a language-specific or FastMCP-specific profile implementation.
- Do not clone/fetch repositories, install dependencies, execute harvested
  code, invoke package managers, run AI, draft packages, publish registry
  metadata, accept packages or relations, remove `preview_only`, or treat AI
  output or plugin decisions as registry truth.

## Dependencies

- P37-T1 repository profile selection contract.
- P36-T1 repository parsing plugin contract.
- P36-T3 plugin-aware source classification hook.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift build --target SpecHarvesterDocs`
