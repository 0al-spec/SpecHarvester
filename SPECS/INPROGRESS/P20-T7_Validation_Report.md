# P20-T7 Validation Report — CodeGraph Compatibility Guard

**Date:** 2026-06-14
**Verdict:** PASS

## Scope

P20-T7 adds an offline compatibility guard for the optional CodeGraph adapter
boundary. The guard validates a pinned local compatibility fixture, required
JSON CLI command expectations, binary availability policy, and fixture-backed
normalization into `source_graph_index`.

The implementation does not install CodeGraph, run `npm`/`npx`, access the
network, or index third-party repositories during ordinary CI.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_codegraph_compatibility.py -q`
  - Result: `7 passed`
- `PYTHONPATH=src pytest tests/test_codegraph_compatibility.py tests/test_docs_contracts.py -q`
  - Result: `97 passed`
- `PYTHONPATH=src python -m pytest`
  - Result: `695 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - Result: `695 passed, 1 skipped`
  - Coverage: `90.75%`
- `PYTHONPATH=src ruff check src tests`
  - Result: passed
- `PYTHONPATH=src ruff format --check src tests`
  - Result: `114 files already formatted`
- `git diff --check`
  - Result: passed
- `swift package dump-package >/dev/null`
  - Result: passed
- `swift build --target SpecHarvesterDocs`
  - Result: passed
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/specharvester-p20-t7-architecture-lint.json`
  - Result: command passed with advisory status
  - Advisory: existing `manifest_parser_pattern` in
    `src/spec_harvester/license_provenance_reports.py`
- `PYTHONPATH=src python -m spec_harvester codegraph-compatibility-report --fixture tests/fixtures/codegraph_compatibility/codegraph-0.9.7.json --output /tmp/specharvester-p20-t7-codegraph-compatibility-report.json`
  - Result: `SpecHarvesterCodeGraphCompatibilityReport` status `passed`
  - Package: `@colbymchenry/codegraph@0.9.7`
  - Commands: `affected`, `callees`, `callers`, `files`, `impact`, `query`,
    `status`
  - Executable check: `skipped` because no executable path was provided

## Acceptance Criteria

- [x] Deterministic JSON report is emitted.
- [x] Local fixture pins CodeGraph package name, version, integrity, license,
      platform package metadata, binary availability policy, and required
      command args.
- [x] Required JSON command expectations cover `status`, `query`, `files`,
      `callers`, `callees`, `impact`, and `affected`, and require `--json`.
- [x] Fixture records normalize into `schemaVersion:
      spec-harvester-codegraph-v1` and `kind: source_graph_index`.
- [x] Ordinary CI can run without CodeGraph, npm, network access, or repository
      indexing.

## Notes

The architecture lint advisory is unchanged by this task and remains outside
the P20-T7 compatibility guard scope.
