# P12-T6 Validation Report

Status: Passed
Date: 2026-05-21
Task: `P12-T6` Popular Repository Smoke Scenario Promotion

## Scope

- Added synthetic Flask/Gin popular repository smoke coverage.
- Verified strict public `LICENSE.txt` handling for Flask-like fixtures.
- Verified Go public interface index emission for Gin-like fixtures.
- Verified Go manifest-only behavior remains non-executing and skipped.
- Verified generated web-framework/domain intents, public interface evidence,
  governance reports, namespace/upstream checks, license/provenance checks, and
  smoke triage summary output.
- Mirrored the real-checkout operator recipe in GitHub docs and DocC.

## Quality Gates

```text
PYTHONPATH=src python -m pytest tests/test_popular_repository_smoke.py tests/test_docs_contracts.py -q
9 passed in 0.07s

PYTHONPATH=src python -m pytest
224 passed in 4.93s

ruff check src tests
All checks passed!

ruff format --check src tests
44 files already formatted

PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
224 passed in 5.46s
Total coverage: 90.91%

swift package dump-package >/dev/null
passed

swift build --target SpecHarvesterDocs
Build of target: 'SpecHarvesterDocs' complete
```

## Result

`P12-T6` meets the acceptance criteria. No generated `.smoke/` outputs were
committed.
