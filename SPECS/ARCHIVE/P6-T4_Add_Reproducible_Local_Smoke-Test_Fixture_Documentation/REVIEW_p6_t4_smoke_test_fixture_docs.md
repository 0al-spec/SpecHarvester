## REVIEW REPORT - p6_t4_smoke_test_fixture_docs

**Scope:** `origin/main..HEAD`  
**Files:** 12

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

- The smoke workflow remains local-only and uses existing commands:
  `source-manifests`, `collect-batch`, `draft`, and governance reports.
- `.smoke/` is the canonical ignored workspace for local inputs, candidate
  output, and advisory reports.
- Legacy `smoke-inputs/` and `smoke-output*/` paths are ignored to prevent
  accidental generated-output churn from earlier local smoke runs.
- The GitHub documentation and DocC mirror intentionally duplicate command
  snippets so the published Pages documentation remains usable without opening
  repository Markdown directly.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`: PASS,
  3 passed.
- `PYTHONPATH=src python -m pytest`: PASS, 121 passed.
- `ruff check src tests`: PASS.
- `ruff format --check src tests`: PASS.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  PASS, total coverage 90.34%.
- `swift package dump-package >/dev/null`: PASS.
- `swift build --target SpecHarvesterDocs`: PASS.

### Next Steps

- No actionable follow-up tasks.
- FOLLOW-UP skipped.
- PR body should use `.github/PULL_REQUEST_TEMPLATE.md` and include the
  validation results above.
