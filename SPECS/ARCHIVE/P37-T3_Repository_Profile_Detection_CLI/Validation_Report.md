# P37-T3 Validation Report

## Verdict

PASS

## Summary

P37-T3 adds an opt-in `repository-profile-detect` CLI/report surface that emits
`SpecHarvesterRepositoryProfileDetection` from operator-supplied static
evidence.

The implementation is intentionally narrow:

- no repository cloning or fetching;
- no source collection;
- no analyzer execution;
- no package manager invocation;
- no AI invocation;
- no candidate drafting;
- no registry publication or acceptance authority.

## Deliverables Checked

- [x] Added `src/spec_harvester/repository_profile_detection.py`.
- [x] Added `repository-profile-detect` CLI command.
- [x] Added tests for auto package-set selection, `none` mode, explicit
  profile override, output file writing, source manifest metadata loading, and
  unsafe evidence path rejection.
- [x] Documented the CLI surface in GitHub docs and DocC.
- [x] Updated capabilities docs to reflect the executable report surface.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_repository_profile_detection.py -q`
  - `6 passed`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile_detection_fixture or repository_profile_selection_contract or current_next_task'`
  - `2 passed, 102 deselected`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py tests/test_repository_profile_detection.py -q`
  - `110 passed`
- `PYTHONPATH=src python -m spec_harvester.cli repository-profile-detect --repository-id example.generic-package-set --repository-url https://example.invalid/generic-package-set --revision 0000000000000000000000000000000000000000 --selection auto --evidence-path workspace.yaml --evidence-path packages/core/package.json --evidence-path packages/adapter/package.json --output /tmp/specharvester-p37-t3-repository-profile-detection.json`
  - smoke passed; stdout and `--output` JSON matched
- `PYTHONPATH=src pytest -q`
  - `741 passed, 1 skipped`
- `PYTHONPATH=src ruff check .`
  - passed
- `PYTHONPATH=src ruff format --check src tests`
  - passed
- `git diff --check`
  - passed
- `swift build --target SpecHarvesterDocs`
  - passed
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - `741 passed, 1 skipped`
  - total coverage: `91.06%`

## Boundary Verification

- [x] The command reads only CLI arguments and optional source manifest
  metadata.
- [x] The command does not collect source files.
- [x] The command does not run analyzers, package managers, or AI.
- [x] The command does not draft packages.
- [x] The command does not publish registry metadata or accept packages or
  relations.
- [x] The generated artifact contains non-authority statements for these
  boundaries.

## Next Step

Proceed to `P37-T4 Connect repository profile selection to autonomous
candidate batch`.
