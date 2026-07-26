# P52-T10 Validation Report

**Task:** Add strict collector support for canonical dual-license filenames
**Date:** 2026-07-27
**Verdict:** PASS

## Result

The strict collector now accepts the exact canonical root filenames
`LICENSE-APACHE` and `LICENSE-MIT`. It continues to reject near-miss and
third-party filenames. Targeted static validation of the existing pinned `uv`
and `actix-web` checkouts produced two license files per repository and no
`missing_license_file` error.

The P52-T6 historical 48/50 static completion result is preserved. P52-T10 is
new follow-up evidence, not a modification of the historical gate outcome.

## Targeted Command

```text
PYTHONPATH=src python -m spec_harvester collect-batch inputs/p52-final-corpus \
  --select uv --select actix-web \
  --out /tmp/specharvester-p52-t10.pPcljW/output \
  --report /tmp/specharvester-p52-t10.pPcljW/batch-validation.json
```

Result: `status: ok`; both records have `licenseFileCount: 2` and empty error
codes. The checkouts matched the pinned revisions in the final corpus manifest.

## Quality Gates

```text
PYTHONPATH=src python -m pytest
965 passed, 1 skipped

ruff check src tests
All checks passed!

ruff format --check src tests
141 files already formatted

PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
965 passed, 1 skipped; total coverage 90.01%

swift package dump-package >/dev/null
PASS

swift build --target SpecHarvesterDocs
PASS
```

## Boundaries

The targeted run used already-present local checkouts. It did not clone or
fetch repositories, install dependencies, invoke package managers, execute
harvested code, run AI or adapters, accept packages or relations, publish
registry metadata, or modify registry truth.
