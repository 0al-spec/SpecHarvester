# P38-T1 Repository Plugin Subsystem Contract

## Motivation

SpecHarvester now has parser profile hooks and repository profile selection,
but the product direction needs a broader plugin subsystem before adding more
language/framework-specific rules. The subsystem must let future plugins
declare what static evidence they can produce, when they apply, and what
diagnostics they emit while keeping the core pipeline deterministic,
language-neutral, and reviewable.

This task documents the contract before implementation.

## Goal

Define a language- and framework-agnostic repository plugin subsystem contract
that can later cover parser profiles, repository profiles, package topology
helpers, evidence producers, and applicability reports without making any
ecosystem normative.

## Deliverables

- Add `docs/REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md`.
- Add DocC mirror `RepositoryPluginSubsystemContract.md`.
- Update docs index, DocC root, capabilities, roadmap, and workplan references.
- Add docs-contract regression coverage.
- Record validation and archive the task through Flow.

## Acceptance Criteria

- The contract defines:
  - plugin identity and versioning;
  - plugin roles;
  - registration metadata;
  - static input evidence;
  - applicability checks;
  - deterministic selection boundaries;
  - output artifact categories;
  - diagnostics;
  - authority and trust boundaries.
- The contract explicitly keeps Python, JavaScript, FastAPI, FastMCP, npm,
  Cargo, Go, SwiftPM, Maven, Gradle, and other ecosystems as examples, not
  normative cases.
- The contract states that plugins must not clone/fetch repositories, install
  dependencies, execute harvested code, invoke package managers, run AI, accept
  packages, accept relations, publish registry metadata, remove `preview_only`,
  or treat plugin output as registry truth.
- The docs explain how Phase 36 parser profiles and Phase 37 repository
  profiles fit into the broader plugin subsystem without rewriting those
  mechanisms in this task.

## Non-Goals

- Do not implement plugin loading or plugin execution.
- Do not add a plugin registry fixture; that is P38-T2.
- Do not add applicability report fixtures; that is P38-T3.
- Do not change parser profile behavior.
- Do not change repository profile scoring.
- Do not add ecosystem-specific plugins.
- Do not run real repositories.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
