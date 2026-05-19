## REVIEW REPORT — P10-T2 Manifest-First Ecosystem Detectors

**Scope:** `origin/main..HEAD`
**Files:** 8

### Summary Verdict

- [ ] Approve
- [x] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

- None found.

### Secondary Issues

- [Low] `Makefile` is a weak language signal when it appears without CMake,
  Meson, Conan, vcpkg, or source-language evidence. Treating it as high
  confidence C/C++ can overstate the profile for repositories that use make as
  a generic task runner. Fix: keep `Makefile` as make ecosystem evidence but
  lower its confidence.

### Architectural Notes

- The detector table centralizes manifest-to-profile mapping and keeps P10-T2
  manifest-first. No package scripts, build systems, package managers, or
  network probes are executed.
- Most detector entries are path/name based. That is acceptable for this task
  because richer parsing and external classifier evaluation belong to later
  P10 tasks.
- `workspace_manifest` records now participate in `ProjectProfile` while
  preserving existing file classification behavior.

### Tests

- `ruff check src tests`: passed.
- `ruff format --check src tests`: passed.
- `PYTHONPATH=src python -m pytest tests/test_collector.py -q`: passed, 63 tests.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`: passed, 182 tests, 90.71% coverage.
- `swift package dump-package >/dev/null`: passed.
- `swift build --target SpecHarvesterDocs`: passed.

### Next Steps

- Apply the low-confidence `Makefile` follow-up before opening the PR.
- Before merge, ensure the PR body follows `.github/PULL_REQUEST_TEMPLATE.md`.
