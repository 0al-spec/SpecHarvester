## REVIEW REPORT — P45-T5 Selected-Member Role Taxonomy Hardening

**Scope:** `origin/main..HEAD`
**Files:** 10

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

- The implementation keeps role normalization inside the package-set AI draft
  proposal normalizer. That is the right boundary because the model output
  remains proposal-only, while deterministic inventory and downstream SpecPM
  acceptance stay authoritative.
- Unknown model roles still produce `selected_member_role_unknown`, but the
  selected-member record now falls back to a canonical `member_package` role.
  This avoids leaking arbitrary model vocabulary to downstream consumers while
  retaining author-review evidence.
- P45-T6 remains a separate stop-policy change. P45-T5 does not reinterpret
  zero-subject single-package proposals or change `no_proposal_subjects`.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_package_set_ai_draft_proposal.py -q`
  passed with 18 tests.
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py::test_docc_and_github_docs_cover_specpm_shared_fixture_policy -q`
  passed.
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py::test_docc_and_github_docs_cover_author_ready_draft_quality_bar -q`
  passed.
- `ruff check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py`
  passed.
- `ruff format --check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py`
  passed.
- `git diff --check` passed.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Continue to P45-T6 for the single-package `no_proposal_subjects` policy.
