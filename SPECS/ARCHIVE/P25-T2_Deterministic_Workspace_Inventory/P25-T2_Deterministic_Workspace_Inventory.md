# P25-T2 — Deterministic Workspace Inventory

## Objective

Emit a deterministic workspace inventory for monorepos before package-set
candidate drafting. The inventory is producer-side evidence for review and
future SpecPM handoff. It must describe observed workspace/package boundaries
without generating, accepting, or publishing SpecPM packages.

## Scope

In scope:

- Add an opt-in `collect-batch` workspace inventory artifact.
- Record repository URL, exact revision, source manifest metadata, workspace
  manifests, workspace include patterns, package manifest paths, package
  ecosystem/name/version metadata, source target paths, proposed stable SpecPM
  package IDs, package roles, and privacy-safe evidence references.
- Keep inventory output deterministic for the same pinned checkout and
  configuration.
- Document the artifact contract for P25-T3 and P25-T5.

Out of scope:

- Drafting package-set or scoped member SpecPM packages.
- Emitting relation proposals.
- Extending bundle-set preflight.
- Rendering package-set viewer panels.
- Executing package scripts, installing dependencies, or reading raw source
  bodies for semantic interpretation.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| Batch collection inventory fixture | Cover a pnpm-style monorepo with root workspace and member package manifests. | `workspace-inventory.json` is written with stable source, workspace, package, role, ID, and evidence records. |
| Determinism test | Run inventory generation twice for the same fixture. | Payloads are byte-stable when rendered with sorted JSON. |
| CLI test | Exercise `collect-batch --emit-workspace-inventory`. | CLI summary links the written inventory artifact. |
| Revision test | Cover `ref` input backed by a git checkout. | Inventory records the checkout commit as `exactRevision` and keeps the declared ref as metadata. |
| Docs contract test | Keep GitHub docs and DocC visible. | Documentation names the artifact, schema identity, and downstream boundary. |

## Implementation Plan

1. Add a small workspace inventory module with a stable JSON shape and renderer.
2. Wire `collect-batch --emit-workspace-inventory` as an opt-in artifact beside
   `harvest.json`.
3. Reuse harvested ProjectProfile manifests and manifest digests rather than
   adding broad source scanning.
4. Parse only allowlisted workspace manifest metadata needed for include
   patterns, starting with `pnpm-workspace.yaml` and `package.json`
   `workspaces`.
5. Add focused tests and docs.

## Acceptance Criteria

- `collect-batch --emit-workspace-inventory` writes
  `workspace-inventory.json` per collected repository.
- The artifact has stable identity fields: `apiVersion`, `kind`,
  `schemaVersion`.
- The artifact records repository URL and an exact revision.
- Workspace manifests include observed include patterns where supported.
- Package records include manifest path, ecosystem, package manager, name,
  version, source target path, proposed SpecPM package ID, role, and digest
  evidence.
- Output is deterministic across repeated runs for the same fixture.
- Existing `collect-batch` behavior is unchanged unless the new flag is set.
- The task leaves package-set candidate generation to P25-T3.

## Notes

- Proposed SpecPM package IDs are review inputs, not namespace authority.
- Package roles are producer hints used to seed review and future drafting.
- Unsupported workspace manifest formats should still appear as evidence, with
  empty include-pattern lists rather than guessed semantics.
