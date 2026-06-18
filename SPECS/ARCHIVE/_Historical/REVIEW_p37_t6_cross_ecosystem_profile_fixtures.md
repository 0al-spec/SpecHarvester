## REVIEW REPORT — P37-T6 Cross-Ecosystem Profile Fixtures

**Scope:** `feature/P37-T5-generic-profile-discovery-hints..HEAD`
**Files:** 21

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

- P37-T6 intentionally adds fixture coverage and documentation rather than a
  new profile plugin implementation.
- The four fixtures are generated from and regression-checked against
  `build_repository_profile_detection`, so they document current selection
  semantics instead of creating a parallel expected-output format.
- The nested and ambiguous fixtures correctly preserve fallback behavior when
  no single high-confidence profile is selected.
- The non-authority boundary remains explicit: fixtures do not accept packages
  or relations, publish registry metadata, remove `preview_only`, or treat
  profile decisions/hints as registry truth.

### Tests

- `PYTHONPATH=src pytest tests/test_repository_profile_detection.py tests/test_docs_contracts.py -q -k 'repository_profile'`
  - `20 passed, 101 deselected`
- `PYTHONPATH=src pytest -q`
  - `755 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - `755 passed, 1 skipped`
  - total coverage `91.15%`
- `PYTHONPATH=src ruff check .`
  - passed
- `PYTHONPATH=src ruff format --check src tests`
  - passed
- `git diff --check`
  - passed
- `swift build --target SpecHarvesterDocs`
  - passed
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/specharvester-p37-t6-architecture-lint.json`
  - advisory `attention`;
  - one existing `manifest_parser_pattern` issue in
    `src/spec_harvester/license_provenance_reports.py`;
  - no P37-T6 file was reported.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Open a stacked PR for P37-T6 after archiving this review.
