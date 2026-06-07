# Xyflow Package-Set Smoke

`xyflow-package-set-smoke` runs the full package-set producer path against a
deterministic local `xyflow` fixture. It proves the package-set pieces work
together without fetching the real repository or executing package code.

The fixture mirrors the real `xyflow` layout where the root `package.json` is
`@xyflow/monorepo` and workspace membership comes from `pnpm-workspace.yaml`.
This guards the product shape that matters for real checkouts: aggregate
`xyflow.workspace`, primary members `xyflow.system`, `xyflow.react`, and
`xyflow.svelte`, skipped examples/tooling/tests, and relation proposals from
the aggregate root to the selected members.

## Command

```bash
python3 -m spec_harvester xyflow-package-set-smoke \
  --output .smoke/xyflow-package-set
```

The command writes `workspace-inventory.json`, `package-set-draft.json`,
`package-relation-proposals.json`, `bundle-set-preflight.json`,
`viewer/package-set.json`, `viewer/index.html`, and
`xyflow-package-set-smoke.json`.

## Covered Flow

The smoke scenario runs `collect-batch --emit-workspace-inventory`,
`draft-package-set`, `preflight-bundle-set`, and `render-package-set-site`.

The summary payload uses:

```json
{
  "apiVersion": "spec-harvester.xyflow-package-set-smoke/v0",
  "kind": "SpecHarvesterXyflowPackageSetSmokeReport",
  "schemaVersion": 1
}
```

## Expected Package Set

The smoke fixture produces separate package subjects:

```text
xyflow.workspace
xyflow.system
xyflow.react
xyflow.svelte
```

It also produces producer-observed `contains` relations:

```text
xyflow.workspace contains xyflow.system
xyflow.workspace contains xyflow.react
xyflow.workspace contains xyflow.svelte
```

Skipped package IDs such as `xyflow.cli`, `xyflow.e2e`,
`xyflow.react_examples`, and `xyflow.svelte_examples` remain visible for
review.

## Boundary

The smoke scenario is local-only. It does not fetch the real `xyflow`
repository, contact networks, run package scripts, run package managers, run
builds, run tests, execute prompts, accept packages, accept relations, or
publish registry metadata.

SpecPM remains the validation, acceptance, and registry authority.
