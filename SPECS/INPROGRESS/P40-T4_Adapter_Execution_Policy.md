# P40-T4 Adapter Execution Policy

## Status

Planned for execution on `feature/P40-T4-adapter-execution-policy`.

## Context

P40-T1 defined the repository plugin adapter boundary, P40-T2 added adapter
manifest declarations, and P40-T3 added a preflight report fixture that records
allowed, rejected, fallback, and blocked adapter decisions without loading or
executing adapter code.

P40-T4 defines the execution policy that future adapter implementations must
satisfy before any non-static runtime path can exist.

## Motivation

Repository plugin adapters should eventually improve evidence quality for
different repository shapes, languages, package managers, and frameworks. That
precision must not become implicit permission to run third-party code, install
dependencies, invoke package managers, crawl networks, or mutate generated
SpecPM artifacts.

The policy needs to make disabled-by-default behavior explicit before future
implementation tasks can add any adapter runtime.

## Deliverables

- Add `docs/REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md`.
- Add DocC mirror
  `Sources/SpecHarvester/Documentation.docc/RepositoryPluginAdapterExecutionPolicy.md`.
- Define execution modes:
  - `disabled`
  - `static_only`
  - `trusted_local_tool`
  - `blocked`
- Define the mode transition requirements from manifest and preflight to any
  future trusted local execution.
- Define deny-by-default capability policy for filesystem writes, network,
  process execution, dependency installation, package managers, environment
  access, harvested code execution, and AI.
- Define required operator opt-in and path allowlist requirements for every
  non-static mode.
- Update adapter contract, manifest fixture, preflight report fixture,
  subsystem, capabilities, roadmap, docs index, DocC root, Workplan, and
  `next.md` references.
- Add regression tests proving the policy is discoverable and preserves the
  no-runtime boundary.

## Acceptance Criteria

- The policy states that all adapter execution is disabled by default.
- `static_only` is the only current safe mode.
- `trusted_local_tool` is future-only and requires an explicit operator opt-in,
  passing preflight, path allowlists, bounded inputs, bounded outputs, timeout,
  diagnostics, no network discovery, no dependency installation, no package
  manager invocation, and no harvested code execution.
- Unsafe or unsupported execution states map to `blocked`.
- The policy states that no adapter output can accept packages, accept
  relations, seed baselines, publish registry metadata, remove `preview_only`,
  or become registry truth.
- Tests cover the GitHub doc, DocC mirror, navigation links, Workplan state,
  and `next.md` state.

## Non-Goals

- Do not implement adapter loading or execution.
- Do not connect adapters to autonomous batch.
- Do not change static plugin applicability evaluation.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`

