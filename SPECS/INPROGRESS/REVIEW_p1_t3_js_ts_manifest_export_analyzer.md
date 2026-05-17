## REVIEW REPORT — p1_t3_js_ts_manifest_export_analyzer

**Scope:** origin/main..HEAD
**Files:** 7

### Summary Verdict
- [ ] Approve
- [ ] Approve with comments
- [x] Request changes
- [ ] Block

### Critical Issues
- [High] `src/spec_harvester/js_ts_public_api.py:51` recognizes
  `export default` only when the default export is a function/class-style
  declaration. JavaScript and TypeScript commonly use expression defaults such
  as `export default createClient;` or `export default memo(Component);`. The
  PRD acceptance criteria require `export default` support broadly, so these
  entrypoints currently omit a public default export. Add a fallback default
  export scanner that emits `default` with `kind: unknown` when no declaration
  kind is available.
- [Medium] `src/spec_harvester/js_ts_public_api.py:270` reads existing
  entrypoint files without catching `OSError`. If a harvested repository has a
  referenced file that exists but cannot be read, analysis aborts instead of
  recording a diagnostic. This violates the deliverable for unreadable static
  entrypoints. Catch read failures and record an `error` diagnostic for that
  path while continuing the package.

### Secondary Issues
- None.

### Architectural Notes
- The analyzer keeps the intended trust boundary: it reads manifest/source
  bytes and scans static export syntax without invoking Node.js, package
  managers, TypeScript, Babel, dependency resolution, package scripts, or
  network access.
- Regex scanning is intentionally scoped as a first-pass static analyzer; P1-T4
  will evaluate whether Tree-sitter should replace or complement this approach.

### Tests
- Current validation passes but does not cover expression-style default exports
  or read failures from existing entrypoint files.
- Coverage threshold was met during EXECUTE: 48 tests, total coverage 92.24%.

### Next Steps
- Add a regression test for `export default <expression>`.
- Add a regression test for unreadable entrypoint diagnostics.
- Re-run targeted analyzer tests and full Flow validation gates before PR.
