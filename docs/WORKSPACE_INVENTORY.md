# Workspace Inventory

Status: Producer evidence contract

`workspace-inventory.json` is an opt-in `collect-batch` artifact for monorepo
and package-set review. It records deterministic producer evidence for
workspace/package discovery before SpecHarvester drafts package-set candidates.

The artifact is not a SpecPM registry payload. SpecPM remains responsible for
validation, accepted-source review, package relation acceptance, and public
index publication.

## Command

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --emit-workspace-inventory
```

For each collected repository, SpecHarvester writes:

```text
candidates/<repository-id>/workspace-inventory.json
```

The batch JSON summary links the artifact under
`collected[].workspaceInventory`.

## JSON Identity

```json
{
  "apiVersion": "spec-harvester.workspace-inventory/v0",
  "kind": "SpecHarvesterWorkspaceInventory",
  "schemaVersion": 1
}
```

The schema is intentionally producer-side. Later SpecPM intake or preflight
jobs may consume the artifact, but acceptance decisions remain maintainer-owned.

## Recorded Evidence

The inventory records:

- repository URL;
- exact revision;
- declared source manifest metadata;
- source target metadata;
- workspace manifests such as `pnpm-workspace.yaml` and root `package.json`
  `workspaces`;
- workspace include/exclude patterns;
- package manifest paths discovered from harvested manifests and supported
  workspace include patterns;
- package ecosystem and package manager metadata;
- package name/version metadata when a safe manifest parser supports it;
- source target paths;
- proposed stable SpecPM package IDs;
- proposed SpecPM package IDs as review-facing metadata;
- package roles such as `workspace`, `core_runtime`, `react_binding`,
  `svelte_binding`, and `member_package`;
- digest-backed evidence references.

## Determinism

The artifact is rendered as sorted JSON. For the same pinned checkout,
repository source manifest, and command options, repeated runs should produce
the same `workspace-inventory.json` bytes.

When a source manifest provides `revision`, that value is used as
`source.exactRevision` with `revisionAuthority: source_manifest_revision`.
When a source manifest provides only `ref`, the checkout must be a git worktree;
SpecHarvester records `git rev-parse HEAD` as `source.exactRevision` and keeps
the declared ref as `source.declaredRef`.

## Privacy and Safety

The inventory includes manifest metadata and digests, not raw source bodies.
SpecHarvester does not:

- execute package scripts;
- install dependencies;
- run package managers;
- run upstream tests;
- call networks;
- publish packages;
- accept package relations.

Unsupported workspace manifest formats remain evidence records with empty
include-pattern lists rather than guessed semantics.

## Package ID Proposals

`proposedSpecpmPackageId` values are review inputs, not namespace authority.

For a package-set repository such as `xyflow`, inventory records may propose:

```text
xyflow.workspace
xyflow.system
xyflow.react
xyflow.svelte
```

Those IDs are stable producer suggestions for P25-T3 package drafting and
future maintainer review. They do not imply accepted ownership, inherited
capabilities, inherited constraints, or public registry visibility.

## Downstream Use

P25-T3 should use the inventory as input when drafting aggregate package-set
candidates and scoped member candidates. P25-T4 should use the inventory and
package-set draft output to emit deterministic `package-relation-proposals.json`
review evidence. `preflight-bundle-set` uses the package-set and relation
records to check multi-package bundle consistency before SpecPM handoff.

Use `draft-package-set` for the P25-T3 drafting step:

```bash
python3 -m spec_harvester draft-package-set \
  candidates/xyflow/workspace-inventory.json \
  --out candidates/xyflow-package-set
```

This writes `package-set-draft.json` and separate preview candidate bundle
directories for selected package roles.
