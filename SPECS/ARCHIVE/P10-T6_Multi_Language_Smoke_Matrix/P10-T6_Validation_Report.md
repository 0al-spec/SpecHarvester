# P10-T6 Validation Report

Status: PASS
Date: 2026-05-20
Task: P10-T6 Multi-Language Smoke Matrix

## Scope Validated

- Added a synthetic multi-language smoke matrix for npm, SPM, Gradle/Maven, Go
  modules, Composer, CMake, Xcode/CocoaPods, RubyGems, Python packaging, and a
  documentation-first manifest-poor fixture.
- Verified `ProjectProfile` languages, ecosystems, analyzer plan ids/statuses,
  manifest paths, diagnostics, strict public license evidence, and collector
  trust-boundary policy.
- Verified the documentation-first fixture drafts non-generic semantic intent
  evidence from `semanticHints` without storing raw documentation bodies.
- Updated GitHub docs and DocC mirror coverage for the smoke matrix contract.

## Commands

```bash
ruff check src tests
```

Result: PASS

```bash
ruff format --check src tests
```

Result: PASS

```bash
PYTHONPATH=src python -m pytest tests/test_multi_language_smoke_matrix.py tests/test_docs_contracts.py -q
```

Result: PASS, `10 passed`

```bash
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result: PASS, `206 passed`, total coverage `90.69%`

```bash
swift package dump-package >/dev/null
```

Result: PASS

```bash
swift build --target SpecHarvesterDocs
```

Result: PASS

## Notes

- The matrix uses synthetic local fixtures under test `tmp_path`; it does not
  clone repositories, execute package managers, install dependencies, run
  package scripts, or commit generated candidates.
- Documentation continues to direct real local smoke runs into ignored `.smoke/`
  outputs.
