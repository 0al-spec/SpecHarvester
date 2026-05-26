# P16-T3 — Package Identity and Namespace Normalization

Branch: `feature/P16-T3-package-identity-namespace-normalization`
Review subject: `p16_t3_package_identity_namespace_normalization`

## Context

Real repository validation produced low-signal namespace/upstream advisories when
generated package namespaces used deterministic snake-case IDs while upstream
repositories used CamelCase, hyphenated, or otherwise separator-varied names.

Example:

- package ID: `navigation_split_view.core`
- package namespace: `navigation_split_view`
- upstream repository: `NavigationSplitView`

The governance report should still flag true ownership/provenance mismatches,
but it should not treat separator and case differences as semantic namespace
conflicts.

## Scope

- Normalize namespace/upstream comparison across case, hyphen, underscore,
  separator, and CamelCase variants.
- Keep normalization local to advisory report comparison logic.
- Preserve raw package IDs, raw namespaces, raw upstream owner/name values, and
  report schema fields.
- Add regression tests for real failure shapes such as `navigation_split_view`
  versus `NavigationSplitView`.

## Non-Goals

- Do not change generated package IDs.
- Do not rewrite accepted or candidate `specpm.yaml` files.
- Do not relax missing or invalid upstream URI handling.
- Do not accept unrelated owner mismatches when neither owner nor repository
  name normalizes to the package namespace.

## Acceptance Criteria

- `namespace_matches_upstream` accepts equivalent separator/case/CamelCase
  variants.
- Namespace/upstream report no longer emits `upstream_namespace_mismatch` for
  normalized repository-name matches.
- Existing missing upstream, invalid upstream URI, duplicate namespace, and true
  mismatch behavior remains unchanged.
- Targeted tests, lint, format, coverage gate, Swift manifest, and DocC target
  build pass or any failure is documented with a blocker.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_namespace_upstream_reports.py -q`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`

