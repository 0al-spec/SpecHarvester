## REVIEW REPORT — p15_t3_structured_quality_report_format

**Scope:** origin/main..HEAD
**Files:** 13 changed, 1685 insertions(+), 11 deletions(-)
**Branch:** feature/p15-t3-quality-report-format

### Summary Verdict

- [x] Approve

### Critical Issues

None.

### Secondary Issues

**[Low] `_derive_analyzer_coverage` uses a narrow fixed set of field names**

The function checks only four hardcoded keys (`pythonPublicApi`, `jsPublicApi`,
`publicInterface`, `semanticEvidence`) when scanning file entries.  If new
analyzer output types are added (e.g., a Go analyzer field), coverage will
silently read `minimal` instead of `partial` or `strong`.

Fix suggestion: Extend the key list when new analyzer fields are added, or
alternatively scan for any non-standard dict-valued field under each file entry
as a heuristic.  Low priority because the `summary.analyzersUsed` fallback
provides partial relief.

**[Nit] Notes parsing with commas in notes text is fragile**

`_parse_quality_report_notes` splits on `,` to extract `id=` and `notes=`
parts.  A notes value containing a comma (e.g., `"good intent, but thin
evidence"`) will be silently truncated.

Fix suggestion: Use `notes=` as a trailing key by splitting on the first
occurrence of `,notes=` rather than splitting all commas.  Very low priority
as the `@file` JSON shorthand is the recommended path for non-trivial notes.

### Architectural Notes

- The module correctly separates execution report concerns (P15-T2 runner) from
  quality concerns (this task).  The layering is clean.
- All derivation helpers are private; `build_quality_report` and
  `build_package_quality_record` are the stable public surface.  This is the
  right surface area.
- Token usage extraction supports three key-name conventions
  (`tokenUsage.prompt`, `usage.promptTokens`, `usage.input_tokens`), which
  covers the most common SpecNode result shapes.
- `TRUST_BOUNDARY_NOTES` is consistent with the pattern used in `smoke_triage`
  and `specnode_refinement`.
- The `@file` notes shorthand is a convenient affordance for multi-package
  operator annotations.

### Tests

- 55 tests in `tests/test_real_repo_quality_report.py` covering all rating
  derivation helpers, `build_package_quality_record`, `build_quality_report`,
  `write_quality_report`, and full CLI integration.
- 1 new docs contract test in `test_docs_contracts.py`.
- Coverage: 95% on `real_repo_quality_report.py`; overall suite at 90.56%
  (≥90% threshold met).
- The uncovered lines (189, 195-196, 230, 250, 299, 316, 337, 342, 352) are
  defensive branches handling malformed or missing data; they are low risk.

### Next Steps

- The two low-priority findings above (hardcoded analyzer keys, comma-in-notes
  fragility) can become P15-T5 or subsequent follow-up tasks if they surface
  during P15-T4 real-repository matrix runs.
- No PR template mismatch detected.
- FOLLOW-UP: no blocker or high-severity actionable issues → FOLLOW-UP skipped.
