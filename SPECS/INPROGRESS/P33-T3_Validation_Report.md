# P33-T3 Validation Report

Task: P33-T3 Deterministic Next-Corpus Dry Run
Date: 2026-06-13
Verdict: PASS

## Dry Run

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p33-next-corpus \
  --out /tmp/specharvester-p33-t3.QV2pVD/deterministic \
  --skip-ai
```

Source manifest digest:

```text
inputs/p33-next-corpus/repositories.yml sha256:72f3064da9f455c069a5fef6eb25321b74a7e075c5287edcede108a0f4cbed75
```

Generated report digests:

```text
autonomous-candidate-batch-report.json sha256:ffcf06735fac8945f8633250b5761af3a233aca7450ce1a18e858aaccfced282
reports/batch-validation-report.json   sha256:ef177176f518d3a5ae9db9ef28b6ed8ac59376cd1f02653a6d0f69b230ab550d
```

Summary:

- processed repositories: 5;
- collected repositories: 5;
- failed repositories: 0;
- generated preview candidates: 5;
- relation proposals: 0;
- passed bundle-set preflights: 5;
- preflight errors/warnings: 0/0;
- AI draft/enrichment: skipped for all repositories;
- author-ready stop policy: `author_ready_draft` and
  `stop_for_author_review` for all repositories.

Repository outcomes:

| Repository | Manifest package id | Candidate ids | Preflight | Proceed to P33-T4 |
| --- | --- | --- | --- | --- |
| `serena` | `serena.core` | `serena.core` | `passed` | yes |
| `transmission` | `transmission.core` | `transmission.core` | `passed` | yes |
| `mcpm-sh` | `mcpm.core` | `mcpm.system` | `passed` | yes |
| `specgraph` | `specgraph.core` | `specgraph.system` | `passed` | yes |
| `specpm` | `specpm.core` | `specpm.core` | `passed` | yes |

Review signals:

- `mcpm-sh`: `package_id_hint_changed_by_package_set_selection` because the
  manifest hint is `mcpm.core`, while deterministic drafting produced
  `mcpm.system`.
- `specgraph`: `package_id_hint_changed_by_package_set_selection` because the
  manifest hint is `specgraph.core`, while deterministic drafting produced
  `specgraph.system`.

These are not P33-T3 blockers. They should be handled during P33-T5
candidate-layer triage.

## Validation Commands

```bash
PYTHONPATH=src python -m spec_harvester source-manifests inputs/p33-next-corpus
```

Result: passed; status `ok`, repository count `5`.

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
```

Result: passed; `79 passed`.

```bash
PYTHONPATH=src python -m pytest -q
```

Result: passed; `655 passed, 1 skipped`.

```bash
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result: passed; `655 passed, 1 skipped`, total coverage `90.56%`.

```bash
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
```

Result: passed.

```bash
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
```

Result: passed.

```bash
swift package --allow-writing-to-directory ./.docc-build \
  generate-documentation \
  --target SpecHarvesterDocs \
  --output-path ./.docc-build \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester
```

Result: passed. The temporary `.docc-build` directory was removed after
validation.

## Boundary Check

P33-T3 did not run live local-model draft/enrichment, clone repositories, fetch
remote state, install dependencies, execute harvested code, run package
scripts, publish registry metadata, accept packages, accept relations, seed
baselines, remove `preview_only`, create a SpecPM pull request, or treat AI
output as registry truth.

## Next Step

P33-T4 should run the same five-repository manifest through live local-model
draft/enrichment with bounded JSON repair and provider receipts.
