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

## Role Selection Profiles

P28-T4 adds named role selection profiles. The `default` profile preserves the
P25-T3 `xyflow` reference selection. The `generic_monorepo` profile selects
`workspace` and `member_package` roles so common monorepos can produce useful
workspace/member package-set output without operator knowledge of
`--role workspace --role member_package`.

```bash
python3 -m spec_harvester draft-package-set \
  candidates/tanstack-query/workspace-inventory.json \
  --out candidates/tanstack-query-package-set \
  --role-profile generic_monorepo
```

If `--role` is supplied one or more times, explicit roles override
`--role-profile` and the draft summary records `selection.roleProfile:
custom`. Profiles are producer preview selection policy only; they do not imply
SpecPM acceptance, namespace authority, or registry publication.

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
