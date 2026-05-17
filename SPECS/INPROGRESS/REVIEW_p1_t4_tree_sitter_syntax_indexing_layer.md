## REVIEW REPORT — p1_t4_tree_sitter_syntax_indexing_layer

**Scope:** origin/main..HEAD
**Files:** 10

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
- The decision is appropriately conservative: Tree-sitter is recommended as an
  optional future syntax-index backend, not as an immediate replacement for the
  existing Python `ast` and JavaScript/TypeScript manifest/export analyzers.
- The trust boundary remains intact: no Tree-sitter dependency, parser artifact,
  package manager invocation, generated grammar, or analyzer runtime path was
  added in P1-T4.
- The evaluation creates a clear bridge to P1-T5 and P2 analyzer/cache tasks by
  defining parser/query versioning, query hashing, deterministic capture
  ordering, and diagnostics expectations.

### Tests
- `PYTHONPATH=src python -m pytest`: pass, 52 tests.
- `ruff check src tests`: pass.
- `ruff format --check src tests`: pass.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  pass, 52 tests, total coverage 92.27%.
- `swift package dump-package >/dev/null`: pass.
- `swift build --target SpecHarvesterDocs`: pass.
- `git diff --check`: pass.
- Type checking is not configured in `.flow/params.yaml` or `pyproject.toml`.

### Next Steps
- FOLLOW-UP skipped: no actionable review findings.
- Next recommended Flow task remains P1-T5: integrate public interface evidence
  into deterministic drafting.
