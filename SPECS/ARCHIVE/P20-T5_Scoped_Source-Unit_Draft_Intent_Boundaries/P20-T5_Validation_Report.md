# P20-T5 Validation Report

**Task:** P20-T5 Scoped Source-Unit Draft Intent Boundaries
**Result:** Passed

## Implementation Summary

- Added `SourceUnitIntentBoundary` as a deterministic source-unit classifier for
  repository, package, folder/module, and single-file targets.
- Updated single-package draft generation to surface the boundary in generated
  summaries, scope includes, constraints, and provenance metadata.
- Updated SpecNode refinement preview input to include the same
  `sourceUnitIntentBoundary` contract in `compactModelInput`.
- Added characterization coverage for scoped folder, single-file, and SpecNode
  refinement-preview behavior.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_collector.py -q -k "source_unit_metadata_for_scoped_folder or source_unit_metadata_for_single_file"`:
  `2 passed, 95 deselected`
- `PYTHONPATH=src pytest tests/test_specnode_refinement_smoke.py -q -k "scoped_source_unit_boundary"`:
  `1 passed, 30 deselected`
- `PYTHONPATH=src pytest tests/test_collector.py tests/test_specnode_refinement_smoke.py -q`:
  `128 passed`
- `PYTHONPATH=src python -m pytest`: `681 passed, 1 skipped`
- `ruff check src tests`: passed
- `ruff format --check src tests`: `110 files already formatted`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  `681 passed, 1 skipped`, total coverage `90.76%`
- `swift package dump-package >/dev/null`: passed
- `swift build --target SpecHarvesterDocs`: passed
- `git diff --check`: passed
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/specharvester-p20-t5-architecture-lint.json`:
  completed with advisory `status: attention` for the existing
  `license_provenance_reports.py` manifest parser pattern baseline; no new
  issue was reported for the P20-T5 files.

## Notes

- No CodeGraph adapter behavior was added.
- No registry acceptance or SpecPM handoff policy was changed.
- The boundary remains proposal/draft metadata and does not promote scoped
  source units into accepted package-set members.
