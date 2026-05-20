## REVIEW REPORT — P12-T1 Strict License Filename Compatibility

**Scope:** `main...HEAD`
**Files:** 12
**Date:** 2026-05-21

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

No Blocker or High findings.

### Secondary Issues

No Medium, Low, or Nit findings requiring follow-up.

### Architectural Notes

- License filename recognition is centralized in `is_license_filename`, avoiding
  drift between candidate collection and file classification.
- The accepted filename set remains intentionally allowlisted and text-only:
  `LICENSE`, `COPYING`, and safe textual extensions. This preserves strict
  public registry behavior without broadening to arbitrary binary or misleading
  filenames.
- Strict public mode still treats repositories with no license-like evidence as
  invalid; relaxed-private behavior is unchanged.

### Tests

- `PYTHONPATH=src python -m pytest`: PASS, `209 passed in 3.54s`
- `ruff check src tests`: PASS
- `ruff format --check src tests`: PASS
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`: PASS, coverage `90.60%`
- `swift package dump-package >/dev/null`: PASS
- `swift build --target SpecHarvesterDocs`: PASS
- Flask/Gin local smoke: PASS, strict batch `status: ok`, Flask harvested
  `LICENSE.txt` as license evidence.

### Next Steps

- No actionable review follow-up is required.
- FOLLOW-UP is skipped.
- Before merge, ensure the PR body uses `.github/PULL_REQUEST_TEMPLATE.md` and
  includes the validation summary.
