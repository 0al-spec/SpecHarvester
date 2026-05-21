## REVIEW REPORT — P11-T4 Patch Proposal Output Schema

**Scope:** `main..HEAD`
**Files:** 20

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

- The change remains documentation-contract only. It does not add model
  execution, provider calls, JSON Schema validator code, or patch application.
- The output boundary preserves the P11 trust model: model output is structured
  proposal metadata, not direct mutation authority or accepted registry truth.
- The contract explicitly requires schema validation before apply and SpecPM
  validation after any accepted local edit.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q` passed.
- `PYTHONPATH=src python -m pytest` passed.
- `ruff check src tests` passed.
- `ruff format --check src tests` passed.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` passed with 90.91% total coverage.
- `swift package dump-package >/dev/null` passed.
- `swift build --target SpecHarvesterDocs` passed.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Continue with `P11-T5` for SpecNode-compatible provider smoke coverage with
  deterministic fallback when no provider is available.
