# P28-T2 — Real Xyflow Refresh Compare Run

## Objective

Run real `xyflow` through the newly added
`fresh-candidate-refresh-run` contract and then through SpecPM's
`producer-bundle prepare-refresh-decision` helper.

The task answers the practical registry question:

```text
Does the current SpecHarvester package-set output contain a contract delta
against the current SpecPM generated xyflow artifacts?
```

## Scope

In scope:

- Use the local real `xyflow` checkout.
- Generate workspace inventory, package-set draft, bundle-set preflight,
  package-set viewer, and fresh candidate refresh run artifacts.
- Feed the fresh generated root into local SpecPM
  `prepare-refresh-decision`.
- Run SpecPM `preflight-refresh-decision`.
- Record the refresh decision status and product interpretation.

Out of scope:

- Opening a SpecPM registry update PR.
- Mutating SpecPM generated or curated artifacts.
- Publishing registry metadata.
- Running package scripts, package managers, or upstream tests in `xyflow`.
- Treating a no-op refresh decision as automatic maintainer acceptance.

## Acceptance Criteria

- Real `xyflow` package-set generation produces the expected four package
  candidates: `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and
  `xyflow.system`.
- SpecHarvester `preflight-bundle-set` passes.
- `fresh-candidate-refresh-run` prepares a fresh generated root for all four
  package candidates.
- SpecPM `prepare-refresh-decision` passes.
- SpecPM `preflight-refresh-decision` passes.
- The final result is recorded as either `no_update_required` or
  `manual_review_required`, with reason and digest counts.
