# P28-T5 Validation Report

Verdict: PASS
Date: 2026-06-13

## Implementation Summary

- Added `SpecHarvesterBaselineSubmissionHandoff`.
- Added `baseline-submission-handoff` CLI.
- The command reads `SpecHarvesterFreshCandidateRefreshRun` and optional SpecPM
  `prepare-report.json`.
- When the prepare report contains
  `refresh_decision_prepare_current_contract_files_missing`, the output status
  is `first_submission_required`.
- When no prepare report is supplied, the output status is
  `baseline_review_required`.
- Prepare reports without missing-baseline diagnostics are rejected to avoid
  creating misleading first-submission evidence.

## Practical TanStack/query Check

Run root:

```text
/tmp/specharvester-p28-t5-baseline-handoff
```

Commands:

```bash
PYTHONPATH=src python3 -m spec_harvester fresh-candidate-refresh-run \
  --bundle-set /tmp/specharvester-p28-t4-tanstack-profile/package-set-profile \
  --fresh-generated-root /tmp/specharvester-p28-t5-baseline-handoff/fresh-generated \
  --source-repository https://github.com/TanStack/query \
  --source-revision feb1efd804c1262106f72c8adc1d82a8ce9cfbb0 \
  --run-label p28-t5-tanstack-baseline-handoff \
  --output /tmp/specharvester-p28-t5-baseline-handoff/fresh-candidate-refresh-run.json

PYTHONPATH=src python3 -m spec_harvester baseline-submission-handoff \
  --fresh-candidate-refresh-run /tmp/specharvester-p28-t5-baseline-handoff/fresh-candidate-refresh-run.json \
  --specpm-prepare-report /tmp/specharvester-p28-t3-tanstack-query-refresh/prepare-report-member.json \
  --output /tmp/specharvester-p28-t5-baseline-handoff/baseline-submission-handoff.json
```

Observed result:

- `status`: `first_submission_required`
- `reason`: `missing_current_generated_baseline`
- package-set id: `tanstack_query.workspace`
- candidate count: `39`
- contract file count: `78`
- missing-baseline diagnostic count: `39`
- `authority.notRefreshDecision`: `true`
- maintainer actions:
  - `first_submission_review`
  - `seed_baseline`
  - `reject_or_request_regeneration`

## Automated Validation

```bash
PYTHONPATH=src pytest tests/test_baseline_submission_handoff.py tests/test_docs_contracts.py -q
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

- targeted tests: `53 passed`
- full tests: `603 passed, 1 skipped`
- coverage: `90%`
- ruff: passed
- format check: passed
- diff check: passed
- Swift docs build: passed
- DocC static generation: passed with pre-existing unrelated warnings for
  `AcceptedPackageUpdateProposals`, `quality-report`, and `specpm validate`.
