# P32-T2 Validation Report: Deferred Candidate Regeneration Runbook

**Date:** 2026-06-13
**Verdict:** PASS

## Scope

P32-T2 added an operator runbook for deferred autonomous candidates. The
runbook documents safe local inputs, regeneration classes, expected artifacts,
stop conditions, re-entry criteria, and non-authority boundaries for the six
deferred candidates:

- `xyflow.workspace`
- `xyflow.react`
- `xyflow.svelte`
- `xyflow.system`
- `cupertino.core`
- `navigation_split_view.core`

## Validation

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
```

Result: `72 passed`

```bash
PYTHONPATH=src pytest -q
```

Result: `648 passed, 1 skipped`

```bash
PYTHONPATH=src ruff check .
```

Result: `All checks passed!`

```bash
PYTHONPATH=src ruff format --check src tests
git diff --check
```

Result: passed

```bash
PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90
```

Result: `648 passed, 1 skipped`; coverage `90.56%`

```bash
swift package dump-package >/tmp/specharvester-p32-t2-package.json
swift build --target SpecHarvesterDocs
```

Result: passed

```bash
rm -rf /tmp/specharvester-p32-t2-docc-build-spec
swift package --allow-writing-to-directory /tmp/specharvester-p32-t2-docc-build-spec \
  generate-documentation \
  --target SpecHarvester \
  --output-path /tmp/specharvester-p32-t2-docc-build-spec \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester
```

Result: passed. The command emitted pre-existing unrelated DocC warnings for
`AcceptedPackageUpdateProposals` and `RealRepositoryQualityReport`.

## Notes

- No actual regeneration was run.
- No LM Studio/provider calls were made.
- No SpecPM registry or accepted-source files were changed.
- The runbook remains review-evidence guidance, not registry authority.
