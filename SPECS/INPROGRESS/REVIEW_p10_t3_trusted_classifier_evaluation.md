## REVIEW REPORT — P10-T3 Trusted Classifier Evaluation

**Scope:** `origin/main..HEAD`
**Files:** 16
**Date:** 2026-05-19

### Summary Verdict

- [ ] Approve
- [x] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

- None.

### Secondary Issues

- [Low] `scancode-toolkit` currently records `license.spdx: Apache-2.0`, but
  the upstream repository exposes mixed top-level license materials and GitHub
  license metadata reports `NOASSERTION`. Because the P10-T3 decision is
  `deferred`, the registry should avoid implying a completed license decision.
  Fix: record `NOASSERTION` and mention Apache-2.0 plus CC-BY-4.0 source
  materials in the notes.
- [Low] The DocC mirror covers the trusted classifier contract but omits the
  external source reference list present in the GitHub-facing document. Fix:
  add the same source links to `TrustedClassifierEvaluation.md` so the DocC
  mirror remains useful on GitHub Pages.

### Architectural Notes

- The full registry is machine-readable in `spec_harvester.classifier_registry`,
  while `harvest.json` emits only a compact registry summary. This is the right
  direction for token economy: governance notes are available when needed but
  routine harvest context stays compact.
- `classifierPolicy.defaultMode == disabled` and `allowedExecutions == ["none"]`
  preserve the existing trust boundary. Future adapters should require an
  explicit policy change before any external process can run.

### Tests

- PASS: `ruff check src tests`
- PASS: `ruff format --check src tests`
- PASS: `PYTHONPATH=src python -m pytest tests/test_classifier_registry.py tests/test_collector.py tests/test_docs_contracts.py -q`
  - Result: 74 passed
- PASS: `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - Result: 188 passed
  - Coverage: 90.70%
- PASS: `swift package dump-package >/dev/null`
- PASS: `swift build --target SpecHarvesterDocs`

### Next Steps

- Run FOLLOW-UP for the two low-severity documentation/registry precision
  issues before opening the PR.
- Verify the PR body matches `.github/PULL_REQUEST_TEMPLATE.md`.
