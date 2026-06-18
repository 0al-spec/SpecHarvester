## REVIEW REPORT — P37-T3 Repository Profile Detection CLI

**Scope:** `feature/P37-T2-repository-profile-detection-fixture..HEAD`
**Files:** 13

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

- The new `repository-profile-detect` command is correctly bounded as a
  producer-side report surface. It does not alter autonomous candidate batch
  behavior yet, so P37-T4 remains a separate integration task.
- The implementation reads only explicit CLI/source-manifest metadata and
  operator-supplied evidence paths. It does not collect source files, invoke
  analyzers, run package managers, call AI, or draft packages.
- The artifact shape remains aligned with P37-T2:
  `SpecHarvesterRepositoryProfileDetection`,
  `producer_profile_selection_only`, selected/fallback profiles, candidates,
  rejected profiles, diagnostics, advisory hints, and non-authority
  statements.
- The simple static scoring is intentionally conservative and generic. Future
  ecosystem-specific profile rules should arrive through P37-T5/P37-T6 rather
  than expanding this command into a hidden plugin registry.

### Tests

- `PYTHONPATH=src pytest tests/test_repository_profile_detection.py -q` -> `6 passed`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile_detection_fixture or repository_profile_selection_contract or current_next_task'` -> `2 passed, 102 deselected`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py tests/test_repository_profile_detection.py -q` -> `110 passed`
- CLI smoke for `repository-profile-detect` with `--output` -> stdout and output JSON matched
- `PYTHONPATH=src pytest -q` -> `741 passed, 1 skipped`
- `PYTHONPATH=src ruff check .` -> passed
- `PYTHONPATH=src ruff format --check src tests` -> passed
- `git diff --check` -> passed
- `swift build --target SpecHarvesterDocs` -> passed
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` -> `741 passed, 1 skipped`, total coverage `91.06%`

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Continue with `P37-T4 Repository Profile Batch Integration`.
