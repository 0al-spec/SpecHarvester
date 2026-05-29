# P17-T1 — Procedural Style Metrics Report

Branch: `feature/P17-T1-procedural-style-metrics`
Review subject: `p17_t1_procedural_style_metrics`

## Objective

Add a deterministic procedural-style metrics report for local Python source so
Phase 17 EO refactoring work can be measured by behavior movement rather than
subjective review impressions.

## Deliverables

- New report module under `src/spec_harvester/` that scans local Python source
  files without importing or executing them.
- Stable JSON report kind and schema version for procedural-style metrics.
- CLI command that prints the report, can write an output file, and can fail on
  configurable hotspot conditions.
- Regression tests for report shape, hotspot detection, missing-path handling,
  deterministic sorting, and CLI behavior.
- GitHub docs and DocC mirror that explain the report contract and trust
  boundary.

## Required Metrics

The report should include deterministic counts for at least:

- top-level function count;
- top-level function span;
- method count;
- method span;
- class count;
- behavior-rich class count;
- DTO-only class count;
- exception-like class count;
- modules with high top-level function concentration;
- largest top-level functions.

The report should also make it possible to compare procedural span against
method span at repository level and per-module level.

## Behavioral Rules

- Scan local `.py` files only.
- Deduplicate overlapping `--path` values.
- Treat unreadable, undecodable, or unparsable files as explicit skipped files
  rather than silently ignoring them.
- Sort files, hotspots, and largest functions deterministically.
- Keep the report advisory by default.
- Support an opt-in failure mode for clear hotspot thresholds so the report can
  later act as a refactor guardrail if the project chooses.

## Proposed Surface

- CLI command name: `procedural-style-report`
- Optional output path similar to `architecture-lint`
- Optional fail flag such as `--fail-on-hotspots`
- Default scan root: `src/spec_harvester`

## Non-Goals

- Do not refactor production code in this task.
- Do not attempt a full Elegant Objects semantic validator.
- Do not analyze non-Python languages yet.
- Do not make the report blocking in CI by default.
- Do not change existing report schemas, docs, or task statuses outside the new
  P17 track unless required for cross-linking.

## Validation

Run the project quality gates after implementation:

- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`

Also run targeted report checks during development:

- `PYTHONPATH=src python -m pytest tests/test_procedural_style_report.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m spec_harvester procedural-style-report --path src/spec_harvester`
