# Author-Ready Calibration Matrix

Status: P27 product calibration artifact

`author-ready-calibration-matrix` turns a real-repository
`quality-report.json` into a product-facing calibration matrix. It answers:

```text
How many author edits remain after SpecHarvester produces a valid starter
package?
```

This is different from `quality-report`. The quality report checks dimensions
such as intent accuracy, capability evidence, analyzer coverage, and SpecPM
status. The calibration matrix translates those dimensions into author work:
edit counts, edit categories, review priority, and repeated generator gaps.

## Command

```bash
PYTHONPATH=src python -m spec_harvester author-ready-calibration-matrix \
  --quality-report .smoke/output/p27-t5-author-ready/quality-report.json \
  --author-notes .smoke/output/p27-t5-author-ready/author-notes.json \
  --output .smoke/output/p27-t5-author-ready/author-ready-calibration-matrix.json
```

`--author-notes` is optional. Without it, the matrix derives estimated author
edits from quality dimensions. With it, operators can record manual estimates
after inspecting generated candidates.

## Payload Identity

```json
{
  "apiVersion": "spec-harvester.author-ready-calibration-matrix/v0",
  "kind": "SpecHarvesterAuthorReadyCalibrationMatrix",
  "schemaVersion": 1
}
```

## Author Notes

Author notes may be a direct package-id map:

```json
{
  "xyflow": {
    "estimatedAuthorEdits": 3,
    "editCategories": ["intent_summary", "capability_evidence"],
    "authorReadyStatus": "author_ready_draft",
    "notes": "Author should tighten React/Svelte boundaries."
  }
}
```

or wrapped under `packages`:

```json
{
  "packages": {
    "flask": {
      "estimatedAuthorEdits": 2,
      "editCategories": ["capability_evidence", "evidence_depth"],
      "generatorFollowUpReasons": ["missing_analyzer_coverage"]
    }
  }
}
```

Supported `authorReadyStatus` values:

- `author_ready_draft`
- `needs_regeneration`
- `blocked`

## Matrix Rows

Each package row records:

- `id` and `packageId`;
- `qualityVerdict` from `SpecHarvesterRealRepositoryQualityReport`;
- `authorReadyStatus`;
- `reviewPriority`: `low`, `medium`, `high`, or `blocking`;
- `estimatedAuthorEdits`;
- `editCategories`;
- `intentAccuracy`, `capabilityEvidenceQuality`, `analyzerCoverage`,
  `specpmStatus`, and `retryOutcome`;
- `generatorFollowUpRecommended` and `generatorFollowUpReasons`;
- `humanReviewNotes`.

Typical edit categories:

- `intent_summary`
- `capability_evidence`
- `evidence_depth`
- `validation`
- `author_curation`

## Summary

The matrix summary records:

- package count;
- author-ready, needs-regeneration, and blocked counts;
- total and average estimated author edits;
- edit category counts;
- review priority counts;
- generator follow-up count;
- `calibrationVerdict`.

Possible `calibrationVerdict` values:

- `author_curation_ready`: remaining work is normal author curation.
- `mixed_author_ready`: some packages need regeneration-level review.
- `generator_follow_up_recommended`: deterministic generator fixes are likely
  useful.
- `blocked_inputs_present`: at least one package is blocked.

## P27-T5 Local Run Pattern

Use local real repository checkouts pinned to exact revisions. Generated
manifests and outputs stay under `.smoke/` and must not be committed.

```bash
python3 scripts/run_real_repository_validation.py \
  --inputs .smoke/p27-t5-inputs \
  --out .smoke/output/p27-t5-author-ready \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/p27-t5-analyzer-cache \
  --specpm-pythonpath ../SpecPM/src

PYTHONPATH=src python -m spec_harvester quality-report \
  --run-report .smoke/output/p27-t5-author-ready/run-report.json \
  --candidates-root .smoke/output/p27-t5-author-ready \
  --output .smoke/output/p27-t5-author-ready/quality-report.json

PYTHONPATH=src python -m spec_harvester author-ready-calibration-matrix \
  --quality-report .smoke/output/p27-t5-author-ready/quality-report.json \
  --output .smoke/output/p27-t5-author-ready/author-ready-calibration-matrix.json
```

## Observed P27-T5 Calibration Run

The P27-T5 local run used six existing real checkouts:

| Repository | Shape | Revision |
| --- | --- | --- |
| `cupertino` | Swift/SPM + Xcode workspace | `65dcae238d30` |
| `navigation-split-view` | Swift/SPM + Xcode project | `2c88df50b8f5` |
| `xyflow` | JavaScript/TypeScript monorepo | `a58568f11bc0` |
| `flask` | Python web framework | `954f5684e484` |
| `gin` | Go web framework | `5f4f9643258d` |
| `docc2context` | Swift/SPM documentation-first CLI | `a2babcc4910c` |

Observed matrix output:

| Package | Status | Estimated edits | Categories | Priority | Generator follow-up |
| --- | --- | ---: | --- | --- | --- |
| `cupertino.core` | `author_ready_draft` | 0 | - | `low` | no |
| `navigation-split-view.core` | `author_ready_draft` | 0 | - | `low` | no |
| `xyflow.core` | `author_ready_draft` | 0 | - | `low` | no |
| `flask.core` | `author_ready_draft` | 1 | `evidence_depth` | `medium` | no |
| `gin.core` | `author_ready_draft` | 1 | `evidence_depth` | `medium` | no |
| `docc2context.core` | `author_ready_draft` | 0 | - | `low` | no |

Observed summary:

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

Product reading: the current generator path produced valid starter packages for
all six repositories. The remaining observed work is normal author curation,
not regeneration: Swift and TypeScript samples needed no estimated edits, while
Python and Go samples each need one evidence-depth pass because their analyzer
coverage is narrower than the multi-source Swift/TypeScript runs.

The committed documentation records the command contract and summary shape, not
the generated `.smoke` output. The local run is reproducible from pinned
checkouts and should be rerun when generator behavior changes.

## Safety Rules

- Do not execute harvested repository code.
- Do not install harvested dependencies.
- Do not run package managers, package scripts, builds, or tests.
- Do not contact package registries during harvesting.
- Do not commit generated `.smoke` outputs.
- Do not treat author edit estimates as SpecPM acceptance, maintainer approval,
  or upstream endorsement.
