# P16-T6 Validation Report

Task: `P16-T6 — Duplicate-Code Quality Report`
Branch: `feature/P16-T6-duplicate-code-quality-gate`
Date: 2026-05-25
Verdict: PASS

## Implementation Summary

- Added `SpecHarvesterCodeDuplicationReport` generation for deterministic,
  local-only duplicate-code review.
- Added `code-duplication-report` CLI with `--path`, `--min-lines`, `--output`,
  and explicit `--fail-on-duplicates`.
- Kept the command advisory by default so current baseline collection does not
  block CI.
- Added GitHub docs and DocC mirror coverage.
- Added regression tests for detection, normalization, output writing,
  fail-on-duplicates, and invalid window handling.

## Duplicate-Code Baseline

Command:

```shell
PYTHONPATH=src python -m spec_harvester code-duplication-report \
  --path src/spec_harvester \
  --min-lines 8 \
  --output /tmp/specharvester-code-duplication-p16-t6.json
```

Summary:

```json
{
  "duplicateBlockCount": 52,
  "duplicateOccurrenceCount": 109,
  "fileCount": 27,
  "minLines": 8,
  "pathCount": 1
}
```

This baseline is advisory only. It should not be used as a blocking CI gate
until a later task defines baseline suppression or fail-on-new-duplicates
semantics.

## Quality Gates

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_code_duplication_report.py tests/test_docs_contracts.py -q` | PASS, 28 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 363 passed, 1 skipped |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 363 passed, 1 skipped, total coverage 90.60% |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Boundaries

- No scanned source code execution.
- No imports from scanned modules.
- No dependency installation.
- No network access.
- No CI blocking by default.
