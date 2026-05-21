## REVIEW REPORT — P11-T3 Provider Adapter Boundary

**Scope:** `main..HEAD`
**Files:** 18

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

- The change remains documentation-contract only. It does not add provider
  runtime code, does not call LM Studio, and does not move provider discovery
  into SpecHarvester.
- The provider boundary preserves the existing P11 trust model: SpecHarvester
  produces deterministic artifacts, SpecNode owns provider execution, and model
  output remains untrusted proposal metadata.

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
- Continue with `P11-T4` for schema-validated model output: candidate patch
  proposals, provenance, usage receipts, and rejection reasons.
