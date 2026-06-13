## REVIEW REPORT — p31_t2_selected_candidate_handoff_proposal_helper

**Scope:** `codex/p31-t1-selected-candidate-handoff-proposal-contract...HEAD`
**Files:** 16

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

- The helper keeps the correct authority boundary. It emits
  `SpecHarvesterSelectedCandidateHandoffProposal` as
  `producer_preview_evidence_only` review evidence and explicitly records that
  it did not create a SpecPM PR, accept packages, accept relations, seed
  baselines, remove `preview_only`, or publish registry metadata.
- The implementation validates the P30 selected handoff dry-run identity before
  building output and rejects selected candidates with non-passing producer
  preflight, warning/error counts, non-`ok` viewer status, non-preview status,
  or non-`external_required` registry acceptance decisions.
- Local candidate, preflight, and viewer roots are optional. When present, the
  helper resolves local artifacts and emits SHA-256 digests from local files;
  when absent, it preserves the selected dry-run digest evidence. That matches
  the P31-T2 scope and leaves the real artifact fixture run to P31-T3.

### Tests

- `PYTHONPATH=src pytest tests/test_selected_candidate_handoff_proposal.py tests/test_docs_contracts.py -q`
  passed with `73 passed`.
- `PYTHONPATH=src pytest -q` passed with `641 passed, 1 skipped`.
- `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90`
  passed with total coverage `90.55%`.
- `PYTHONPATH=src ruff check .` passed.
- `PYTHONPATH=src ruff format --check src tests` passed.
- `git diff --check` passed.
- `swift build --target SpecHarvesterDocs` passed.
- Static DocC generation passed with pre-existing unrelated warnings for
  `AcceptedPackageUpdateProposals` and inline command references.
- CLI smoke for `selected-candidate-handoff-proposal` passed and produced
  valid JSON plus Markdown handoff body.

### Next Steps

- FOLLOW-UP skipped: no actionable findings were found.
- Continue with P31-T3 to run the helper on the real P30 selected candidate
  artifacts and record a dry-run handoff proposal fixture.
