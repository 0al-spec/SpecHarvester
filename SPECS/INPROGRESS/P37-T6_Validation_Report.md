# P37-T6 Validation Report

## Task

P37-T6 Cross-Ecosystem Profile Fixtures

## Verdict

PASS

## Summary

P37-T6 adds cross-ecosystem repository profile detection fixtures proving the
generic profile selection contract across multiple static repository shapes.
The fixture set remains producer-side evidence only and does not introduce
ecosystem-specific plugins or change scoring behavior.

## Implemented

- Added workspace-shaped fixture:
  `cross-ecosystem-workspace.example.json`.
- Added single-package fixture:
  `cross-ecosystem-single-package.example.json`.
- Added nested-package fixture:
  `cross-ecosystem-nested-package.example.json`.
- Added ambiguous multi-signal fixture:
  `cross-ecosystem-ambiguous-multi-signal.example.json`.
- Added regression tests ensuring each fixture matches
  `build_repository_profile_detection`.
- Added outcome tests for:
  - `generic.package_set.v0` high-confidence selection;
  - `generic.single_package.v0` high-confidence selection;
  - nested manifest fallback;
  - ambiguous multi-signal fallback.
- Added GitHub docs and DocC mirror for cross-ecosystem profile fixtures.
- Linked the fixture set from repository profile selection docs, capabilities,
  roadmap, docs index, and DocC root.

## Validation Commands

```shell
PYTHONPATH=src pytest tests/test_repository_profile_detection.py tests/test_docs_contracts.py -q -k 'repository_profile'
```

Result: `20 passed, 101 deselected`.

```shell
PYTHONPATH=src pytest -q
```

Result: `755 passed, 1 skipped`.

```shell
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result: `755 passed, 1 skipped`; total coverage `91.15%`.

```shell
PYTHONPATH=src ruff check .
```

Result: passed.

```shell
PYTHONPATH=src ruff format --check src tests
```

Result: `120 files already formatted`.

```shell
git diff --check
```

Result: passed.

```shell
swift build --target SpecHarvesterDocs
```

Result: passed.

```shell
PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/specharvester-p37-t6-architecture-lint.json
```

Result: advisory `attention` with one existing
`manifest_parser_pattern` issue in `src/spec_harvester/license_provenance_reports.py`.
No P37-T6 file was reported.

## Notes

The architecture lint issue is pre-existing advisory technical debt and is not
introduced by P37-T6.
