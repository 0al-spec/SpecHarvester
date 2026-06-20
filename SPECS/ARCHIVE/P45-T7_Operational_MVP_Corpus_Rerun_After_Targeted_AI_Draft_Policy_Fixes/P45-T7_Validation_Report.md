# P45-T7 Validation Report

Task: P45-T7 Operational MVP Corpus Rerun After Targeted AI Draft Policy Fixes
Date: 2026-06-20
Branch: `feature/P45-T7-operational-mvp-rerun-after-targeted-ai-draft-policy-fixes`
Verdict: PASS

## Scope

P45-T7 reran the bounded operational MVP corpus after P45-T5 and P45-T6 over
the same pinned local checkouts as P45-T3:

- xyflow `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`;
- FastAPI `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263`;
- Gin `5f4f9643258dc2a65e684b63f12c8d543c936c67`.

Final run root:

```text
/tmp/specharvester-p45-t7-targeted-ai-draft-policy-rerun-20260620T163422Z
```

## Runtime Commands

```bash
PYTHONPATH=src uv run python -m spec_harvester source-manifests /tmp/specharvester-p45-t7-targeted-ai-draft-policy-rerun-20260620T163422Z/inputs
```

Result: PASS, `repositoryCount: 3`.

```bash
PYTHONPATH=src uv run python -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p45-t7-targeted-ai-draft-policy-rerun-20260620T163422Z/inputs --out /tmp/specharvester-p45-t7-targeted-ai-draft-policy-rerun-20260620T163422Z/output-static --skip-ai --repository-profile-selection auto
```

Result: PASS, batch status `passed`.

```bash
PYTHONPATH=src uv run python -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p45-t7-targeted-ai-draft-policy-rerun-20260620T163422Z/inputs --out /tmp/specharvester-p45-t7-targeted-ai-draft-policy-rerun-20260620T163422Z/output-ai --repository-profile-selection auto --lm-studio-base-url http://127.0.0.1:1234 --lm-studio-model openai/gpt-oss-20b --json-repair-max-attempts 1
```

Result: PASS, batch status `passed`.

## Final Result Summary

| Mode | Processed | Failed | Preflight passed | Candidates | Relations | AI draft proposals | AI enrichment proposals |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| static-only | 3 | 0 | 3 | 6 | 3 | 0 | 0 |
| AI-enabled | 3 | 0 | 3 | 6 | 3 | 3 | 3 |

AI-enabled output:

- AI proposal artifacts: 6.
- AI enrichment proposal members: 6.
- AI draft provider total tokens: 19,179.
- AI enrichment provider total tokens: 81,140.
- Raw prompts, raw provider responses, secrets, and chain-of-thought were not
  persisted.
- AI output remained proposal-only and did not change registry truth.

## Comparison Against P45-T3

| Repository | P45-T3 AI draft signal | P45-T7 AI draft signal | Outcome |
| --- | --- | --- | --- |
| xyflow | `selected_member_role_unknown`, continue generation | completed, stop for author review | role and relation target blockers resolved |
| FastAPI | `no_proposal_subjects`, continue generation | `ai_json_repair_needed`, stop for author review | zero-subject policy accepted successful repair as non-blocking |
| Gin | `no_proposal_subjects`, continue generation | completed, stop for author review | zero-subject blocker resolved |

The AI draft layer has no blocking repositories after P45-T7. The remaining
warning is in Gin AI enrichment: `model_evidence_path_unsupported` with two
warning diagnostics. P45-T8 owns the final Phase 46 readiness decision.

## Fixture and Docs Validation

| Command | Result |
| --- | --- |
| `python3 -m json.tool tests/fixtures/operational_mvp_quality_hardening/p45-t7-operational-mvp-targeted-ai-draft-policy-rerun.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'operational_mvp_targeted_ai_draft_policy_rerun or current_next_task'` | PASS, 1 passed, 159 deselected |
| `ruff check tests/test_docs_contracts.py` | PASS |
| `ruff format --check tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |

## Notes

- Earlier P45-T7 live attempts exposed bounded AI draft normalization gaps in
  P45-T6. Those fixes were committed as follow-ups to the P45-T6 branch before
  this final P45-T7 run was recorded.
- P45-T7 does not broaden the corpus, accept packages or relations, publish
  registry metadata, seed baselines, remove `preview_only`, enable trusted
  local adapter execution, or make the Phase 46 readiness decision.
