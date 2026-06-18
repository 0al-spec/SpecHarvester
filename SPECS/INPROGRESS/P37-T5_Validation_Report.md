# P37-T5 Validation Report

## Task

P37-T5 Generic Profile Discovery Hints

## Verdict

PASS

## Summary

P37-T5 defines a versioned generic repository profile hint vocabulary and keeps
the vocabulary producer-side evidence only. Existing repository profile
detection now emits canonical hint ids through the shared vocabulary, rejects
unknown built-in hint ids, and documents the contract in GitHub docs and DocC.

## Implemented

- Added `SpecHarvesterRepositoryProfileHintVocabulary`.
- Added `spec-harvester.repository-profile-hints/v0`.
- Added `producer_profile_hint_vocabulary_only`.
- Added the machine-readable vocabulary fixture at
  `tests/fixtures/repository_profile_detection/generic-hint-vocabulary.example.json`.
- Covered 13 generic hint ids:
  - `package_set_root`;
  - `member_package`;
  - `meta_package`;
  - `primary_package`;
  - `cli_package`;
  - `bridge_package`;
  - `plugin_package`;
  - `example_package`;
  - `test_package`;
  - `documentation_source`;
  - `generated_artifact`;
  - `internal_utility`;
  - `evidence_only`.
- Updated current repository profile detection to emit canonical ids for:
  - `package_set_root`;
  - `member_package`;
  - `documentation_source`.
- Documented the non-authority boundary:
  - hints do not accept packages;
  - hints do not accept relations;
  - hints do not remove `preview_only`;
  - hints do not publish registry metadata;
  - hints do not treat profile hints as registry truth.

## Validation Commands

```shell
PYTHONPATH=src pytest tests/test_repository_profile_detection.py tests/test_docs_contracts.py -q -k 'repository_profile'
```

Result: `14 passed, 101 deselected`.

```shell
PYTHONPATH=src pytest -q
```

Result: `749 passed, 1 skipped`.

```shell
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result: `749 passed, 1 skipped`; total coverage `91.13%`.

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
PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/specharvester-p37-t5-architecture-lint.json
```

Result: advisory `attention` with one existing
`manifest_parser_pattern` issue in `src/spec_harvester/license_provenance_reports.py`.
No new P37-T5 module was reported.

## Notes

The architecture lint issue is pre-existing advisory technical debt and is not
introduced by P37-T5.
