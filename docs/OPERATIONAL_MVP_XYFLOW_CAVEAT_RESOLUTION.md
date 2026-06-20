# Operational MVP Xyflow Caveat Resolution

Status: P44-T3 quality-hardening caveat resolution.

P44-T3 resolves the xyflow manual-correction caveats for P44 rerun purposes:
partial `PublicInterfaceIndex` evidence and the SoundBlaster/xyflow
operator-checkout fork origin.

The durable fixture is:

```text
tests/fixtures/operational_mvp_quality_hardening/p44-t3-operational-mvp-xyflow-caveat-resolution.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.operational-mvp-xyflow-caveat-resolution/v0
kind: SpecHarvesterOperationalMVPXyflowCaveatResolution
authority: producer_operational_mvp_xyflow_caveat_resolution_only
```

## Decision

Both caveats are accepted for the bounded P44 rerun and remain
registry-promotion blockers:

| Caveat | P44 rerun | Registry promotion |
| --- | --- | --- |
| `partial_public_interface_index` | accepted | blocked |
| `operator_checkout_origin_fork_mismatch` | accepted | blocked |

This means the P44-T4 rerun can proceed using the same pinned xyflow evidence,
but the result must not claim complete public-index evidence or canonical
upstream acceptance.

## Boundary

P44-T3 does not clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, run AI, enable trusted local adapter
execution, accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, treat AI output as registry truth, treat
adapter output as registry truth, or treat caveat-resolution output as registry
truth.
