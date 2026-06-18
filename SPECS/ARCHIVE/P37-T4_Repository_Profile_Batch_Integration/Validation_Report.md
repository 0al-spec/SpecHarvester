# P37-T4 Validation Report

## Scope

P37-T4 connects repository profile selection to `autonomous-candidate-batch` as
producer-side evidence.

Implemented:

- `AutonomousCandidateBatchOptions.repository_profile_selection` with default
  `none`;
- CLI flag `--repository-profile-selection`;
- per-repository `SpecHarvesterRepositoryProfileDetection` artifacts under
  `reports/repository-profile-detections/<repository-id>/`;
- per-repository `repositoryProfileDetection` report summaries;
- top-level `repositoryProfileSelection` batch metadata;
- static evidence extraction from existing `workspace-inventory.json`;
- docs, DocC, capabilities, roadmap, and regression tests.

The task intentionally does not apply advisory hints to drafting and does not
change package acceptance, relation acceptance, registry publication, or
`preview_only` behavior.

## Acceptance Criteria

- [x] Batch accepts `auto | none | <profile-id>` profile selection.
- [x] Default mode is `none`.
- [x] Each processed repository gets a detection artifact and report summary.
- [x] Auto mode selects `generic.package_set.v0` from workspace/member manifest
  evidence.
- [x] Explicit profile ids record `overrideSource: cli`.
- [x] Detection artifacts preserve
  `apiVersion: spec-harvester.repository-profile-detection/v0`,
  `kind: SpecHarvesterRepositoryProfileDetection`, `schemaVersion: 1`, and
  `authority: producer_profile_selection_only`.
- [x] Advisory hints remain evidence only:
  `advisoryHintsAppliedToDrafting: false`.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py tests/test_repository_profile_detection.py -q`
  - Result: `20 passed`.
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile_selection_contract or repository_profile_plugin_selection_plan or current_next_task'`
  - Result: `2 passed, 102 deselected`.
- `PYTHONPATH=src pytest -q`
  - Result: `745 passed, 1 skipped`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - Result: `745 passed, 1 skipped`; total coverage `91.12%`.
- `PYTHONPATH=src ruff check .`
  - Result: passed.
- `PYTHONPATH=src ruff format --check src tests`
  - Result: `119 files already formatted`.
- `git diff --check`
  - Result: passed.
- `swift build --target SpecHarvesterDocs`
  - Result: passed.
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/specharvester-p37-t4-architecture-lint.json`
  - Result: completed with advisory `status: attention`.
  - Existing unrelated advisory:
    `src/spec_harvester/license_provenance_reports.py`
    `manifest_parser_pattern`.
- `PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch /tmp/nonexistent --out /tmp/specharvester-p37-t4-invalid --skip-ai --repository-profile-selection ''`
  - Result: expected validation error with exit code `2` and message
    `--repository-profile-selection must be non-empty`.

## Notes

The first targeted test run exposed two implementation issues and both were
fixed before final validation:

- writing `repository-profile-detection.json` inside `package-sets/<id>/`
  made the drafter reject a non-empty output directory;
- treating every `package.json` as workspace evidence caused nested member
  manifests to be counted as workspace manifests.

The final implementation writes detection artifacts under `reports/` and only
treats root-level `package.json` as workspace evidence.

## Follow-Up

Proceed to `P37-T5 Define generic workspace/member discovery hints produced
by profiles`.
