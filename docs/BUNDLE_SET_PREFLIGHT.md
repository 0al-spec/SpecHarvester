# Bundle-Set Preflight

Status: Producer-side verifier

`preflight-bundle-set` verifies a generated package-set output directory before
SpecPM handoff. It checks the set as a whole: package-set summary, member
candidate bundles, relation proposals, digest references, and review
boundaries.

The verifier is review evidence. It does not accept packages, does not accept
relations, mutate SpecPM sources, or publish registry metadata.

## Command

```bash
python3 -m spec_harvester preflight-bundle-set \
  candidates/xyflow-package-set
```

The input directory is the output of `draft-package-set`:

```text
candidates/xyflow-package-set/package-set-draft.json
candidates/xyflow-package-set/package-relation-proposals.json
candidates/xyflow-package-set/xyflow.workspace/specpm.yaml
candidates/xyflow-package-set/xyflow.system/specpm.yaml
candidates/xyflow-package-set/xyflow.react/specpm.yaml
candidates/xyflow-package-set/xyflow.svelte/specpm.yaml
```

## Report Identity

The command prints a deterministic JSON report:

```json
{
  "apiVersion": "spec-harvester.bundle-set-preflight/v0",
  "kind": "SpecHarvesterBundleSetPreflightReport",
  "schemaVersion": 1
}
```

`status` is `passed` when the bundle set has no error diagnostics and `failed`
otherwise.

## Checks

Bundle-set preflight checks:

- `package-set-draft.json` identity and summary counts;
- `package-relation-proposals.json` identity;
- unique candidate `packageId` values;
- each candidate directory exists;
- each candidate passes ordinary `preflight-candidate-bundle`;
- relation source and target package existence;
- relation `source.packageId` and `target.packageId` point to generated
  candidates;
- relation inputs reference the current `package-set-draft.json` digest;
- workspace inventory input consistency;
- relation `workspaceInventory` input matches the package-set draft
  `workspaceInventory` record;
- relation and package-set authority remain producer observed review evidence;
- relation review statuses remain explicit review states.

If `workspace-inventory.json` is also present in the package-set directory, the
verifier checks its digest. The current `draft-package-set` flow records the
inventory path and digest but does not copy the inventory file into the output
directory, so the required consistency check is between package-set and
relation input records.

## Diagnostics

Important failure codes include:

- `candidate_package_id_duplicate`
- `candidate_bundle_missing`
- `candidate_preflight_failed`
- `relation_source_missing`
- `relation_target_missing`
- `relation_package_set_draft_digest_mismatch`
- `workspace_inventory_input_mismatch`

Diagnostics are sorted for deterministic review.

## Boundary

SpecHarvester does not:

- accept package-set candidates;
- accept package relations;
- publish public registry metadata;
- infer inherited capabilities or constraints;
- execute package scripts;
- install dependencies;
- run package managers.

P25-T6 owns static viewer panels for package-set review. P25-T7 owns the
end-to-end `xyflow` smoke scenario.
