# P16-T9 Validation Report

Task: `P16-T9 — Architecture Lint Guardrails`
Branch: `feature/P16-T9-architecture-lint-guardrails`
Date: 2026-05-25
Verdict: PASS

## Implementation Summary

- Added `SpecHarvesterArchitectureLintReport` generation.
- Added `architecture-lint` CLI with `--path`, `--output`, and
  `--fail-on-issues`.
- Added initial project-specific guardrail rules:
  - `helper_name_relapse`
  - `constructor_io`
  - `static_domain_helper`
  - `manifest_parser_pattern`
- Added a non-blocking CI architecture lint baseline step.
- Added GitHub docs, DocC mirror, and docs contract coverage.
- Added regression tests for each rule, missing paths, output writing, and
  fail-on-issues behavior.

## Architecture Lint Baseline

Command:

```shell
PYTHONPATH=src python -m spec_harvester architecture-lint \
  --path src/spec_harvester \
  --output /tmp/specharvester-architecture-lint.json
```

Summary:

```json
{
  "fileCount": 28,
  "issueCount": 3,
  "issuesByCode": {
    "manifest_parser_pattern": 3
  },
  "pathCount": 1
}
```

The findings are advisory and point to the known duplicated manifest parser
logic in:

- `src/spec_harvester/accepted_diff.py`
- `src/spec_harvester/license_provenance_reports.py`
- `src/spec_harvester/namespace_reports.py`

## Quality Gates

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_architecture_lint.py tests/test_docs_contracts.py -q` | PASS, 31 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 381 passed, 1 skipped |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 381 passed, 1 skipped, total coverage 90.75% |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Boundaries

- The linter reads local Python source files only.
- It does not execute scanned code, install dependencies, access the network,
  or mutate source files.
- CI runs the linter as advisory baseline collection only.
- This task does not perform the Elegant Objects refactor itself.
