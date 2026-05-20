# P12-T2 Go Public Interface Evidence

Status: In Progress
Created: 2026-05-21
Task: `P12-T2` Add a deterministic Go public interface analyzer or
manifest-plus-source fallback for `go.mod` projects.

## Problem

`gin-gonic/gin` is detected as a Go module from `go.mod`, but analyzer
orchestration currently leaves it at `manifest_only`. That gives weak-model
drafting little deterministic material about exported packages, functions,
types, methods, constants, and variables.

SpecHarvester needs compact local-only public interface evidence for Go
repositories without executing `go`, package scripts, tests, builds, or network
probes.

## Goals

- Emit a `public-interface-index.json` for Go module repositories when Go source
  files are present.
- Extract exported package-level declarations and exported methods using
  deterministic source parsing.
- Include package/module metadata, source paths, counts, diagnostics, and trust
  policy fields consistent with existing `PublicInterfaceIndex` output.
- Integrate the Go analyzer into existing analyzer orchestration so `collect-batch
  --emit-interface-indexes` upgrades Go projects from `manifest_only` to useful
  interface evidence.
- Verify the behavior with synthetic fixtures and a local Gin smoke rerun when
  the checkout is available.

## Non-Goals

- Do not execute the Go toolchain, package scripts, tests, builds, or network
  operations.
- Do not resolve build tags, generated code, cgo, vendored dependency APIs, or
  full Go type information.
- Do not claim semantic compatibility or accepted SpecPM registry truth.
- Do not improve Flask/Gin intent inference; that remains `P12-T3`.
- Do not solve SpecPM `public_interface_index` vocabulary warnings; that remains
  `P12-T4`.

## Design

- Add a Go source analyzer that uses Python deterministic parsing rather than
  invoking `go`.
- Read `go.mod` to identify the module path.
- Scan repository Go source files while excluding common vendor, hidden,
  generated, build, and test-fixture paths already filtered by the collector.
- Extract:
  - package names and source files;
  - exported `func` declarations;
  - exported methods and receiver type names;
  - exported `type`, `const`, and `var` declarations.
- Prefer signature summaries over raw body content so the index stays compact.
- Mark parser limitations through diagnostics instead of failing the whole
  analyzer.

## Deliverables

- New Go public API analyzer module.
- Analyzer orchestration registration for Go module profiles.
- Unit tests covering exported declarations, unexported filtering, methods,
  grouped declarations, generated/test-file skipping, and orchestration.
- Documentation and DocC mirror updates for Go deterministic interface evidence.
- Flow validation report and archive artifacts.

## Acceptance Criteria

- A Go module fixture with source files produces a complete public interface
  index with packages and exported symbols.
- Unexported Go declarations are not emitted as public symbols.
- The analyzer does not execute `go`, package scripts, tests, builds, or network
  calls.
- `gin-gonic/gin` local smoke no longer reports Go interface extraction as only
  `manifest_only` when source files are available.
- Configured Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_go_public_api.py tests/test_analyzer_orchestration.py -q`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- Local smoke rerun for Gin if `/Users/egor/Development/GitHub/gin` is available.
