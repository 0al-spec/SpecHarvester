# P25-T6 Validation Report

**Task:** P25-T6 Static Viewer Package-Set Panels
**Date:** 2026-06-06
**Verdict:** PASS

## Summary

P25-T6 extends the static viewer from single generated SpecPackage candidates
to generated package-set output directories. The new `render-package-set-site`
command consumes `package-set-draft.json`, `package-relation-proposals.json`,
optional `bundle-set-preflight.json`, and generated member candidate manifests.

The rendered static site writes `package-set.json` and displays package-set
summary, member package cards, relation proposal badges, producer-observed
review status, bundle-set preflight status, and result scope examples. The
viewer remains review evidence only; it does not accept packages, accept
relations, publish registry metadata, or execute package code.

## Validation Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src pytest tests/test_static_spec_renderer.py tests/test_docs_contracts.py -q` | PASS, 52 passed |
| `PYTHONPATH=src ruff check .` | PASS |
| `ruff format --check src tests` | PASS, 87 files already formatted |
| `PYTHONPATH=src pytest -q` | PASS, 533 passed, 1 skipped |

## Acceptance Criteria

- `python -m spec_harvester render-package-set-site --bundle-set <dir> --output <site>`
  writes `index.html`, `assets/spec-renderer.css`, `assets/spec-renderer.js`,
  and `package-set.json`.
- The package-set payload has stable identity:
  `apiVersion: spec-harvester.static-package-set-renderer/v0` and
  `kind: SpecHarvesterStaticPackageSet`.
- The viewer payload lists aggregate and scoped member packages separately.
- The viewer payload lists `contains` relation proposals with
  `producer_observed` review status.
- Bundle-set preflight status is visible when a preflight report is present.
- The viewer remains static review evidence and does not accept packages,
  accept relations, publish registry metadata, or execute package code.

## Residual Notes

P25-T7 should exercise the full `xyflow` scenario end to end: workspace
inventory, package-set drafting, scoped member packages, relation proposals,
bundle-set preflight, and package-set viewer output.
