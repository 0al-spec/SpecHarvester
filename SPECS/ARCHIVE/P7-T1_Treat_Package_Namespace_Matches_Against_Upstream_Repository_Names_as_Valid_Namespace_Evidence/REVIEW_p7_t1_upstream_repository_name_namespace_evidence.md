## REVIEW REPORT - p7_t1_upstream_repository_name_namespace_evidence

**Scope:** `origin/main..HEAD`  
**Files:** 9

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

- GitHub upstream parsing now produces both owner and repository name while
  keeping the existing owner-only helper for compatibility.
- Namespace evidence is still intentionally narrow: only GitHub HTTPS/HTTP and
  SSH forms supported before this task are accepted.
- Namespace/upstream and license/provenance reports share the same matching
  helper, avoiding drift between governance surfaces.
- The local smoke signal that created this task is resolved:
  `namespace-upstream.json` reports `issueCount=0` and license/provenance no
  longer echoes namespace mismatch issues.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_namespace_upstream_reports.py tests/test_license_provenance_risk_reports.py -q`:
  PASS, 14 passed.
- `PYTHONPATH=src python -m pytest`: PASS, 125 passed.
- `ruff check src tests`: PASS.
- `ruff format --check src tests`: PASS.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  PASS, total coverage 90.33%.
- `swift package dump-package >/dev/null`: PASS.
- `swift build --target SpecHarvesterDocs`: PASS.

### Next Steps

- No actionable follow-up tasks.
- FOLLOW-UP skipped.
- Continue with `P7-T2` after this PR is merged.
