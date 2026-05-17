# P1-T3 Add JavaScript and TypeScript Manifest/Export Analyzer

Status: Planned
Selected: 2026-05-17
Branch: `feature/P1-T3-js-ts-manifest-export-analyzer`
Review subject: `p1_t3_js_ts_manifest_export_analyzer`

## Objective

Implement a standalone JavaScript and TypeScript static analyzer for
SpecHarvester. The analyzer must inspect package manifests and static export
entrypoints, then emit a valid `PublicInterfaceIndex` without executing package
code, importing modules, installing dependencies, running package scripts, or
making network calls.

This task creates a standalone analyzer surface for future integration. It does
not wire the analyzer into `collect-local`, `draft`, or CLI commands.

## Deliverables

- Add `src/spec_harvester/js_ts_public_api.py`.
- Add tests in `tests/test_js_ts_public_api.py`.
- Emit a `SpecHarvesterPublicInterfaceIndex` with analyzer policy metadata.
- Discover `package.json` manifests deterministically while skipping common
  generated, package-manager, cache, and VCS directories.
- Read manifest fields that identify public entrypoints:
  - `main`
  - `module`
  - `types`
  - `typings`
  - `exports`
  - `bin`
- Analyze static JavaScript and TypeScript export declarations from discovered
  entrypoint files.
- Record malformed manifests or unreadable static entrypoints as diagnostics
  instead of failing the whole analysis.
- Attach file evidence with relative path and SHA-256 digest.
- Create `SPECS/INPROGRESS/P1-T3_Validation_Report.md` during EXECUTE.

## Acceptance Criteria

- Analyzer output validates with `validate_public_interface_index`.
- Output is deterministic for the same source tree.
- Manifest parsing never runs package scripts and never installs dependencies.
- `exports` object traversal records static file targets from string leaves.
- `bin` string and object forms are handled.
- Static exports produce public symbols for:
  - `export function`
  - `export class`
  - `export interface`
  - `export type`
  - `export enum`
  - `export const`, `export let`, and `export var`
  - `export { name }` and `export { name as alias }`
  - `export default`
- Missing referenced entrypoint files produce diagnostics and do not abort the
  whole analysis.
- Analyzer metadata declares `execution: none`, `networkAccess: none`,
  `packageScripts: not_run`, and `confidence: medium`.

## Trust Boundary

The analyzer may read manifest and source bytes, parse JSON with the Python
standard library, and scan source text for static export syntax. It must not
execute JavaScript or TypeScript files, invoke Node.js, import harvested
modules, resolve package dependencies, run package managers, evaluate
annotations, or inspect runtime objects.

## Test-First Plan

| Phase | Input | Output | Verification |
|-------|-------|--------|--------------|
| Analyzer tests | Small temp npm package fixtures | Failing tests for manifest entrypoints, static exports, diagnostics, and deterministic ordering | `PYTHONPATH=src python -m pytest tests/test_js_ts_public_api.py` |
| Implementation | Test expectations and `interface_index.py` | `js_ts_public_api.py` | Targeted tests pass |
| Full validation | Repository gates from `.flow/params.yaml` | Validation report | Pytest, Ruff, coverage, Swift gates pass |

## TODO Plan

1. Add tests for manifest field discovery, static export symbol extraction,
   evidence, summaries, and deterministic ordering.
2. Add tests for malformed manifests and missing entrypoint diagnostics.
3. Implement deterministic package manifest discovery and static export
   scanning.
4. Validate analyzer output through `validate_public_interface_index`.
5. Run Flow quality gates and record results.

## Non-Goals

- No CLI command or `collect-local` integration.
- No dependency graph resolution.
- No execution of Node.js, npm, pnpm, yarn, TypeScript compiler, Babel, or
  package scripts.
- No full ECMAScript parser or Tree-sitter integration.
- No JavaScript type inference or runtime value evaluation.

---
**Archived:** 2026-05-17
**Verdict:** PASS
