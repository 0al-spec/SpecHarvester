# P17-T5 Validation Report

Task: P17-T5 Collector and Drafter Vertical Slice Objects
Date: 2026-06-14
Verdict: PASS

## Summary

P17-T5 moved the single-package draft candidate bundle materialization path
behind `SinglePackageDraftBundle`.

`draft_spec_package` still owns package manifest, BoundarySpec, capability,
intent, evidence, provenance, compatibility, and keyword assembly. The new
object owns the explicit output behavior for:

- candidate directory creation;
- bundled `harvest.json` materialization;
- optional `public-interface-index.json` emission;
- `specpm.yaml` and `specs/*.spec.yaml` writing;
- producer validation and diagnostics reports;
- author-ready quality report;
- producer receipt emission;
- wrapper-compatible result payload assembly.

## Implementation Evidence

- Added `SinglePackageDraftBundle` with explicit `materialize()` behavior.
- Kept `DraftOptions` and `draft_spec_package(options)` as the public API.
- Preserved generated file names, result fields, producer receipt output roles,
  report paths, diagnostics entries, author-ready summary, and the rule that
  `producer-receipt.json` is excluded from receipt `outputs[]`.
- Added object-level characterization coverage for bundle materialization.
- Updated EO strategy docs and DocC mirror to record the P17-T5 drafter output
  slice.

## Procedural Style Evidence

Parent branch baseline for `drafter.py`:

```text
behaviorRichClassCount=0
topLevelFunctionCount=75
topLevelFunctionSpan=1665
methodCount=0
methodSpan=0
```

P17-T5 result for `drafter.py`:

```text
behaviorRichClassCount=1
topLevelFunctionCount=75
topLevelFunctionSpan=1550
methodCount=10
methodSpan=194
```

`drafter.py` remains an intentional procedural hotspot. The task only moved the
first mature output-materialization slice.

## Architecture Lint Evidence

Command:

```bash
PYTHONPATH=src python -m spec_harvester architecture-lint \
  --path src/spec_harvester/drafter.py \
  --output /tmp/p17-t5-architecture-lint.json
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
PYTHONPATH=src python -m pytest tests/test_collector.py -q -k 'draft_spec_package or single_package_draft_bundle'
PYTHONPATH=src ruff format src/spec_harvester/drafter.py tests/test_collector.py
PYTHONPATH=src ruff check src/spec_harvester/drafter.py tests/test_collector.py
PYTHONPATH=src ruff format --check src/spec_harvester/drafter.py tests/test_collector.py
PYTHONPATH=src python -m pytest tests/test_collector.py -q -k 'draft_spec_package or single_package_draft_bundle'
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'eo_refactoring_strategy or current_next_task'
PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester/drafter.py --output /tmp/p17-t5-architecture-lint.json
PYTHONPATH=src python -m spec_harvester procedural-style-report --path src/spec_harvester/drafter.py --output /tmp/p17-t5-procedural-style-after.json
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_docs_contracts.py -q -k 'draft_spec_package or single_package_draft_bundle or eo_refactoring_strategy or current_next_task'
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q
swift build --target SpecHarvesterDocs
swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --disable-indexing --transform-for-static-hosting --hosting-base-path SpecHarvester --output-path ./.docc-build
swift package dump-package >/dev/null
```

## Validation Results

- Focused drafter tests: `36 passed, 60 deselected`.
- Focused drafter/docs tests: `37 passed, 147 deselected`.
- Focused docs-contract test: `1 passed, 87 deselected`.
- Ruff check: passed.
- Ruff format check: `109 files already formatted`.
- Git diff whitespace check: passed.
- Full pytest: `678 passed, 1 skipped`.
- Coverage: `678 passed, 1 skipped`, total coverage `90.71%`, coverage gate
  passed with required threshold `90%`.
- Swift package dump: passed.
- Swift docs target build: passed.
- Static DocC generation: passed with pre-existing unrelated warnings for
  `AcceptedPackageUpdateProposals` and inline command references.
- Architecture lint smoke for `drafter.py`: `status: ok`.
- Procedural-style smoke: behavior-rich drafter classes increased from `0` to
  `1`, and `drafter.py` top-level span dropped from `1665` to `1550`.

## Acceptance Criteria

- Existing `draft_spec_package` tests pass without generated contract changes:
  satisfied.
- The new object constructor performs no filesystem access, subprocess
  execution, network access, package installation, or repository imports:
  satisfied.
- Filesystem writes happen through explicit behavior methods: satisfied.
- `producer-receipt.json` remains excluded from receipt `outputs[]`: satisfied.
- Optional public interface index behavior remains unchanged: satisfied.
- Coverage remains above 90%: satisfied.
