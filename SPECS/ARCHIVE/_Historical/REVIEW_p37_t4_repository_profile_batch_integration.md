## REVIEW REPORT — P37-T4 Repository Profile Batch Integration

**Scope:** `main..HEAD`
**Files:** 18

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

None.

### Secondary Issues

None outstanding.

During review, one consistency issue was found and fixed before this report was
finalized: top-level `repositoryProfileSelection.mode` now uses the same
trimmed selection value as the emitted `SpecHarvesterRepositoryProfileDetection`
artifact.

### Architectural Notes

- The integration preserves the existing autonomous batch drafting path.
- Profile detection artifacts are written under `reports/` rather than
  `package-sets/`, so they do not make package-set draft directories non-empty
  before drafting.
- `package.json` is treated as workspace evidence only at repository root. This
  avoids accidentally counting nested member package manifests as workspace
  manifests.
- Profile decisions remain producer-side evidence only:
  `advisoryHintsAppliedToDrafting: false`.

### Tests

Validation evidence is recorded in
`SPECS/ARCHIVE/P37-T4_Repository_Profile_Batch_Integration/Validation_Report.md`.

Most relevant checks:

- `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py tests/test_repository_profile_detection.py -q`
  -> `21 passed`.
- `PYTHONPATH=src pytest -q`
  -> `746 passed, 1 skipped`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  -> `746 passed, 1 skipped`, coverage `91.12%`.
- `PYTHONPATH=src ruff check .`
  -> passed.
- `PYTHONPATH=src ruff format --check src tests`
  -> passed.
- `git diff --check`
  -> passed.
- `swift build --target SpecHarvesterDocs`
  -> passed.

Architecture lint was also run and reported one existing unrelated advisory in
`src/spec_harvester/license_provenance_reports.py`.

### Next Steps

FOLLOW-UP is skipped: there are no actionable review findings for this task.

Proceed to `P37-T5 Generic Profile Discovery Hints`.
