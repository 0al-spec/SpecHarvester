# P17-T4 Validation Report

Task: P17-T4 Public API Analyzer Pipeline Objects
Date: 2026-06-14
Verdict: PASS

## Summary

P17-T4 moved the top-level public API analyzer pipelines for Python, Go, and
JavaScript/TypeScript behind language-specific behavior-rich analyzer objects.

Public analyzer functions and generated `PublicInterfaceIndex` payloads remain
compatible:

- `analyze_python_public_api`;
- `analyze_python_public_api_with_options`;
- `analyze_go_public_api`;
- `analyze_go_public_api_with_options`;
- `analyze_js_ts_public_api`;
- `analyze_js_ts_public_api_with_options`.

## Implementation Evidence

- Added `PythonPublicApiAnalyzer` with deterministic `index()` behavior.
- Added `GoPublicApiAnalyzer` with deterministic `index()` behavior.
- Added `JavaScriptTypeScriptPublicApiAnalyzer` with deterministic `index()`
  behavior.
- Kept parser, symbol, diagnostic, evidence, cache payload, analyzer metadata,
  and `PublicInterfaceIndex` validation helpers unchanged.
- Added object-level characterization tests that compare object output with the
  public wrapper output.
- Updated EO strategy docs and DocC mirror to record the analyzer pipeline slice.

## Procedural Style Evidence

Parent branch baseline across `python_public_api.py`, `go_public_api.py`, and
`js_ts_public_api.py`:

```text
behaviorRichClassCount=0
topLevelFunctionCount=75
topLevelFunctionSpan=1085
methodCount=0
methodSpan=0
```

P17-T4 result across the same modules:

```text
behaviorRichClassCount=3
topLevelFunctionCount=75
topLevelFunctionSpan=927
methodCount=24
methodSpan=219
```

The modules remain procedural hotspots because parser and symbol internals were
intentionally left untouched for future narrower slices.

## Architecture Lint Evidence

Command:

```bash
PYTHONPATH=src python -m spec_harvester architecture-lint \
  --path src/spec_harvester/python_public_api.py \
  --path src/spec_harvester/go_public_api.py \
  --path src/spec_harvester/js_ts_public_api.py \
  --output /tmp/p17-t4-architecture-lint.json
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
PYTHONPATH=src python -m pytest tests/test_python_public_api.py tests/test_go_public_api.py tests/test_js_ts_public_api.py -q
PYTHONPATH=src ruff check src/spec_harvester/python_public_api.py src/spec_harvester/go_public_api.py src/spec_harvester/js_ts_public_api.py tests/test_python_public_api.py tests/test_go_public_api.py tests/test_js_ts_public_api.py
PYTHONPATH=src ruff check --fix tests/test_go_public_api.py
PYTHONPATH=src ruff format src/spec_harvester/python_public_api.py src/spec_harvester/go_public_api.py src/spec_harvester/js_ts_public_api.py tests/test_python_public_api.py tests/test_go_public_api.py tests/test_js_ts_public_api.py
PYTHONPATH=src ruff check src/spec_harvester/python_public_api.py src/spec_harvester/go_public_api.py src/spec_harvester/js_ts_public_api.py tests/test_python_public_api.py tests/test_go_public_api.py tests/test_js_ts_public_api.py
PYTHONPATH=src python -m pytest tests/test_python_public_api.py tests/test_go_public_api.py tests/test_js_ts_public_api.py -q
PYTHONPATH=src python -m spec_harvester procedural-style-report --path /tmp/p17-t4-before --output /tmp/p17-t4-procedural-style-before.json
PYTHONPATH=src python -m spec_harvester procedural-style-report --path src/spec_harvester/python_public_api.py --path src/spec_harvester/go_public_api.py --path src/spec_harvester/js_ts_public_api.py --output /tmp/p17-t4-procedural-style-after.json
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'current_next_task or eo_refactoring_strategy'
PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester/python_public_api.py --path src/spec_harvester/go_public_api.py --path src/spec_harvester/js_ts_public_api.py --output /tmp/p17-t4-architecture-lint.json
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
PYTHONPATH=src python -m pytest tests/test_python_public_api.py tests/test_go_public_api.py tests/test_js_ts_public_api.py tests/test_docs_contracts.py -q -k 'public_api or current_next_task or eo_refactoring_strategy'
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q
swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --disable-indexing --transform-for-static-hosting --hosting-base-path SpecHarvester --output-path ./.docc-build
```

## Validation Results

- Focused analyzer tests: `28 passed`.
- Focused analyzer/docs test set: `29 passed, 87 deselected`.
- Focused docs-contract test: `1 passed, 87 deselected`.
- Ruff check: passed.
- Ruff format check: `109 files already formatted`.
- Git diff whitespace check: passed.
- Swift package dump: passed.
- Swift docs target build: passed.
- Full pytest: `677 passed, 1 skipped`.
- Coverage: `677 passed, 1 skipped`, total coverage `90.68%`, coverage gate
  passed with required threshold `90%`.
- Static DocC generation: passed with pre-existing unrelated warnings for
  `AcceptedPackageUpdateProposals` and inline command references.
- Architecture lint smoke for the three analyzer modules: `status: ok`.
- Procedural-style smoke: behavior-rich analyzer classes increased from `0` to
  `3`, and analyzer top-level span dropped from `1085` to `927`.

## Acceptance Criteria

- `PublicInterfaceIndex` shape and validation behavior are preserved:
  satisfied.
- Analyzer ids, versions, confidence values, execution policy, package language
  values, diagnostics, evidence records, entrypoint sorting, and cache behavior
  are preserved: satisfied.
- Public analyzer functions keep their signatures and still accept either
  `Path` plus keyword options or `PublicApiAnalyzerOptions`: satisfied.
- Constructors remain simple and do not perform filesystem access, subprocesses,
  repository imports, package installation, or network access: satisfied.
- Coverage remains above 90%: satisfied.
