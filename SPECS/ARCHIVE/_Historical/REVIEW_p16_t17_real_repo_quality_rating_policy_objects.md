## REVIEW REPORT — P16-T17 Real Repository Quality Rating Policy Objects

**Scope:** `origin/main..HEAD`
**Files:** 8

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

- `DraftRatingPreflight` now owns the shared dry-run, draft-step, missing-artifact,
  and candidate-payload checks that were previously duplicated between intent
  and capability scoring.
- `IntentRatingPolicy` and `CapabilityRatingPolicy` keep the dimension-specific
  scoring rules isolated while preserving the old `_derive_*` helper entrypoints.
- `real_repo_quality_report.py` continues to expose the quality rating literal
  names via imports, preserving existing tests and caller imports.
- Both duplicate-code backends now report zero duplicate blocks for
  `src/spec_harvester`.
- Architecture lint still reports the pre-existing advisory
  `manifest_parser_pattern` in `license_provenance_reports.py`.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_real_repo_quality_report.py -q`
  - PASS: 77 passed.
- `PYTHONPATH=src python -m pytest`
  - PASS: 415 passed, 1 skipped.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 415 passed, 1 skipped, total coverage 91.85%.
- `ruff check src tests`
  - PASS.
- `ruff format --check src tests`
  - PASS: 68 files already formatted.
- `swift package dump-package >/dev/null`
  - PASS.
- `swift build --target SpecHarvesterDocs`
  - PASS.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t17-dup-builtin.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t17-dup-pylint.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`.
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t17-architecture-lint.json`
  - ATTENTION: one existing advisory `manifest_parser_pattern`.

### Next Steps

- FOLLOW-UP skipped: review found no new actionable issues.
- Continue with P16-T18 to archive the practical-minimum duplicate-code baseline
  and decide whether the current duplication goal can be closed after CI.
