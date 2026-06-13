# P30-T1 Validation Report

Task: `P30-T1 Limited Popular-Library Corpus Plan`

Verdict: `PASS`

## Implemented

- Added `docs/LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md`.
- Added DocC mirror `LimitedPopularLibraryCorpusPlan`.
- Added `inputs/limited-popular-libraries.example.yml` with six pinned seed
  corpus entries:
  - `flask -> flask.core`
  - `gin -> gin.core`
  - `xyflow -> xyflow.workspace`
  - `cupertino -> cupertino.core`
  - `navigation-split-view -> navigation-split-view.core`
  - `docc2context -> docc2context.core`
- Fixed `inputs/repositories.example.yml` so the example input directory parses
  with the current repository source manifest reader.
- Updated docs index, DocC root, Roadmap, Workplan, and `next.md`.
- Added docs-contract coverage for the P30 plan, source manifest, and Flow
  pointers.

## Validation

| Gate | Result |
| --- | --- |
| `PYTHONPATH=src python -m spec_harvester source-manifests inputs` | passed; `repositoryCount: 7` |
| `PYTHONPATH=src pytest tests/test_docs_contracts.py -q` | `57 passed` |
| `PYTHONPATH=src pytest -q` | `625 passed, 1 skipped` |
| `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | `625 passed, 1 skipped`; coverage `90.58%` |
| `PYTHONPATH=src ruff check .` | passed |
| `PYTHONPATH=src ruff format --check src tests` | passed |
| `git diff --check` | passed |
| `swift build --target SpecHarvesterDocs` | passed |
| `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` | passed with pre-existing unrelated DocC warnings for `AcceptedPackageUpdateProposals` |

## Product Boundary

P30-T1 is a planning and manifest task only. It does not run the larger corpus,
call LM Studio, accept packages, accept relations, seed baselines, publish
registry metadata, remove `preview_only`, or convert generated preview evidence
into accepted SpecPM truth.

The next executable task is `P30-T2`: run deterministic `--skip-ai` scraping
over the selected limited corpus and record outcomes.
