## REVIEW REPORT — P20-T5 Scoped Source-Unit Draft Intent Boundaries

**Scope:** `codex/p17-t6-specnode-refinement-orchestration-objects...HEAD`
**Files:** 11

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

- `SourceUnitIntentBoundary` owns the source-unit classification decision
  without I/O, subprocesses, imports from analyzed repositories, or network
  access.
- Draft generation and SpecNode refinement preview now share the same
  repository/package/folder-module/single-file boundary instead of duplicating
  prompt wording.
- The change keeps CodeGraph integration out of scope and does not alter
  registry acceptance or package-set promotion policy.

### Tests

- `PYTHONPATH=src python -m pytest`: `681 passed, 1 skipped`
- `ruff check src tests`: passed
- `ruff format --check src tests`: passed
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  total coverage `90.76%`
- `swift package dump-package >/dev/null`: passed
- `swift build --target SpecHarvesterDocs`: passed
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`: `88 passed`

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Next planned task remains `P20-T6 CodeGraph Adapter Boundary`.
