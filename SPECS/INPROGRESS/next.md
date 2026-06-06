# Next Task: P25-T5 Bundle-Set Preflight

**Status:** Selected
**Last Archived:** P25-T4 Package Relation Proposal Output
**Archived:** 2026-06-06

## Recently Archived

- `P25-T4` added deterministic `package-relation-proposals.json` output for
  package-set drafts, starting with producer-observed `contains` relations from
  `xyflow.workspace` to `xyflow.system`, `xyflow.react`, and `xyflow.svelte`.
  Relation proposals reference `workspace-inventory.json` and
  `package-set-draft.json` with digests and remain review evidence, not
  accepted registry metadata.
- `P25-T3` added `draft-package-set`, producing deterministic
  `package-set-draft.json` output plus preview-only candidate bundles for
  `xyflow.workspace`, `xyflow.system`, `xyflow.react`, and `xyflow.svelte`
  from `workspace-inventory.json`.
- `P25-T2` added opt-in deterministic `workspace-inventory.json` emission for
  monorepos, including exact revision, workspace manifests, package manifest
  paths, package metadata, source target paths, proposed SpecPM package IDs,
  roles, and digest-backed evidence references.

## Motivation

- Package-set drafting now produces multiple candidate bundles plus relation
  proposal evidence, but there is no single producer-side verifier for the
  whole bundle set.
- Before SpecPM handoff, maintainers need one preflight report that checks
  consistency across candidates, receipts, reports, relation source/target existence
  checks, workspace inventory, privacy, and human review boundaries.

## Goal

- Extend candidate bundle preflight for bundle sets, checking unique package
  IDs, per-package required files, receipt/report digests, relation
  source/target existence, workspace inventory consistency, privacy status, and
  human review boundary without accepting packages automatically.

## Next Step

Start `P25-T5` by defining the bundle-set preflight input shape and verifying
`package-set-draft.json` plus `package-relation-proposals.json` against the
generated candidate bundle directories.
