# P45-T2 Validation Report

## Verdict

PASS on 2026-06-20.

## Scope

Implemented the package-set AI draft proposal validation guard.

The guard is producer-side evidence only. It records a machine-readable
`validationGuard` summary before proposal normalization and reports:

- `package_set_subject_identity_missing` when neither model output nor
  deterministic request context identifies the package set;
- `excluded_package_unknown` for multi-package inventories before unknown
  exclusions can become proposal evidence.

Safe P45-T1 normalization remains clean:

- request-backed missing `packageSet.packageId` passes without
  `package_set_id_missing`;
- single-package model-side unknown exclusions pass without
  `excluded_package_unknown`.

Existing hard failures remain fail-closed through the existing proposal
normalizer:

- package-set id mismatch;
- selected member unknown;
- unsupported relation type;
- invalid relation endpoint.

## Validation Commands

```bash
PYTHONPATH=src python -m pytest tests/test_package_set_ai_draft_proposal.py -q
```

Result: `15 passed in 0.12s`.

```bash
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'author_ready_draft_quality_bar or current_next_task'
```

Result: `1 passed, 156 deselected in 0.04s`.

```bash
ruff check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py
```

Result: `All checks passed!`.

```bash
ruff format --check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py
```

Result: `3 files already formatted`.

```bash
git diff --check
```

Result: passed with no output.

## Boundaries

- Did not rerun the bounded operational MVP corpus; that remains P45-T3.
- Did not broaden the corpus.
- Did not add Workplan tasks.
- Did not call hosted AI services.
- Did not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Did not accept packages, accept relations, publish registry metadata, seed
  baselines, remove `preview_only`, or treat AI output as registry truth.
