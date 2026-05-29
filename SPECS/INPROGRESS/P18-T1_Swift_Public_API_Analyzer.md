# P18-T1 — Swift Public API Analyzer

Branch: `feature/P18-T1-swift-public-api-analyzer`
Review subject: `p18_t1_swift_public_api_analyzer`

## Context

SpecHarvester already has `PublicInterfaceIndex`, shared public API analyzer
options, analyzer orchestration, cache support, and drafter ingestion for
`public-interface-index.json`. Python, JavaScript/TypeScript, and Go can emit
deterministic public interface evidence, but Swift/SPM repositories currently
fall back to manifest and documentation evidence only.

That leaves Swift candidates with weaker interface signals even though Swift
package discovery and product intent extraction already exist.

## Scope

- Add a deterministic Swift public API analyzer module.
- Scan `.swift` files as untrusted text without invoking SwiftPM, `swift`,
  build tools, package scripts, tests, or network probes.
- Extract `public` and `open` declarations for classes, structs, protocols,
  enums, actors, functions, initializers, properties, and enum cases where the
  syntax is visible through a lightweight parser.
- Emit `PublicInterfaceIndex` packages, entrypoints, symbols, evidence paths,
  source digests, analyzer version, execution policy, and diagnostics through
  the existing schema.
- Register the analyzer in `ANALYZER_ADAPTERS`.
- Add Swift/SPM analyzer-plan wiring so project profiles can request the Swift
  analyzer automatically.
- Add regression tests for extraction, filtering, cache behavior, diagnostics,
  and orchestration.

## Non-Goals

- Do not execute SwiftPM, compilers, formatters, tests, package plugins, build
  scripts, dependency installers, or network operations against harvested code.
- Do not perform full Swift parsing, type-checking, macro expansion, access
  control inference, conditional compilation evaluation, or protocol witness
  resolution.
- Do not model imported dependency APIs or generated build output.
- Do not change drafter behavior except through the existing
  `public-interface-index.json` evidence path.
- Do not refactor all public API analyzers into EO objects; that remains
  `P17-T4`.

## Design

- Follow the existing public analyzer contract used by Python, JS/TS, and Go:
  a public `analyze()` function accepts source path, optional package id,
  source revision, and cache directory.
- Use deterministic text parsing with comment/string masking and brace-depth
  tracking rather than invoking Swift tooling.
- Treat explicitly `public` or `open` declarations as public symbols.
- Preserve compact signatures and symbol names suitable for weak-model drafting;
  bodies are never emitted.
- Record parser limitations as diagnostics instead of failing a whole harvest
  when individual files are unreadable or syntactically unusual.
- Keep Swift-specific policy inside `swift_public_api.py` and only add narrow
  registry/profile hooks elsewhere.

## Acceptance Criteria

- A Swift package fixture emits `public-interface-index.json` evidence with
  package metadata, entrypoints, public symbols, analyzer provenance, and source
  digests.
- Internal/private Swift declarations are not emitted as public symbols.
- Public/open nested declarations are named with their containing type when
  statically visible.
- Project-profile analyzer orchestration can run the Swift analyzer when an SPM
  or Swift source profile requests it.
- Cache behavior matches the existing public API analyzer pattern.
- Configured Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_swift_public_api.py tests/test_analyzer_orchestration.py -q`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
