# Next Task: P25-T6 Static Viewer Package-Set Panels

**Status:** Selected
**Last Archived:** P25-T5 Bundle-Set Preflight
**Archived:** 2026-06-06

## Recently Archived

- `P25-T5` added `preflight-bundle-set`, a producer-side verifier for generated
  package-set output directories. It checks `package-set-draft.json`,
  `package-relation-proposals.json`, candidate bundle directories,
  per-candidate preflight status, relation source/target existence, digest
  references, workspace inventory input consistency, and producer review
  boundaries.
- `P25-T4` added deterministic `package-relation-proposals.json` output for
  package-set drafts, starting with producer-observed `contains` relations from
  `xyflow.workspace` to `xyflow.system`, `xyflow.react`, and `xyflow.svelte`.
- `P25-T3` added `draft-package-set`, producing deterministic
  `package-set-draft.json` output plus preview-only candidate bundles for
  `xyflow.workspace`, `xyflow.system`, `xyflow.react`, and `xyflow.svelte`
  from `workspace-inventory.json`.

## Motivation

- Package-set generation now has workspace inventory, scoped candidate bundles,
  relation proposals, and bundle-set preflight evidence.
- Reviewers still need a static viewer surface that shows the aggregate package,
  scoped members, relation proposal badges, and result-scope examples without
  hiding member packages under the aggregate package.

## Goal

- Extend static viewer output to make package-set review ergonomic: show
  package-set summary, member package cards, relation proposal badges,
  producer-observed review status, and clear boundaries between aggregate and
  scoped package subjects.

## Next Step

Start `P25-T6` by defining the static viewer package-set input shape and mapping
`package-set-draft.json`, `package-relation-proposals.json`, and
`preflight-bundle-set` report output into viewer payload sections.

