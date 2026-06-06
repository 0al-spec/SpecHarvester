# Workspace Inventory

`workspace-inventory.json` is an opt-in `collect-batch` artifact for monorepo
and package-set review.

It records deterministic producer evidence before SpecHarvester drafts
package-set candidates. It is not a SpecPM registry payload and does not accept
packages or package relations.

## Command

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --emit-workspace-inventory
```

For each collected repository, the command writes:

```text
candidates/<repository-id>/workspace-inventory.json
```

The batch summary links the artifact under `collected[].workspaceInventory`.

## JSON Identity

```json
{
  "apiVersion": "spec-harvester.workspace-inventory/v0",
  "kind": "SpecHarvesterWorkspaceInventory",
  "schemaVersion": 1
}
```

## Evidence Shape

The inventory records repository URL, exact revision, source manifest metadata,
workspace manifests, workspace include patterns, package manifest paths,
package ecosystem/name/version metadata, source target paths, proposed SpecPM
package IDs, package roles, and digest-backed evidence references.

Package roles are producer hints such as `workspace`, `core_runtime`,
`react_binding`, `svelte_binding`, and `member_package`.

## Boundary

SpecHarvester does not execute package scripts, install dependencies, run
package managers, publish packages, accept package relations, or claim namespace
authority.

`proposedSpecpmPackageId` values are review inputs for later package-set
drafting. They do not imply inherited capabilities, inherited constraints, or
public registry visibility.

For the `xyflow` reference scenario, inventory records may propose
`xyflow.workspace`, `xyflow.system`, `xyflow.react`, and `xyflow.svelte`.

P25-T3 should consume this inventory for package-set and scoped member drafting.
P25-T4 should consume it with package-set draft output for deterministic
`package-relation-proposals.json` review evidence. `preflight-bundle-set`
checks bundle-set consistency through the package-set and relation records.

Use `draft-package-set` for the P25-T3 drafting step:

```bash
python3 -m spec_harvester draft-package-set \
  candidates/xyflow/workspace-inventory.json \
  --out candidates/xyflow-package-set
```
