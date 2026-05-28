# P16-T4 Validation Report

Date: 2026-05-28
Branch: `feature/P16-T4-reduce-broad-semantic-intents`
Verdict: PASS

## Summary

- Added a governance duplicate-claim comparison policy for broad
  language-neutral semantic intents.
- Broad intents remain visible in parsed `records`, but are no longer counted
  as duplicate intent findings.
- Specific duplicate intents and duplicate capabilities retain existing
  reporting behavior.
- Updated GitHub docs, DocC mirror, and docs contract coverage.

## Behavior Validation

- `PYTHONPATH=src python -m pytest tests/test_governance_reports.py tests/test_docs_contracts.py -q`
  - PASS: 31 passed
- Broad intents covered as record-only:
  - `intent.api.contract_surface`
  - `intent.metadata.schema_validation`
  - `intent.package.public_repository_metadata`
- Specific duplicate intent still reported:
  - `intent.web.framework_surface`

## Quality Gates

- `PYTHONPATH=src python -m pytest`
  - PASS: 418 passed, 1 skipped
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 418 passed, 1 skipped, total coverage 91.87%
- `ruff check src tests`
  - PASS
- `ruff format --check src tests`
  - PASS: 68 files already formatted
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Advisory Checks

- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t4-dup-builtin.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t4-dup-pylint.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t4-architecture-lint.json`
  - ATTENTION: one existing advisory `manifest_parser_pattern` in
    `src/spec_harvester/license_provenance_reports.py`

## Notes

- The architecture lint advisory predates this task and is unrelated to broad
  semantic intent filtering.
- This task does not change generated `specpm.yaml` manifests; it only changes
  duplicate finding classification in governance reports.
