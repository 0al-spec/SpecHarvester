# P1-T5 Validation Report

Task: Integrate Public Interface Evidence into Deterministic Drafting
Branch: `feature/P1-T5-integrate-public-interface-evidence-into-drafting`
Date: 2026-05-17
Verdict: PASS

## Implementation Summary

Implemented deterministic `PublicInterfaceIndex` consumption in the draft
pipeline:

- Added `DraftOptions.interface_index` and CLI `draft --interface-index`.
- Added auto-detection for `public-interface-index.json` and
  `public_interface_index.json` beside `harvest.json`.
- Validates supplied index artifacts with `validate_public_interface_index`
  before writing candidate files.
- Copies the normalized index into the candidate output as
  `public-interface-index.json`.
- Enriches generated `interfaces.inbound` entries with package, language,
  entrypoint, symbol, signature, and source evidence metadata.
- Adds BoundarySpec evidence and provenance records for the public interface
  index.
- Preserves manifest-only draft behavior when no public interface index is
  provided.
- Updates GitHub docs and DocC pages for the new draft input.

## Validation Commands

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_collector.py -q` | PASS, 35 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 56 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, 13 files already formatted |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 56 passed, total coverage 91.34% |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `git diff --check` | PASS |

## Trust Boundary Validation

- `draft` reads only `harvest.json` and an explicit or colocated
  `PublicInterfaceIndex` JSON artifact.
- `draft` does not execute analyzers, import harvested modules, run package
  scripts, install dependencies, or inspect raw repository source trees.
- Invalid public interface index input fails before candidate manifest/spec
  files are written.

## Residual Risks

- Public interface data remains analyzer-produced evidence, not accepted
  registry truth.
- Symbol summaries can grow large for packages with broad public APIs; later
  tasks may need size limits or compact LLM-facing summaries.
