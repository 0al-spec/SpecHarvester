# P45-T5 Validation Report

Task: P45-T5 Selected-Member Role Taxonomy Hardening
Date: 2026-06-20
Branch: `feature/P45-T5-selected-member-role-taxonomy-hardening`
Verdict: PASS

## Scope

P45-T5 tightened the package-set AI draft selected-member role contract. The
implementation now normalizes canonical proposal roles, adjacent inventory and
profile roles, and common model labels before selected members are written as
proposal evidence. Unsupported labels remain warning-level
`selected_member_role_unknown` diagnostics and fall back to `member_package` in
the selected-member record.

## Validation Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_package_set_ai_draft_proposal.py -q` | PASS, 18 passed |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py::test_docc_and_github_docs_cover_specpm_shared_fixture_policy -q` | PASS, 1 passed |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py::test_docc_and_github_docs_cover_author_ready_draft_quality_bar -q` | PASS, 1 passed |
| `ruff check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py` | PASS |
| `ruff format --check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |

## Notes

- P45-T5 does not run the bounded operational MVP corpus. P45-T7 owns that
  evidence after P45-T5 and P45-T6 are both complete.
- P45-T5 does not change the single-package `no_proposal_subjects` stop policy.
  P45-T6 owns that decision.
- AI sidecars remain proposal-only and do not mutate registry truth, accept
  packages, accept relations, or persist raw prompts, raw responses, secrets, or
  chain-of-thought.
