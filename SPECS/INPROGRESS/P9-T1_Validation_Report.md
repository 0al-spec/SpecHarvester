# P9-T1 Validation Report

## Result

PASS

## Scope

Validated deterministic semantic intent drafting for Swift packages with richer
static documentation evidence and primary package manifest filtering.

## Quality Gates

- `PYTHONPATH=src python -m pytest`: PASS, 174 passed.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`: PASS, 174 passed, total coverage 90.22%.
- `ruff check src tests`: PASS.
- `ruff format --check src tests`: PASS.
- `swift package dump-package >/dev/null`: PASS.
- `swift build --target SpecHarvesterDocs`: PASS.

## Smoke Evidence

- Ran `collect-batch` for local `Puzzle` with `--relaxed-private`.
- Draft output changed from Swift product-only intent claims to semantic iOS
  screen composition claims:
  - `intent.ios.collection_layout_composition`
  - `intent.ios.screen_diagnostics`
  - `intent.ios.screen_level_composition`
  - `intent.ios.screen_state_binding`
  - `intent.ios.uikit_swiftui_migration`
  - `intent.swift.macro_developer_experience`
- The generated Puzzle boundary summary is now:
  `Provide a screen-level composition framework for incrementally migrating UIKit-heavy iOS screens to mixed UIKit/SwiftUI surfaces.`
- Primary inbound package interfaces no longer include generated dependency or
  fixture package manifests such as SwiftSyntax checkout manifests.

## Notes

- Generated candidates remain `preview_only`.
- The implementation uses only static allowlisted markdown headings, package
  manifests, and optional public interface symbol names.
- No harvested package scripts, dependencies, repository code, or network probes
  are executed.
