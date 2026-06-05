# Validation Report: P24-T1 Harvested Spec Quality Depth

**Date:** 2026-06-05
**Verdict:** PASS

## Scope

P24-T1 improves generated SpecPM candidate quality by making draft manifests more
subject-focused and by linking harvested evidence to interface and compatibility
contract nodes that SpecPM validates.

## Checks

| Check | Result |
|---|---|
| `PYTHONPATH=src python -m pytest tests/test_collector.py -q -k 'subject_focused_manifest_summary or supports_interfaces_and_compatibility_with_evidence'` | PASS, `2 passed` |
| SpecHarvester draft fixture + adjacent SpecPM `validate --json` | PASS, exit `0`, `error_count: 0`, only expected `preview_only_package` warning |
| `PYTHONPATH=src python -m pytest` | PASS, `496 passed, 1 skipped` |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, `83 files already formatted` |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, coverage `91.56%` |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `PYTHONPATH=src python -m spec_harvester code-duplication-report --backend pylint --path src/spec_harvester --min-lines 8 --output /tmp/spec-harvester-p24-t1-pylint-duplicates.json` | PASS, `duplicateBlockCount: 0` |
| `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/spec-harvester-p24-t1-architecture-lint.json` | PASS with advisory `status: attention` |

## Integration Notes

The practical SpecPM validation generated a local package fixture, drafted a
candidate bundle with SpecHarvester, then validated the candidate directory using
the adjacent SpecPM CLI:

```bash
PYTHONPATH=/Users/egor/Development/GitHub/0AL/SpecPM/src \
  python -m specpm.cli validate /tmp/spec-harvester-p24-t1-*/candidate --json
```

The final report had `error_count: 0`, `status: warning_only`, and exactly one
warning: `preview_only_package`. Earlier unknown evidence support target warnings
were eliminated by linking compatibility evidence to the declared `compatibility`
target instead of undeclared sub-targets.

## Residuals

Architecture lint reports an existing advisory outside the P24-T1 change:

- `src/spec_harvester/license_provenance_reports.py`: `manifest_parser_pattern`

This advisory is unrelated to harvested spec quality depth and does not block
the task.
