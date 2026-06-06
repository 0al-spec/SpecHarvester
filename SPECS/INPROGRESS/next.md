# Next Task: P25-T7 Xyflow Package-Set Smoke Scenario

**Status:** Selected
**Last Archived:** P25-T6 Static Viewer Package-Set Panels
**Archived:** 2026-06-06

## Recently Archived

- `P25-T6` added `render-package-set-site`, a static viewer path for generated
  package-set outputs. It reads `package-set-draft.json`,
  `package-relation-proposals.json`, optional `bundle-set-preflight.json`, and
  generated candidate manifests, then writes `package-set.json`, static assets,
  member package cards, relation proposal badges, producer-observed review
  status, and result scope examples.
- `P25-T5` added `preflight-bundle-set`, a producer-side verifier for generated
  package-set output directories.
- `P25-T4` added deterministic `package-relation-proposals.json` output for
  producer-observed `contains` relations.

## Motivation

- The package-set pipeline now exists as separate pieces: workspace inventory,
  package-set drafting, relation proposals, bundle-set preflight, and static
  viewer output.
- Reviewers need one practical `xyflow` scenario that proves these pieces work
  together and preserves the intended product boundary: broad workspace
  discovery plus scoped member packages.

## Goal

- Add an `xyflow` monorepo smoke fixture or local smoke scenario that exercises
  workspace inventory, package-set candidate generation, scoped member package
  generation, relation proposals, bundle-set preflight, and viewer output
  against the SpecPM reference scenario.

## Next Step

Start `P25-T7` by choosing the fixture shape and expected artifacts for a
repeatable `xyflow` package-set smoke run.
