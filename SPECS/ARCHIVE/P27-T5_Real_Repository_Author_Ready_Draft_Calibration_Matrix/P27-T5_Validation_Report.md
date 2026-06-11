# P27-T5 Validation Report

Verdict: PASS
Date: 2026-06-12

## Scope

P27-T5 added a product calibration layer for author-ready drafts:

- `SpecHarvesterAuthorReadyCalibrationMatrix`
- `author-ready-calibration-matrix` CLI command
- optional author notes for manual edit estimates
- real repository calibration documentation for six pinned local checkouts
- GitHub docs, DocC, roadmap, workflow, and docs-contract coverage

The matrix translates `SpecHarvesterRealRepositoryQualityReport` rows into
author-facing work estimates: `authorReadyStatus`, `estimatedAuthorEdits`,
`editCategories`, `reviewPriority`, and generator follow-up reasons.

## Real Repository Calibration Run

Local run path:

```text
.smoke/p27-t5-inputs
  -> scripts/run_real_repository_validation.py
  -> quality-report
  -> author-ready-calibration-matrix
```

Pinned checkouts:

| Repository | Revision | Package |
| --- | --- | --- |
| `cupertino` | `65dcae238d30` | `cupertino.core` |
| `navigation-split-view` | `2c88df50b8f5` | `navigation-split-view.core` |
| `xyflow` | `a58568f11bc0` | `xyflow.core` |
| `flask` | `954f5684e484` | `flask.core` |
| `gin` | `5f4f9643258d` | `gin.core` |
| `docc2context` | `a2babcc4910c` | `docc2context.core` |

Observed quality report:

- package count: 6
- pass count: 6
- review count: 0
- fail count: 0
- unscored count: 0

Observed calibration matrix:

| Package | Status | Estimated edits | Categories | Priority | Generator follow-up |
| --- | --- | ---: | --- | --- | --- |
| `cupertino.core` | `author_ready_draft` | 0 | - | `low` | no |
| `navigation-split-view.core` | `author_ready_draft` | 0 | - | `low` | no |
| `xyflow.core` | `author_ready_draft` | 0 | - | `low` | no |
| `flask.core` | `author_ready_draft` | 1 | `evidence_depth` | `medium` | no |
| `gin.core` | `author_ready_draft` | 1 | `evidence_depth` | `medium` | no |
| `docc2context.core` | `author_ready_draft` | 0 | - | `low` | no |

Summary:

- `packageCount`: 6
- `authorReadyDraftCount`: 6
- `needsRegenerationCount`: 0
- `blockedCount`: 0
- `totalEstimatedAuthorEdits`: 2
- `averageEstimatedAuthorEdits`: 0.33
- `editCategoryCounts`: `evidence_depth` = 2
- `reviewPriorityCounts`: `low` = 4, `medium` = 2
- `generatorFollowUpCount`: 0
- `calibrationVerdict`: `author_curation_ready`

Product conclusion: the tested generator path produced valid starter packages
for all six repositories. Remaining observed work is normal author curation,
not regeneration. Python and Go samples need one evidence-depth pass each
because analyzer coverage is narrower than the multi-source Swift and
JavaScript/TypeScript runs.

Generated `.smoke` outputs remain local evidence and are not committed.

## Validation Commands

```bash
PYTHONPATH=src python -m spec_harvester source-manifests .smoke/p27-t5-inputs
```

Result: passed; produced a six-repository source manifest summary.

```bash
python3 scripts/run_real_repository_validation.py \
  --inputs .smoke/p27-t5-inputs \
  --out .smoke/output/p27-t5-author-ready \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/p27-t5-analyzer-cache \
  --specpm-pythonpath ../SpecPM/src
```

Result: passed; `run-report.json` status `ok`, package count 6.

```bash
PYTHONPATH=src python -m spec_harvester quality-report \
  --run-report .smoke/output/p27-t5-author-ready/run-report.json \
  --candidates-root .smoke/output/p27-t5-author-ready \
  --output .smoke/output/p27-t5-author-ready/quality-report.json
```

Result: passed; `SpecHarvesterRealRepositoryQualityReport`, package count 6,
pass count 6.

```bash
PYTHONPATH=src python -m spec_harvester author-ready-calibration-matrix \
  --quality-report .smoke/output/p27-t5-author-ready/quality-report.json \
  --output .smoke/output/p27-t5-author-ready/author-ready-calibration-matrix.json
```

Result: passed; `SpecHarvesterAuthorReadyCalibrationMatrix`, package count 6,
`calibrationVerdict` = `author_curation_ready`.

```bash
PYTHONPATH=src pytest tests/test_author_ready_calibration_matrix.py tests/test_docs_contracts.py -q
```

Result: 53 passed.

```bash
PYTHONPATH=src python -m pytest -q
```

Result: 586 passed, 1 skipped.

```bash
PYTHONPATH=src python -m pytest --cov=spec_harvester \
  --cov-report=term-missing --cov-fail-under=90
```

Result: 586 passed, 1 skipped; total coverage 90.18%.

```bash
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
swift build --target SpecHarvesterDocs
```

Result: passed.

```bash
rm -rf .docc-build && \
swift package --allow-writing-to-directory ./.docc-build generate-documentation \
  --target SpecHarvester \
  --output-path ./.docc-build \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester; \
rc=$?; rm -rf .docc-build; exit $rc
```

Result: passed. Existing unrelated DocC warnings remain for
`AcceptedPackageUpdateProposals` and inline command references in
`RealRepositoryQualityReport`.

## Boundary Checks

- The calibration matrix reads existing local JSON artifacts only.
- It does not execute harvested repository code.
- It does not install dependencies, run package managers, run builds/tests, or
  contact package registries.
- It does not mutate candidates or accepted SpecPM packages.
- It is product calibration evidence, not SpecPM acceptance authority.

