## REVIEW REPORT — P31-T4 Selected Candidate Handoff Preflight Expectations

**Scope:** `codex/p31-t3-real-selected-candidate-handoff-proposal-dry-run...HEAD`
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

- The change keeps the boundary correctly scoped: SpecHarvester documents the
  downstream SpecPM preflight expectations, but does not implement a SpecPM
  command or grant acceptance authority to producer evidence.
- The new contract explicitly keeps
  `SpecHarvesterSelectedCandidateHandoffProposal` as
  `producer_preview_evidence_only` review evidence. A future
  `SpecPMSelectedCandidateHandoffPreflightReport` may check consistency, but a
  pass still does not accept packages, accept relations, seed baselines, remove
  `preview_only`, publish registry metadata, or create/merge a SpecPM pull
  request.
- The P31-T5 follow-up is appropriate because deferred P30 candidates still need
  regeneration requirements before they can enter selected handoff.

### Tests

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q` passed with
  `69 passed`.
- `PYTHONPATH=src pytest -q` passed with `645 passed, 1 skipped`.
- Coverage passed at `90.56%`, above the 90% gate.
- Ruff, format, diff-check, Swift build, and DocC generation passed. DocC
  generation emitted only pre-existing unrelated warnings for
  `AcceptedPackageUpdateProposals` and `RealRepositoryQualityReport`.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Continue with `P31-T5 Deferred Selected Candidate Regeneration Requirements`.
