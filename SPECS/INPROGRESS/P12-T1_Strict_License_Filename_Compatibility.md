# P12-T1 Strict License Filename Compatibility

Status: In Progress
Created: 2026-05-21
Task: `P12-T1` Accept common public license filenames such as `LICENSE.txt` in
strict public mode while keeping the current hard failure for repositories with
no license-like file.

## Problem

Strict public mode currently rejects `pallets/flask` with
`missing_license_file` even though the repository contains `LICENSE.txt`.
The collector already treats names beginning with `LICENSE` or `COPYING` as
license-like files, but the batch validation gate only counts exact
`kind: license` records produced from the current allowlist.

For public SpecPM.dev use, absence of license evidence should remain a hard
error. The problem is that common safe filename variants such as `LICENSE.txt`
are evidence, not absence.

## Goals

- Treat common license-like filenames with safe text extensions as license
  evidence in strict public mode.
- Preserve hard strict-mode failure for repositories with no license-like file.
- Keep deterministic local-only behavior with no SPDX lookup, dependency
  installation, package script execution, or network access.
- Preserve existing license hint inference and license provenance behavior.
- Verify the Flask-style `LICENSE.txt` case with regression tests and a local
  smoke rerun when the checkout is available.

## Non-Goals

- Do not add a full license classifier.
- Do not change relaxed-private mode policy.
- Do not accept arbitrary binary or misleading filenames as license evidence.
- Do not implement Go public interface analysis; that remains `P12-T2`.
- Do not solve SpecPM `public_interface_index` vocabulary warnings; that remains
  `P12-T4`.

## Design

- Centralize license filename recognition so collection and batch validation use
  the same predicate.
- Accept base license names and safe textual variants such as:
  - `LICENSE`
  - `LICENSE.txt`
  - `LICENSE.md`
  - `COPYING`
  - `COPYING.txt`
  - `COPYING.md`
- Reject unrelated names that merely contain license text in the middle of a
  path or binary-like suffixes.
- Ensure strict validation uses collected license-like records instead of only
  a narrower exact filename assumption.

## Deliverables

- Update collector or validation helpers for shared license filename detection.
- Add regression tests for `LICENSE.txt` in strict batch collection.
- Add a negative regression proving no-license repositories still fail strict
  mode.
- Update batch validation documentation and DocC mirror if wording currently
  implies only exact `LICENSE` or `COPYING`.
- Create validation report and archive artifacts through Flow.

## Acceptance Criteria

- A repository containing `LICENSE.txt` passes strict public batch validation
  when other required evidence is present.
- A repository with no license-like file still fails strict public batch
  validation with `missing_license_file`.
- Existing `LICENSE` / `COPYING` behavior remains unchanged.
- Generated license provenance remains deterministic.
- Flow quality gates pass with coverage at or above the configured threshold.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_batch_collection.py tests/test_batch_validation_report.py -q`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- Local smoke rerun for Flask/Gin if `/Users/egor/Development/GitHub/flask`
  and `/Users/egor/Development/GitHub/gin` are available.
