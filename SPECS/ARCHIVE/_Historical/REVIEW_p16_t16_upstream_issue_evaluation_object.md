## REVIEW REPORT — P16-T16 Upstream Issue Evaluation Object

**Scope:** `origin/main..HEAD`
**Files:** 9

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

- `UpstreamIssuePolicy` now owns upstream artifact parsing, namespace matching,
  duplicate detection, and report-specific issue severity mapping.
- `namespace_reports.py` keeps the previous upstream parsing and normalization
  names re-exported for existing callers while delegating implementation to the
  new behavior-rich object.
- `license_provenance_reports.py` now uses the same upstream issue evaluator
  instead of duplicating verified-upstream checks locally.
- `pylint` duplicate-code remains at zero duplicate blocks. The builtin
  duplicate-code backend now reports seven advisory windows, all within
  `real_repo_quality_report.py`; this is tracked by P16-T17.
- Architecture lint still reports the pre-existing advisory
  `manifest_parser_pattern` in `license_provenance_reports.py`.

### Tests

- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 411 passed, 1 skipped, total coverage 91.76%.
- `ruff check src tests`
  - PASS.
- `ruff format --check src tests`
  - PASS: 67 files already formatted.
- `swift package dump-package >/dev/null`
  - PASS.
- `swift build --target SpecHarvesterDocs`
  - PASS.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t16-dup-builtin.json`
  - ATTENTION: `duplicateBlockCount=7`, `duplicateOccurrenceCount=14`; all
    occurrences are in `src/spec_harvester/real_repo_quality_report.py`.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t16-dup-pylint.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`.
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t16-architecture-lint.json`
  - ATTENTION: one existing advisory `manifest_parser_pattern`.

### Next Steps

- FOLLOW-UP skipped: no new actionable issues were found during review.
- Continue with P16-T17 to remove the remaining builtin duplicate-code windows
  from `real_repo_quality_report.py`.
