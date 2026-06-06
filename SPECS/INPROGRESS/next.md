# Next Task: P25-T2 Deterministic Workspace Inventory

**Status:** Selected
**Last Archived:** P25-T1 Package Set Contract Alignment
**Archived:** 2026-06-06

## Recently Archived

- `P25-T1` mapped SpecPM package-set contracts to SpecHarvester implementation
  work for workspace inventory, package-set candidates, scoped member
  candidates, relation proposals, bundle-set preflight, static viewer output,
  and the `xyflow` smoke/reference scenario.

## Motivation

- SpecHarvester now has a documented package-set alignment contract.
- Runtime work should start with deterministic workspace inventory so later
  package-set candidate generation is evidence-backed and reproducible.

## Goal

- Emit a deterministic workspace inventory for monorepos, including repository URL,
  exact revision, workspace manifests, package manifest paths, package
  ecosystem/name/version metadata, source target paths, proposed stable SpecPM
  package IDs, package roles, and privacy-safe evidence references.

## Next Step

Start `P25-T2` by defining the workspace inventory JSON shape and fixture
expectations before wiring broader package-set candidate generation.
