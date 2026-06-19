# P38-T5 Validation Report

## Task

P38-T5 Repository Plugin Cross-Ecosystem Fixtures.

## Summary

PASS. Added a static cross-ecosystem repository plugin applicability fixture
matrix under `tests/fixtures/repository_plugins/cross_ecosystem/`.

The matrix covers:

- manifest-backed single-package repository;
- workspace or multi-package repository;
- documentation-heavy repository;
- nested package roots;
- ambiguous mixed layout.

The fixtures remain producer-side review evidence only. They do not execute
plugins, load third-party plugin code, clone or fetch repositories, run package
managers, install dependencies, execute harvested code, invoke AI, accept
packages or relations, publish registry metadata, remove `preview_only`, or
treat plugin decisions as registry truth.

## Validation

| Command | Result |
| --- | --- |
| `for f in tests/fixtures/repository_plugins/cross_ecosystem/*.json; do python3 -m json.tool "$f" >/dev/null \|\| exit 1; done` | PASS |
| `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin_cross_ecosystem or current_next_task'` | PASS, `1 passed, 110 deselected` |
| `PYTHONPATH=src pytest -q` | PASS, `764 passed, 1 skipped` |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `764 passed, 1 skipped`, total coverage `91.16%` |
| `PYTHONPATH=src ruff check .` | PASS |
| `PYTHONPATH=src ruff format --check src tests` | PASS, `120 files already formatted` |
| `git diff --check` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Review Notes

- Regression coverage verifies identity, summary counts, decision sets,
  diagnostics, non-authority statements, docs links, and DocC links.
- Regression coverage also checks that every selected plugin has all required
  declared `inputEvidenceKinds[]` available in the fixture's
  `staticEvidence.evidenceKinds[]`.
- P38-T5 intentionally adds examples only. Runtime plugin discovery, plugin
  execution, and registry authority remain out of scope.
