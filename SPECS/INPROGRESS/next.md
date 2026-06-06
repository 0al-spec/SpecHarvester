# Next Task: P25-T4 Package Relation Proposal Output

**Status:** Selected
**Last Archived:** P25-T3 Package-Set and Scoped Member Candidate Drafting
**Archived:** 2026-06-06

## Recently Archived

- `P25-T3` added `draft-package-set`, producing deterministic
  `package-set-draft.json` output plus preview-only candidate bundles for
  `xyflow.workspace`, `xyflow.system`, `xyflow.react`, and `xyflow.svelte`
  from `workspace-inventory.json`. Skipped packages are recorded with explicit
  reasons, and candidate generation remains independent from namespace
  authority, relation materialization, and SpecPM acceptance.
- `P25-T2` added opt-in deterministic `workspace-inventory.json` emission for
  monorepos, including exact revision, workspace manifests, package manifest
  paths, package metadata, source target paths, proposed SpecPM package IDs,
  roles, and digest-backed evidence references.
- `P25-T1` mapped SpecPM package-set contracts to SpecHarvester implementation
  work for workspace inventory, package-set candidates, scoped member
  candidates, relation proposals, bundle-set preflight, static viewer output,
  and the `xyflow` smoke/reference scenario.

## Motivation

- Package-set drafting now creates independently reviewable aggregate and
  scoped member candidate bundles, but the output does not yet describe how
  those package subjects relate.
- SpecPM package-set discovery needs explicit relation evidence, starting with
  `contains` proposals from aggregate workspace packages to scoped member
  packages.

## Goal

- Emit package relation proposal output for generated package-set bundles,
  starting with `contains` relations from aggregate workspace packages such as
  `xyflow.workspace` to scoped member packages such as `xyflow.system`,
  `xyflow.react`, and `xyflow.svelte`.
- Keep relation output as producer-observed review material, not registry
  authority or automatic acceptance.

## Next Step

Start `P25-T4` by defining the relation proposal artifact shape and the mapping
from `package-set-draft.json` plus `workspace-inventory.json` into deterministic
`contains` proposals.
