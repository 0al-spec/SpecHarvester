# Roadmap

SpecHarvester is in bootstrap phase as a bounded producer pipeline for
candidate SpecPM packages.

The canonical repository roadmap is `docs/ROADMAP.md`. This DocC page mirrors
that direction for public documentation readers.

## Milestones

### Phase 0: Bootstrap

- Define repository boundary and trust model.
- Implement safe local evidence collection.
- Add tests for snapshot shape and CLI output.

### Phase 1: Candidate Drafting

- Add deterministic candidate drafting from evidence snapshots.
- Emit `specpm.yaml` and `specs/*.spec.yaml` into candidate package
  directories.
- Mark generated candidates as unofficial and community-observed.
- Validate generated candidates with SpecPM.
- Promote reviewed candidates into accepted source roots.

### Phase 2: AI-Assisted Refinement

- Add a model adapter interface.
- Refine deterministic candidates with bounded model output.
- Preserve static evidence provenance and review constraints.

### Phase 3: Batch Harvesting

- Add repository source manifests.
- Collect snapshots for selected public repositories.
- Generate candidate specs into deterministic paths.
- Emit review reports with validation status and confidence notes.

### Phase 4: Registry Integration

- Produce PR-ready accepted package manifest entries.
- Support public index candidate review.
- Export observed intent catalog inputs for SpecPM and SpecGraph workflows.
- Automate pull request creation from promoted accepted package sources.

### Phase 5: Governance

- Add duplicate intent detection.
- Add namespace and upstream relationship checks.
- Add policy reports for generated package claims.

## Non-Goals

SpecHarvester does not become the registry, the canonical package authority, or
the execution runtime for harvested repositories.

## References

- `docs/ROADMAP.md`
- <doc:HarvesterArchitecture>
- <doc:ProposalAutomation>
