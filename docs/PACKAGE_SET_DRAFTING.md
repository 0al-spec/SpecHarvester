# Package-Set Drafting

Status: Producer preview contract

`draft-package-set` consumes `workspace-inventory.json` and drafts multiple
preview SpecPM candidate bundles from one monorepo inventory.

The command is the P25-T3 bridge between deterministic workspace discovery and
future relation/preflight/viewer work. It does not publish packages or accept
package-set relations.

## Command

```bash
python3 -m spec_harvester draft-package-set \
  candidates/xyflow/workspace-inventory.json \
  --out candidates/xyflow-package-set
```

The output root contains:

```text
candidates/xyflow-package-set/package-set-draft.json
candidates/xyflow-package-set/package-relation-proposals.json
candidates/xyflow-package-set/xyflow.workspace/specpm.yaml
candidates/xyflow-package-set/xyflow.system/specpm.yaml
candidates/xyflow-package-set/xyflow.react/specpm.yaml
candidates/xyflow-package-set/xyflow.svelte/specpm.yaml
```

Each generated package directory is an ordinary preview candidate bundle with
`specpm.yaml`, `specs/*.spec.yaml`, `harvest.json`, `producer-receipt.json`,
`validation-report.json`, and `diagnostics.json`.

Package-set drafting preserves package manifest `description` and `license`
metadata from `workspace-inventory.json` when present. This keeps scoped
package candidates closer to reviewable accepted-source input without changing
the producer boundary: generated bundles still remain `preview_only` until
maintainer review.

## JSON Identity

The draft-set summary uses:

```json
{
  "apiVersion": "spec-harvester.package-set-draft/v0",
  "kind": "SpecHarvesterPackageSetDraft",
  "schemaVersion": 1
}
```

The summary records:

- source repository and exact revision;
- referenced `workspace-inventory.json` digest;
- selected inventory roles;
- generated candidate package IDs and relative paths;
- aggregate `authorReadyDraftSummary` from member quality reports;
- skipped package IDs and reasons;
- relation proposal path, review status, and relation count;
- producer preview authority and non-goals.

## Default Selection

The initial P25-T3 selection drafts these inventory roles:

- `workspace`
- `core_runtime`
- `react_binding`
- `svelte_binding`

This keeps the `xyflow` reference path focused on:

```text
xyflow.workspace
xyflow.system
xyflow.react
xyflow.svelte
```

Other inventory packages such as examples, tooling, and tests are recorded in
`skipped[]` with `role_not_selected_for_initial_package_set_draft`. They are not
silently lost.

Operators can repeat `--role` to override the selected role set for local
experiments.

## Role Selection Profiles

P28-T4 adds named role selection profiles so common monorepo intent can be
declared without remembering raw role flags.

The default profile is `default`, which preserves the P25-T3 `xyflow`
reference selection:

```bash
python3 -m spec_harvester draft-package-set \
  candidates/xyflow/workspace-inventory.json \
  --out candidates/xyflow-package-set \
  --role-profile default
```

For generic monorepos, use `generic_monorepo`:

```bash
python3 -m spec_harvester draft-package-set \
  candidates/tanstack-query/workspace-inventory.json \
  --out candidates/tanstack-query-package-set \
  --role-profile generic_monorepo
```

`generic_monorepo` selects:

- `workspace`
- `member_package`

This captures the P28-T3 `TanStack/query` observation: the useful
workspace/member package-set should be a named producer-side selection, not
operator memory of `--role workspace --role member_package`.

If `--role` is supplied one or more times, explicit roles override
`--role-profile` and the draft summary records `selection.roleProfile:
custom`. Profiles are producer preview selection policy only; they do not imply
SpecPM acceptance, namespace authority, or registry publication.

## Boundary

Generated candidates remain `preview_only`. Proposed package IDs are review
inputs, not namespace authority.

SpecHarvester does not execute package scripts during package-set drafting.

The command does not:

- run bundle-set preflight; use `preflight-bundle-set` for that step;
- render package-set viewer panels;
- mutate SpecPM accepted sources;
- publish public registry metadata;
- execute package scripts;
- install dependencies;
- run package managers.

P25-T4 emits relation proposals such as `contains`. Use `preflight-bundle-set`
to verify generated package candidates and relation output together. Use
`render-package-set-site` to preview the generated set with member package
cards, relation proposal badges, producer-observed review status, and result
scope examples.
