# P20-T6 Validation Report

**Task:** P20-T6 CodeGraph Adapter Boundary
**Result:** Passed

## Implementation Summary

- Added `codegraph-source-graph-index` as an explicit opt-in CLI boundary for
  normalizing existing CodeGraph JSON or SQLite artifacts.
- Added `CodeGraphSourceGraphIndex` payload generation with
  `schemaVersion: spec-harvester-codegraph-v1` and `kind: source_graph_index`.
- Recorded untrusted third-party analyzer trust policy, source target metadata,
  input digests, optional executable digest, source file digests, bounded
  nodes/edges, and diagnostics.
- Enforced safe relative paths, deterministic ordering, and node/edge limits.
- Documented the operator boundary in GitHub docs and DocC, including the P20-T7
  split for pinned executable/interface compatibility checks.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_codegraph_source_graph.py -q`:
  `4 passed`
- `PYTHONPATH=src pytest tests/test_codegraph_source_graph.py tests/test_docs_contracts.py -q`:
  `93 passed`
- `PYTHONPATH=src python -m pytest`: `686 passed, 1 skipped`
- `ruff check src tests`: passed
- `ruff format --check src tests`: `112 files already formatted`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  `686 passed, 1 skipped`, total coverage `90.76%`
- `swift package dump-package >/dev/null`: passed
- `swift build --target SpecHarvesterDocs`: passed
- `git diff --check`: passed
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/specharvester-p20-t6-architecture-lint.json`:
  completed with advisory `status: attention` for the existing
  `license_provenance_reports.py` manifest parser pattern baseline; no new
  issue was reported for the P20-T6 files.

## Notes

- No CodeGraph install, npm command, network access, or repository indexing was
  added.
- The adapter reads pre-existing artifacts only.
- P20-T7 remains responsible for pinned CodeGraph executable/version/interface
  compatibility checks.
