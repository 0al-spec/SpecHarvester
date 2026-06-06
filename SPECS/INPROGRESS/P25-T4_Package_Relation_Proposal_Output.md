# P25-T4 — Package Relation Proposal Output

## Objective

Emit deterministic package relation proposal output for generated package-set
bundles. Initial support should create `contains` relation proposals from an
aggregate workspace package such as `xyflow.workspace` to scoped member
packages such as `xyflow.system`, `xyflow.react`, and `xyflow.svelte`.

## Scope

In scope:

- Add a relation proposal artifact written beside `package-set-draft.json`.
- Generate initial `contains` proposals from selected workspace-role
  candidates to selected non-workspace candidates.
- Record relation type, source package ID, target package ID, evidence paths,
  and `reviewStatus: producer_observed`.
- Reference workspace inventory and package-set draft inputs with digests.
- Document relation proposal output and producer/review boundaries.

Out of scope:

- Relation acceptance or SpecPM registry mutation.
- Bundle-set preflight across packages and relations. P25-T5 owns that.
- Static viewer relation panels. P25-T6 owns that.
- Search behavior, dependency solving, package execution, package script
  execution, dependency installation, or package-manager execution.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| Relation proposal fixture | Draft from an `xyflow`-like package set. | Output includes three `contains` relations from `xyflow.workspace` to selected members. |
| Evidence coverage | Ensure relation evidence is reviewable. | Each relation records workspace manifests and source/target package manifest evidence. |
| Determinism | Compare repeated draft outputs. | `package-relation-proposals.json` bytes are identical across output roots. |
| CLI coverage | Exercise `draft-package-set` end to end. | CLI result reports relation proposal path and relation count. |
| Docs contract | Keep GitHub docs and DocC visible. | Docs name the artifact, schema identity, `contains`, `producer_observed`, P25-T5, and P25-T6. |

## Implementation Plan

1. Define `package-relation-proposals.json` identity and deterministic renderer.
2. Extend package-set drafting to compute workspace-to-member `contains`
   relations from selected candidates and inventory package records.
3. Include digest-backed references to `workspace-inventory.json` and
   `package-set-draft.json` without self-hashing the relation artifact.
4. Update tests, docs, validation report, archive, and review artifacts.

## Acceptance Criteria

- `draft-package-set <workspace-inventory.json> --out <dir>` writes
  `package-relation-proposals.json` beside `package-set-draft.json`.
- The relation artifact has stable identity fields:
  `apiVersion: spec-harvester.package-relation-proposals/v0` and
  `kind: SpecHarvesterPackageRelationProposals`.
- For an `xyflow`-like fixture, generated relations include:
  `xyflow.workspace contains xyflow.system`,
  `xyflow.workspace contains xyflow.react`, and
  `xyflow.workspace contains xyflow.svelte`.
- Each relation has `reviewStatus: producer_observed`.
- Evidence includes workspace manifests and source/target package manifest
  paths with digest records when present.
- Relation source and target package IDs match generated candidate subjects.
- Relation output remains producer review evidence, not accepted registry
  metadata.

## Notes

- This task creates proposal data only. P25-T5 is responsible for checking
  relation source/target existence as part of bundle-set preflight.
- Maintainers can accept, reject, or defer each relation independently in the
  later SpecPM review path.
