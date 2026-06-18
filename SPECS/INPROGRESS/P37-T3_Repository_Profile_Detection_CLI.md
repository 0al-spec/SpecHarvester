# P37-T3 Repository Profile Detection CLI

## Motivation

P37-T1 defined the repository profile selection contract and P37-T2 made the
`SpecHarvesterRepositoryProfileDetection` artifact concrete with a versioned
fixture. The next step is a narrow executable surface that can emit this
artifact from explicit operator-provided static evidence.

This command should give operators and future automation a deterministic way
to record "which repository profile would apply and why" before the decision is
wired into autonomous candidate batch behavior.

## Goal

Implement an opt-in CLI/report surface that writes a
`SpecHarvesterRepositoryProfileDetection` JSON artifact.

The surface must remain intentionally narrow:

- it reads static metadata supplied through CLI arguments or an existing source
  manifest;
- it accepts `auto`, `none`, or an explicit profile id;
- it records candidate profiles, rejected profiles, diagnostics, non-authority
  statements, and advisory downstream hints;
- it does not collect source files, run analyzers, run AI, draft packages, or
  publish registry metadata.

## Deliverables

- Add a small `repository_profile_detection` domain module.
- Add a `repository-profile-detect` CLI command.
- Add unit/CLI tests for:
  - auto package-set selection from static evidence paths;
  - `none` selection mode;
  - explicit profile-id override;
  - output file writing;
  - source manifest metadata loading;
  - no dependency on source collection or AI.
- Document the CLI surface in
  `docs/REPOSITORY_PROFILE_SELECTION_CONTRACT.md` and DocC.
- Archive the task through Flow.

## CLI Shape

The command should support:

```bash
spec-harvester repository-profile-detect \
  --repository-id example.generic-package-set \
  --repository-url https://example.invalid/generic-package-set \
  --revision 0000000000000000000000000000000000000000 \
  --selection auto \
  --evidence-path workspace.yaml \
  --evidence-path packages/core/package.json \
  --evidence-path packages/adapter/package.json \
  --output repository-profile-detection.json
```

It may also read repository identity from a source manifest directory:

```bash
spec-harvester repository-profile-detect \
  --source-manifest inputs \
  --source-id example.generic-package-set \
  --selection auto \
  --evidence-path workspace.yaml
```

## Acceptance Criteria

- The command emits:
  - `apiVersion: spec-harvester.repository-profile-detection/v0`;
  - `kind: SpecHarvesterRepositoryProfileDetection`;
  - `schemaVersion: 1`;
  - `authority: producer_profile_selection_only`.
- `auto` mode selects `generic.package_set.v0` when static evidence includes
  workspace evidence plus member package manifests.
- `auto` mode falls back to `generic.repository.v0` when evidence is
  insufficient or ambiguous.
- `none` mode emits no selected profile and records an explicit disabled
  diagnostic while preserving a deterministic artifact.
- explicit profile-id mode records the selected profile and marks the override
  source as CLI.
- The command can print JSON to stdout and optionally write the same JSON to
  `--output`.
- The command can read repository identity from
  `read_repository_source_manifests` without expanding supported manifest
  schema in this task.
- The report records non-authority statements proving it does not clone/fetch
  repositories, install dependencies, execute harvested code, invoke package
  managers, run AI, draft packages, publish registry metadata, accept packages
  or relations, seed baselines, remove `preview_only`, or treat plugin/AI
  decisions as registry truth.

## Non-Goals

- Do not connect profile selection to autonomous candidate batch behavior.
- Do not implement a general plugin registry.
- Do not implement ecosystem-specific profile plugins.
- Do not collect source files, run analyzers, run package managers, run AI, or
  draft packages.
- Do not publish registry metadata, accept packages or relations, remove
  `preview_only`, or treat AI output or plugin decisions as registry truth.

## Dependencies

- P37-T1 repository profile selection contract.
- P37-T2 repository profile detection fixture.
- Existing `read_repository_source_manifests` helper.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_repository_profile_detection.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift build --target SpecHarvesterDocs`
