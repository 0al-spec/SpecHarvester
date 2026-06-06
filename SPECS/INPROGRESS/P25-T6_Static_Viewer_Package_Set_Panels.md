# P25-T6 — Static Viewer Package-Set Panels

## Objective

Extend the static viewer so reviewers can inspect generated package-set output
as a coherent multi-package review surface instead of opening each candidate
bundle separately.

## Scope

In scope:

- Add a package-set static render path that consumes a `draft-package-set`
  output directory.
- Read `package-set-draft.json`, `package-relation-proposals.json`, optional
  bundle-set preflight output, and generated candidate manifests.
- Emit a static viewer payload with package-set summary, member package cards,
  relation proposal badges, preflight status, and producer-observed review
  status.
- Add CLI support for rendering package-set output.
- Update viewer JavaScript/CSS to render both single-package and package-set
  payloads.
- Document the package-set viewer boundary.

Out of scope:

- Accepting packages or package relations.
- Changing SpecPM registry metadata.
- Executing package scripts, package managers, build systems, or generated
  prompts.
- Adding the full `xyflow` end-to-end smoke scenario. P25-T7 owns that.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| Render generated package set | Draft an `xyflow`-like package set, preflight it, render viewer. | `package-set.json` contains package-set summary, members, relations, and preflight status. |
| Missing relation artifact | Render an incomplete package-set directory. | Renderer returns error diagnostics without writing stale viewer output. |
| CLI coverage | Run `render-package-set-site --bundle-set <dir> --output <site>`. | CLI prints status and writes static assets. |
| Viewer asset coverage | Inspect JS/CSS. | Assets contain package-set render functions, member cards, relation badges, and result-scope text. |
| Docs contract | Keep GitHub docs and DocC visible. | Docs name command, payload kind, relation badges, member cards, and non-goals. |

## Implementation Plan

1. Add package-set renderer classes beside the existing static renderer path.
2. Reuse the existing site writer and static assets, with JS dispatching on
   `payload.packageSet`.
3. Add `render-package-set-site` CLI command.
4. Add tests, docs, validation report, archive, and review artifacts.

## Acceptance Criteria

- `python -m spec_harvester render-package-set-site --bundle-set <dir> --output <site>`
  writes `index.html`, `assets/spec-renderer.css`, `assets/spec-renderer.js`,
  and `package-set.json`.
- The package-set payload has stable identity:
  `apiVersion: spec-harvester.static-package-set-renderer/v0` and
  `kind: SpecHarvesterStaticPackageSet`.
- The viewer payload lists aggregate and scoped member packages separately.
- The viewer payload lists `contains` relation proposals with
  `producer_observed` review status.
- Bundle-set preflight status is visible when a preflight report is present.
- The viewer remains static review evidence and does not accept packages,
  accept relations, publish registry metadata, or execute package code.

