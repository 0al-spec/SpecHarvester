## REVIEW REPORT — p16_t5_rerun_local_validation_matrix

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
- P16-T5 is measurement and documentation work; it does not change runtime
  harvesting, drafting, governance, analyzer, or SpecPM proposal behavior.
- The rerun uses ignored `.smoke/` inputs and outputs only.  No generated
  candidates, raw harvest snapshots, run reports, quality reports, or triage
  JSON are committed.
- The P15-T4 to P16-T5 delta is material: total advisory issues dropped from
  12 to 5, namespace issues dropped from 1 to 0, and broad language-neutral
  duplicate intent noise is no longer present in `duplicates.intent`.
- Remaining review signals are explicitly documented:
  `intent.web.request_response_context` remains a possible future semantic
  tightening candidate, and Flask's `collected_unknown_license_evidence` is the
  expected low-severity P16-T2 behavior rather than a regression.

### Tests
- `PYTHONPATH=src python -m spec_harvester source-manifests .smoke/p16-t5-inputs`
  - PASS: 6 repositories validated.
- `PYTHONPATH=src python scripts/run_real_repository_validation.py --inputs .smoke/p16-t5-inputs --out .smoke/output/p16-t5-local-validation --emit-interface-indexes --analyzer-cache-dir .smoke/output/p16-t5-analyzer-cache --skip-specpm-validation`
  - PASS: runner status `ok`, 6 packages collected and drafted.
- `PYTHONPATH=src python -m spec_harvester quality-report --run-report .smoke/output/p16-t5-local-validation/run-report.json --candidates-root .smoke/output/p16-t5-local-validation --output .smoke/output/p16-t5-local-validation/quality-report.json`
  - PASS: 6 pass, 0 review, 0 fail, 0 unscored.
- `PYTHONPATH=/Users/egor/Development/GitHub/0AL/SpecPM/src python -m specpm.cli validate ".smoke/output/p16-t5-local-validation/<id>" --json`
  - PASS with expected warning-only status for all 6 preview candidates.
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
  - PASS: 24 passed.
- `PYTHONPATH=src python -m pytest`
  - PASS: 418 passed, 1 skipped.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 418 passed, 1 skipped, total coverage 91.87%.
- `ruff check src tests`
  - PASS.
- `ruff format --check src tests`
  - PASS: 68 files already formatted.
- `swift package dump-package >/dev/null`
  - PASS.
- `swift build --target SpecHarvesterDocs`
  - PASS.
- `git diff --check`
  - PASS.

### Next Steps
- FOLLOW-UP skipped: no actionable defect in the P16-T5 changeset.
- Continue with `P16-T8` after this PR merges.
