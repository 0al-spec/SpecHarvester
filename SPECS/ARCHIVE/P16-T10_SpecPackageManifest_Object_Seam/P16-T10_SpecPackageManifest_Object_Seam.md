# P16-T10 — SpecPackageManifest Object Seam

Branch: `feature/P16-T10-specpackage-manifest-object`
Review subject: `p16_t10_specpackage_manifest_object_seam`

## Context

Architecture lint now identifies repeated `specpm.yaml` parser patterns in
report modules. Before replacing those procedural parsers, the codebase needs a
small behavior-rich object that owns manifest reading and common manifest
queries.

This task follows the local Elegant Objects refactor guide from
`../../PromptEval/tools/prompt-eval/prompts/elegant_objects/eo_refactor.md`:
preserve observable behavior first, create a narrow seam, keep constructors
simple, and avoid broad helper/service naming.

## Goal

Introduce `SpecPackageManifest` as the shared object seam for `specpm.yaml`
reading without changing existing report outputs yet.

## Deliverables

- Add a frozen `SpecPackageManifest` object.
- Add a small artifact value object owned by the manifest module.
- Support manifest behavior needed by follow-up report refactors:
  - required `metadata.id` / `metadata.version`
  - namespace derivation
  - metadata access
  - foreign artifact access
  - index intents and capabilities
  - license evidence paths shape used by later license report work
- Add characterization tests for valid manifests, missing metadata, artifacts,
  claims, and license evidence.
- Update architecture lint so the shared manifest object is the allowed parser
  home while existing report parser modules remain advisory baseline findings.

## Non-Goals

- Do not rewrite report modules in this PR.
- Do not change public report JSON.
- Do not make architecture lint blocking.
- Do not replace SpecPM validation or implement a full YAML parser.

## Acceptance Criteria

- The new object reads the same manifest fragments currently duplicated across
  report modules.
- Constructors remain simple; I/O happens in explicit behavior.
- Existing tests and architecture lint baseline continue to pass.
- Full Flow quality gates pass.
