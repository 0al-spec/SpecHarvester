# P25-T7 — Xyflow Package-Set Smoke Scenario

## Objective

Add a repeatable `xyflow` package-set smoke scenario that exercises the full
local package-set producer path end to end.

## Scope

In scope:

- Create a deterministic synthetic `xyflow` monorepo fixture with workspace,
  system, React, Svelte, and skipped package records.
- Run the complete package-set path:
  `collect-batch --emit-workspace-inventory` ->
  `draft-package-set` ->
  `preflight-bundle-set` ->
  `render-package-set-site`.
- Emit a machine-readable smoke summary with artifact paths, package IDs,
  relation pairs, preflight status, and viewer output status.
- Add CLI support so operators can run the scenario locally.
- Add tests and documentation that prove the smoke scenario covers aggregate
  and scoped member package boundaries.

Out of scope:

- Fetching the real `xyflow` repository from the network.
- Running package managers, package scripts, builds, tests, or generated
  prompts.
- Accepting generated packages or relations into SpecPM.
- Publishing registry metadata.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| End-to-end smoke | Run the synthetic `xyflow` package-set smoke. | Summary status is `passed`, four member packages are generated, three `contains` relations are present, preflight passes, viewer writes `package-set.json`. |
| CLI smoke | Run `xyflow-package-set-smoke --output <dir>`. | CLI prints the summary and writes all smoke artifacts. |
| Docs contract | Keep GitHub docs and DocC visible. | Docs name the command, artifact layout, package IDs, relation pairs, non-goals, and P25 completion. |

## Implementation Plan

1. Add a small `xyflow_package_set_smoke` module with fixture writing and smoke
   orchestration.
2. Wire a CLI command.
3. Add regression tests for the summary and CLI behavior.
4. Document the scenario in GitHub docs and DocC.
5. Archive P25-T7 and update `next.md`.

## Acceptance Criteria

- The smoke scenario produces `xyflow.workspace`, `xyflow.system`,
  `xyflow.react`, and `xyflow.svelte` as separate candidate subjects.
- The smoke scenario records `xyflow.workspace contains xyflow.system`,
  `xyflow.workspace contains xyflow.react`, and
  `xyflow.workspace contains xyflow.svelte`.
- Bundle-set preflight passes without executing harvested repository code,
  package scripts, package managers, builds, tests, or prompts.
- The static viewer emits `package-set.json` and keeps aggregate/scoped
  package boundaries visible.
- The scenario is deterministic and local-only.
