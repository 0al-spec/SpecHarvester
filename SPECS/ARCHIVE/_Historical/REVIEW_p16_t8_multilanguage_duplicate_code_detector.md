## REVIEW REPORT — p16_t8_multilanguage_duplicate_code_detector

**Scope:** `origin/main..HEAD`
**Files:** 11
**Date:** 2026-05-28

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

- None.

### Secondary Issues

- None.

### Architectural Notes

- The `jscpd` integration is an optional adapter behind the existing
  `SpecHarvesterCodeDuplicationReport` schema, so consumers do not need a
  schema-version migration for this task.
- The backend remains outside default CI and project dependencies. This is the
  correct boundary until the project defines pinned npm installation, caching,
  and fail-on-new-duplicate semantics.
- A self-review issue was fixed before this report: `jscpd` now emits a
  backend-specific trust-boundary note instead of reusing the stronger builtin
  claim that no dependency installation or network access can occur. Wrapper
  commands such as `npx` are now explicitly documented as external trust
  boundary behavior.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_code_duplication_report.py tests/test_docs_contracts.py -q`
  - PASS: 45 passed.
- `PYTHONPATH=src python -m pytest`
  - PASS: 424 passed, 1 skipped.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 424 passed, 1 skipped, total coverage 91.72%.
- `ruff check src tests`
  - PASS.
- `ruff format --check src tests`
  - PASS.
- `swift package dump-package >/dev/null`
  - PASS.
- `swift build --target SpecHarvesterDocs`
  - PASS.
- `git diff --check`
  - PASS.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Before merge, ensure the PR body follows `.github/PULL_REQUEST_TEMPLATE.md`
  and calls out that `jscpd` is opt-in, operator-provided, and not executed by
  default CI.
