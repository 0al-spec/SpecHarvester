# REVIEW P28-T2 — Real Xyflow Refresh Compare Run

Date: 2026-06-12
Verdict: PASS

## Review Subject

P28-T2 runs real `xyflow` through SpecHarvester's package-set pipeline,
exports the result with `fresh-candidate-refresh-run`, and verifies the fresh
root with SpecPM `prepare-refresh-decision` and
`preflight-refresh-decision`.

## Findings

No actionable issues found.

## Evidence Reviewed

- Real `xyflow` source revision:
  `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`.
- SpecHarvester generated 4 package-set candidates.
- SpecHarvester bundle-set preflight passed.
- SpecPM prepare report passed.
- SpecPM refresh-decision preflight passed.
- SpecPM verified 8 generated contract-file digests.
- Decision status was `no_update_required` with reason `no_contract_delta`.

## Product Interpretation

The run confirms the refresh compare loop works end to end. It also confirms
that the latest SpecHarvester output does not justify a registry update for
`xyflow` because contract-bearing files match current generated artifacts.

This is the desired behavior: newer producer evidence does not become a
registry update unless `specpm.yaml` or `specs/*.spec.yaml` has a meaningful
contract delta.

## Residual Risk

The run is still calibrated on `xyflow`. P28-T3 should repeat the same flow on
a second package-set-capable repository to check that the handoff is not
overfit to the `xyflow.workspace/react/svelte/system` shape.

## Follow-Up

Proceed to `P28-T3` second real repository refresh compare run.
