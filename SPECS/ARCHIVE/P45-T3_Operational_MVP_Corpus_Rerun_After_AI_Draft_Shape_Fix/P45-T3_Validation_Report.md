# P45-T3 Validation Report

## Verdict

PASS on 2026-06-20.

## Scope

P45-T3 reran the bounded operational MVP corpus after the P45 AI draft shape
fixes:

- xyflow at `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`;
- FastAPI at `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263`;
- Gin at `5f4f9643258dc2a65e684b63f12c8d543c936c67`.

The rerun records static-only and AI-enabled results, compares warning counts
and proposal counts against P44-T4, and preserves proposal-only boundaries.

## Run Root

```text
/tmp/specharvester-p45-t3-ai-draft-shape-rerun-20260620T133739Z
```

## Commands and Results

```bash
curl --silent --show-error --max-time 5 http://127.0.0.1:1234/v1/models
```

Result: provider available; `openai/gpt-oss-20b` listed by LM Studio.

```bash
PYTHONPATH=src uv run python -m spec_harvester source-manifests /tmp/specharvester-p45-t3-ai-draft-shape-rerun-20260620T133739Z/inputs
```

Result: passed, `repositoryCount: 3`.

```bash
PYTHONPATH=src uv run python -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p45-t3-ai-draft-shape-rerun-20260620T133739Z/inputs --out /tmp/specharvester-p45-t3-ai-draft-shape-rerun-20260620T133739Z/output-static --skip-ai --repository-profile-selection auto
```

Result: passed.

```bash
PYTHONPATH=src uv run python -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p45-t3-ai-draft-shape-rerun-20260620T133739Z/inputs --out /tmp/specharvester-p45-t3-ai-draft-shape-rerun-20260620T133739Z/output-ai --repository-profile-selection auto --lm-studio-base-url http://127.0.0.1:1234 --lm-studio-model openai/gpt-oss-20b --json-repair-max-attempts 1
```

Result: passed.

```bash
python3 -m json.tool tests/fixtures/operational_mvp_quality_hardening/p45-t3-operational-mvp-ai-draft-shape-rerun.example.json >/dev/null
```

Result: passed.

```bash
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'operational_mvp_ai_draft_shape_rerun or current_next_task'
```

Result: `1 passed, 157 deselected in 2.27s`.

```bash
ruff check tests/test_docs_contracts.py
```

Result: `All checks passed!`.

```bash
ruff format --check tests/test_docs_contracts.py
```

Result: `1 file already formatted`.

```bash
git diff --check
```

Result: passed with no output.

## Rerun Summary

| Mode | Processed | Failed | Preflight passed | Candidates | Relations | AI draft proposals | AI enrichment proposals |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| static-only | 3 | 0 | 3 | 6 | 3 | 0 | 0 |
| AI-enabled | 3 | 0 | 3 | 6 | 3 | 3 | 3 |

AI-enabled output produced 6 proposal artifacts and 6 enrichment proposal
members. AI enrichment was not applied into preview candidates.

Token summary:

- AI draft provider total tokens: 17,837;
- AI enrichment provider total tokens: 80,994.

## Warning Comparison Against P44-T4

| Repository | P44-T4 AI draft warnings | P45-T3 AI draft warnings | Result |
| --- | --- | --- | --- |
| xyflow | `package_set_id_missing` | `selected_member_role_unknown` | changed, not resolved |
| FastAPI | `package_set_id_missing` | none | resolved |
| Gin | `excluded_package_unknown` | none | resolved |

Summary:

- old identity/unknown-exclusion warning class resolved across all three
  repositories;
- warning repository count fell from 3 to 1;
- warning diagnostic count stayed 3 because xyflow has three
  `selected_member_role_unknown` diagnostics;
- FastAPI and Gin draft proposals are diagnostic-clean but have stop-policy
  reason `no_proposal_subjects`;
- P45-T3 is ready to feed P45-T4 readiness evaluation but does not itself make
  the readiness decision.

## Boundaries

P45-T3 did not broaden the corpus, clone or fetch repositories, install
dependencies, invoke package managers, execute harvested code, enable trusted
local adapter execution, apply AI enrichment, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, persist raw
prompts, persist raw provider responses, persist secrets, persist
chain-of-thought, treat AI output as registry truth, or add Workplan tasks.
