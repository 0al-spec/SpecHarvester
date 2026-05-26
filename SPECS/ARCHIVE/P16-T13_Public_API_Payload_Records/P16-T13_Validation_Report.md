# P16-T13 Validation Report

Task: `P16-T13 — Public API Payload Records`
Branch: `feature/P16-T13-public-api-payload-records`
Date: 2026-05-26
Verdict: PASS

## Implemented

- Added `PublicApiPayloadPath` as a shared object for cached public API payload
  path validation.
- Refactored Python and Go public API analyzers to use the shared object for
  entrypoints, symbols, diagnostics, and evidence paths.
- Added direct regression coverage for valid entrypoints, symbols, diagnostics,
  mismatched paths, missing symbols, and missing evidence.

## Duplicate-Code Baseline

| Backend | Before | After | Result |
| --- | ---: | ---: | --- |
| builtin duplicate blocks | 18 | 13 | improved |
| builtin duplicate occurrences | 37 | 27 | improved |
| pylint duplicate blocks | 2 | 1 | improved |
| pylint duplicate occurrences | 4 | 2 | improved |

Remaining pylint cluster:

- semantic keyword lists in `collector.py` and `drafter.py`

## Architecture Lint Baseline

| Metric | Result |
| --- | --- |
| issueCount | 1 |
| issuesByCode | `manifest_parser_pattern: 1` |
| remaining file | `src/spec_harvester/license_provenance_reports.py` |

The remaining architecture-lint issue is unrelated to this payload refactor and
stays as a separate task.

## Validation

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_python_public_api.py tests/test_go_public_api.py tests/test_public_api_payload_records.py -q` | PASS, 17 passed |
| `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t13-dup-builtin.json` | PASS, 13 duplicate blocks |
| `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t13-dup-pylint.json` | PASS, 1 duplicate block |
| `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t13-architecture-lint.json` | PASS, 1 advisory issue |
| `PYTHONPATH=src python -m pytest` | PASS, 398 passed, 1 skipped |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 398 passed, 1 skipped, total coverage 91.46% |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Risk Notes

- Analyzer cache payload schemas are unchanged.
- The shared object only validates already-read local cache payload data; it
  does not execute repository code, import scanned modules, or mutate source
  files.

