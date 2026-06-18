# P38-T3 Validation Report

## Task

P38-T3 Repository Plugin Applicability Report Fixture.

## Scope

- Added `SpecHarvesterRepositoryPluginApplicabilityReport` fixture at
  `tests/fixtures/repository_plugins/generic-applicability-report.example.json`.
- Added GitHub docs and DocC docs for the applicability report fixture.
- Linked the fixture from repository plugin registry docs, subsystem contract,
  docs index, capabilities, roadmap, and DocC root.
- Added docs-contract regression coverage for fixture identity, registry
  alignment, selected/rejected/fallback/blocked decisions, decision authority,
  plugin output authority, diagnostics, follow-ups, and non-authority
  boundaries.

## Boundary Checked

The fixture remains producer-side decision evidence. It does not load
third-party plugin code, execute plugins, run plugin code, clone or fetch
repositories, install dependencies, execute harvested code, invoke package
managers, run AI, change parser profile behavior, change repository profile
scoring, accept packages, accept relations, publish registry metadata, seed
baselines, remove `preview_only`, treat plugin decisions as registry truth, or
treat AI output as registry truth.

## Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin or current_next_task'
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
swift build --target SpecHarvesterDocs
```

## Results

- Targeted docs-contract tests: `3 passed, 107 deselected`.
- Full pytest: `761 passed, 1 skipped`.
- Coverage gate: `91.15%`, above the `90%` threshold.
- Ruff lint: passed.
- Ruff format check: passed after formatting `tests/test_docs_contracts.py`.
- Diff whitespace check: passed.
- Swift docs target build: passed.

## Verdict

PASS.
