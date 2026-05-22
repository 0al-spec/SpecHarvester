# REVIEW REPORT — P13-T1 SpecNode Refinement Prompt Contract

**Scope:** `origin/main..HEAD`
**Files:** 22

## Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

## Critical Issues

- None.

## Secondary Issues

- None.

## Architectural Notes

- The change keeps prompt text as repository-owned contract policy rather than
  an ad-hoc runtime option.
- The prompt contract is positioned between deterministic `refine-preview`
  planning and provider execution, without moving provider calls into
  SpecHarvester.
- The contract explicitly preserves existing authority limits:
  `modelFilesystemAccess: none`, `modelShellAccess: none`, and
  `candidateMutation: proposal_only`.
- Evidence-reference, negative-claim, and confidence-calibration rules address
  the observed weak-model failure mode where output described SpecPM generation
  instead of target package behavior.

## Tests

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
  - PASS: 14 passed
- `PYTHONPATH=src python -m pytest`
  - PASS: 247 passed
- `ruff check src tests`
  - PASS
- `ruff format --check src tests`
  - PASS
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: total coverage 91.22%
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Continue with `P13-T2` to define the clean-context semantic review pass.
