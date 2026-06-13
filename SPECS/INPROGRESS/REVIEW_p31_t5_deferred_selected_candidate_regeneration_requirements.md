## REVIEW REPORT — P31-T5 Deferred Selected Candidate Regeneration Requirements

**Scope:** `codex/p31-t4-selected-candidate-handoff-preflight-expectations...HEAD`
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

- The change keeps P31-T5 correctly scoped as a regeneration-requirements
  contract. It does not regenerate candidates, rerun LM Studio or SpecNode,
  create selected handoff artifacts, or mutate SpecPM state.
- The fixture is useful because it records the three distinct deferred
  candidate classes separately: package-set identity regeneration,
  warning-bearing enrichment regeneration, and identity-drift resolution.
- The fixture verifies source digests against P30-T4, P30-T5, and P31-T3
  recorded evidence. That makes the requirement contract traceable to the
  actual selected/deferred split rather than a new self-contained assertion.
- The non-authority boundary is preserved: this remains producer preview
  evidence and does not accept packages, accept relations, seed baselines,
  remove `preview_only`, publish registry metadata, or create a SpecPM pull
  request.

### Tests

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q` passed with
  `70 passed`.
- `PYTHONPATH=src pytest -q` passed with `646 passed, 1 skipped`.
- Coverage passed at `90.56%`, above the 90% gate.
- Ruff, format, diff-check, Swift build, and DocC generation passed. DocC
  generation emitted only pre-existing unrelated warnings for
  `AcceptedPackageUpdateProposals` and `RealRepositoryQualityReport`.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Phase 31 is complete. The next operator should choose a new task from the
  remaining backlog rather than extending Phase 31 implicitly.
