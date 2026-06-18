# P37-T2 Validation Report

## Verdict

PASS

## Summary

P37-T2 adds the first machine-readable
`SpecHarvesterRepositoryProfileDetection` fixture:

```text
tests/fixtures/repository_profile_detection/generic-package-set.example.json
```

The fixture records a high-confidence `auto` selection of
`generic.package_set.v0`, a `generic.repository.v0` fallback, rejected lower
confidence candidates, diagnostics, advisory downstream hints, and explicit
non-authority statements.

The fixture is documentation/test contract only. It does not implement runtime
profile detection, add a CLI, change autonomous candidate batch behavior, or
publish registry metadata.

## Deliverables Checked

- [x] Added
  `tests/fixtures/repository_profile_detection/generic-package-set.example.json`.
- [x] Documented the fixture in
  `docs/REPOSITORY_PROFILE_SELECTION_CONTRACT.md`.
- [x] Mirrored the fixture documentation in DocC.
- [x] Added docs-contract regression coverage for required fixture shape,
  selection fields, candidate/rejection records, diagnostics, advisory hints,
  follow-up links, and non-authority statements.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile_detection_fixture or repository_profile_selection_contract or current_next_task'`
  - `2 passed, 102 deselected`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
  - `104 passed`
- `PYTHONPATH=src pytest -q`
  - `735 passed, 1 skipped`
- `PYTHONPATH=src ruff check .`
  - passed
- `PYTHONPATH=src ruff format --check src tests`
  - passed
- `python -m json.tool tests/fixtures/repository_profile_detection/generic-package-set.example.json >/dev/null`
  - passed
- `git diff --check`
  - passed
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - `735 passed, 1 skipped`
  - total coverage: `91.03%`
- `swift build --target SpecHarvesterDocs`
  - passed

## Boundary Verification

- [x] No runtime profile detector was added.
- [x] No CLI/report surface was added.
- [x] No autonomous candidate batch behavior was changed.
- [x] No language-specific profile implementation was added.
- [x] The fixture states it does not clone/fetch repositories, install
  dependencies, execute harvested code, invoke package managers, run AI, draft
  packages, publish registry metadata, accept packages or relations, seed
  baselines, remove `preview_only`, treat plugin decisions as registry truth,
  or treat AI output as registry truth.

## Next Step

Proceed to `P37-T3 Implement an opt-in repository profile detection CLI/report
surface`.
