## REVIEW REPORT — p31_t3_real_selected_candidate_handoff_proposal_dry_run

**Scope:** `codex/p31-t2-selected-candidate-handoff-proposal-helper...HEAD`
**Files:** 19

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

- The P31-T3 fixture is correctly framed as historical producer preview
  evidence, not as live CI input and not as SpecPM authority. The `/tmp` paths
  inside the fixture record the real P30 local artifact provenance from the dry
  run; they are not consumed by tests as required filesystem state.
- The helper improvement to preserve relative dry-run source paths makes the
  committed fixture more portable while still computing SHA-256 digests from
  resolved local files when they exist.
- The generated JSON and Markdown artifacts keep the selected/deferred split
  from P30-T5: only `flask.core`, `gin.core`, and `docc2context.core` proceed
  as selected handoff evidence; the six deferred candidates remain excluded.
- The non-authority boundary remains explicit: no SpecPM PR, package
  acceptance, relation acceptance, baseline seeding, `preview_only` removal, or
  registry publication.

### Tests

- `PYTHONPATH=src pytest tests/test_selected_candidate_handoff_proposal.py tests/test_docs_contracts.py -q`
  passed with `76 passed`.
- `PYTHONPATH=src pytest -q` passed with `644 passed, 1 skipped`.
- `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90`
  passed with total coverage `90.56%`.
- `PYTHONPATH=src ruff check .` passed.
- `PYTHONPATH=src ruff format --check src tests` passed.
- `git diff --check` passed.
- `swift build --target SpecHarvesterDocs` passed.
- Static DocC generation passed with pre-existing unrelated warnings for
  `AcceptedPackageUpdateProposals` and inline command references.
- CLI smoke regenerated the P31-T3 JSON/Markdown output and matched the
  committed JSON fixture.

### Next Steps

- FOLLOW-UP skipped: no actionable findings were found.
- Continue with P31-T4 to define downstream SpecPM-side preflight expectations
  for `SpecHarvesterSelectedCandidateHandoffProposal` evidence.
