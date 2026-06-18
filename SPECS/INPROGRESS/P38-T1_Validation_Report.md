# P38-T1 Validation Report

Task: `P38-T1` Repository Plugin Subsystem Contract.

## Summary

PASS.

The task documents a language- and framework-agnostic repository plugin
subsystem contract without implementing plugin loading, plugin execution,
plugin registry fixtures, applicability fixtures, parser profile behavior
changes, repository profile scoring changes, ecosystem-specific plugins, or
real-repository runs.

## Changed Surface

- Added `docs/REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md`.
- Added DocC mirror
  `Sources/SpecHarvester/Documentation.docc/RepositoryPluginSubsystemContract.md`.
- Linked the contract from docs index, DocC root, capabilities, and roadmap.
- Added docs-contract regression coverage for the new contract and current
  P38 `next.md` states.

## Contract Coverage

The contract defines:

- plugin identity and versioning;
- plugin roles;
- registration metadata;
- static input evidence;
- applicability checks and reports;
- deterministic selection boundaries;
- output artifact categories;
- diagnostics;
- authority and trust boundaries.

The contract keeps Python, JavaScript, FastAPI, FastMCP, npm, Cargo, Go,
SwiftPM, Maven, Gradle, and other ecosystems as examples, not normative
plugin rules.

## Non-Authority Boundary

The contract states that repository plugins must not clone or fetch
repositories, install dependencies, execute harvested code, invoke package
managers, run AI, accept packages, accept relations, publish registry metadata,
seed baselines, remove `preview_only`, treat plugin output as registry truth,
or treat AI output as registry truth.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin or current_next_task'`
  - Result: `1 passed, 107 deselected`
- `PYTHONPATH=src pytest -q`
  - Result: `758 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - Result: `758 passed, 1 skipped`, total coverage `91.15%`
- `PYTHONPATH=src ruff check .`
  - Result: passed
- `PYTHONPATH=src ruff format --check src tests`
  - Result: passed
- `git diff --check`
  - Result: passed
- `swift build --target SpecHarvesterDocs`
  - Result: passed

## Verdict

PASS. P38-T1 is ready for archive and review.

