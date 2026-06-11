# Package-Set Viewer

Status: Producer-side static review surface

`render-package-set-site` builds a static browser preview for generated
package-set output. It is the multi-package counterpart to `render-spec-site`.

The command consumes `package-set-draft.json`,
`package-relation-proposals.json`, optional `bundle-set-preflight.json`, and
the generated member candidate manifests. It writes a standalone viewer that
shows package-set summary, member package cards, relation proposal badges,
producer-observed review status, author review checklists, weak claim and
evidence-gap prompts, recommended edits, and result scope examples.

## Command

```bash
python3 -m spec_harvester render-package-set-site \
  --bundle-set candidates/xyflow-package-set \
  --output previews/xyflow-package-set
```

The output directory contains:

- `index.html`
- `assets/spec-renderer.js`
- `assets/spec-renderer.css`
- `package-set.json`

## Payload Identity

The normalized JSON payload uses a stable renderer identity:

```json
{
  "apiVersion": "spec-harvester.static-package-set-renderer/v0",
  "kind": "SpecHarvesterStaticPackageSet",
  "schemaVersion": 1
}
```

`package-set.json` is review data, not SpecPM registry data.

## Review Surface

The viewer presents:

- package-set summary from `package-set-draft.json`;
- aggregate `authorReadyDraftSummary` with the stop-policy decision;
- aggregate `authorReview` with a human-facing author review checklist;
- member package cards for aggregate and scoped candidates;
- per-member quality report status, author action items, and reviewable
  dimensions in `package-set.json`;
- relation proposal badges for `contains` links;
- producer-observed review status such as `producer_observed`;
- bundle-set preflight status when `bundle-set-preflight.json` is present;
- result scope examples that distinguish aggregate workspace packages from
  scoped member packages.

## Author Review Payload

`authorReview` is derived from existing member
`author-ready-draft-quality-report.json` evidence and the aggregate
`authorReadyDraftSummary`. It is a human review surface, not a new source of
truth.

The aggregate payload includes:

- `decision`: the same stop decision as the stop-policy summary;
- `checklist[]`: author review checklist items such as whether generation can
  stop or whether blockers need repair;
- `weakClaims[]`: reviewable dimensions such as `repositorySpecificity`,
  `packageTopology`, or `claimConservatism`;
- `evidenceGaps[]`: action items and reviewable dimensions that point at weak
  or missing evidence;
- `recommendedEdits[]`: practical edits for identity, summaries, capabilities,
  intents, constraints, and evidence support;
- `memberActions[]`: per-member action item summaries for aggregate and scoped
  packages;
- `nonAuthority[]`: explicit reminders that the viewer is not SpecPM registry
  acceptance, maintainer approval, or upstream endorsement.

Member cards also expose a compact `authorReview` block with action items,
reviewable dimensions, and evidence gaps for that member. This lets an author
review `xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
`xyflow.workspace` without reading raw JSON first.

The first supported scenario is the P25 package-set flow for `xyflow.workspace`,
`xyflow.system`, `xyflow.react`, and `xyflow.svelte`.

## Boundary

The package-set viewer does not accept packages, does not accept relations,
does not publish public registry metadata, and does not execute package code.

SpecHarvester owns the generated review bundle. SpecPM remains the validation,
acceptance, and registry authority. P25-T7 owns the end-to-end `xyflow` smoke
scenario that should exercise this viewer against a real package-set fixture.
