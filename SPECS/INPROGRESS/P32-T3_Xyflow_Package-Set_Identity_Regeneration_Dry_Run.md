# P32-T3 Xyflow Package-Set Identity Regeneration Dry Run

**Status:** Planned
**Selected:** 2026-06-13
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness

## Motivation

P32-T2 defines the safe operator runbook for deferred candidate regeneration.
The next practical gap is proving that the xyflow package-set candidates can
be regenerated as a coherent package-set, with `xyflow.workspace` as the root
identity and stable member candidates for React, Svelte, and system packages.

Without a recorded dry run, xyflow remains deferred because the earlier
candidate-layer triage could not prove package-set identity and relation
topology strongly enough for selected handoff.

## Goal

Run a bounded xyflow-only package-set identity regeneration dry run using the
P32-T2 runbook, record the resulting evidence, and decide whether
`xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and `xyflow.system` can
re-enter selected handoff or must remain deferred.

## Deliverables

- Verify `inputs/limited-popular-libraries/repositories.yml` and the local
  xyflow checkout before running regeneration.
- Run `autonomous-candidate-batch --select xyflow` into a fresh
  `.smoke/p32-deferred-regeneration/<attempt-id>/xyflow` output root.
- Preserve durable, reviewable output by adding a machine-readable dry-run
  fixture under `tests/fixtures/xyflow_package_set_identity_regeneration/`.
- Add a GitHub docs page and DocC mirror summarizing the dry run, evidence,
  verdict, non-authority boundary, and next handoff decision.
- Link the dry-run report from the deferred regeneration runbook, autonomous
  candidate tech-debt plan, selected candidate handoff docs, SpecPM handoff
  docs, roadmap, and docs index.
- Add docs-contract tests covering identity, members, relations, preflight,
  viewer, `preview_only`, `external_required`, and non-authority boundaries.
- Archive Flow artifacts and leave the next pointer on P32-T4.

## Acceptance Criteria

- Source manifest validation passes before the dry run.
- The local xyflow checkout exists, is a git worktree, and matches the pinned
  revision `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`.
- The dry run is scoped to `--select xyflow`.
- The dry-run evidence records exactly these package ids:
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and `xyflow.system`.
- The package-set identity is `xyflow.workspace`.
- Relation evidence records:
  - `xyflow.workspace contains xyflow.react`;
  - `xyflow.workspace contains xyflow.svelte`;
  - `xyflow.workspace contains xyflow.system`.
- `bundle-set-preflight.json` reports `passed` with warning count `0` and
  error count `0`.
- Static viewer output is present.
- Each candidate remains `preview_only`.
- Registry acceptance remains `external_required`.
- The fixture states whether xyflow can enter selected handoff or remains
  deferred.
- No SpecPM PR is created, no package or relation is accepted, no baseline is
  seeded, and no registry metadata is published.

## Non-Goals

- No broad limited-corpus rerun.
- No Cupertino or NavigationSplitView regeneration; that is P32-T4.
- No accepted-source mutation.
- No SpecPM repository mutation.
- No package or relation acceptance.
- No baseline seeding.
- No removal of `preview_only`.
- No registry publication.
