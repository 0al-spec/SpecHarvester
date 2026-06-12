# P28-T3 — Second Real Repository Refresh Compare Run

## Objective

Repeat the `fresh-candidate-refresh-run` and SpecPM
`producer-bundle prepare-refresh-decision` loop on a second real
package-set-capable repository so the handoff contract is not calibrated only
against `xyflow`.

Selected repository:

- Repository: `https://github.com/TanStack/query`
- Pinned revision: `feb1efd804c1262106f72c8adc1d82a8ce9cfbb0`
- Local checkout: `/tmp/specharvester-p28-t3-tanstack-query-source`

## Motivation

P28-T2 proved that the refresh compare loop works for real `xyflow`, where
SpecPM already has generated artifacts. P28-T3 should test a different
workspace shape with more packages and framework bindings.

This task is also allowed to expose a product boundary: if SpecPM has no
current generated baseline for the second repository, the correct output is a
recorded structured compare result and a follow-up, not an invented registry
update.

## Scope

In scope:

- Use the pinned real `TanStack/query` checkout.
- Generate workspace inventory, package-set draft, bundle-set preflight,
  package-set viewer, and fresh candidate refresh run artifacts.
- Feed the fresh generated root into local SpecPM
  `prepare-refresh-decision`.
- Run SpecPM `preflight-refresh-decision` only if a refresh decision is
  produced.
- Record the result and product interpretation.

Out of scope:

- Publishing or proposing TanStack/query packages to SpecPM.
- Mutating SpecPM accepted/generated artifacts.
- Running package managers, package scripts, upstream builds, or tests in the
  harvested repository.
- Treating generated package-set members as registry truth.

## Acceptance Criteria

- SpecHarvester collection and package-set drafting run against the pinned
  TanStack/query checkout.
- Bundle-set preflight passes, or any blocker is recorded with diagnostics.
- `fresh-candidate-refresh-run` prepares a fresh generated root for the drafted
  package-set members.
- SpecPM `prepare-refresh-decision` is run against the fresh generated root.
- The final result is recorded as one of:
  - `no_update_required`;
  - `manual_review_required`;
  - structured missing-baseline / unsupported-compare result with follow-up.
- The validation report records commands, source revision, candidate count,
  relation count, SpecPM result, and product verdict.

## Dependencies

- SpecHarvester P28-T1 `fresh-candidate-refresh-run`.
- SpecHarvester P28-T2 real xyflow refresh compare precedent.
- SpecPM `producer-bundle prepare-refresh-decision` and
  `preflight-refresh-decision`.
