# P10-T4 ProjectProfile Analyzer Orchestration

Status: In Progress
Created: 2026-05-20
Task: `P10-T4` Wire `ProjectProfile` into analyzer orchestration so
`collect-batch` can recommend or emit public-interface indexes from existing
static analyzers, including Python `ast` and JavaScript/TypeScript export
analyzers, before `draft` runs.

## Problem

SpecHarvester already emits `ProjectProfile.analyzerPlan` and already has
deterministic Python and JavaScript/TypeScript public API analyzers. Operators
still have to run those analyzers manually and pass `public-interface-index.json`
into `draft`. Batch collection should be able to use the manifest-first
`ProjectProfile` plan to emit public interface indexes before drafting without
executing harvested package code.

## Goals

- Add a deterministic analyzer orchestration boundary that consumes
  `ProjectProfile.analyzerPlan`.
- Support existing built-in static analyzers:
  - `spec_harvester.python_public_api`
  - `spec_harvester.js_ts_public_api`
- Add an opt-in `collect-batch` mode that writes `public-interface-index.json`
  beside `harvest.json` for repositories with recommended analyzer plans.
- Report analyzer orchestration outcomes in `collect-batch` output without
  making analyzer output authoritative.
- Preserve strict trust rules: no package scripts, no package manager
  execution, no build systems, no dependency installation, and no network.

## Non-Goals

- Do not run analyzers by default for every `collect-batch` invocation.
- Do not add external classifier/tool execution.
- Do not implement Swift, Java/Kotlin, Go, PHP, C/C++, Objective-C, Ruby, or
  Rust analyzers in this task.
- Do not change `draft` to inspect raw repository source.
- Do not treat analyzer output as acceptance evidence or registry authority.

## Proposed Shape

- Add a small orchestration module that maps supported `ProjectProfile`
  analyzer ids to existing analyzer functions.
- The orchestrator should:
  - accept source checkout path, harvest snapshot, optional package id, and
    optional cache directory;
  - run only known analyzer ids with `status: recommended`;
  - skip `manifest_only` and unknown analyzer plan entries with diagnostics;
  - merge one or more built-in `PublicInterfaceIndex` outputs into a single
    deterministic index;
  - record orchestration diagnostics without failing collection when no
    supported analyzer is present.
- Extend `collect-batch` with opt-in flags:
  - `--emit-interface-indexes`
  - `--analyzer-cache-dir <path>`

## Acceptance Criteria

- `collect-batch --emit-interface-indexes` writes
  `public-interface-index.json` next to `harvest.json` for Python and
  JavaScript/TypeScript repositories when `ProjectProfile.analyzerPlan`
  recommends a built-in analyzer.
- Batch JSON output records an `interfaceIndex` summary per collected
  repository, including written/skipped status and diagnostics.
- Default `collect-batch` behavior remains unchanged and does not run analyzers.
- Analyzer orchestration uses only static local source reads and preserves
  analyzer policy values: `execution: none`, `networkAccess: none`, and
  `packageScripts: not_run`.
- Tests cover Python emission, JavaScript/TypeScript emission, mixed analyzer
  merge behavior, default disabled behavior, unsupported/manifest-only skips,
  and CLI flags.
- Documentation covers the opt-in batch interface-index flow.

## Validation Plan

- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest tests/test_analyzer_orchestration.py tests/test_batch_collection.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
