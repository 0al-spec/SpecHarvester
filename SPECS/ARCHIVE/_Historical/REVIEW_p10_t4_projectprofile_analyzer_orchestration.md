## REVIEW REPORT — P10-T4 ProjectProfile Analyzer Orchestration

**Scope:** `origin/main..HEAD`
**Files:** 17
**Date:** 2026-05-20

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

- `collect-batch` remains safe by default: analyzers run only when
  `--emit-interface-indexes` is explicitly provided.
- The orchestrator consumes `ProjectProfile.analyzerPlan` rather than scanning
  arbitrary languages opportunistically. This keeps analyzer selection tied to
  deterministic manifest-first evidence.
- Batch JSON records only interface-index status and summary metadata, not the
  full index payload. This is appropriate for token economy; the full
  `PublicInterfaceIndex` stays in `public-interface-index.json`.
- Unsupported and `manifest_only` plans are skipped rather than treated as
  failures, which preserves multi-language incremental adoption.

### Tests

- PASS: `ruff check src tests`
- PASS: `ruff format --check src tests`
- PASS: `PYTHONPATH=src python -m pytest tests/test_analyzer_orchestration.py tests/test_batch_collection.py tests/test_docs_contracts.py -q`
  - Result: 32 passed
- PASS: `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - Result: 198 passed
  - Coverage: 90.71%
- PASS: `swift package dump-package >/dev/null`
- PASS: `swift build --target SpecHarvesterDocs`
- PASS: local smoke `collect-batch --emit-interface-indexes`
  - Result: Python and JavaScript/TypeScript analyzers executed.
  - Result: merged `PublicInterfaceIndex.summary.status == complete`.

### Next Steps

- No actionable follow-up is required for this task.
- FOLLOW-UP is skipped.
- Verify the PR body matches `.github/PULL_REQUEST_TEMPLATE.md` before opening
  the pull request.
