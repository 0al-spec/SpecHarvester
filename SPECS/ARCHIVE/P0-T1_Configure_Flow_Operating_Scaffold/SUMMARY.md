# P0-T1 Configure Flow Operating Scaffold

Status: PASS
Date: 2026-05-17
Branch: main working tree

## Summary

Configured the repository-local Flow operating layer for future SpecHarvester
tasks.

## Delivered

- Added `SPECS/PRD.md`.
- Added `SPECS/Workplan.md`.
- Added Flow command procedures under `SPECS/COMMANDS/`.
- Added `SPECS/INPROGRESS/next.md`.
- Added `SPECS/ARCHIVE/INDEX.md`.
- Linked the Flow entrypoint from `README.md` and `docs/README.md`.
- Added coverage support to dev dependencies.
- Updated CI to enforce `pytest --cov=spec_harvester --cov-fail-under=90`.
- Added tests for existing edge cases so the current repository satisfies the
  coverage gate.

## Validation

- `ruff check src tests`: pass.
- `ruff format --check src tests`: pass.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`: pass, 31 tests, 91.41% coverage.
- `swift package dump-package >/dev/null`: pass.
- `swift build --target SpecHarvesterDocs`: pass.

## Follow-Up

- Next recommended task: `P1-T1 Define PublicInterfaceIndex snapshot schema`.
