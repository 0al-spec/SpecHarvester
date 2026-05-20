# P12-T2 Validation Report

Task: `P12-T2 Go Public Interface Evidence`
Date: 2026-05-21
Verdict: PASS

## Scope

Implemented a deterministic, local-only Go public API analyzer and wired it into
`ProjectProfile.analyzerPlan` / `collect-batch --emit-interface-indexes`.

The analyzer reads Go source files directly from the checkout, parses exported
package-level declarations and exported methods, and writes a
`PublicInterfaceIndex` without invoking `go`, package managers, package
scripts, tests, builds, or network operations.

## Regression Coverage

- Added Go analyzer tests for exported functions, methods, structs,
  interfaces, types, constants, variables, grouped declarations, unexported
  filtering, generated-file skipping, `_test.go` skipping, vendor/testdata
  skipping, cache reuse, no-source diagnostics, and bad source roots.
- Added analyzer orchestration coverage for `spec_harvester.go_public_api`.
- Updated multi-language smoke matrix expectations so Go modules now recommend
  the Go public API analyzer.
- Updated documentation and DocC mirror references for supported analyzer ids.

## Quality Gates

| Gate | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest` | PASS, `215 passed in 2.56s` |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, `43 files already formatted` |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `215 passed`, total coverage `90.66%` |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Local Gin Smoke

Command:

```bash
PYTHONPATH=src python -m spec_harvester collect-batch .smoke/inputs \
  --out .smoke/output/p12-t2-popular-candidates \
  --report .smoke/output/p12-t2-popular-batch-validation.json \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/analyzer-cache \
  --select gin
```

Result: PASS, batch `status: ok`.

Gin interface index summary:

- `status: complete`
- `packageCount: 7`
- `entrypointCount: 58`
- `symbolCount: 460`
- `diagnosticCount: 0`
- `executedAnalyzerIds: ["spec_harvester.go_public_api"]`

Repository revision:

- `gin-gonic/gin` at `5f4f9643258dc2a65e684b63f12c8d543c936c67`

## Notes

- `spec_harvester.c_cpp_manifest_profile` still appears in the Gin plan because
  collected build metadata is present; it remains `manifest_only` and is
  skipped by analyzer orchestration.
- The Go analyzer is intentionally syntax-light and does not perform Go type
  checking, build-tag resolution, cgo handling, or dependency loading.
