# P17-T3 Validation Report

Task: P17-T3 Report Builder Behavior Objects
Date: 2026-06-14
Verdict: PASS

## Summary

P17-T3 refactored the accepted candidate diff report builder behind
behavior-rich objects while preserving the public
`SpecHarvesterAcceptedCandidateDiffReport` output contract.

The public compatibility functions remain in place for CLI and downstream
imports:

- `build_accepted_candidate_diff_report`;
- `collect_package_diff_records`;
- `latest_accepted_by_package_id`;
- `build_candidate_comparison`;
- `diff_records`;
- `write_accepted_candidate_diff_report`.

## Implementation Evidence

- Added `AcceptedCandidateDiffReport` for report assembly.
- Added `PackageDiffSource` for deterministic `specpm.yaml` source scanning and
  issue generation.
- Added `AcceptedPackageVersions` for latest accepted version selection.
- Added `CandidateComparison` and `PackageRecordDiff` for comparison and delta
  behavior.
- Added `AcceptedCandidateDiffReportWriter` for JSON report writing.
- Added object-level characterization tests while keeping existing public
  wrapper and CLI tests unchanged.
- Updated EO strategy docs and DocC mirror to record the completed report-object
  slice.

## Procedural Style Evidence

Parent branch baseline for `accepted_diff.py`:

```text
behaviorRichClassCount=0
topLevelFunctionCount=13
topLevelFunctionSpan=204
methodCount=0
methodSpan=0
```

P17-T3 result for `accepted_diff.py`:

```text
behaviorRichClassCount=4
topLevelFunctionCount=13
topLevelFunctionSpan=87
methodCount=18
methodSpan=168
```

This moves the accepted diff report decisions behind behavior methods while
leaving compatibility wrappers available for existing callers.

## Architecture Lint Evidence

Command:

```bash
PYTHONPATH=src python -m spec_harvester architecture-lint \
  --path src/spec_harvester/accepted_diff.py \
  --output /tmp/p17-t3-architecture-lint.json
```

Result:

```json
{
  "status": "ok",
  "summary": {
    "issueCount": 0,
    "skippedFileCount": 0
  }
}
```

## Validation Commands

```bash
PYTHONPATH=src python -m pytest tests/test_accepted_candidate_diff.py tests/test_accepted_candidate_impact.py tests/test_accepted_package_update_proposal.py -q
PYTHONPATH=src ruff check src/spec_harvester/accepted_diff.py tests/test_accepted_candidate_diff.py
PYTHONPATH=src ruff format src/spec_harvester/accepted_diff.py tests/test_accepted_candidate_diff.py
PYTHONPATH=src ruff check src/spec_harvester/accepted_diff.py tests/test_accepted_candidate_diff.py
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'eo_refactoring_strategy or current_next_task'
PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester/accepted_diff.py --output /tmp/p17-t3-architecture-lint.json
PYTHONPATH=src python -m spec_harvester procedural-style-report --path src/spec_harvester/accepted_diff.py --output /tmp/p17-t3-procedural-style.json
PYTHONPATH=src python -m spec_harvester procedural-style-report --path /tmp/p17-t3-accepted-diff-before.py --output /tmp/p17-t3-procedural-style-before.json
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
PYTHONPATH=src python -m pytest tests/test_accepted_candidate_diff.py tests/test_accepted_candidate_impact.py tests/test_accepted_package_update_proposal.py tests/test_docs_contracts.py -q -k 'accepted_candidate or eo_refactoring_strategy or current_next_task'
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q
swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --disable-indexing --transform-for-static-hosting --hosting-base-path SpecHarvester --output-path ./.docc-build
```

## Validation Results

- Focused accepted diff/downstream accepted report tests: `34 passed`.
- Focused docs-contract test: `1 passed, 87 deselected`.
- Focused accepted/docs test set: `22 passed, 100 deselected`.
- Ruff check: passed.
- Ruff format check: `109 files already formatted`.
- Git diff whitespace check: passed.
- Swift package dump: passed.
- Swift docs target build: passed.
- Full pytest: `674 passed, 1 skipped`.
- Coverage: `674 passed, 1 skipped`, total coverage `90.63%`, coverage gate
  passed with required threshold `90%`.
- Static DocC generation: passed with pre-existing unrelated warnings for
  `AcceptedPackageUpdateProposals` and inline command references.
- Architecture lint smoke for `accepted_diff.py`: `status: ok`.
- Procedural-style smoke for `accepted_diff.py`: `behaviorRichClassCount: 4`,
  `topLevelFunctionSpan: 87`.

## Acceptance Criteria

- `SpecHarvesterAcceptedCandidateDiffReport` schema fields are preserved:
  satisfied.
- Existing issue codes remain unchanged: satisfied.
- Existing comparison statuses remain unchanged: satisfied.
- Metadata, intent, capability, and upstream artifact diff semantics remain
  unchanged: satisfied.
- CLI `accepted-candidate-diff-report` output behavior remains unchanged:
  satisfied.
- Downstream accepted impact and update proposal imports keep working:
  satisfied.
- Coverage remains above 90%: satisfied.
