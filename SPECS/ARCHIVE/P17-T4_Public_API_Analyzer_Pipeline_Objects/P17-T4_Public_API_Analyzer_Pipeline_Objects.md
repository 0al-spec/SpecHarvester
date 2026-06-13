# P17-T4 Public API Analyzer Pipeline Objects

Status: Planned
Phase: Phase 17. Elegant Objects Refactoring Strategy
Owner: SpecHarvester public interface indexing track

## Objective

Refactor the public API analyzer entry pipelines into language-specific
behavior objects while preserving public analyzer functions and
`PublicInterfaceIndex` payloads.

The P17-T4 slice covers the top-level pipeline for:

- Python AST public API analysis;
- Go source public API analysis;
- JavaScript/TypeScript manifest export analysis.

This is not a parser rewrite. The goal is to move root normalization, cache
coordination, diagnostics aggregation, package assembly, analyzer metadata, and
index validation behind named analyzer objects that carry
`PublicApiAnalyzerOptions`.

## Motivation

P17-T3 proved the report-object seam on a mature report contract. Public API
analyzers are the next procedural concentration. They already share
`PublicApiAnalyzerOptions` and payload record objects, but their top-level
pipelines still live as large procedural functions.

Moving the top-level pipelines behind language-specific analyzer objects gives
future P17 work stable seams for deeper parse, diagnostic, symbol, and evidence
objects without changing generated indexes now.

## Deliverables

- Add `PythonPublicApiAnalyzer` with a deterministic `index()` method.
- Add `GoPublicApiAnalyzer` with a deterministic `index()` method.
- Add `JavaScriptTypeScriptPublicApiAnalyzer` with a deterministic `index()`
  method.
- Keep compatibility wrappers unchanged:
  - `analyze_python_public_api`;
  - `analyze_python_public_api_with_options`;
  - `analyze_go_public_api`;
  - `analyze_go_public_api_with_options`;
  - `analyze_js_ts_public_api`;
  - `analyze_js_ts_public_api_with_options`.
- Add direct object-level characterization tests for all three analyzer
  objects.
- Update EO strategy docs and docs-contract tests to record the completed
  analyzer pipeline slice.
- Add validation report and Flow archive/review artifacts.

## Acceptance Criteria

- Existing `PublicInterfaceIndex` shape and validation behavior remain
  unchanged for Python, Go, and JS/TS analyzer tests.
- Analyzer ids, analyzer versions, confidence values, execution policy, package
  language values, diagnostics, evidence records, entrypoint sorting, and cache
  behavior remain unchanged.
- Existing public analyzer functions keep their signatures and continue to
  accept either a `Path` plus keyword options or a `PublicApiAnalyzerOptions`
  object.
- Constructors do not perform filesystem access, subprocesses, imports from
  analyzed repositories, package installation, or network access.
- Coverage remains at or above 90%.

## Test-First Plan

1. Add object-level tests that instantiate the three analyzer objects with
   `PublicApiAnalyzerOptions` and assert their indexes match the corresponding
   public wrapper outputs.
2. Keep existing Python, Go, and JS/TS analyzer tests unchanged as public
   contract characterization.
3. Run focused analyzer tests before full quality gates.

## Implementation Plan

### Phase 1: Analyzer Object Seams

Inputs:

- current `*_with_options` functions;
- existing helper functions for source discovery, parsing, cache reads/writes,
  symbols, diagnostics, and package assembly.

Outputs:

- one language-specific analyzer object per module with an `index()` method;
- wrappers that delegate to the objects.

Verification:

- direct object tests match wrapper output;
- existing analyzer tests pass unchanged.

### Phase 2: Documentation and Metrics

Inputs:

- EO refactoring strategy;
- docs-contract assertions;
- procedural-style report.

Outputs:

- docs and DocC mention the P17-T4 analyzer-object slice;
- validation records object movement metrics.

Verification:

- docs-contract tests pass;
- architecture lint does not report new issues.

### Phase 3: Flow Validation

Inputs:

- `.flow/params.yaml` quality gates;
- P17 acceptance metrics.

Outputs:

- validation report;
- archived task artifacts;
- review report.

Verification:

- focused analyzer tests;
- full pytest;
- ruff check and format check;
- coverage gate;
- Swift docs build and static DocC generation.

## Non-Goals

- Do not rewrite parser internals for Python, Go, or JS/TS.
- Do not change `PublicInterfaceIndex` schema or analyzer metadata.
- Do not change cache key formats or payload shapes.
- Do not change analyzer orchestration, collector, drafter, SpecPM, SpecNode,
  package-set, or autonomous batch contracts.
- Do not remove public analyzer compatibility functions.
