## REVIEW REPORT — P15-T1 Real-Repository Refinement Validation Plan

**Scope:** origin/main..HEAD
**Files:** 12
**Date:** 2026-05-23

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

- None.

### Secondary Issues

- [Medium] `docs/REAL_REPOSITORY_REFINEMENT_VALIDATION.md` and the DocC mirror
  used unsupported source-manifest keys in the example: `package_id` and
  `strict_public`. The implemented manifest parser accepts `packageId`, and
  strict/relaxed mode is a `collect-batch` CLI policy rather than a manifest
  key. Fix: use `packageId` and document that strict public mode is the default
  while `--relaxed-private` is explicit.

### Architectural Notes

- The SpecNode boundary is correctly stated as external: SpecHarvester validates
  and reports contract-facing artifacts, but does not own SpecNode runtime,
  provider discovery, model execution, scheduling, provider lifecycle, or
  provider-specific orchestration.
- The routing table is useful for two-repository work: SpecHarvester issues stay
  in this Workplan, SpecNode protocol/runtime issues become SpecNode work, and
  Platform remains limited to workspace catalog, launch profile, topology, and
  provider wiring concerns.
- `.0al` remains a local coordination ledger rather than canonical product
  behavior.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q` — PASS,
  17 passed after correcting the manifest key guidance.
- `ruff format --check src tests` — PASS.
- `git diff --check` — PASS.
- Full quality gates were recorded in
  `SPECS/ARCHIVE/P15-T1_Real_Repository_Refinement_Validation_Plan/P15-T1_Validation_Report.md`.

### Next Steps

- FOLLOW-UP completed: the manifest example correction was applied in the
  GitHub and DocC validation plan, with docs contract coverage for `packageId`
  and `--relaxed-private`.
- Full Flow quality gates were rerun after the correction.
