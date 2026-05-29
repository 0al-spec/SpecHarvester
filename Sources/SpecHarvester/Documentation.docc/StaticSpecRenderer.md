# Static Spec Renderer

`render-spec-site` builds a static browser preview for one generated SpecPM
candidate package.

The command is for reviewer ergonomics only. It does not validate, publish,
accept, sign, execute, or mutate package semantics. SpecPM remains the
validation and registry authority.

## Command

```bash
spec-harvester render-spec-site \
  --candidate .specharvester/candidates/demo.core \
  --output .specharvester/previews/demo.core
```

The output directory contains:

- `index.html`
- `assets/spec-renderer.js`
- `assets/spec-renderer.css`
- `spec-package.json`

Open `index.html` from local disk or serve the directory from any static host.
The same file layout is suitable for GitHub Pages or a later standalone viewer
repository.

## Input Contract

The candidate directory must contain:

- `specpm.yaml`
- referenced `specs/*.spec.yaml` files from `specpm.yaml` `specs[].path`

Optional input:

- `specpm-validation.json` or `validation.json`

If validation JSON is absent, the viewer reports `SpecPM validation: not
provided`. It does not run SpecPM itself.

## Trust Boundary

The renderer treats candidate files as untrusted data:

- no package code execution;
- no package scripts;
- no dependency installation;
- no build tools;
- no network probes;
- no browser-side YAML parsing;
- no path traversal outside the candidate root;
- no symlinked `specpm.yaml` or referenced spec input;
- no YAML anchors, aliases, custom tags, multiple documents, or non-JSON YAML
  values.

Python reads YAML locally, normalizes it into `spec-package.json`, and the
browser reads only that JSON payload. The JavaScript renderer escapes text
before inserting it into HTML and writes the raw JSON view through text content.

## Relation To SpecPM

SpecPM already has a static registry viewer for `/v0` public index JSON. This
renderer covers a different review step: local generated candidate packages
before they are accepted into a registry.

The intended boundary is:

- SpecHarvester: deterministic candidate generation and static preview.
- SpecPM: schema validation, compatibility policy, public index generation, and
  package acceptance.
- Future standalone renderer: reusable static UI around the stable
  `SpecHarvesterStaticSpecPackage` JSON contract.

## Extraction Notes

The implementation deliberately keeps the browser side small:

- one JSON contract: `SpecHarvesterStaticSpecPackage`;
- one HTML file;
- one JavaScript asset;
- one CSS asset;
- no npm build step;
- no runtime dependency fetching.

That makes later extraction straightforward: keep the Python normalizer in
SpecHarvester or expose it as a small producer command, then move the static UI
assets and JSON contract tests into a dedicated repository.
