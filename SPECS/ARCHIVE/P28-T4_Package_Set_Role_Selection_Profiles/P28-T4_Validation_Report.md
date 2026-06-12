# P28-T4 Validation Report

Verdict: PASS
Date: 2026-06-13

## Implementation Summary

- Added package-set role selection profiles to `draft-package-set`.
- Added `--role-profile generic_monorepo` for workspace/member package-set
  drafting.
- Preserved explicit `--role` override behavior; explicit roles record
  `selection.roleProfile: custom`.
- Updated GitHub docs, DocC docs, and docs-contract coverage.

## Practical TanStack/query Check

Source checkout:

```text
/tmp/specharvester-p28-t3-tanstack-query-source
```

Revision:

```text
feb1efd804c1262106f72c8adc1d82a8ce9cfbb0
```

Run root:

```text
/tmp/specharvester-p28-t4-tanstack-profile
```

Commands:

```bash
PYTHONPATH=src python3 -m spec_harvester collect-batch \
  /tmp/specharvester-p28-t4-tanstack-profile/inputs \
  --out /tmp/specharvester-p28-t4-tanstack-profile/candidates \
  --emit-workspace-inventory \
  --report /tmp/specharvester-p28-t4-tanstack-profile/batch-validation.json

PYTHONPATH=src python3 -m spec_harvester draft-package-set \
  /tmp/specharvester-p28-t4-tanstack-profile/candidates/tanstack-query/workspace-inventory.json \
  --out /tmp/specharvester-p28-t4-tanstack-profile/package-set-profile \
  --role-profile generic_monorepo
```

Observed result:

- `selection.roleProfile`: `generic_monorepo`
- `selection.roles`: `workspace`, `member_package`
- candidate count: `39`
- relation proposal count: `38`
- skipped count: `61`

This matches the useful P28-T3 TanStack/query shape without requiring explicit
`--role workspace --role member_package`.

## Automated Validation

```bash
PYTHONPATH=src pytest tests/test_package_set_drafter.py tests/test_docs_contracts.py -q
PYTHONPATH=src pytest -q
PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing -q
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
swift build --target SpecHarvesterDocs
swift package --allow-writing-to-directory ./.docc-build generate-documentation \
  --target SpecHarvester \
  --output-path ./.docc-build \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester
```

Results:

- targeted tests: `69 passed`
- full tests: `597 passed, 1 skipped`
- coverage: `90%`
- ruff: passed
- format check: passed
- diff check: passed
- Swift docs build: passed
- DocC static generation: passed with pre-existing unrelated warnings for
  `AcceptedPackageUpdateProposals`, `quality-report`, and `specpm validate`.
