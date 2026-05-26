# P16-T12 Validation Report

Task: `P16-T12 — Report Source Records Object`
Branch: `feature/P16-T12-report-source-records-object`
Date: 2026-05-26
Verdict: PASS

## Implemented

- Added `SpecpmReportSourceRecords` as a shared object for accepted/candidate
  `specpm.yaml` traversal.
- Added `ReportSourceIssuePolicy` to preserve report-specific symlink and
  invalid-manifest issue shape.
- Refactored governance duplicate claim, namespace/upstream, and license
  provenance reports to use the shared object.
- Added direct regression coverage for shared traversal, symlink issues, invalid
  manifest issues, source sorting, and missing-root errors.

## Duplicate-Code Baseline

| Backend | Before | After | Result |
| --- | ---: | ---: | --- |
| builtin duplicate blocks | 21 | 18 | improved |
| builtin duplicate occurrences | 46 | 37 | improved |
| pylint duplicate blocks | 4 | 2 | improved |
| pylint duplicate occurrences | 8 | 4 | improved |

Remaining pylint clusters are outside this task:

- semantic keyword lists in `collector.py` and `drafter.py`
- public API symbol/evidence/path helpers in `go_public_api.py` and
  `python_public_api.py`

## Architecture Lint Baseline

| Metric | Result |
| --- | --- |
| issueCount | 1 |
| issuesByCode | `manifest_parser_pattern: 1` |
| remaining file | `src/spec_harvester/license_provenance_reports.py` |

The remaining architecture-lint issue is the known license provenance manifest
parser pattern and is intentionally left for a separate task.

## Validation

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_report_source_records.py tests/test_governance_reports.py tests/test_namespace_upstream_reports.py tests/test_license_provenance_risk_reports.py -q` | PASS, 29 passed |
| `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t12-dup-builtin.json` | PASS, 18 duplicate blocks |
| `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t12-dup-pylint.json` | PASS, 2 duplicate blocks |
| `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t12-architecture-lint.json` | PASS, 1 advisory issue |
| `PYTHONPATH=src python -m pytest` | PASS, 396 passed, 1 skipped |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 396 passed, 1 skipped, total coverage 91.32% |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Risk Notes

- The refactor preserves issue codes and messages by parameterizing report-local
  issue policy rather than hardcoding one global policy.
- The shared object remains local-only and reads `specpm.yaml` files as
  untrusted data; it does not execute repository code or import scanned modules.

