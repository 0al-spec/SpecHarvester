## REVIEW REPORT — P45-T1 AI Draft Subject Identity Fix

**Scope:** `origin/main..HEAD`
**Files:** 10

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

- The implementation keeps the authority boundary intact: model output remains
  proposal-only, and deterministic request/inventory identity remains the source
  used for normalization.
- `package_set_id_mismatch`, selected-member validation, relation validation,
  unsupported evidence-path diagnostics, and multi-package
  `excluded_package_unknown` diagnostics still fail or warn as before.
- Single-package unknown exclusions are now treated as bounded model-side noise
  only when the inventory has one deterministic package subject.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_package_set_ai_draft_proposal.py -q`
  passed with `14 passed`.
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'author_ready_draft_quality_bar or current_next_task or operational_mvp_post_hardening_readiness_decision'`
  passed with `2 passed, 155 deselected`.
- `ruff check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py`
  passed.
- `ruff format --check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py`
  passed.
- `git diff --check` passed.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings were identified.
- Continue with existing Workplan task `P45-T2`; no new Workplan tasks were
  added.
