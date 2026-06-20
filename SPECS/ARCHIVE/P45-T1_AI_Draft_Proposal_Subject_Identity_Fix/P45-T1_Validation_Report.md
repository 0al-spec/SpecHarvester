# P45-T1 Validation Report

Task: AI Draft Proposal Subject Identity Fix

Status: PASS

## Scope

P45-T1 narrows AI draft proposal subject identity warnings by treating safe
producer-side normalization as clean proposal evidence:

- missing `packageSet.packageId` uses the deterministic request package-set id
  without emitting `package_set_id_missing`;
- unknown `excludedPackages` entries are ignored for single-package inventories
  when deterministic package identity is stable;
- unknown exclusions for multi-package inventories still emit
  `excluded_package_unknown`.

## Validation Commands

```bash
PYTHONPATH=src python -m pytest tests/test_package_set_ai_draft_proposal.py -q
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'author_ready_draft_quality_bar or current_next_task'
ruff check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py
ruff format --check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py
git diff --check
```

## Validation Outcomes

- Focused AI draft proposal tests: PASS, `14 passed`
- Focused docs contract: PASS, `1 passed, 156 deselected`
- Ruff lint: PASS
- Ruff format check: PASS
- Whitespace diff check: PASS

## Boundaries

P45-T1 did not broaden the corpus, call hosted AI services, rerun the bounded
operational MVP corpus, accept packages or relations, publish registry metadata,
seed baselines, remove `preview_only`, enable trusted local adapter execution,
execute harvested code, install dependencies, invoke package managers, persist
raw prompts, persist raw provider responses, persist secrets, persist
chain-of-thought, or add Workplan tasks.
