## REVIEW REPORT — P10-T5 Language-Neutral Semantic Extraction

**Scope:** `origin/main..HEAD`
**Files:** 18
**Date:** 2026-05-20

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

None.

### Secondary Issues

None.

### Architectural Notes

- The collector stores bounded `semanticHints` and does not persist raw
  Markdown bodies in `harvest.json`, preserving the existing compact evidence
  contract.
- Language-neutral clusters are advisory and deterministic. They are used as a
  capability intent fallback only when manifest-derived capability entries are
  absent, while repositories with supported package manifests keep their
  manifest-derived intents.
- Existing Swift/iOS semantic profile behavior remains compatible because those
  domain-specific intent IDs still opt into replacing manifest fallback
  capability intents.

### Tests

- `ruff check src tests`: PASS
- `ruff format --check src tests`: PASS
- `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_docs_contracts.py -q`:
  PASS, `75 passed`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  PASS, `203 passed`, total coverage `90.68%`
- `swift package dump-package >/dev/null`: PASS
- `swift build --target SpecHarvesterDocs`: PASS

### Next Steps

- FOLLOW-UP skipped: no actionable review findings were found.
- Verify the PR body uses `.github/PULL_REQUEST_TEMPLATE.md` before merge.
