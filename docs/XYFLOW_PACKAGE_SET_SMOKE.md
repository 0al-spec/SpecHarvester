# Xyflow Package-Set Smoke

Status: Local synthetic smoke scenario

`xyflow-package-set-smoke` runs the full package-set producer path against a
deterministic local `xyflow` fixture. It proves the package-set pieces work
together without fetching the real repository or executing package code.

The fixture mirrors the real `xyflow` layout where the root `package.json` is
`@xyflow/monorepo` and workspace membership comes from `pnpm-workspace.yaml`.
This guards the product shape that matters for real checkouts:

- root aggregate candidate: `xyflow.workspace`;
- primary members: `xyflow.system`, `xyflow.react`, `xyflow.svelte`;
- skipped non-primary packages: examples, tooling, and tests;
- relation proposals from the aggregate root to the selected members.

## Command

```bash
python3 -m spec_harvester xyflow-package-set-smoke \
  --output .smoke/xyflow-package-set
```

The output directory must be empty. The command writes:

```text
.smoke/xyflow-package-set/fixture/xyflow/
.smoke/xyflow-package-set/inputs/repositories.yml
.smoke/xyflow-package-set/candidates/xyflow/workspace-inventory.json
.smoke/xyflow-package-set/package-set/package-set-draft.json
.smoke/xyflow-package-set/package-set/package-relation-proposals.json
.smoke/xyflow-package-set/package-set/bundle-set-preflight.json
.smoke/xyflow-package-set/viewer/package-set.json
.smoke/xyflow-package-set/viewer/index.html
.smoke/xyflow-package-set/xyflow-package-set-smoke.json
```

## Covered Flow

The smoke scenario runs:

1. `collect-batch --emit-workspace-inventory`
2. `draft-package-set`
3. `preflight-bundle-set`
4. `render-package-set-site`

The summary payload uses:

```json
{
  "apiVersion": "spec-harvester.xyflow-package-set-smoke/v0",
  "kind": "SpecHarvesterXyflowPackageSetSmokeReport",
  "schemaVersion": 1
}
```

`status: passed` means the complete local package-set path produced the
expected package IDs, relation proposals, passing bundle-set preflight, and
viewer output.

## Expected Package Set

The smoke fixture must produce separate package subjects:

```text
xyflow.workspace
xyflow.system
xyflow.react
xyflow.svelte
```

The smoke fixture must produce producer-observed `contains` relations:

```text
xyflow.workspace contains xyflow.system
xyflow.workspace contains xyflow.react
xyflow.workspace contains xyflow.svelte
```

Skipped package IDs such as `xyflow.cli`, `xyflow.e2e`,
`xyflow.react_examples`, and `xyflow.svelte_examples` remain visible in the
package-set draft so reviewers can see what was intentionally excluded from
the first package-set candidate set.

## Boundary

The smoke scenario is local-only. It does not fetch the real `xyflow`
repository, contact networks, run package scripts, run package managers, run
builds, run tests, execute prompts, accept packages, accept relations, or
publish registry metadata.

The scenario is evidence that SpecHarvester can produce reviewable package-set
artifacts. SpecPM remains the validation, acceptance, and registry authority.
