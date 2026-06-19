# P39-T5 Repository Plugin Applicability Batch Integration

## Motivation

P39-T3 added the deterministic repository plugin applicability helper and
P39-T4 exposed it through `repository-plugin-applicability-detect`.
`autonomous-candidate-batch` can already copy an explicit
`--repository-plugin-applicability` sidecar report, but it cannot yet generate
that report from static evaluator inputs as an opt-in batch step.

## Goal

Integrate static evaluator output into `autonomous-candidate-batch` as an
explicit opt-in sidecar path, while preserving explicit
`--repository-plugin-applicability` as the highest-precedence input and keeping
the resulting report producer-side evidence only.

## Deliverables

- Add explicit autonomous batch CLI options for:
  - repository plugin registry JSON;
  - static evidence envelope JSON.
- Generate a repository plugin applicability report only when both opt-in inputs
  are provided and no explicit `--repository-plugin-applicability` sidecar is
  provided.
- Preserve explicit `--repository-plugin-applicability` precedence over any
  auto-generated report path.
- Store the generated report under the existing
  `reports/repository-plugin-applicability/repository-plugin-applicability-report.json`
  sidecar output location.
- Keep sidecar metadata `appliedToDrafting: false` and
  `registryAuthority: false`.
- Add regression tests covering:
  - default behavior remains `not_provided`;
  - opt-in generated report is recorded;
  - explicit sidecar wins when both explicit and auto inputs are provided;
  - invalid auto-detection input returns a structured failure.
- Update GitHub docs and DocC docs.
- Archive Flow artifacts and update `next.md` to P39-T6.

## Acceptance Criteria

- `autonomous-candidate-batch` defaults to no generated plugin applicability
  report.
- Passing both auto inputs generates and records a
  `SpecHarvesterRepositoryPluginApplicabilityReport` sidecar.
- Passing only one auto input fails with an actionable message.
- Passing `--repository-plugin-applicability` still records the explicit report
  and ignores auto-generation inputs.
- Generated sidecar records include selected/rejected/fallback/blocked summary
  counts, diagnostic codes, report digest, `appliedToDrafting: false`, and
  `registryAuthority: false`.
- The batch path does not load or execute plugins, read repository source
  files, clone or fetch repositories, install dependencies, invoke package
  managers, execute harvested code, run AI for applicability detection, accept
  packages or relations, publish registry metadata, remove `preview_only`, or
  treat plugin decisions as registry truth.

## Non-Goals

- Do not make plugin applicability automatic by default.
- Do not override explicit `--repository-plugin-applicability`.
- Do not create static evidence envelopes from repository checkouts.
- Do not execute plugin code.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI for applicability detection.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat plugin decisions as registry truth.

## Dependencies

- P39-T3 deterministic evaluator helper.
- P39-T4 `repository-plugin-applicability-detect` CLI/report surface.
- Existing `autonomous-candidate-batch --repository-plugin-applicability`
  sidecar copy path.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q -k 'repository_plugin_applicability'`
- `PYTHONPATH=src pytest tests/test_repository_plugin_applicability_cli.py -q`
- `PYTHONPATH=src pytest tests/test_repository_plugin_applicability_evaluator.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'static_repository_plugin_applicability_evaluator_plan or static_plugin_evidence_envelope or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
