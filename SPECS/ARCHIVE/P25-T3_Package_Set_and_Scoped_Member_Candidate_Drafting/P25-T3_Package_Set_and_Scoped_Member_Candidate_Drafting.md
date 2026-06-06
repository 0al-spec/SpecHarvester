# P25-T3 — Package-Set and Scoped Member Candidate Drafting

## Objective

Draft aggregate package-set candidates alongside scoped member package
candidates from `workspace-inventory.json`. The output should let a monorepo
such as `xyflow` produce separate preview candidates like `xyflow.workspace`,
`xyflow.system`, `xyflow.react`, and `xyflow.svelte` without collapsing all
observed intent into one package subject.

## Scope

In scope:

- Add an explicit package-set drafting command that consumes
  `workspace-inventory.json`.
- Generate separate preview candidate bundle directories for the aggregate
  workspace package and selected scoped member packages.
- Reuse existing single-package candidate bundle generation, producer reports,
  receipts, and preflight-compatible layout where practical.
- Emit a deterministic package-set draft summary artifact that lists generated
  and skipped inventory packages.
- Document the command and producer/review boundary.

Out of scope:

- Relation proposal emission. P25-T4 owns `contains` and other relation output.
- Bundle-set preflight. P25-T5 owns multi-package consistency checks.
- Static viewer package-set panels. P25-T6 owns the review UI.
- SpecPM acceptance, public registry mutation, namespace authority, dependency
  solving, package script execution, dependency installation, or package-manager
  execution.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| Package-set drafting fixture | Draft from an `xyflow`-like workspace inventory. | Output contains `xyflow.workspace`, `xyflow.system`, `xyflow.react`, and `xyflow.svelte` candidate dirs. |
| Candidate bundle preflight | Verify generated candidates keep the existing bundle contract. | Each generated candidate passes producer-side candidate bundle preflight. |
| Skipped package coverage | Ensure examples/tooling/tests are not silently lost. | Draft summary records skipped `member_package` packages with reasons. |
| CLI coverage | Exercise `draft-package-set` from command line. | CLI prints deterministic summary and writes package-set draft output. |
| Docs contract test | Keep GitHub docs and DocC visible. | Docs name the command, summary artifact, preview-only boundary, and P25-T4/P25-T5 split. |

## Implementation Plan

1. Add a package-set drafter module and deterministic JSON summary renderer.
2. Convert selected inventory package records into bounded synthetic harvest
   snapshots consumed by the existing `draft_spec_package` path.
3. Default generation to roles needed for the package-set reference path:
   `workspace`, `core_runtime`, `react_binding`, and `svelte_binding`.
4. Record skipped packages such as examples, tooling, and tests in the
   draft-set summary for later review.
5. Add CLI wiring, tests, docs, validation report, archive, and review artifacts.

## Acceptance Criteria

- `draft-package-set <workspace-inventory.json> --out <dir>` writes a
  deterministic package-set draft summary.
- The command creates separate candidate bundle directories for aggregate and
  selected scoped packages.
- For an `xyflow`-like fixture, generated package IDs include
  `xyflow.workspace`, `xyflow.system`, `xyflow.react`, and `xyflow.svelte`.
- Generated candidates remain `preview_only`.
- Generated candidates pass existing producer-side candidate bundle preflight.
- Skipped inventory packages are recorded in the summary with explicit reasons.
- Relation proposals remain absent until P25-T4.
- Existing single-package `draft` behavior is unchanged.

## Notes

- The package-set draft summary is producer evidence, not SpecPM registry
  metadata.
- Proposed package IDs remain review inputs, not namespace ownership claims.
- P25-T3 intentionally keeps relation materialization separate so maintainers
  can review package candidate quality before relation proposal semantics.
