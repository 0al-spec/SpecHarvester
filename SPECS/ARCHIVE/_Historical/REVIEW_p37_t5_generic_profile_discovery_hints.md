## REVIEW REPORT — P37-T5 Generic Profile Discovery Hints

**Scope:** `origin/main..HEAD`
**Files:** 20

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

- The new `repository_profile_hints` module is intentionally small and
  schema-focused. It defines stable producer-side vocabulary constants,
  non-authority statements, a fixture builder, and validation for built-in hint
  ids.
- Existing repository profile detection keeps its current behavior and now
  validates emitted hint ids through the canonical vocabulary.
- The change does not apply hints to drafting, package acceptance, relation
  acceptance, registry publication, or `preview_only` removal.
- The next planned task, P37-T6, should prove the same selection/hint contract
  against multiple repository shapes instead of adding ecosystem-specific
  plugins prematurely.

### Tests

- `PYTHONPATH=src pytest tests/test_repository_profile_detection.py tests/test_docs_contracts.py -q -k 'repository_profile'`
  - `14 passed, 101 deselected`
- `PYTHONPATH=src pytest -q`
  - `749 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - `749 passed, 1 skipped`
  - total coverage `91.13%`
- `PYTHONPATH=src ruff check .`
  - passed
- `PYTHONPATH=src ruff format --check src tests`
  - passed
- `git diff --check`
  - passed
- `swift build --target SpecHarvesterDocs`
  - passed
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/specharvester-p37-t5-architecture-lint.json`
  - advisory `attention`;
  - one existing `manifest_parser_pattern` issue in
    `src/spec_harvester/license_provenance_reports.py`;
  - no P37-T5 file was reported.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Open a stacked PR for P37-T5 after archiving this review.
