# P27-T2 Validation Report

Task: `P27-T2 Author-Ready Draft Quality Report`

## Result

Implemented.

## Scope Validated

- Generated candidate bundles now emit
  `author-ready-draft-quality-report.json`.
- The report exposes:
  - `apiVersion: spec-harvester.author-ready-draft-quality/v0`;
  - `kind: SpecHarvesterAuthorReadyDraftQualityReport`;
  - `authorReadyDraft.status`;
  - hard gates;
  - advisory dimensions;
  - structured `authorActionItems`.
- `producer-receipt.json` includes the report as `outputs[].role:
  quality_report` with a SHA-256 digest.
- Package-set member records and handoff proposals link member quality reports.
- Static renderer JSON exposes `producer.quality`.
- GitHub docs and DocC mirror the contract.

## Commands

```bash
PYTHONPATH=src pytest tests/test_author_ready_quality_report.py tests/test_collector.py tests/test_candidate_bundle_e2e.py tests/test_package_set_drafter.py tests/test_package_set_handoff_proposal.py tests/test_static_spec_renderer.py tests/test_docs_contracts.py -q
```

Result: `181 passed`.

```bash
PYTHONPATH=src ruff check src tests
```

Result: passed.

```bash
PYTHONPATH=src ruff format --check src tests
```

Result: passed.

```bash
git diff --check
```

Result: passed.

```bash
PYTHONPATH=src pytest -q
```

Result before review follow-up: `569 passed, 1 skipped`.

Final result after review follow-up: `570 passed, 1 skipped`.

```bash
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result before review follow-up: `569 passed, 1 skipped`; total coverage
`90.12%`.

Final result after review follow-up: `570 passed, 1 skipped`; total coverage
`90.12%`.

```bash
swift build --target SpecHarvesterDocs
```

Result: passed.

```bash
rm -rf .docc-build && swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester; rc=$?; rm -rf .docc-build; exit $rc
```

Result: passed with pre-existing unrelated DocC warnings for
`AcceptedPackageUpdateProposals` and inline command links.

## Notes

- The quality report is producer-side review evidence only.
- `author_ready_draft` means a valid starter package is ready for author review;
  it is not SpecPM registry acceptance, maintainer approval, or upstream
  endorsement.
- `producer-receipt.json` remains outside `outputs[]` to avoid the self-hash
  problem.
