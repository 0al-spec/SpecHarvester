## REVIEW REPORT — P10-T1 ProjectProfile Schema

**Scope:** `origin/main..HEAD`
**Files:** 8

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

- None found.

### Secondary Issues

- None found.

### Architectural Notes

- `projectProfile` is embedded as evidence in harvest snapshots and does not
  affect drafting behavior yet. That is appropriate for P10-T1 because later
  detector and analyzer orchestration tasks can consume the schema without
  changing candidate generation in the same step.
- Current support intentionally maps only existing parsed manifest evidence:
  `package.json` to npm/JavaScript and `Package.swift` to SwiftPM/Swift. Broader
  manifest coverage belongs in `P10-T2`.
- Analyzer plan entries are advisory and deterministic. They do not execute
  analyzers or harvested package code.

### Tests

- `ruff check src tests`: passed.
- `ruff format --check src tests`: passed.
- `PYTHONPATH=src python -m pytest tests/test_collector.py -q`: passed, 61 tests.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`: passed, 180 tests, 90.66% coverage.
- `swift package dump-package >/dev/null`: passed.
- `swift build --target SpecHarvesterDocs`: passed.

### Next Steps

- No follow-up tasks are required from this review.
- Continue with `P10-T2` to add manifest-first ecosystem detectors for the wider
  language and package-manager matrix.
- Before merge, ensure the PR body follows `.github/PULL_REQUEST_TEMPLATE.md`.
