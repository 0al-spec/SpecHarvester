# P16-T12 — Report Source Records Object

Branch: `feature/P16-T12-report-source-records-object`
Review subject: `p16_t12_report_source_records_object`

## Context

Duplicate-code metrics still show repeated accepted/candidate source traversal
logic across report modules. The duplicated behavior includes resolving source
roots, rejecting missing roots, walking `specpm.yaml` files, skipping symlinked
manifests, turning parser `ValueError` exceptions into `invalid_specpm_manifest`
issues, and sorting records deterministically.

This belongs in one behavior-rich object rather than repeated module-local
functions.

## Scope

- Add a shared report source records object for local `specpm.yaml` traversal.
- Use it from:
  - governance duplicate claim report
  - namespace/upstream report
  - license provenance report
- Preserve existing report schemas, issue codes, messages, sorting, and trust
  boundaries.
- Add regression coverage for shared symlink/invalid manifest behavior where it
  is currently duplicated.
- Re-run duplicate-code and architecture-lint baselines after the refactor.

## Non-Goals

- Do not refactor semantic intent generation.
- Do not change generated candidates or accepted SpecPM packages.
- Do not change `SpecPackageManifest` parsing semantics.
- Do not change public JSON schemas beyond preserving existing outputs.
- Do not execute harvested repository code.

## Acceptance Criteria

- Report modules delegate accepted/candidate manifest traversal to a shared
  object.
- Existing tests for governance, namespace/upstream, and license provenance
  reports pass unchanged or with behavior-preserving regressions.
- Duplicate-code baseline improves or any unchanged clusters are documented.
- Architecture lint remains at or below the current advisory baseline.
- Full Flow validation passes.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_governance_reports.py tests/test_namespace_upstream_reports.py tests/test_license_provenance_risk_reports.py -q`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t12-dup-builtin.json`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t12-dup-pylint.json`
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t12-architecture-lint.json`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`

