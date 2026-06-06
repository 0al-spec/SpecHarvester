# Roadmap

## Phase 0: Bootstrap

- Define repository boundary and trust model.
- Implement safe local evidence collection.
- Add tests for snapshot shape and CLI output.

## Phase 1: Candidate Drafting

- Add deterministic candidate drafting from evidence snapshots.
- Emit `specpm.yaml` and `specs/*.spec.yaml` into candidate package
  directories.
- Mark generated candidates as unofficial and community-observed.
- Validate generated candidates with SpecPM.
- Promote reviewed candidates into accepted source roots.

## Phase 2: AI-Assisted Refinement

- Add a model adapter interface.
- Refine deterministic candidates with bounded model output.
- Preserve static evidence provenance and review constraints.

## Phase 3: Batch Harvesting

- Add repository source manifests.
- Collect snapshots for selected public repositories.
- Generate candidate specs into deterministic paths.
- Emit review reports with validation status and confidence notes.

## Phase 4: Registry Integration

- Produce PR-ready accepted package manifest entries.
- Support public index candidate review.
- Export observed intent catalog inputs for SpecPM / SpecGraph workflows.
- Automate PR creation from promoted accepted package sources.
- Include producer bundle evidence links in SpecPM proposal artifacts and pull
  request bodies without making producer output registry authority.
- Keep SpecPM contract fixtures and SpecHarvester generated bundle examples
  aligned through an explicit shared fixture policy.
- Preserve a stable producer evidence layout and `producerEvidenceLinks` role
  vocabulary for a future optional SpecPM CI preflight gate.
- Reference external SpecPM registry acceptance decision records from handoff
  artifacts without writing maintainer approval into generated receipts.
- Produce package-set and scoped member package candidate bundle sets for
  monorepos, aligned with SpecPM package-set, relation, search, registry
  metadata, and multi-package intake contracts.
- Package-set contract alignment is documented before runtime monorepo
  discovery implementation, mapping SpecPM contracts to workspace inventory,
  package-set candidates, scoped member packages, relation proposals,
  bundle-set preflight, static viewer previews, and the `xyflow` smoke
  scenario.

## Phase 5: Governance

- Add duplicate intent detection.
- Add namespace and upstream relationship checks.
- Add policy reports for generated package claims.
