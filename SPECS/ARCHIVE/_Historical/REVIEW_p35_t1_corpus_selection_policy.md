## REVIEW REPORT — P35-T1 Corpus Selection Policy

**Scope:** `origin/main..HEAD`  
**Files:** 14

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

- The policy correctly moves source selection ahead of harvesting and treats
  repository/package-family selection as an operator-reviewed planning step.
- The boundary is consistent with existing SpecHarvester contracts: local
  pinned checkouts only, no clone/fetch/install/execute behavior, no registry
  publication, no package or relation acceptance, and no AI output as registry
  truth.
- The follow-up sequence is clear: `P35-T2` should define the
  `SpecHarvesterCorpusPlan` machine-readable format before seed corpus
  selection or reporting automation is implemented.

### Tests

Validation evidence is recorded in
`SPECS/ARCHIVE/P35-T1_Corpus_Selection_Policy/Validation_Report.md`.

Recorded passing gates:

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- DocC static generation command from `.github/workflows/docs.yml`

Coverage remained above the configured threshold: `90.96%` with required
`90%`.

### Next Steps

- No actionable follow-up is required from this review.
- Proceed to archive this review report.
- Next planned Flow task is `P35-T2 SpecHarvesterCorpusPlan`.
