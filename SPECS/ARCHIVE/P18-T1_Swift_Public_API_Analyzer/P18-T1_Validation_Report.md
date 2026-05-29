# P18-T1 Validation Report

Status: PASS
Date: 2026-05-29

## Scope

- Added deterministic Swift public API extraction for `.swift` sources.
- Registered `spec_harvester.swift_public_api` in analyzer orchestration.
- Updated Swift/SPM `ProjectProfile.analyzerPlan` to recommend the Swift
  analyzer when source files are present and remain `manifest_only` otherwise.
- Kept drafter ingestion unchanged by emitting the existing
  `PublicInterfaceIndex` contract.
- Extracted shared Swift text comment handling and shared public API entrypoint
  cache behavior to avoid new duplication.

## Quality Gates

| Gate | Result |
|---|---|
| Targeted Swift/orchestration/batch tests | PASS (`10 passed`) |
| Full tests | PASS (`437 passed, 1 skipped`) |
| Coverage | PASS (`91.99%`, threshold `90%`) |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| Builtin duplicate-code report | PASS (`0` duplicate blocks) |
| Pylint duplicate-code report | PASS (`0` duplicate blocks) |
| Architecture lint | PASS with existing advisory |

## Notes

- Architecture lint still reports one pre-existing advisory
  `manifest_parser_pattern` in `src/spec_harvester/license_provenance_reports.py`.
  P18-T1 did not modify that file.
- The Swift analyzer is intentionally syntax-light. It does not execute SwiftPM,
  compile code, expand macros, evaluate conditional compilation, or resolve type
  information.
