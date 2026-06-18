# P38-T2 Validation Report

Task: `P38-T2` Repository Plugin Registry Fixture.

## Summary

PASS.

The task adds a machine-readable `SpecHarvesterRepositoryPluginRegistry`
fixture for declared producer-side plugin contracts. It does not implement
plugin loading, plugin execution, applicability evaluation, autonomous batch
integration, parser profile behavior changes, repository profile scoring
changes, ecosystem-specific plugins, or real-repository runs.

## Changed Surface

- Added `tests/fixtures/repository_plugins/generic-registry.example.json`.
- Added `docs/REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md`.
- Added DocC mirror
  `Sources/SpecHarvester/Documentation.docc/RepositoryPluginRegistryFixture.md`.
- Linked the fixture from the plugin subsystem contract, docs index, DocC root,
  capabilities, and roadmap.
- Added docs-contract regression coverage for the fixture and P38 next-task
  states.

## Fixture Coverage

The fixture defines:

- `apiVersion: spec-harvester.repository-plugins/v0`;
- `kind: SpecHarvesterRepositoryPluginRegistry`;
- `schemaVersion: 1`;
- `authority: producer_plugin_registry_only`;
- plugin roles for `parser_profile`, `repository_profile`,
  `evidence_producer`, `topology_helper`, and `review_surface`;
- static input evidence kinds;
- output artifact kinds;
- safety constraints;
- applicability signals;
- fallback behavior;
- diagnostics;
- non-authority statements.

## Non-Authority Boundary

The fixture states that registry records do not load third-party plugin code,
execute plugins, clone or fetch repositories, install dependencies, execute
harvested code, invoke package managers, run AI, accept packages, accept
relations, publish registry metadata, seed baselines, remove `preview_only`,
treat plugin output as registry truth, or treat AI output as registry truth.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin or current_next_task'`
  - Result: `2 passed, 107 deselected`
- `PYTHONPATH=src pytest -q`
  - Result: `760 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - Result: `760 passed, 1 skipped`, total coverage `91.15%`
- `PYTHONPATH=src ruff check .`
  - Result: passed
- `PYTHONPATH=src ruff format --check src tests`
  - Result: passed
- `git diff --check`
  - Result: passed
- `swift build --target SpecHarvesterDocs`
  - Result: passed

## Verdict

PASS. P38-T2 is ready for archive and review.

