# P30-T2 Validation Report

Task: `P30-T2 Deterministic Limited Corpus Batch`
Branch: `codex/p30-t2-deterministic-limited-corpus-batch`
Date: 2026-06-13

## Deterministic Batch

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --out /tmp/specharvester-p30-t2.7rNeq2/deterministic \
  --skip-ai
```

Result:

- status: `passed`;
- processed repositories: `6`;
- collected repositories: `6`;
- failed repositories: `0`;
- generated preview candidates: `9`;
- relation proposals: `3`;
- passed bundle-set preflights: `6`;
- skipped package records: `7`;
- AI draft: `skipped` for all repositories;
- AI enrichment: `skipped` for all repositories.

Report digests:

```text
autonomous-candidate-batch-report.json sha256:f2e6ad92cb9a6686e8d7bf333b173aeb91dd7d3005c955da7dece5cda620500c
batch-validation-report.json           sha256:ef81c8a2f8a4b7a720f19112bd46b72c96e5c9ff07695c9591221950e58c29f5
```

## Repository Outcomes

| Repository | Manifest package id | Candidate ids | Candidates | Relations | Preflight | Author-ready decision |
| --- | --- | --- | ---: | ---: | --- | --- |
| `flask` | `flask.core` | `flask.core` | 1 | 0 | `passed` | `stop_for_author_review` |
| `gin` | `gin.core` | `gin.core` | 1 | 0 | `passed` | `stop_for_author_review` |
| `xyflow` | `xyflow.workspace` | `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system` | 4 | 3 | `passed` | `stop_for_author_review` |
| `cupertino` | `cupertino.core` | `cupertino.core` | 1 | 0 | `passed` | `stop_for_author_review` |
| `navigation-split-view` | `navigation-split-view.core` | `navigation_split_view.core` | 1 | 0 | `passed` | `stop_for_author_review` |
| `docc2context` | `docc2context.core` | `docc2context.core` | 1 | 0 | `passed` | `stop_for_author_review` |

## Product Finding

The deterministic batch is ready for P30-T3 live LM Studio comparison, but one
candidate-layer review item must stay visible for P30-T4 triage:

- `package_id_hint_mismatch`: the `navigation-split-view.core` manifest hint
  normalized to generated candidate id `navigation_split_view.core`.

This does not block P30-T3 because the generated candidate validates and
bundle-set preflight passed. It does block treating the deterministic result as
automatic SpecPM intake.

## Quality Gates

- `PYTHONPATH=src python -m spec_harvester source-manifests inputs/limited-popular-libraries` -> `ok`, `repositoryCount: 6`
- `python -m json.tool tests/fixtures/limited_popular_library_deterministic_batch/p30-t2-limited-popular-libraries.example.json` -> passed
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q` -> `59 passed`
- `PYTHONPATH=src python -m pytest -q` -> `627 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` -> `627 passed, 1 skipped`, coverage `90.58%`
- `PYTHONPATH=src ruff check .` -> passed
- `PYTHONPATH=src ruff format --check src tests` -> passed
- `git diff --check` -> passed
- `swift package dump-package >/tmp/specharvester-p30-t2-package.json` -> passed
- `swift build --target SpecHarvesterDocs` -> passed
- `swift package --allow-writing-to-directory /tmp/specharvester-p30-t2-docc-build-spec generate-documentation --target SpecHarvester --output-path /tmp/specharvester-p30-t2-docc-build-spec --transform-for-static-hosting --hosting-base-path SpecHarvester` -> passed with pre-existing unrelated DocC warnings about `AcceptedPackageUpdateProposals`.

## Boundary Check

P30-T2 remains producer preview evidence only:

- no AI provider call;
- no repository clone or fetch;
- no dependency installation;
- no harvested package execution;
- no package acceptance;
- no relation acceptance;
- no baseline seeding;
- no registry publication;
- no `preview_only` removal.
