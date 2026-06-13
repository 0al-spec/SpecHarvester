## REVIEW REPORT — P33-T2 Next-Corpus Source Manifest Fixture

**Scope:** `codex/p33-t1-bounded-corpus-expansion-plan..HEAD`
**Files:** 16
**Date:** 2026-06-13

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
- The source manifest uses the existing `inputs/*.yml` contract and is parsed
  by `read_repository_source_manifests`, so P33-T2 does not introduce a
  parallel manifest format.
- Every next-corpus entry is pinned by exact `revision`, has a local checkout
  path, and records package ID hints plus review labels.
- The companion fixture preserves the Phase 33 boundary: local-only existing
  checkouts, no clone/fetch/install/execute behavior, no package scripts, no
  registry publication, no package or relation acceptance, no baseline seeding,
  no `preview_only` removal, and no AI output as registry truth.

### Tests
- `PYTHONPATH=src python3 -m spec_harvester source-manifests inputs/p33-next-corpus`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'bounded_corpus_expansion_plan or next_corpus_source_manifest' -x --tb=short`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format tests/test_docs_contracts.py`
- `PYTHONPATH=src ruff format --check src tests`

### Next Steps
- FOLLOW-UP skipped: no actionable issues were found.
- Open the stacked PR against
  `codex/p33-t1-bounded-corpus-expansion-plan` after ARCHIVE-REVIEW and final
  validation.
