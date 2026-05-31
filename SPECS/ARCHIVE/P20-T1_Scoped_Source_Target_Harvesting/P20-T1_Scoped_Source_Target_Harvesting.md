# P20-T1 Scoped Source Target Harvesting

**Date:** 2026-05-31
**Verdict:** PASS

## Goal

Allow SpecHarvester to create evidence snapshots and draft candidate specs for
repository roots, scoped folders, and single files, so monorepo modules that are
not standalone package-manager projects can still be covered.

## Changes

- Added first-class `source.target` snapshot metadata with `repository`,
  `folder`, and `file` target kinds.
- Added `collect-local --target` and source-manifest `target` support.
- Preserved strict-public behavior by keeping staged-change checks at checkout
  scope while allowing scoped targets to inherit root license evidence.
- Collected safe source entrypoint files for scoped folder/file targets and
  added source-only analyzer planning for built-in Swift, Python, and Go public
  API analyzers.
- Added Tuist manifest evidence detection for `Project.swift`,
  `Workspace.swift`, and `Tuist.swift` without executing Tuist or Swift code.
- Updated drafting so scoped targets generate source-unit wording and preserve
  `sourceTarget` provenance.

## Validation

- `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_source_manifest.py tests/test_batch_collection.py -q`

## Follow-Up

- `P20-T2`: deterministic Tuist manifest parsing.
- `P20-T3`: optional `codegraph` adapter evaluation.
- `P20-T4`: scoped-source smoke fixtures.
- `P20-T5`: stronger source-unit intent drafting/refinement rules.
