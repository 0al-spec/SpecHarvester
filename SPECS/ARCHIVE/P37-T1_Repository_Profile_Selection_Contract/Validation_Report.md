# P37-T1 Validation Report

## Verdict

PASS

## Scope

P37-T1 documents the language- and framework-agnostic repository profile
selection contract and links it through GitHub-facing docs, DocC docs,
capabilities, roadmap, and docs-contract regression tests.

## Deliverables

- `docs/REPOSITORY_PROFILE_SELECTION_CONTRACT.md`
- `Sources/SpecHarvester/Documentation.docc/RepositoryProfileSelectionContract.md`
- links from docs index, DocC root, capabilities, and roadmap
- docs-contract regression coverage for:
  - selection model;
  - artifact shape;
  - selection modes;
  - precedence;
  - confidence;
  - generic hints;
  - fallback behavior;
  - non-authority boundaries.

## Validation Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile_selection_contract or repository_profile_plugin_selection_plan or current_next_task'
PYTHONPATH=src pytest -q
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
swift build --target SpecHarvesterDocs
```

## Results

- Targeted docs-contract tests: `2 passed, 101 deselected`
- Full tests: `734 passed, 1 skipped`
- Ruff check: passed
- Ruff format check: passed
- Diff whitespace check: passed
- Coverage: `91.03%`, above the `90%` threshold
- Swift docs build: passed

## Boundary

The task is documentation and contract planning only. It does not implement
repository profile detection, a runtime plugin registry, a language-specific
profile, or autonomous candidate batch behavior.

The contract remains producer-side evidence only and does not clone/fetch
repositories, install dependencies, execute harvested code, invoke package
managers, run AI, draft packages, publish registry metadata, accept packages or
relations, remove `preview_only`, or treat AI output or plugin decisions as
registry truth.
