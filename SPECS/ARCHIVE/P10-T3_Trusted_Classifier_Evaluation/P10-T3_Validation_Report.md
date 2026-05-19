# P10-T3 Validation Report

Task: `P10-T3` Trusted Classifier Evaluation
Date: 2026-05-19
Verdict: PASS

## Scope

- Added a machine-readable trusted classifier registry for GitHub Linguist,
  go-enry, Syft, ScanCode Toolkit, Universal Ctags, and Tree-sitter.
- Added disabled-by-default `classifierPolicy` metadata to local harvest
  snapshots.
- Kept external classifier output advisory and untrusted, with manifest-first
  `ProjectProfile` evidence as the merge precedence rule.
- Added GitHub documentation plus DocC mirror for the classifier trust boundary.
- Added regression tests for registry decisions, default fallback behavior, and
  documentation coverage.

## Quality Gates

- PASS: `ruff check src tests`
- PASS: `ruff format --check src tests`
- PASS: `PYTHONPATH=src python -m pytest tests/test_classifier_registry.py tests/test_collector.py tests/test_docs_contracts.py -q`
  - Result: 74 passed
- PASS: `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - Result: 188 passed
  - Coverage: 90.70%
- PASS: `swift package dump-package >/dev/null`
- PASS: `swift build --target SpecHarvesterDocs`
- PASS: local smoke check for `collect-local .`
  - Result: `classifierPolicy.defaultMode == disabled`
  - Result: six registry summary tools present without executing external tools

## Notes

- No external classifier binaries were installed or executed.
- `harvest.json` stores a compact registry summary to avoid increasing routine
  prompt context with long license and decision notes.
- The full reviewed registry remains available in
  `spec_harvester.classifier_registry`.
