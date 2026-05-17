## REVIEW REPORT — p1_t2_python_static_public_api_analyzer

**Scope:** origin/main..HEAD
**Files:** 6

### Summary Verdict
- [ ] Approve
- [ ] Approve with comments
- [x] Request changes
- [ ] Block

### Critical Issues
- [High] `src/spec_harvester/python_public_api.py:50` catches only
  `SyntaxError` from `ast.parse`, but CPython raises `ValueError` for source
  strings containing null bytes. A single malformed `.py` file can therefore
  abort the whole analyzer instead of producing a diagnostic, which violates the
  PRD acceptance criterion that parse errors are recorded as `diagnostics[]`.
  Fix by normalizing non-syntax AST parse failures into the same diagnostic
  shape and add a regression test with a null byte source file.

### Secondary Issues
- None.

### Architectural Notes
- The analyzer otherwise preserves the intended trust boundary: it reads source
  bytes, parses AST, and does not import harvested modules, execute package
  code, run package scripts, or require network access.

### Tests
- Existing validation covers ordinary syntax errors but not AST parse
  `ValueError` cases.
- Coverage threshold was met during EXECUTE: 43 tests, total coverage 92.77%.

### Next Steps
- Add the null byte parse diagnostic regression test.
- Update the analyzer to catch and report `ValueError` from `ast.parse`.
- Re-run targeted analyzer tests and full Flow validation gates before PR.
