# Package-Set Viewer

`render-package-set-site` builds a static browser preview for generated
package-set output. It is the multi-package counterpart to `render-spec-site`.

The command consumes `package-set-draft.json`,
`package-relation-proposals.json`, optional `bundle-set-preflight.json`, and
member candidate manifests. It writes a standalone viewer with package-set
summary, member package cards, relation proposal badges, producer-observed
review status, and result scope examples.

## Command

```bash
python3 -m spec_harvester render-package-set-site \
  --bundle-set candidates/xyflow-package-set \
  --output previews/xyflow-package-set
```

## Payload Identity

```json
{
  "apiVersion": "spec-harvester.static-package-set-renderer/v0",
  "kind": "SpecHarvesterStaticPackageSet",
  "schemaVersion": 1
}
```

The output includes `index.html`, `assets/spec-renderer.js`,
`assets/spec-renderer.css`, and `package-set.json`.

## Review Surface

The viewer shows package-set summary, aggregate `authorReadyDraftSummary`,
per-member quality report status and author action items, aggregate and scoped
member package cards, `contains` relation proposal badges, `producer_observed`
review status, bundle-set preflight status when available, and result scope
examples for the generated package set.

## Boundary

The package-set viewer does not accept packages, does not accept relations,
does not publish public registry metadata, and does not execute package code.

SpecPM remains the validation, acceptance, and registry authority. P25-T7 owns
the end-to-end `xyflow` smoke scenario.
