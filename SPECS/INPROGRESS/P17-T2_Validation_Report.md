# P17-T2 Validation Report

Task: P17-T2 CLI Domain Command Objects
Date: 2026-06-14
Verdict: PASS

## Summary

P17-T2 split selected CLI report execution bodies out of `cli.py` into
behavior-rich command objects in `src/spec_harvester/cli_report_commands.py`.

The parser shell remains in `cli.py`; public CLI command names, parser flags,
default values, JSON error output, report schemas, and exit-code behavior are
preserved for:

- `code-duplication-report`;
- `architecture-lint`;
- `procedural-style-report`.

## Implementation Evidence

- Added `CodeDuplicationReportCommand`.
- Added `ArchitectureLintCommand`.
- Added `ProceduralStyleReportCommand`.
- Added direct command-object characterization tests in
  `tests/test_cli_report_commands.py`.
- Existing CLI tests for the three commands still pass unchanged.
- EO documentation records the P17-T2 command-object slice.

## Procedural Style Evidence

Command:

```bash
PYTHONPATH=src python -m spec_harvester procedural-style-report \
  --path src/spec_harvester/cli.py \
  --path src/spec_harvester/cli_report_commands.py \
  --output /tmp/p17-t2-procedural-style.json
```

Result summary:

```json
{
  "behaviorRichClassCount": 3,
  "classCount": 4,
  "methodCount": 16,
  "methodSpan": 73,
  "topLevelFunctionCount": 36,
  "topLevelFunctionSpan": 1608
}
```

`src/spec_harvester/cli_report_commands.py` contains:

```text
topLevelFunctionCount=4
topLevelFunctionSpan=8
methodCount=16
methodSpan=73
behaviorRichClassCount=3
```

`cli.py` remains a hotspot because parser construction and many other command
wrappers are intentionally out of scope for P17-T2.

## Architecture Lint Evidence

Command:

```bash
PYTHONPATH=src python -m spec_harvester architecture-lint \
  --path src/spec_harvester/cli_report_commands.py \
  --output /tmp/p17-t2-architecture-lint.json
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
PYTHONPATH=src python -m pytest tests/test_cli_report_commands.py tests/test_code_duplication_report.py tests/test_architecture_lint.py tests/test_procedural_style_report.py -q
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'eo_refactoring_strategy or limited_corpus_intake_readiness_decision or next_corpus_intake_readiness_decision'
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
PYTHONPATH=src python -m pytest -q
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q
swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --disable-indexing --transform-for-static-hosting --hosting-base-path SpecHarvester --output-path ./.docc-build
PYTHONPATH=src python -m spec_harvester procedural-style-report --path src/spec_harvester/cli.py --path src/spec_harvester/cli_report_commands.py --output /tmp/p17-t2-procedural-style.json
PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester/cli_report_commands.py --output /tmp/p17-t2-architecture-lint.json
```

## Validation Results

- Focused report command tests: `46 passed`.
- Focused docs-contract tests: `4 passed, 84 deselected`.
- Ruff check: passed.
- Ruff format check: `109 files already formatted`.
- Git diff whitespace check: passed.
- Full pytest: `669 passed, 1 skipped`.
- Swift package dump: passed.
- Swift docs target build: passed.
- Coverage: `669 passed, 1 skipped`, total coverage `90.60%`, coverage gate
  passed with required threshold `90%`.
- Static DocC generation: passed with pre-existing unrelated warnings for
  `AcceptedPackageUpdateProposals` and inline command references.
- Procedural style smoke: produced `behaviorRichClassCount: 3` for the new
  command-object slice.
- Architecture lint smoke for `cli_report_commands.py`: `status: ok`.

## Acceptance Criteria

- `code-duplication-report` preserves parser flags, JSON error output,
  output-file behavior, report schema, and fail-on-duplicates exit code:
  satisfied.
- `architecture-lint` preserves parser flags, JSON error output, output-file
  behavior, report schema, and fail-on-issues exit code: satisfied.
- `procedural-style-report` preserves parser flags, procedural-style error
  mapping, output-file behavior, report schema, and fail-on-hotspots exit code:
  satisfied.
- No SpecPM or SpecNode contracts changed: satisfied.
- Coverage remains above 90%: satisfied.
