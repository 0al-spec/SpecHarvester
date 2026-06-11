# Author-Ready Calibration Matrix

`author-ready-calibration-matrix` turns a real-repository `quality-report.json`
into a product-facing calibration matrix. It answers how many author edits
remain after SpecHarvester produces a valid starter package.

This is different from `quality-report`: the quality report records dimensions
such as intent accuracy, capability evidence, analyzer coverage, and SpecPM
status. The calibration matrix translates those dimensions into edit counts,
edit categories, review priority, and repeated generator gaps.

## Command

```bash
PYTHONPATH=src python -m spec_harvester author-ready-calibration-matrix \
  --quality-report .smoke/output/p27-t5-author-ready/quality-report.json \
  --author-notes .smoke/output/p27-t5-author-ready/author-notes.json \
  --output .smoke/output/p27-t5-author-ready/author-ready-calibration-matrix.json
```

## Payload Identity

```json
{
  "apiVersion": "spec-harvester.author-ready-calibration-matrix/v0",
  "kind": "SpecHarvesterAuthorReadyCalibrationMatrix",
  "schemaVersion": 1
}
```

## Author Notes

`--author-notes` is optional. Without it, the matrix derives estimated author
edits from quality dimensions. With it, operators can record manual estimates
after inspecting generated candidates.

Author notes may provide `estimatedAuthorEdits`, `editCategories`,
`authorReadyStatus`, `notes`, and `generatorFollowUpReasons` per package id.
Supported `authorReadyStatus` values are `author_ready_draft`,
`needs_regeneration`, and `blocked`.

## Matrix Rows

Each package row records `id`, `packageId`, `qualityVerdict`,
`authorReadyStatus`, `reviewPriority`, `estimatedAuthorEdits`,
`editCategories`, `intentAccuracy`, `capabilityEvidenceQuality`,
`analyzerCoverage`, `specpmStatus`, `retryOutcome`,
`generatorFollowUpRecommended`, `generatorFollowUpReasons`, and
`humanReviewNotes`.

Typical edit categories are `intent_summary`, `capability_evidence`,
`evidence_depth`, `validation`, and `author_curation`.

## Summary

The matrix summary records package count, author-ready count,
needs-regeneration count, blocked count, total and average estimated author
edits, edit category counts, review priority counts, generator follow-up count,
and `calibrationVerdict`.

Possible `calibrationVerdict` values are `author_curation_ready`,
`mixed_author_ready`, `generator_follow_up_recommended`, and
`blocked_inputs_present`.

## P27-T5 Local Run Pattern

Use local real repository checkouts pinned to exact revisions. Generated
manifests and outputs stay under `.smoke/` and must not be committed.

The P27-T5 local run used `cupertino`, `navigation-split-view`, `xyflow`,
`flask`, `gin`, and `docc2context` checkouts to calibrate the author-ready
surface across Swift, JavaScript/TypeScript, Python, Go, monorepo, and
documentation-first shapes.

Observed matrix output:

| Package | Status | Estimated edits | Categories | Priority | Generator follow-up |
| --- | --- | ---: | --- | --- | --- |
| `cupertino.core` | `author_ready_draft` | 0 | - | `low` | no |
| `navigation-split-view.core` | `author_ready_draft` | 0 | - | `low` | no |
| `xyflow.core` | `author_ready_draft` | 0 | - | `low` | no |
| `flask.core` | `author_ready_draft` | 1 | `evidence_depth` | `medium` | no |
| `gin.core` | `author_ready_draft` | 1 | `evidence_depth` | `medium` | no |
| `docc2context.core` | `author_ready_draft` | 0 | - | `low` | no |

Observed summary: 6 packages, 6 `author_ready_draft` rows, 0
`needs_regeneration`, 0 `blocked`, 2 total estimated author edits, 0.33 average
estimated author edits, `evidence_depth` = 2, review priorities `low` = 4 and
`medium` = 2, 0 generator follow-ups, and `calibrationVerdict` =
`author_curation_ready`.

Product reading: the current generator path produced valid starter packages for
all six repositories. The remaining observed work is normal author curation,
not regeneration: Swift and TypeScript samples needed no estimated edits, while
Python and Go samples each need one evidence-depth pass because their analyzer
coverage is narrower than the multi-source Swift/TypeScript runs.

## Safety Rules

The matrix does not execute harvested repository code, install dependencies,
run package managers, run package scripts, run builds or tests, contact package
registries, publish registry metadata, or imply SpecPM acceptance, maintainer
approval, or upstream endorsement.
