# Next Task: P25-T3 Package-Set and Scoped Member Candidate Drafting

**Status:** Selected
**Last Archived:** P25-T2 Deterministic Workspace Inventory
**Archived:** 2026-06-06

## Recently Archived

- `P25-T2` added opt-in deterministic `workspace-inventory.json` emission for
  monorepos, including exact revision, workspace manifests, package manifest
  paths, package metadata, source target paths, proposed SpecPM package IDs,
  roles, and digest-backed evidence references.
- `P25-T1` mapped SpecPM package-set contracts to SpecHarvester implementation
  work for workspace inventory, package-set candidates, scoped member
  candidates, relation proposals, bundle-set preflight, static viewer output,
  and the `xyflow` smoke/reference scenario.

## Motivation

- Workspace inventory now provides deterministic producer evidence for
  monorepo package boundaries.
- The next runtime step is to draft aggregate package-set candidates and scoped
  member package candidates without collapsing repository intent into one
  package subject.

## Goal

- Draft package-set candidates alongside scoped member package candidates so a
  repository such as `xyflow` can produce `xyflow.workspace`, `xyflow.system`,
  `xyflow.react`, and `xyflow.svelte` without overwriting one package subject
  with another.

## Next Step

Start `P25-T3` by defining how `workspace-inventory.json` maps to aggregate
package-set candidate output and scoped member candidate output while keeping
candidate generation preview-only and maintainer-reviewed.
