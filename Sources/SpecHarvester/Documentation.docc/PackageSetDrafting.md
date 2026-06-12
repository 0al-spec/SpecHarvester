# Package-Set Drafting

`draft-package-set` consumes `workspace-inventory.json` and drafts multiple
preview SpecPM candidate bundles from one monorepo inventory.

It bridges deterministic workspace discovery and later package relation,
bundle-set preflight, and viewer work. It does not publish packages or accept
package-set relations.

## Command

```bash
python3 -m spec_harvester draft-package-set \
  candidates/xyflow/workspace-inventory.json \
  --out candidates/xyflow-package-set
```

The output includes:

```text
package-set-draft.json
package-relation-proposals.json
xyflow.workspace/specpm.yaml
xyflow.system/specpm.yaml
xyflow.react/specpm.yaml
xyflow.svelte/specpm.yaml
```

Each package directory is an ordinary preview candidate bundle with
`specpm.yaml`, `specs/*.spec.yaml`, `harvest.json`, `producer-receipt.json`,
`validation-report.json`, and `diagnostics.json`.

Package-set drafting preserves package manifest `description` and `license`
metadata from `workspace-inventory.json` when present. This keeps scoped
package candidates closer to reviewable accepted-source input without changing
the producer boundary: generated bundles still remain `preview_only` until
maintainer review.

## Summary Identity

```json
{
  "apiVersion": "spec-harvester.package-set-draft/v0",
  "kind": "SpecHarvesterPackageSetDraft",
  "schemaVersion": 1
}
```

The summary records source repository and exact revision, workspace inventory
digest, selected roles, generated package IDs, relative candidate paths,
aggregate `authorReadyDraftSummary`, skipped packages, relation proposal path,
relation count, and producer preview non-goals.

## Default Selection

P25-T3 drafts `workspace`, `core_runtime`, `react_binding`, and
`svelte_binding` roles by default.

For `xyflow`, this produces `xyflow.workspace`, `xyflow.system`,
`xyflow.react`, and `xyflow.svelte`. Other packages such as examples, tooling,
and tests are recorded under `skipped[]` with
`role_not_selected_for_initial_package_set_draft`.

## Boundary

Generated candidates remain `preview_only`. Proposed package IDs are review
inputs, not namespace authority.

SpecHarvester does not execute package scripts during package-set drafting.

P25-T4 emits relation proposals such as `contains`. Use
`preflight-bundle-set` for bundle-set preflight. Use
`render-package-set-site` to preview member package cards, relation proposal
badges, producer-observed review status, and result scope examples. This
command does not execute package scripts, install dependencies, run package
managers, mutate SpecPM accepted sources, or publish registry metadata.
