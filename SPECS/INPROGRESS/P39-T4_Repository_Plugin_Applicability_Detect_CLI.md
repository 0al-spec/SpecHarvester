# P39-T4 Repository Plugin Applicability Detect CLI

## Motivation

P39-T3 implemented
`spec_harvester.repository_plugin_applicability.evaluate_repository_plugin_applicability`
as a deterministic helper. The helper is testable, but operators and CI still
need a stable command that can read static JSON inputs and write a reviewable
`SpecHarvesterRepositoryPluginApplicabilityReport` artifact.

## Goal

Expose the P39-T3 helper through a deterministic
`repository-plugin-applicability-detect` CLI command that reads a
`SpecHarvesterRepositoryPluginRegistry` JSON file and a
`SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` JSON file, writes a
`SpecHarvesterRepositoryPluginApplicabilityReport` JSON file, and prints a
compact summary.

## Deliverables

- Add a `repository-plugin-applicability-detect` CLI command.
- Accept explicit `--registry`, `--static-evidence-envelope`, and `--out`
  arguments.
- Read only the provided registry and static evidence envelope JSON files.
- Write a deterministic
  `SpecHarvesterRepositoryPluginApplicabilityReport` JSON artifact.
- Print selected/rejected/fallback/blocked/diagnostic counts to stdout.
- Add CLI regression tests for:
  - success path using the P39-T2 fixture;
  - invalid registry or static evidence identity;
  - unsafe evidence path rejection;
  - missing evidence fallback/blocking behavior.
- Update GitHub docs and DocC docs.
- Archive Flow artifacts and update `next.md` to P39-T5.

## Acceptance Criteria

- `python -m spec_harvester repository-plugin-applicability-detect --registry
  <registry.json> --static-evidence-envelope <envelope.json> --out
  <report.json>` exits `0` for valid inputs.
- The output JSON has `apiVersion:
  spec-harvester.repository-plugin-applicability/v0`, `kind:
  SpecHarvesterRepositoryPluginApplicabilityReport`, `schemaVersion: 1`, and
  `authority: producer_plugin_applicability_only`.
- The output report contains selected, rejected, fallback, blocked, summary,
  diagnostics, sidecar boundary, and non-authority fields from the helper.
- The command prints a compact summary including selected, rejected, fallback,
  blocked, and diagnostics counts.
- Invalid input identities and unsafe evidence paths produce non-zero CLI
  failures with actionable error messages.
- The command does not change `autonomous-candidate-batch` behavior.
- The command does not load or execute plugins, read repository source files,
  clone or fetch repositories, install dependencies, invoke package managers,
  execute harvested code, run AI, accept packages or relations, publish
  registry metadata, remove `preview_only`, or treat plugin decisions as
  registry truth.

## Non-Goals

- Do not integrate generated reports into `autonomous-candidate-batch`.
- Do not add auto-detection from repository checkouts.
- Do not execute plugin code.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat plugin decisions as registry truth.

## Dependencies

- P38-T2 `SpecHarvesterRepositoryPluginRegistry`.
- P38-T3 `SpecHarvesterRepositoryPluginApplicabilityReport`.
- P39-T2 `SpecHarvesterRepositoryPluginStaticEvidenceEnvelope`.
- P39-T3 deterministic evaluator helper.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_repository_plugin_applicability_cli.py -q`
- `PYTHONPATH=src pytest tests/test_repository_plugin_applicability_evaluator.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'static_repository_plugin_applicability_evaluator_plan or static_plugin_evidence_envelope or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
