# Roadmap

## Phase 0: Bootstrap

- Define repository boundary and trust model.
- Implement safe local evidence collection.
- Add tests for snapshot shape and CLI output.

## Phase 1: Candidate Drafting

- Add a model adapter interface.
- Generate candidate `specpm.yaml` and `specs/*.spec.yaml` from evidence
  snapshots.
- Mark generated candidates as unofficial and community-observed.
- Validate generated candidates with SpecPM.

## Phase 2: Batch Harvesting

- Add repository source manifests.
- Collect snapshots for selected public repositories.
- Generate candidate specs into deterministic paths.
- Emit review reports with validation status and confidence notes.

## Phase 3: Registry Integration

- Produce PR-ready accepted package manifest entries.
- Support public index candidate review.
- Export observed intent catalog inputs for SpecPM / SpecGraph workflows.

## Phase 4: Governance

- Add duplicate intent detection.
- Add namespace and upstream relationship checks.
- Add policy reports for generated package claims.
