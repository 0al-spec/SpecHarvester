# P38-T4 Repository Plugin Batch Integration

## Motivation

P38-T2 added a machine-readable repository plugin registry fixture and P38-T3
added an applicability report fixture. The autonomous candidate batch path
still does not surface those plugin decisions in its batch artifacts, so a
reviewer cannot see which repository plugin contracts would apply to a
candidate run.

## Goal

Connect repository plugin registry and applicability output to autonomous
candidate batch as sidecar producer evidence, without executing plugins or
changing existing parser profile and repository profile behavior.

## Deliverables

- Add an autonomous candidate batch input option for repository plugin
  applicability evidence.
- Copy or reference the applicability report as batch sidecar producer evidence
  in a deterministic output location.
- Add the sidecar reference to the autonomous batch report so downstream review
  can discover the evidence.
- Preserve existing parser profile and repository profile behavior.
- Add docs and DocC updates for the batch integration boundary.
- Add regression coverage for sidecar evidence emission, artifact identity,
  copied digest/reference shape, and non-authority statements.
- Archive the task through Flow.

## Acceptance Criteria

- `autonomous-candidate-batch` can receive an optional
  `SpecHarvesterRepositoryPluginApplicabilityReport` JSON input.
- When provided, the batch output contains a sidecar artifact under a stable
  `reports/repository-plugin-applicability/` path.
- The autonomous batch report references the sidecar artifact with:
  - path;
  - SHA-256 digest;
  - `apiVersion`;
  - `kind`;
  - `authority`;
  - selected/rejected/fallback/blocked counts.
- The integration validates the report identity before recording it.
- Existing default batch behavior is unchanged when no plugin applicability
  input is provided.
- The report remains producer-side sidecar evidence and is not treated as
  package truth, relation truth, parser profile truth, repository profile
  truth, AI truth, or SpecPM registry truth.

## Non-Goals

- Do not implement plugin execution.
- Do not load third-party plugin code.
- Do not implement runtime plugin applicability evaluation.
- Do not change parser profile behavior.
- Do not change repository profile scoring.
- Do not run package managers.
- Do not install dependencies.
- Do not invoke AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat plugin decisions as registry truth.

## Dependencies

- P38-T2 `SpecHarvesterRepositoryPluginRegistry` fixture.
- P38-T3 `SpecHarvesterRepositoryPluginApplicabilityReport` fixture.
- Existing autonomous candidate batch report and docs.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin or autonomous_candidate_batch or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
