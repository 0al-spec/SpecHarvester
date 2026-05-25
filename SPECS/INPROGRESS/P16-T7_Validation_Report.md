# P16-T7 Validation Report

Task: `P16-T7 — Pylint Duplicate-Code Backend`
Branch: `feature/P16-T7-pylint-duplicate-code-checks`
Date: 2026-05-25
Verdict: PASS

## Implementation Summary

- Added `pylint` as a development dependency.
- Added `--backend builtin|pylint` to `code-duplication-report`.
- Converted `pylint` `duplicate-code` / `R0801` JSON output into the stable
  `SpecHarvesterCodeDuplicationReport` contract.
- Added a non-blocking CI duplicate-code baseline step using the `pylint`
  backend.
- Updated GitHub docs and DocC mirror.
- Added regression tests for `R0801` parsing, missing tool handling, and CLI
  backend selection.

## Pylint Baseline

Command:

```shell
PYTHONPATH=src python -m spec_harvester code-duplication-report \
  --backend pylint \
  --path src/spec_harvester \
  --min-lines 8 \
  --output /tmp/specharvester-pylint-dup.json
```

Summary:

```json
{
  "backend": "pylint",
  "duplicateBlockCount": 7,
  "duplicateOccurrenceCount": 14,
  "fileCount": 27,
  "minLines": 8,
  "pathCount": 1,
  "tool": {
    "messageCount": 7,
    "name": "pylint",
    "returnCode": 8
  }
}
```

The CI step is intentionally non-blocking because current repository baseline
contains duplicate-code findings. Blocking enforcement should wait for baseline
suppression or fail-on-new-duplicates semantics.

## Quality Gates

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_code_duplication_report.py tests/test_docs_contracts.py -q` | PASS, 35 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 370 passed, 1 skipped |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 370 passed, 1 skipped, total coverage 90.70% |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Boundaries

- The `pylint` backend is a local analyzer invocation.
- It does not execute scanned repository code or install harvested
  dependencies.
- CI does not fail on duplicate findings in this task.
- `jscpd` remains a future multi-language backend candidate, not part of this
  PR.
