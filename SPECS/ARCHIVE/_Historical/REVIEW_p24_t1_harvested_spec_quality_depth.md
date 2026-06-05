## REVIEW REPORT — P24-T1 Harvested Spec Quality Depth

**Scope:** origin/main..HEAD
**Files:** 8

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

- Compatibility evidence intentionally links to the declared `compatibility`
  target instead of undeclared `compatibility.languages.*` or
  `compatibility.platforms.*` targets. This keeps generated candidates aligned
  with current SpecPM validation while still preserving detailed compatibility
  values in `specpm.yaml`.
- Generated candidates remain `preview_only` and maintainer-reviewed; this task
  improves deterministic draft quality without changing registry authority or
  executing package code.
- The existing architecture-lint advisory in
  `src/spec_harvester/license_provenance_reports.py` is unrelated to this
  change and remains a separate cleanup concern.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_collector.py -q -k 'subject_focused_manifest_summary or supports_interfaces_and_compatibility_with_evidence'`
- SpecHarvester draft fixture plus adjacent SpecPM `validate --json`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --backend pylint --path src/spec_harvester --min-lines 8 --output /tmp/spec-harvester-p24-t1-pylint-duplicates.json`
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/spec-harvester-p24-t1-architecture-lint.json`

Coverage is above the configured threshold at `91.56%`.

### Next Steps

- FOLLOW-UP is skipped for this PR: no actionable review findings were found.
- A separate future task can compare the improved draft output against a real
  `xyflow.core` rerun if we want a before/after quality report.
