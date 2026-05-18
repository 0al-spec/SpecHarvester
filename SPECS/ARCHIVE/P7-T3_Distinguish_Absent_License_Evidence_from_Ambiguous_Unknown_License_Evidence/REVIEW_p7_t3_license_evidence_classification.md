## REVIEW REPORT - p7_t3_license_evidence_classification

**Scope:** `origin/main..HEAD`
**Files:** 11

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

- License evidence classification is recorded at draft time, where harvest
  snapshot context is still available. The governance report then reads the
  persisted `metadata.licenseEvidence` field instead of inferring intent from
  `UNKNOWN` alone.
- Existing manifests without `metadata.licenseEvidence` retain the legacy
  `unknown_license` path, avoiding invented evidence for older accepted or
  candidate metadata.
- The implementation keeps the trust boundary static: no repository code
  execution, package installation, external SPDX lookup, or network access is
  introduced.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_license_provenance_risk_reports.py -q` - PASS, 63 passed.
- `PYTHONPATH=src python -m pytest` - PASS, 135 passed.
- `ruff check src tests` - PASS.
- `ruff format --check src tests` - PASS.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` - PASS, 90.34% total coverage.
- `swift package dump-package >/dev/null` - PASS.
- `swift build --target SpecHarvesterDocs` - PASS.
- Local smoke license/provenance report - PASS,
  `issuesByCode.absent_license_evidence=1` and no generic `unknown_license` for
  `puzzle.core`.

### Next Steps

- FOLLOW-UP skipped: review found no actionable issues for P7-T3.
- Open a PR using the project pull request template and include the validation
  results above.
