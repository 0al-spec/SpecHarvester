# Bundle-Set Preflight

`preflight-bundle-set` verifies a generated package-set output directory before
SpecPM handoff.

It checks `package-set-draft.json`, `package-relation-proposals.json`, member
candidate bundles, relation endpoints, digest references, and producer review
boundaries. It is review evidence, does not accept packages, and does not
accept relations.

## Command

```bash
python3 -m spec_harvester preflight-bundle-set \
  candidates/xyflow-package-set
```

## Report Identity

```json
{
  "apiVersion": "spec-harvester.bundle-set-preflight/v0",
  "kind": "SpecHarvesterBundleSetPreflightReport",
  "schemaVersion": 1
}
```

## Checks

Bundle-set preflight checks:

- package-set draft identity and summary counts;
- package relation proposal identity;
- unique candidate `packageId` values;
- per-candidate `preflight-candidate-bundle` status;
- per-candidate `diagnosticsStatus` remaining `clean` or `warnings`;
- relation source and target package existence;
- relation source and target package IDs pointing to generated candidates;
- package-set draft digest referenced by relation proposals;
- workspace inventory input consistency;
- producer-observed authority and review status boundaries.

When `workspace-inventory.json` is present beside the package-set artifacts,
the verifier checks its digest. Otherwise it verifies that the package-set draft
and relation proposal records agree on the same inventory path and digest.

## Boundary

The verifier does not publish registry metadata, accept packages, accept
relations, infer trust inheritance, execute package scripts, install
dependencies, or run package managers.

`render-package-set-site` can display this report beside member package cards,
relation proposal badges, producer-observed review status, and result scope
examples. P25-T7 owns the end-to-end `xyflow` smoke scenario.
